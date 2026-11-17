"""Tests for the dataset and the filter CLI. Pure stdlib unittest."""
import json, os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import validate  # noqa: E402
import agents as A  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, "data", "agents.json"), encoding="utf-8"))
AGENTS = DATA["agents"]


class TestDataset(unittest.TestCase):
    def test_structural_valid(self):
        self.assertEqual(validate.structural_check(DATA), [])

    def test_count_matches(self):
        self.assertEqual(DATA["count"], len(AGENTS))

    def test_at_least_40(self):
        self.assertGreaterEqual(len(AGENTS), 40)

    def test_unique_ids(self):
        ids = [a["id"] for a in AGENTS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_unique_repos(self):
        repos = [a["github"].lower() for a in AGENTS if a["github"]]
        self.assertEqual(len(repos), len(set(repos)))

    def test_oss_have_repo_and_license(self):
        for a in AGENTS:
            if a["open_source"]:
                self.assertTrue(a["github"], f"{a['name']} OSS but no repo")
                self.assertNotEqual(a["license"], "proprietary", a["name"])

    def test_proprietary_marked(self):
        for a in AGENTS:
            if not a["open_source"] and a["source"] == "homepage":
                self.assertEqual(a["license"], "proprietary", a["name"])

    def test_sorted_by_name(self):
        names = [a["name"] for a in AGENTS]
        self.assertEqual(names, sorted(names, key=str.lower))


class TestFilter(unittest.TestCase):
    def test_category(self):
        cli = A.filter_agents(AGENTS, category="cli-agent")
        self.assertTrue(cli)
        self.assertTrue(all(a["category"] == "cli-agent" for a in cli))

    def test_open_source_split(self):
        oss = A.filter_agents(AGENTS, open_source=True)
        prop = A.filter_agents(AGENTS, open_source=False)
        self.assertEqual(len(oss) + len(prop), len(AGENTS))
        self.assertTrue(all(a["open_source"] for a in oss))

    def test_license_substring(self):
        mit = A.filter_agents(AGENTS, license="mit")
        self.assertTrue(mit)
        self.assertTrue(all("mit" in a["license"].lower() for a in mit))

    def test_local_includes_partial(self):
        loc = A.filter_agents(AGENTS, local=True)
        self.assertTrue(all(a["local_models"] in A.TRUEISH for a in loc))

    def test_min_stars(self):
        big = A.filter_agents(AGENTS, min_stars=50000)
        self.assertTrue(all((a["stars"] or 0) >= 50000 for a in big))

    def test_combined(self):
        r = A.filter_agents(AGENTS, open_source=True, local=True, provider=True)
        for a in r:
            self.assertTrue(a["open_source"])
            self.assertIn(a["local_models"], A.TRUEISH)
            self.assertIn(a["provider_flexibility"], A.TRUEISH)

    def test_render_md_header(self):
        md = A.render_md(AGENTS[:3])
        self.assertIn("| Name |", md)
        self.assertEqual(md.count("\n"), 4)  # header + sep + 3 rows

    def test_cli_runs_json(self):
        # smoke: main() with json format shouldn't raise
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            A.main(["--category", "ide-agent", "--format", "json"])
        parsed = json.loads(buf.getvalue())
        self.assertTrue(all(a["category"] == "ide-agent" for a in parsed))


if __name__ == "__main__":
    unittest.main(verbosity=2)
