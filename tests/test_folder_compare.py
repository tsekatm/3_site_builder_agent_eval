"""Tests for folder comparison engine."""

import pytest
from pathlib import Path

from eval_core.folder_compare.tree_diff import FolderComparer
from eval_core.folder_compare.content_diff import ContentComparer


class TestFolderComparer:
    def _create_gold(self, tmp_path):
        gold = tmp_path / "gold"
        gold.mkdir()
        (gold / "index.html").write_text("<html><body>Hello</body></html>")
        (gold / "css").mkdir()
        (gold / "css" / "styles.css").write_text(":root { --primary-color: #B85C38; }")
        return gold

    def test_perfect_match_no_violations(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html><body>Hello</body></html>")
        (agent / "css").mkdir()
        (agent / "css" / "styles.css").write_text(":root { --primary-color: #B85C38; }")

        comparer = FolderComparer(gold, agent)
        violations = comparer.compare()
        structural = [v for v in violations if v.category == "structural"]
        assert len(structural) == 0

    def test_missing_index_html(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "css").mkdir()
        (agent / "css" / "styles.css").write_text(":root {}")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_required_files()
        index_violations = [v for v in violations if "index.html" in v.file]
        assert len(index_violations) == 1
        assert index_violations[0].severity.value == "critical"
        assert index_violations[0].deduction == -3.0

    def test_missing_css(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html></html>")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_required_files()
        css_violations = [v for v in violations if "styles.css" in str(v.file)]
        assert len(css_violations) == 1
        assert css_violations[0].severity.value == "major"

    def test_extra_files_detected(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html></html>")
        (agent / "css").mkdir()
        (agent / "css" / "styles.css").write_text(":root {}")
        (agent / "extra.txt").write_text("unexpected")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_extra_files()
        assert len(violations) == 1
        assert violations[0].id == "STRUCT-EXTRA-FILES"

    def test_placeholder_tokens_detected(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html><h1>{{BUSINESS_NAME}}</h1><p>{{TAGLINE}}</p></html>")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_placeholder_tokens()
        assert len(violations) == 2
        assert all(v.id == "CONTENT-PLACEHOLDER" for v in violations)

    def test_css_variable_mismatch(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html></html>")
        (agent / "css").mkdir()
        (agent / "css" / "styles.css").write_text(":root { --primary-color: #FF0000; }")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_css_variables()
        mismatch = [v for v in violations if v.id == "VIS-COLOUR-MISMATCH"]
        assert len(mismatch) == 1

    def test_missing_css_variable(self, tmp_path):
        gold = self._create_gold(tmp_path)
        agent = tmp_path / "agent"
        agent.mkdir()
        (agent / "index.html").write_text("<html></html>")
        (agent / "css").mkdir()
        (agent / "css" / "styles.css").write_text(":root { }")

        comparer = FolderComparer(gold, agent)
        violations = comparer.check_css_variables()
        missing = [v for v in violations if v.id == "CODE-HARDCODED-VALUES"]
        assert len(missing) == 1


class TestContentComparer:
    def test_missing_meta_description(self, tmp_path):
        gold = tmp_path / "gold.html"
        agent = tmp_path / "agent.html"
        gold.write_text('<html><head><meta name="description" content="test"></head></html>')
        agent.write_text("<html><head></head></html>")

        comparer = ContentComparer(gold, agent)
        violations = comparer.check_meta_tags()
        desc_violations = [v for v in violations if "description" in v.description]
        assert len(desc_violations) >= 1

    def test_multiple_h1_detected(self, tmp_path):
        gold = tmp_path / "gold.html"
        agent = tmp_path / "agent.html"
        gold.write_text("<html><body><h1>One</h1></body></html>")
        agent.write_text("<html><body><h1>One</h1><h1>Two</h1></body></html>")

        comparer = ContentComparer(gold, agent)
        violations = comparer.check_heading_hierarchy()
        assert len(violations) == 1
        assert "Multiple H1" in violations[0].description

    def test_missing_alt_text(self, tmp_path):
        gold = tmp_path / "gold.html"
        agent = tmp_path / "agent.html"
        gold.write_text('<html><body><img src="test.jpg" alt="test"></body></html>')
        agent.write_text('<html><body><img src="test.jpg"></body></html>')

        comparer = ContentComparer(gold, agent)
        violations = comparer.check_alt_text()
        assert len(violations) == 1
        assert violations[0].id == "A11Y-MISSING-ALT"

    def test_missing_skip_link(self, tmp_path):
        gold = tmp_path / "gold.html"
        agent = tmp_path / "agent.html"
        gold.write_text('<html><body><a href="#main">Skip</a></body></html>')
        agent.write_text("<html><body></body></html>")

        comparer = ContentComparer(gold, agent)
        violations = comparer.check_skip_link()
        assert len(violations) == 1
        assert violations[0].id == "A11Y-NO-SKIP-LINK"

    def test_no_violations_on_good_html(self, tmp_path):
        html = '''<html><head>
            <meta name="viewport" content="width=device-width">
            <meta name="description" content="Test site">
            <meta property="og:title" content="Test">
            <meta property="og:description" content="Test desc">
        </head><body>
            <a href="#main-content">Skip to main content</a>
            <h1>Title</h1>
            <img src="test.jpg" alt="Test image">
        </body></html>'''

        gold = tmp_path / "gold.html"
        agent = tmp_path / "agent.html"
        gold.write_text(html)
        agent.write_text(html)

        comparer = ContentComparer(gold, agent)
        violations = comparer.compare()
        assert len(violations) == 0
