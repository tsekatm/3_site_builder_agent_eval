"""Tests for FigmaDesignExtractor — mocked Figma API."""

import pytest
from unittest.mock import patch, MagicMock

from eval_core.figma.extractor import (
    FigmaDesignExtractor,
    DesignContext,
    parse_figma_url,
    _rgba_to_hex,
    _hex_to_hsl,
    _luminance,
)


# ---------------------------------------------------------------------------
# URL parsing tests
# ---------------------------------------------------------------------------

class TestParseFigmaUrl:
    def test_full_url_with_node_id(self):
        url = "https://www.figma.com/design/w8Qtdxpc6i6aOgcha3dllW/Experience-Madikwe?node-id=1-864&m=dev"
        result = parse_figma_url(url)
        assert result["file_key"] == "w8Qtdxpc6i6aOgcha3dllW"
        assert result["file_name"] == "Experience-Madikwe"
        assert result["node_id"] == "1-864"

    def test_full_url_without_node_id(self):
        url = "https://www.figma.com/design/abc123def456/My-Design"
        result = parse_figma_url(url)
        assert result["file_key"] == "abc123def456"
        assert result["file_name"] == "My-Design"
        assert result["node_id"] is None

    def test_raw_file_key(self):
        result = parse_figma_url("w8Qtdxpc6i6aOgcha3dllW")
        assert result["file_key"] == "w8Qtdxpc6i6aOgcha3dllW"
        assert result["node_id"] is None

    def test_file_url(self):
        url = "https://www.figma.com/file/abc123def456/Design?node-id=2:3"
        result = parse_figma_url(url)
        assert result["file_key"] == "abc123def456"
        assert result["node_id"] == "2:3"

    def test_invalid_url_raises(self):
        with pytest.raises(ValueError, match="Could not extract"):
            parse_figma_url("not-a-figma-url")


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

class TestColourHelpers:
    def test_rgba_to_hex_opaque(self):
        assert _rgba_to_hex(1.0, 0.0, 0.0) == "#ff0000"
        assert _rgba_to_hex(0.0, 0.5, 1.0) == "#0080ff"

    def test_rgba_to_hex_transparent(self):
        result = _rgba_to_hex(1.0, 1.0, 1.0, 0.5)
        assert result == "#ffffff80"

    def test_hex_to_hsl_red(self):
        h, s, l = _hex_to_hsl("#ff0000")
        assert abs(h - 0) < 1  # hue ~0
        assert s > 0.9  # fully saturated

    def test_hex_to_hsl_white(self):
        h, s, l = _hex_to_hsl("#ffffff")
        assert l == 1.0

    def test_luminance_black(self):
        assert _luminance("#000000") == 0.0

    def test_luminance_white(self):
        assert _luminance("#ffffff") == 1.0


# ---------------------------------------------------------------------------
# Fixture: Madikwe-like Figma data
# ---------------------------------------------------------------------------

SAMPLE_FIGMA_NODE_RESPONSE = {
    "name": "Experience Madikwe",
    "nodes": {
        "1:864": {
            "document": {
                "id": "1:864",
                "type": "FRAME",
                "name": "Home",
                "absoluteBoundingBox": {"x": 0, "y": 0, "width": 1920, "height": 4457},
                "children": [
                    # Navigation/Footer group
                    {
                        "id": "1:900",
                        "type": "GROUP",
                        "name": "Footer",
                        "absoluteBoundingBox": {"x": 0, "y": 4089, "width": 1920, "height": 368},
                        "fills": [{"type": "SOLID", "visible": True, "color": {"r": 0.6, "g": 0.5, "b": 0.3, "a": 1.0}}],
                        "children": [
                            {
                                "id": "1:901",
                                "type": "TEXT",
                                "name": "Footer Nav",
                                "characters": "HOME\nABOUT MADIKWE\nLODGES\nGETTING HERE",
                                "style": {"fontFamily": "Avenir", "fontSize": 16, "fontWeight": 500,
                                          "textAlignHorizontal": "LEFT"},
                                "fills": [{"type": "SOLID", "visible": True,
                                           "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}],
                                "absoluteBoundingBox": {"x": 400, "y": 4100, "width": 200, "height": 100},
                            },
                            {
                                "id": "1:902",
                                "type": "TEXT",
                                "name": "Contact Info",
                                "characters": "PARK RANGER Phone: +27183509938 Email us: madikweadmin@experiencemadikwe.com",
                                "style": {"fontFamily": "Avenir", "fontSize": 16, "fontWeight": 350,
                                          "textAlignHorizontal": "LEFT"},
                                "fills": [{"type": "SOLID", "visible": True,
                                           "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}],
                                "absoluteBoundingBox": {"x": 1000, "y": 4100, "width": 500, "height": 50},
                            },
                            {
                                "id": "1:903",
                                "type": "TEXT",
                                "name": "Copyright",
                                "characters": "© 2025 Experience Madikwe. All Rights Reserved.",
                                "style": {"fontFamily": "Avenir", "fontSize": 16, "fontWeight": 350,
                                          "textAlignHorizontal": "LEFT"},
                                "fills": [{"type": "SOLID", "visible": True,
                                           "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}],
                                "absoluteBoundingBox": {"x": 0, "y": 4400, "width": 500, "height": 30},
                            },
                        ],
                    },
                    # Hero image
                    {
                        "id": "1:865",
                        "type": "RECTANGLE",
                        "name": "image",
                        "fills": [{"type": "IMAGE", "visible": True, "imageRef": "hero_ref_123"}],
                        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 1920, "height": 926},
                    },
                    # Hero text
                    {
                        "id": "1:870",
                        "type": "TEXT",
                        "name": "Hero Heading",
                        "characters": "Join Us for an Unforgettable African Safari Experience",
                        "style": {"fontFamily": "Marcellus", "fontSize": 64, "fontWeight": 400,
                                  "textAlignHorizontal": "LEFT"},
                        "fills": [{"type": "SOLID", "visible": True,
                                   "color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}}],
                        "absoluteBoundingBox": {"x": 20, "y": 300, "width": 674, "height": 230},
                    },
                    # Choosing a Lodge heading
                    {
                        "id": "1:880",
                        "type": "TEXT",
                        "name": "Choosing a Lodge",
                        "characters": "Choosing a Lodge",
                        "style": {"fontFamily": "Marcellus", "fontSize": 40, "fontWeight": 400,
                                  "textAlignHorizontal": "CENTER"},
                        "fills": [{"type": "SOLID", "visible": True,
                                   "color": {"r": 0.11, "g": 0.11, "b": 0.11, "a": 1.0}}],
                        "absoluteBoundingBox": {"x": 730, "y": 1200, "width": 461, "height": 48},
                    },
                    # Lodge description
                    {
                        "id": "1:881",
                        "type": "TEXT",
                        "name": "Lodge Description",
                        "characters": "Madikwe's 22 safari lodges cater to a diverse range guests needs including luxury, family and eco options and everything in between.",
                        "style": {"fontFamily": "Avenir", "fontSize": 18, "fontWeight": 350,
                                  "textAlignHorizontal": "CENTER"},
                        "fills": [{"type": "SOLID", "visible": True,
                                   "color": {"r": 0.11, "g": 0.11, "b": 0.11, "a": 1.0}}],
                        "absoluteBoundingBox": {"x": 507, "y": 1260, "width": 906, "height": 77},
                    },
                    # Lodge image cards (3 of 9 for brevity)
                    {
                        "id": "1:890",
                        "type": "RECTANGLE",
                        "name": "image",
                        "fills": [{"type": "IMAGE", "visible": True, "imageRef": "lodge1_ref"}],
                        "absoluteBoundingBox": {"x": 20, "y": 1400, "width": 516, "height": 356},
                    },
                    {
                        "id": "1:891",
                        "type": "RECTANGLE",
                        "name": "image",
                        "fills": [{"type": "IMAGE", "visible": True, "imageRef": "lodge2_ref"}],
                        "absoluteBoundingBox": {"x": 560, "y": 1400, "width": 516, "height": 356},
                    },
                    {
                        "id": "1:892",
                        "type": "RECTANGLE",
                        "name": "image",
                        "fills": [{"type": "IMAGE", "visible": True, "imageRef": "lodge3_ref"}],
                        "absoluteBoundingBox": {"x": 1100, "y": 1400, "width": 516, "height": 356},
                    },
                    # Features stats
                    {
                        "id": "1:895",
                        "type": "TEXT",
                        "name": "Big 5 Safaris",
                        "characters": "Big 5 Safaris",
                        "style": {"fontFamily": "Marcellus", "fontSize": 30, "fontWeight": 400,
                                  "textAlignHorizontal": "CENTER"},
                        "fills": [{"type": "SOLID", "visible": True,
                                   "color": {"r": 0.11, "g": 0.11, "b": 0.11, "a": 1.0}}],
                        "absoluteBoundingBox": {"x": 50, "y": 2800, "width": 200, "height": 40},
                    },
                    {
                        "id": "1:896",
                        "type": "TEXT",
                        "name": "22 Lodges",
                        "characters": "22 Private Safari Lodges",
                        "style": {"fontFamily": "Marcellus", "fontSize": 30, "fontWeight": 400,
                                  "textAlignHorizontal": "CENTER"},
                        "fills": [{"type": "SOLID", "visible": True,
                                   "color": {"r": 0.11, "g": 0.11, "b": 0.11, "a": 1.0}}],
                        "absoluteBoundingBox": {"x": 300, "y": 2800, "width": 300, "height": 40},
                    },
                ],
            },
        },
    },
}


# ---------------------------------------------------------------------------
# Extractor tests
# ---------------------------------------------------------------------------

class TestFigmaDesignExtractor:
    @pytest.fixture
    def extractor(self):
        return FigmaDesignExtractor(access_token="test-token")

    def _make_file_data(self):
        """Convert SAMPLE response into file_data format."""
        node = SAMPLE_FIGMA_NODE_RESPONSE["nodes"]["1:864"]["document"]
        return {
            "name": "Experience Madikwe",
            "document": {
                "id": "0:0",
                "name": "Document",
                "type": "DOCUMENT",
                "children": [node],
            },
        }

    def test_extract_text_content_verbatim(self, extractor):
        file_data = self._make_file_data()
        texts = extractor._extract_text_content(file_data)
        text_strings = [t["text"] for t in texts]
        assert "Join Us for an Unforgettable African Safari Experience" in text_strings
        assert "Choosing a Lodge" in text_strings
        assert "Big 5 Safaris" in text_strings
        assert "22 Private Safari Lodges" in text_strings

    def test_extract_text_sorted_by_position(self, extractor):
        file_data = self._make_file_data()
        texts = extractor._extract_text_content(file_data)
        ys = [t["y"] for t in texts]
        assert ys == sorted(ys), "Texts should be sorted by Y position"

    def test_extract_text_includes_styling(self, extractor):
        file_data = self._make_file_data()
        texts = extractor._extract_text_content(file_data)
        hero_text = next(t for t in texts if "Unforgettable" in t["text"])
        assert hero_text["font_family"] == "Marcellus"
        assert hero_text["font_size"] == 64
        assert hero_text["font_weight"] == 400
        assert hero_text["text_colour"] == "#ffffff"

    def test_extract_image_fills(self, extractor):
        file_data = self._make_file_data()
        images = extractor._extract_image_fills(file_data)
        assert len(images) >= 4  # hero + 3 lodge cards
        hero = next(i for i in images if i["width"] == 1920)
        assert hero["image_ref"] == "hero_ref_123"
        assert hero["height"] == 926

    def test_extract_inline_colours(self, extractor):
        file_data = self._make_file_data()
        colours = extractor._extract_inline_colours(file_data)
        hex_values = [c["hex"] for c in colours]
        assert "#ffffff" in hex_values  # white text
        assert "#1c1c1c" in hex_values  # dark text

    def test_extract_inline_typography(self, extractor):
        file_data = self._make_file_data()
        typo = extractor._extract_inline_typography(file_data)
        families = [t["font_family"] for t in typo]
        assert "Marcellus" in families
        assert "Avenir" in families

    def test_classify_typography(self, extractor):
        styles = [
            {"font_family": "Marcellus", "font_size": 64, "font_weight": 400},
            {"font_family": "Marcellus", "font_size": 40, "font_weight": 400},
            {"font_family": "Avenir", "font_size": 18, "font_weight": 350},
            {"font_family": "Avenir", "font_size": 16, "font_weight": 500},
        ]
        result = extractor._classify_typography(styles)
        assert result.heading_font == "Marcellus"
        assert result.body_font == "Avenir"

    def test_classify_colours(self, extractor):
        colours = [
            {"hex": "#ffffff", "source": "fills", "node_type": "TEXT", "name": "text", "parent_section": "root"},
            {"hex": "#1c1c1c", "source": "fills", "node_type": "TEXT", "name": "text", "parent_section": "root"},
            {"hex": "#fdfaf7", "source": "fills", "node_type": "FRAME", "name": "bg", "parent_section": "root"},
            {"hex": "#760906", "source": "fills", "node_type": "FRAME", "name": "btn", "parent_section": "root"},
            {"hex": "#48631b", "source": "fills", "node_type": "FRAME", "name": "accent", "parent_section": "root"},
        ]
        texts = [
            {"text_colour": "#1c1c1c"},
            {"text_colour": "#1c1c1c"},
            {"text_colour": "#ffffff"},
        ]
        result = extractor._classify_colours(colours, texts)
        assert result.text_primary == "#1c1c1c"
        assert result.background == "#fdfaf7"
        # Primary should be one of the saturated colours
        assert result.primary in ("#760906", "#48631b")

    @patch.object(FigmaDesignExtractor, "_get")
    @patch.object(FigmaDesignExtractor, "_export_images")
    def test_extract_full_pipeline(self, mock_export, mock_get, extractor):
        """Test the full extract() pipeline with mocked API."""
        # Mock _get for fetch_node
        mock_get.return_value = SAMPLE_FIGMA_NODE_RESPONSE

        # Mock _export_images
        mock_export.return_value = {
            "1:865": "https://figma-export.s3.amazonaws.com/hero.png",
            "1:890": "https://figma-export.s3.amazonaws.com/lodge1.png",
            "1:891": "https://figma-export.s3.amazonaws.com/lodge2.png",
            "1:892": "https://figma-export.s3.amazonaws.com/lodge3.png",
            "1:864": "https://figma-export.s3.amazonaws.com/screenshot.png",
        }

        # We need to mock _fetch_node to return proper file_data
        with patch.object(extractor, "_fetch_node") as mock_fetch:
            node = SAMPLE_FIGMA_NODE_RESPONSE["nodes"]["1:864"]["document"]
            mock_fetch.return_value = {
                "name": "Experience Madikwe",
                "document": {
                    "id": "0:0",
                    "name": "Document",
                    "type": "DOCUMENT",
                    "children": [node],
                },
            }

            ctx = extractor.extract(
                "https://www.figma.com/design/w8Qtdxpc6i6aOgcha3dllW/Experience-Madikwe?node-id=1-864"
            )

        assert isinstance(ctx, DesignContext)
        assert ctx.file_name == "Experience Madikwe"
        assert ctx.node_id == "1:864"
        assert len(ctx.raw_texts) >= 5
        assert len(ctx.raw_images) >= 4
        assert ctx.typography.heading_font == "Marcellus"
        assert ctx.typography.body_font == "Avenir"
