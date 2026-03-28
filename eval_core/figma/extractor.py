"""FigmaDesignExtractor — standalone Figma API extraction for site generation.

Reuses patterns from mcp_facade/facade/figma_client.py but runs standalone
without MCP or boto3 dependencies. Extracts everything needed to generate
a faithful HTML/CSS site from a Figma design.
"""

from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import parse_qs

import httpx


# ---------------------------------------------------------------------------
# URL parsing (from figma_client.py lines 35-78)
# ---------------------------------------------------------------------------

_FIGMA_KEY_RE = re.compile(r"^[A-Za-z0-9]{6,}$")
_KEY_IN_PATH_RE = re.compile(r"(?:file|design)/([A-Za-z0-9]{6,})(?:/([^?/]*))?")


def parse_figma_url(url: str) -> dict:
    """Parse Figma URL or raw file key -> {file_key, file_name, node_id}."""
    url = url.strip()
    if _FIGMA_KEY_RE.match(url):
        return {"file_key": url, "file_name": None, "node_id": None}

    match = _KEY_IN_PATH_RE.search(url)
    if match:
        file_key = match.group(1)
        file_name = match.group(2) if match.group(2) else None
        node_id = None
        qmark = url.find("?")
        if qmark != -1:
            query = parse_qs(url[qmark + 1:])
            node_id = query.get("node-id", [None])[0]
        return {"file_key": file_key, "file_name": file_name, "node_id": node_id}

    raise ValueError(f"Could not extract Figma file key from: '{url[:200]}'")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Section:
    """A semantic page section detected from the Figma design."""
    name: str
    semantic_role: str  # navigation | hero | content | grid | cta | footer | stats
    layout_description: str
    texts: list[dict] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    background: Optional[dict] = None  # {type: "colour"|"image"|"gradient", value: ...}
    y_position: float = 0.0
    width: float = 0.0
    height: float = 0.0
    frame_data: Optional[dict] = None  # raw frame for debugging


@dataclass
class ColourPalette:
    """Colour palette with semantic roles."""
    all_colours: list[dict] = field(default_factory=list)
    primary: str = ""
    secondary: str = ""
    accent: str = ""
    background: str = "#ffffff"
    text_primary: str = "#000000"
    text_secondary: str = "#ffffff"


@dataclass
class TypographySystem:
    """Typography system extracted from the design."""
    heading_font: str = ""
    body_font: str = ""
    all_styles: list[dict] = field(default_factory=list)


@dataclass
class DesignContext:
    """Complete design context extracted from Figma."""
    file_name: str = ""
    node_name: str = ""
    node_id: str = ""
    dimensions: dict = field(default_factory=dict)
    sections: list[Section] = field(default_factory=list)
    colours: ColourPalette = field(default_factory=ColourPalette)
    typography: TypographySystem = field(default_factory=TypographySystem)
    gradients: list[dict] = field(default_factory=list)
    screenshot_url: str = ""
    raw_frames: list[dict] = field(default_factory=list)
    raw_texts: list[dict] = field(default_factory=list)
    raw_images: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def _rgba_to_hex(r: float, g: float, b: float, a: float = 1.0) -> str:
    ri, gi, bi = round(r * 255), round(g * 255), round(b * 255)
    if a < 1.0:
        ai = round(a * 255)
        return f"#{ri:02x}{gi:02x}{bi:02x}{ai:02x}"
    return f"#{ri:02x}{gi:02x}{bi:02x}"


def _hex_to_hsl(hex_colour: str) -> tuple[float, float, float]:
    """Convert hex to HSL (0-360, 0-1, 0-1)."""
    h = hex_colour.lstrip("#")
    if len(h) == 8:
        h = h[:6]
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return (0.0, 0.0, l)
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hue = ((g - b) / d + (6 if g < b else 0)) / 6
    elif mx == g:
        hue = ((b - r) / d + 2) / 6
    else:
        hue = ((r - g) / d + 4) / 6
    return (hue * 360, s, l)


def _luminance(hex_colour: str) -> float:
    """Relative luminance (0=black, 1=white)."""
    _, _, l = _hex_to_hsl(hex_colour)
    return l


# ---------------------------------------------------------------------------
# FigmaDesignExtractor
# ---------------------------------------------------------------------------

class FigmaDesignExtractor:
    """Standalone Figma design extractor — no MCP, no boto3."""

    BASE_URL = "https://api.figma.com"

    def __init__(self, access_token: str):
        self._token = access_token

    # -- API calls ----------------------------------------------------------

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        headers = {"X-Figma-Token": self._token}
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

    def _fetch_node(self, file_key: str, node_id: str) -> dict:
        data = self._get(
            f"/v1/files/{file_key}/nodes",
            params={"ids": node_id},
        )
        node_data = data.get("nodes", {}).get(node_id, {})
        document = node_data.get("document", {})
        return {
            "name": data.get("name", ""),
            "document": {
                "id": "0:0",
                "name": "Document",
                "type": "DOCUMENT",
                "children": [document] if document else [],
            },
        }

    def _export_images(self, file_key: str, node_ids: list[str],
                       fmt: str = "png", scale: int = 2) -> dict[str, str]:
        """Export nodes as images, returns {node_id: temp_url}."""
        if not node_ids:
            return {}
        data = self._get(
            f"/v1/images/{file_key}",
            params={"ids": ",".join(node_ids), "format": fmt, "scale": str(scale)},
        )
        return data.get("images", {})

    # -- Tree walkers (from figma_client.py) ---------------------------------

    def _extract_frames(self, file_data: dict) -> list[dict]:
        frames: list[dict] = []
        document = file_data.get("document", {})
        self._walk_frames(document.get("children", []), frames,
                          parent_name="root", parent_id="")
        return frames

    def _walk_frames(self, children: list, frames: list,
                     parent_name: str, parent_id: str) -> None:
        for child in children:
            node_type = child.get("type", "")
            node_name = child.get("name", "")
            node_id = child.get("id", "")

            if node_type in ("FRAME", "COMPONENT", "COMPONENT_SET", "SECTION", "GROUP"):
                bbox = child.get("absoluteBoundingBox", {})

                bg_colour = None
                has_bg_image = False
                for fill in child.get("fills", []):
                    if not fill.get("visible", True):
                        continue
                    if fill.get("type") == "SOLID":
                        c = fill.get("color", {})
                        r = round(c.get("r", 0) * 255)
                        g = round(c.get("g", 0) * 255)
                        b = round(c.get("b", 0) * 255)
                        a = c.get("a", 1.0)
                        bg_colour = f"#{r:02x}{g:02x}{b:02x}" if a >= 1.0 else f"rgba({r},{g},{b},{a:.2f})"
                    elif fill.get("type") == "IMAGE":
                        has_bg_image = True

                box_shadow = None
                for effect in child.get("effects", []):
                    if effect.get("type") == "DROP_SHADOW" and effect.get("visible", True):
                        c = effect.get("color", {})
                        r = round(c.get("r", 0) * 255)
                        g = round(c.get("g", 0) * 255)
                        b = round(c.get("b", 0) * 255)
                        a = c.get("a", 1.0)
                        ox = effect.get("offset", {}).get("x", 0)
                        oy = effect.get("offset", {}).get("y", 4)
                        blur = effect.get("radius", 8)
                        box_shadow = f"{ox}px {oy}px {blur}px rgba({r},{g},{b},{a:.2f})"
                        break

                frames.append({
                    "node_id": node_id,
                    "name": node_name,
                    "type": node_type,
                    "parent_section": parent_name,
                    "parent_id": parent_id,
                    "layout_mode": child.get("layoutMode"),
                    "primary_axis_align": child.get("primaryAxisAlignItems", "MIN"),
                    "counter_axis_align": child.get("counterAxisAlignItems", "MIN"),
                    "padding_left": child.get("paddingLeft", 0),
                    "padding_right": child.get("paddingRight", 0),
                    "padding_top": child.get("paddingTop", 0),
                    "padding_bottom": child.get("paddingBottom", 0),
                    "item_spacing": child.get("itemSpacing", 0),
                    "background_colour": bg_colour,
                    "has_bg_image": has_bg_image,
                    "corner_radius": child.get("cornerRadius", 0),
                    "clips_content": child.get("clipsContent", False),
                    "box_shadow": box_shadow,
                    "width": bbox.get("width", 0),
                    "height": bbox.get("height", 0),
                    "x": bbox.get("x", 0),
                    "y": bbox.get("y", 0),
                    "child_count": len(child.get("children", [])),
                })

                ctx_name, ctx_id = node_name, node_id
            else:
                ctx_name, ctx_id = parent_name, parent_id

            if "children" in child:
                self._walk_frames(child["children"], frames,
                                  parent_name=ctx_name, parent_id=ctx_id)

    def _extract_text_content(self, file_data: dict) -> list[dict]:
        texts: list[dict] = []
        document = file_data.get("document", {})
        self._walk_text(document.get("children", []), texts,
                        parent_name="root", parent_id="")
        texts.sort(key=lambda t: (t.get("y", 0), t.get("x", 0)))
        return texts

    def _walk_text(self, children: list, texts: list,
                   parent_name: str, parent_id: str) -> None:
        for child in children:
            node_type = child.get("type", "")
            node_name = child.get("name", "")
            if node_type == "TEXT":
                characters = child.get("characters", "")
                if characters and characters.strip():
                    style = child.get("style", {})
                    bbox = child.get("absoluteBoundingBox", {})
                    text_colour = None
                    for fill in child.get("fills", []):
                        if fill.get("type") == "SOLID" and fill.get("visible", True):
                            c = fill.get("color", {})
                            r = round(c.get("r", 0) * 255)
                            g = round(c.get("g", 0) * 255)
                            b = round(c.get("b", 0) * 255)
                            a = c.get("a", 1.0)
                            text_colour = f"#{r:02x}{g:02x}{b:02x}" if a >= 1.0 else f"rgba({r},{g},{b},{a:.2f})"
                            break
                    texts.append({
                        "node_id": child.get("id", ""),
                        "node_name": node_name,
                        "text": characters.strip(),
                        "parent_section": parent_name,
                        "parent_id": parent_id,
                        "font_size": style.get("fontSize"),
                        "font_weight": style.get("fontWeight"),
                        "font_family": style.get("fontFamily"),
                        "line_height": style.get("lineHeightPx"),
                        "text_align": style.get("textAlignHorizontal", "LEFT"),
                        "text_colour": text_colour,
                        "x": bbox.get("x", 0),
                        "y": bbox.get("y", 0),
                        "width": bbox.get("width", 0),
                        "height": bbox.get("height", 0),
                    })
            if "children" in child:
                ctx_name = node_name if node_type in ("FRAME", "SECTION", "COMPONENT", "GROUP") else parent_name
                ctx_id = child.get("id", "") if node_type in ("FRAME", "SECTION", "COMPONENT", "GROUP") else parent_id
                self._walk_text(child["children"], texts,
                                parent_name=ctx_name, parent_id=ctx_id)

    def _extract_image_fills(self, file_data: dict) -> list[dict]:
        images: list[dict] = []
        seen: set[str] = set()
        document = file_data.get("document", {})
        self._walk_images(document.get("children", []), images, seen,
                          parent_name="root", parent_id="")
        return images

    def _walk_images(self, children: list, images: list, seen: set,
                     parent_name: str, parent_id: str) -> None:
        for child in children:
            node_id = child.get("id", "")
            node_name = child.get("name", "")
            node_type = child.get("type", "")
            ctx_name = node_name if node_type in ("FRAME", "SECTION", "COMPONENT", "GROUP") else parent_name
            ctx_id = node_id if node_type in ("FRAME", "SECTION", "COMPONENT", "GROUP") else parent_id

            for fill in child.get("fills", []):
                if fill.get("type") == "IMAGE" and fill.get("visible", True):
                    if node_id and node_id not in seen:
                        seen.add(node_id)
                        bbox = child.get("absoluteBoundingBox", {})
                        images.append({
                            "node_id": node_id,
                            "node_name": node_name,
                            "parent_section": ctx_name,
                            "parent_id": ctx_id,
                            "image_ref": fill.get("imageRef", ""),
                            "x": bbox.get("x", 0),
                            "y": bbox.get("y", 0),
                            "width": bbox.get("width", 0),
                            "height": bbox.get("height", 0),
                        })
                    break

            if "children" in child:
                self._walk_images(child["children"], images, seen,
                                  parent_name=ctx_name, parent_id=ctx_id)

    def _extract_inline_colours(self, file_data: dict) -> list[dict]:
        seen: set[str] = set()
        colours: list[dict] = []
        document = file_data.get("document", {})
        self._walk_colours(document.get("children", []), colours, seen)
        return colours

    def _walk_colours(self, children: list, colours: list, seen: set,
                      parent_name: str = "root") -> None:
        for child in children:
            node_name = child.get("name", "")
            node_type = child.get("type", "")
            ctx = node_name if node_type in ("FRAME", "SECTION", "COMPONENT") else parent_name
            for prop in ("fills", "strokes"):
                for fill in child.get(prop, []):
                    if not fill.get("visible", True):
                        continue
                    if fill.get("type") == "SOLID":
                        c = fill.get("color", {})
                        hex_val = _rgba_to_hex(c.get("r", 0), c.get("g", 0),
                                               c.get("b", 0), c.get("a", 1.0))
                        if hex_val not in seen:
                            seen.add(hex_val)
                            colours.append({
                                "name": node_name,
                                "hex": hex_val,
                                "source": prop,
                                "parent_section": ctx,
                                "node_type": node_type,
                            })
            if "children" in child:
                self._walk_colours(child["children"], colours, seen, parent_name=ctx)

    def _extract_inline_typography(self, file_data: dict) -> list[dict]:
        seen: set[str] = set()
        typography: list[dict] = []
        document = file_data.get("document", {})
        self._walk_typography(document.get("children", []), typography, seen)
        return typography

    def _walk_typography(self, children: list, typography: list, seen: set) -> None:
        for child in children:
            if child.get("type") == "TEXT":
                style = child.get("style", {})
                family = style.get("fontFamily", "")
                size = style.get("fontSize", 16)
                weight = style.get("fontWeight", 400)
                key = f"{family}:{size}:{weight}"
                if key not in seen and family:
                    seen.add(key)
                    typography.append({
                        "name": child.get("name", "Text"),
                        "font_family": family,
                        "font_size": size,
                        "font_weight": weight,
                        "line_height": style.get("lineHeightPx"),
                        "letter_spacing": style.get("letterSpacing", 0),
                    })
            if "children" in child:
                self._walk_typography(child["children"], typography, seen)

    def _extract_gradients(self, file_data: dict) -> list[dict]:
        gradients: list[dict] = []
        document = file_data.get("document", {})
        self._walk_gradients(document.get("children", []), gradients, parent_name="root")
        return gradients

    def _walk_gradients(self, children: list, gradients: list,
                        parent_name: str) -> None:
        for child in children:
            node_name = child.get("name", "")
            node_type = child.get("type", "")
            ctx = node_name if node_type in ("FRAME", "SECTION", "COMPONENT") else parent_name
            for fill in child.get("fills", []):
                if not fill.get("visible", True):
                    continue
                if not fill.get("type", "").startswith("GRADIENT_"):
                    continue
                stops = fill.get("gradientStops", [])
                if not stops:
                    continue
                css_stops = []
                for stop in stops:
                    c = stop.get("color", {})
                    r, g, b = round(c.get("r", 0) * 255), round(c.get("g", 0) * 255), round(c.get("b", 0) * 255)
                    a = c.get("a", 1.0)
                    pos = round(stop.get("position", 0) * 100)
                    clr = f"rgba({r},{g},{b},{a:.2f})" if a < 1.0 else f"rgb({r},{g},{b})"
                    css_stops.append(f"{clr} {pos}%")
                handles = fill.get("gradientHandlePositions", [])
                angle = self._gradient_angle(handles)
                gradients.append({
                    "node_name": node_name,
                    "parent_section": ctx,
                    "gradient_type": fill["type"],
                    "css": f"linear-gradient({angle}deg, {', '.join(css_stops)})",
                    "stop_count": len(stops),
                })
            if "children" in child:
                self._walk_gradients(child["children"], gradients, parent_name=ctx)

    @staticmethod
    def _gradient_angle(handles: list) -> int:
        if len(handles) < 2:
            return 180
        p0, p1 = handles[0], handles[1]
        dx = p1.get("x", 1) - p0.get("x", 0)
        dy = p1.get("y", 1) - p0.get("y", 0)
        return round(math.degrees(math.atan2(dx, -dy))) % 360

    # -- Colour role classification -----------------------------------------

    def _classify_colours(self, colours: list[dict],
                          texts: list[dict]) -> ColourPalette:
        palette = ColourPalette(all_colours=colours)
        if not colours:
            return palette

        # Collect text colours
        text_colours: dict[str, int] = {}
        for t in texts:
            tc = t.get("text_colour")
            if tc and not tc.startswith("rgba"):
                text_colours[tc] = text_colours.get(tc, 0) + 1

        # Collect frame background colours
        bg_colours: dict[str, int] = {}
        for c in colours:
            if c.get("node_type") in ("FRAME", "SECTION", "COMPONENT"):
                bg_colours[c["hex"]] = bg_colours.get(c["hex"], 0) + 1

        # Text primary = most common text colour
        if text_colours:
            sorted_tc = sorted(text_colours.items(), key=lambda x: -x[1])
            palette.text_primary = sorted_tc[0][0]
            # Find white/light text for dark backgrounds
            for tc, _ in sorted_tc:
                if _luminance(tc) > 0.8:
                    palette.text_secondary = tc
                    break

        # Background = lightest colour used as frame bg, or most common
        if bg_colours:
            sorted_bg = sorted(bg_colours.keys(), key=lambda h: -_luminance(h))
            palette.background = sorted_bg[0]

        # Primary/accent = most saturated non-white, non-black colours
        saturated = []
        for c in colours:
            h = c["hex"]
            if h.startswith("rgba"):
                continue
            _, s, l = _hex_to_hsl(h)
            if s > 0.15 and 0.1 < l < 0.9:
                saturated.append((h, s, l))

        saturated.sort(key=lambda x: -x[1])
        seen = set()
        unique_saturated = []
        for h, s, l in saturated:
            if h not in seen:
                seen.add(h)
                unique_saturated.append((h, s, l))

        if unique_saturated:
            palette.primary = unique_saturated[0][0]
        if len(unique_saturated) > 1:
            palette.secondary = unique_saturated[1][0]
        if len(unique_saturated) > 2:
            palette.accent = unique_saturated[2][0]

        return palette

    # -- Typography classification ------------------------------------------

    def _classify_typography(self, styles: list[dict]) -> TypographySystem:
        system = TypographySystem(all_styles=styles)
        if not styles:
            return system

        # Count font family usage
        family_sizes: dict[str, list[float]] = {}
        for s in styles:
            fam = s.get("font_family", "")
            if fam:
                family_sizes.setdefault(fam, []).append(s.get("font_size", 16))

        if not family_sizes:
            return system

        # Heading font = family used at largest sizes
        # Body font = family used at smallest/most common sizes
        families_by_max_size = sorted(
            family_sizes.items(),
            key=lambda x: -max(x[1]),
        )

        system.heading_font = families_by_max_size[0][0]
        if len(families_by_max_size) > 1:
            system.body_font = families_by_max_size[1][0]
        else:
            system.body_font = system.heading_font

        return system

    # -- Main extraction pipeline -------------------------------------------

    def extract(self, figma_url: str) -> DesignContext:
        """Extract complete design context from a Figma URL."""
        parsed = parse_figma_url(figma_url)
        file_key = parsed["file_key"]
        node_id = parsed.get("node_id")

        if node_id:
            node_id = node_id.replace("-", ":")
            file_data = self._fetch_node(file_key, node_id)
        else:
            file_data = self._get(f"/v1/files/{file_key}")

        file_name = file_data.get("name", "")
        children = file_data.get("document", {}).get("children", [])
        target = children[0] if children else {}
        node_name = target.get("name", "")
        bbox = target.get("absoluteBoundingBox", {})

        # Extract everything
        frames = self._extract_frames(file_data)
        texts = self._extract_text_content(file_data)
        images = self._extract_image_fills(file_data)
        colours = self._extract_inline_colours(file_data)
        typography_styles = self._extract_inline_typography(file_data)
        gradients = self._extract_gradients(file_data)

        # Detect small icon frames (vector components without IMAGE fills)
        # These need to be exported as PNG since they aren't in image_fills
        image_node_id_set = {img["node_id"] for img in images}
        icon_frames = []
        for child in target.get("children", []):
            cid = child.get("id", "")
            ctype = child.get("type", "")
            bbox_c = child.get("absoluteBoundingBox", {})
            w = bbox_c.get("width", 0)
            h = bbox_c.get("height", 0)
            # Small frames/components that aren't already in image_fills
            if (ctype in ("FRAME", "COMPONENT", "INSTANCE", "GROUP")
                    and w < 120 and h < 120 and w > 20 and h > 20
                    and cid not in image_node_id_set):
                icon_frames.append({
                    "node_id": cid,
                    "node_name": child.get("name", "icon"),
                    "parent_section": target.get("name", "root"),
                    "parent_id": target.get("id", ""),
                    "image_ref": "",
                    "x": bbox_c.get("x", 0),
                    "y": bbox_c.get("y", 0),
                    "width": w,
                    "height": h,
                    "is_icon_frame": True,
                })
        images.extend(icon_frames)

        # Export images (batch all node IDs in one call)
        image_node_ids = [img["node_id"] for img in images if img.get("node_id")]
        if image_node_ids:
            exported = self._export_images(file_key, image_node_ids)
            for img in images:
                nid = img.get("node_id", "")
                if nid in exported and exported[nid]:
                    img["temp_url"] = exported[nid]

        # Export full-page screenshot
        screenshot_url = ""
        screenshot_node = node_id or (target.get("id") if target else "")
        if screenshot_node:
            screenshot_export = self._export_images(
                file_key, [screenshot_node], fmt="png", scale=1,
            )
            screenshot_url = screenshot_export.get(screenshot_node, "")

        # Classify
        palette = self._classify_colours(colours, texts)
        typo_system = self._classify_typography(typography_styles)

        # Detect sections
        from eval_core.figma.section_detector import detect_sections
        sections = detect_sections(frames, texts, images, target)

        return DesignContext(
            file_name=file_name,
            node_name=node_name,
            node_id=node_id or "",
            dimensions={"width": bbox.get("width", 0), "height": bbox.get("height", 0)},
            sections=sections,
            colours=palette,
            typography=typo_system,
            gradients=gradients,
            screenshot_url=screenshot_url,
            raw_frames=frames,
            raw_texts=texts,
            raw_images=images,
        )
