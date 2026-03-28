"""Section detector — groups flat Figma nodes into semantic page sections.

Groups top-level children of the target node into semantic sections
(header, hero, content, grid, footer) using frame name heuristics,
position analysis, and child-content analysis.
"""

from __future__ import annotations

import re
from typing import Optional

from eval_core.figma.extractor import Section


# ---------------------------------------------------------------------------
# Name-based role detection
# ---------------------------------------------------------------------------

_ROLE_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("navigation", re.compile(r"(header|nav|navigation|menu|top.?bar)", re.I)),
    ("hero", re.compile(r"(hero|banner|masthead|landing|splash|cover)", re.I)),
    ("footer", re.compile(r"(footer|bottom.?bar|copyright)", re.I)),
    ("cta", re.compile(r"(cta|call.?to.?action|contact|get.?in.?touch|reach)", re.I)),
    ("stats", re.compile(r"(stats|features|highlights|numbers|icons?)", re.I)),
    ("grid", re.compile(r"(grid|gallery|cards|lodg|portfolio|showcase|projects)", re.I)),
    ("about", re.compile(r"(about|who.?we|story|mission|await)", re.I)),
    ("testimonials", re.compile(r"(testimon|review|quote|client)", re.I)),
    ("pricing", re.compile(r"(pric|plan|package|tier)", re.I)),
]


def _classify_by_name(name: str) -> Optional[str]:
    """Match frame name against known patterns."""
    for role, pattern in _ROLE_PATTERNS:
        if pattern.search(name):
            return role
    return None


# ---------------------------------------------------------------------------
# Structure-based role detection
# ---------------------------------------------------------------------------

def _classify_by_structure(frame: dict, index: int, total: int,
                           child_frames: list[dict],
                           child_images: list[dict]) -> str:
    """Classify role by position and content structure."""
    width = frame.get("width", 0)
    height = frame.get("height", 0)
    has_bg_image = frame.get("has_bg_image", False)
    child_count = frame.get("child_count", 0)

    # First frame with horizontal layout and small height = navigation
    if index == 0 and height < 150:
        return "navigation"

    # Last frame = footer
    if index == total - 1:
        return "footer"

    # Large frame with background image near top = hero
    if has_bg_image and height > 400 and index <= 2:
        return "hero"

    # Frame with many similar-sized image children = grid
    if child_images:
        # Check if images are similar sizes (grid pattern)
        if len(child_images) >= 4:
            widths = [img.get("width", 0) for img in child_images]
            if widths:
                avg_w = sum(widths) / len(widths)
                similar = sum(1 for w in widths if abs(w - avg_w) < avg_w * 0.3)
                if similar >= len(widths) * 0.6:
                    return "grid"

    # Frame with icon-sized children in horizontal layout = stats
    if child_count >= 3 and frame.get("layout_mode") == "HORIZONTAL":
        if all(cf.get("width", 0) < 200 for cf in child_frames[:5]):
            return "stats"

    return "content"


# ---------------------------------------------------------------------------
# Layout description generator
# ---------------------------------------------------------------------------

def _describe_layout(frame: dict, child_frames: list[dict],
                     child_texts: list[dict], child_images: list[dict],
                     role: str) -> str:
    """Generate human-readable layout description."""
    layout_mode = frame.get("layout_mode")
    width = frame.get("width", 0)
    height = frame.get("height", 0)
    has_bg_image = frame.get("has_bg_image", False)
    bg_colour = frame.get("background_colour")

    parts = []

    # Overall layout
    if layout_mode == "HORIZONTAL":
        parts.append("horizontal layout")
    elif layout_mode == "VERTICAL":
        parts.append("vertical layout")
    else:
        parts.append(f"absolute layout ({int(width)}x{int(height)}px)")

    # Background
    if has_bg_image:
        parts.append("with background image")
    elif bg_colour:
        parts.append(f"background: {bg_colour}")

    # Content arrangement
    if role == "grid" and child_images:
        cols = _detect_columns(child_images)
        rows = max(1, len(child_images) // cols) if cols else 1
        parts.append(f"{cols}x{rows} image grid ({len(child_images)} items)")

    elif role == "hero":
        if child_texts:
            text_x = min(t.get("x", 0) for t in child_texts)
            text_w = max(t.get("width", 0) for t in child_texts)
            if text_w < width * 0.6:
                parts.append("text left-aligned with dark overlay")
            else:
                parts.append("centered text with dark overlay")

    elif child_texts and child_images:
        # Check for split layout (text one side, image other)
        if len(child_images) == 1:
            img = child_images[0]
            avg_text_x = sum(t.get("x", 0) for t in child_texts) / len(child_texts)
            img_x = img.get("x", 0)
            if img_x > avg_text_x + 200:
                text_pct = int((avg_text_x + max(t.get("width", 0) for t in child_texts)) / width * 100)
                parts.append(f"2-column split: text left ~{text_pct}%, image right ~{100-text_pct}%")
            elif img_x < avg_text_x - 200:
                parts.append("2-column split: image left, text right")

    # Padding/spacing
    pad_l = frame.get("padding_left", 0)
    pad_t = frame.get("padding_top", 0)
    spacing = frame.get("item_spacing", 0)
    if pad_l or pad_t:
        parts.append(f"padding: {int(pad_t)}px {int(pad_l)}px")
    if spacing:
        parts.append(f"gap: {int(spacing)}px")

    return "; ".join(parts)


def _detect_columns(images: list[dict]) -> int:
    """Detect number of columns from image positions."""
    if not images:
        return 1
    # Group by similar Y positions (same row)
    ys = sorted(set(round(img.get("y", 0) / 50) * 50 for img in images))
    if not ys:
        return 1
    # Count items in first row
    first_row_y = ys[0]
    first_row = [img for img in images if abs(round(img.get("y", 0) / 50) * 50 - first_row_y) < 2]
    return max(1, len(first_row))


# ---------------------------------------------------------------------------
# Main detection
# ---------------------------------------------------------------------------

def detect_sections(frames: list[dict], texts: list[dict],
                    images: list[dict], target_node: dict) -> list[Section]:
    """Detect semantic page sections from extracted Figma data.

    Handles both well-structured designs (top-level frames = sections) and
    flat designs (65+ direct children that need Y-position clustering).

    Args:
        frames: All frames extracted from the design
        texts: All text content
        images: All image fills
        target_node: The root node of the design

    Returns:
        List of Section objects sorted by Y position
    """
    if not target_node:
        return []

    target_id = target_node.get("id", "")

    # Get top-level children of the target node
    top_level_frames = [f for f in frames if f.get("parent_id") == target_id]

    # If many small top-level children (flat design), cluster by Y position
    if len(top_level_frames) > 15:
        sections = _detect_from_flat_design(top_level_frames, frames, texts, images, target_node)
        return _absorb_tiny_sections(sections)
    # Note: _absorb_tiny_sections is also called at the end for non-flat designs

    # If we have no top-level frames, fallback
    if not top_level_frames:
        top_level_frames = _cluster_into_sections(frames, target_node)

    # Sort by Y position
    top_level_frames.sort(key=lambda f: f.get("y", 0))

    sections: list[Section] = []
    total = len(top_level_frames)

    for idx, frame in enumerate(top_level_frames):
        fid = frame.get("node_id", "")
        fname = frame.get("name", f"Section {idx + 1}")

        # Classify role
        role = _classify_by_name(fname)

        # Collect children of this section
        child_frames = [f for f in frames if f.get("parent_id") == fid]
        child_texts = [t for t in texts
                       if t.get("parent_id") == fid or t.get("parent_section") == fname]
        child_images = [i for i in images
                        if i.get("parent_id") == fid or i.get("parent_section") == fname]

        # Also collect texts/images from nested children
        descendant_ids = _get_descendant_ids(fid, frames)
        for did in descendant_ids:
            child_texts.extend(t for t in texts if t.get("parent_id") == did
                               and t not in child_texts)
            child_images.extend(i for i in images if i.get("parent_id") == did
                                and i not in child_images)

        if not role:
            role = _classify_by_structure(frame, idx, total,
                                          child_frames, child_images)

        # Generate layout description
        layout_desc = _describe_layout(frame, child_frames, child_texts,
                                       child_images, role)

        # Determine background
        background = None
        if frame.get("has_bg_image"):
            # Find the image fill for this frame
            frame_img = next((i for i in images if i.get("node_id") == fid), None)
            background = {"type": "image", "image": frame_img}
        elif frame.get("background_colour"):
            background = {"type": "colour", "value": frame["background_colour"]}

        # Sort texts by reading order within section
        child_texts.sort(key=lambda t: (t.get("y", 0), t.get("x", 0)))

        sections.append(Section(
            name=fname,
            semantic_role=role,
            layout_description=layout_desc,
            texts=child_texts,
            images=child_images,
            background=background,
            y_position=frame.get("y", 0),
            width=frame.get("width", 0),
            height=frame.get("height", 0),
            frame_data=frame,
        ))

    # Handle orphan texts/images not in any section
    assigned_text_ids = {id(t) for s in sections for t in s.texts}
    assigned_img_ids = {id(i) for s in sections for i in s.images}
    orphan_texts = [t for t in texts if id(t) not in assigned_text_ids]
    orphan_images = [i for i in images if id(i) not in assigned_img_ids]

    if orphan_texts or orphan_images:
        # Try to assign orphans to nearest section by Y position
        for item in orphan_texts + orphan_images:
            y = item.get("y", 0)
            best_section = None
            best_dist = float("inf")
            for section in sections:
                sy = section.y_position
                sh = section.height
                if sy <= y <= sy + sh:
                    best_section = section
                    break
                dist = min(abs(y - sy), abs(y - (sy + sh)))
                if dist < best_dist:
                    best_dist = dist
                    best_section = section
            if best_section:
                if item in orphan_texts:
                    best_section.texts.append(item)
                else:
                    best_section.images.append(item)

    return _absorb_tiny_sections(sections)


def _get_descendant_ids(parent_id: str, frames: list[dict]) -> set[str]:
    """Get all descendant frame IDs recursively."""
    descendants: set[str] = set()
    queue = [parent_id]
    while queue:
        pid = queue.pop()
        for f in frames:
            if f.get("parent_id") == pid:
                fid = f["node_id"]
                if fid not in descendants:
                    descendants.add(fid)
                    queue.append(fid)
    return descendants


def _absorb_tiny_sections(sections: list[Section]) -> list[Section]:
    """Absorb tiny sections (< 150px tall, few items) into the nearest larger section.

    Flat Figma designs often have small groups (CTAs, icon frames) that
    shouldn't be their own page sections. Merge their content into the
    nearest substantial section.
    """
    if len(sections) < 2:
        return sections

    substantial = []
    tiny = []
    for s in sections:
        # Keep sections that have real content or are large enough
        has_images = len(s.images) > 0 and any(
            img.get("width", 0) > 200 for img in s.images
        )
        is_large = s.height > 150
        has_many_texts = len(s.texts) >= 3
        is_footer = s.semantic_role == "footer"

        if is_large or has_images or has_many_texts or is_footer:
            substantial.append(s)
        else:
            tiny.append(s)

    if not tiny:
        return sections

    # Absorb each tiny section into the nearest substantial section by Y
    for t in tiny:
        best = None
        best_dist = float("inf")
        for s in substantial:
            dist = abs(t.y_position - s.y_position)
            if dist < best_dist:
                best_dist = dist
                best = s
        if best:
            best.texts.extend(t.texts)
            best.images.extend(t.images)
            best.texts.sort(key=lambda x: (x.get("y", 0), x.get("x", 0)))

    return substantial


def _cluster_into_sections(frames: list[dict], target_node: dict) -> list[dict]:
    """Fallback: cluster frames by Y position into sections when no
    clear top-level structure exists."""
    if not frames:
        return []
    root_name = target_node.get("name", "root")
    return [f for f in frames if f.get("parent_section") == root_name]


# ---------------------------------------------------------------------------
# Flat design handler — clusters 65+ direct children by Y bands
# ---------------------------------------------------------------------------

def _detect_from_flat_design(top_level_frames: list[dict],
                              all_frames: list[dict],
                              texts: list[dict],
                              images: list[dict],
                              target_node: dict) -> list[Section]:
    """Handle flat Figma designs where all elements are direct children.

    Groups elements by Y-position bands (large gaps = new section).
    """
    # Collect ALL items (frames, texts, images) with Y positions
    all_items: list[dict] = []

    for f in top_level_frames:
        all_items.append({
            "type": "frame", "data": f,
            "y": f.get("y", 0), "height": f.get("height", 0),
            "name": f.get("name", ""),
        })

    # Also add orphan texts/images from direct children of target
    target_id = target_node.get("id", "")
    target_name = target_node.get("name", "")

    for t in texts:
        if t.get("parent_id") == target_id or t.get("parent_section") == target_name:
            all_items.append({
                "type": "text", "data": t,
                "y": t.get("y", 0), "height": t.get("height", 0),
                "name": t.get("node_name", ""),
            })

    for img in images:
        if img.get("parent_id") == target_id or img.get("parent_section") == target_name:
            all_items.append({
                "type": "image", "data": img,
                "y": img.get("y", 0), "height": img.get("height", 0),
                "name": img.get("node_name", ""),
            })

    if not all_items:
        return []

    # Sort by Y position
    all_items.sort(key=lambda x: x["y"])

    # Cluster by Y gaps — a gap > 100px between bottom of one item and top of next = new section
    clusters: list[list[dict]] = [[]]
    for item in all_items:
        if clusters[-1]:
            last = clusters[-1][-1]
            last_bottom = last["y"] + last["height"]
            gap = item["y"] - last_bottom
            if gap > 100:
                clusters.append([])
        clusters[-1].append(item)

    # Convert clusters to sections
    sections: list[Section] = []
    for cluster_idx, cluster in enumerate(clusters):
        cluster_texts = [item["data"] for item in cluster if item["type"] == "text"]
        cluster_images = [item["data"] for item in cluster if item["type"] == "image"]
        cluster_frames = [item["data"] for item in cluster if item["type"] == "frame"]

        # Also collect nested texts/images from frames in this cluster
        for frame_item in [item for item in cluster if item["type"] == "frame"]:
            fid = frame_item["data"].get("node_id", "")
            fname = frame_item["data"].get("name", "")
            descendant_ids = _get_descendant_ids(fid, all_frames)
            descendant_ids.add(fid)
            for did in descendant_ids:
                for t in texts:
                    if t.get("parent_id") == did and t not in cluster_texts:
                        cluster_texts.append(t)
                for img in images:
                    if img.get("parent_id") == did and img not in cluster_images:
                        cluster_images.append(img)

        # Sort texts by reading order
        cluster_texts.sort(key=lambda t: (t.get("y", 0), t.get("x", 0)))

        # Determine section name from content
        name = _infer_section_name(cluster, cluster_texts, cluster_images, cluster_idx)

        # Determine role
        role = _classify_by_name(name)
        if not role:
            role = _infer_role_from_content(
                cluster, cluster_texts, cluster_images, cluster_idx, len(clusters),
            )

        # Y bounds
        min_y = min(item["y"] for item in cluster)
        max_bottom = max(item["y"] + item["height"] for item in cluster)
        total_width = max((item["data"].get("width", 0) for item in cluster), default=0)

        # Background
        background = None
        bg_frame = next(
            (item for item in cluster if item["type"] == "frame"
             and item["data"].get("has_bg_image")),
            None,
        )
        if bg_frame:
            bg_img = next((img for img in cluster_images
                           if img.get("node_id") == bg_frame["data"].get("node_id")), None)
            background = {"type": "image", "image": bg_img}
        else:
            bg_frame = next(
                (item for item in cluster if item["type"] == "frame"
                 and item["data"].get("background_colour")),
                None,
            )
            if bg_frame:
                background = {"type": "colour", "value": bg_frame["data"]["background_colour"]}

        # Layout description
        layout = _describe_cluster_layout(cluster, cluster_texts, cluster_images, role)

        sections.append(Section(
            name=name,
            semantic_role=role,
            layout_description=layout,
            texts=cluster_texts,
            images=cluster_images,
            background=background,
            y_position=min_y,
            width=total_width,
            height=max_bottom - min_y,
        ))

    return sections


def _infer_section_name(cluster: list[dict], texts: list[dict],
                        images: list[dict], idx: int) -> str:
    """Infer a meaningful section name from cluster content."""
    # Try frame/group names first
    for item in cluster:
        if item["type"] == "frame":
            name = item["name"]
            role = _classify_by_name(name)
            if role:
                return name

    # Use first large heading text
    for t in texts:
        size = t.get("font_size", 16)
        if size >= 30 and len(t.get("text", "")) > 5:
            text = t["text"]
            return text[:50].strip()

    # Use frame name
    for item in cluster:
        if item["type"] == "frame":
            name = item["name"]
            if name and not name.startswith("Rectangle") and not name.startswith("Ellipse"):
                return name

    return f"Section {idx + 1}"


def _infer_role_from_content(cluster: list[dict], texts: list[dict],
                              images: list[dict], idx: int, total: int) -> str:
    """Infer semantic role from cluster content."""
    # First cluster with large image = hero
    if idx <= 1:
        large_images = [item for item in cluster
                        if item["type"] == "image" and item["data"].get("width", 0) > 1000]
        if large_images:
            return "hero"

    # Last cluster = footer
    if idx == total - 1:
        return "footer"

    # Many similar-sized images = grid
    if len(images) >= 4:
        widths = [img.get("width", 0) for img in images]
        if widths:
            avg_w = sum(widths) / len(widths)
            similar = sum(1 for w in widths if abs(w - avg_w) < avg_w * 0.3)
            if similar >= len(widths) * 0.6:
                return "grid"

    # Small items (icons) = stats
    small_frames = [item for item in cluster
                    if item["type"] == "frame" and item["data"].get("width", 0) < 100]
    if len(small_frames) >= 3:
        return "stats"

    # First cluster with nav-like text
    if idx == 0:
        for t in texts:
            text = t.get("text", "").lower()
            if any(kw in text for kw in ("home", "contact", "about", "menu")):
                return "navigation"

    return "content"


def _describe_cluster_layout(cluster: list[dict], texts: list[dict],
                              images: list[dict], role: str) -> str:
    """Generate layout description for a Y-clustered section."""
    parts = []

    # Count item types
    n_images = len(images)
    n_texts = len(texts)

    if role == "hero":
        parts.append("full-width hero section")
        if any(item["type"] == "image" and item["data"].get("width", 0) > 1000 for item in cluster):
            parts.append("background image with text overlay")
    elif role == "grid":
        cols = _detect_columns(images)
        rows = max(1, n_images // cols) if cols else 1
        parts.append(f"{cols}x{rows} image grid ({n_images} items)")
    elif role == "stats":
        n_icons = sum(1 for item in cluster
                      if item["type"] == "frame" and item["data"].get("width", 0) < 100)
        parts.append(f"stats/features row with {n_icons} icons")
    elif role == "footer":
        parts.append("footer section")
    elif role == "navigation":
        parts.append("navigation bar")
    else:
        if n_images == 1 and n_texts > 0:
            parts.append("content section with image and text")
        elif n_images > 1:
            parts.append(f"content section with {n_images} images")
        else:
            parts.append(f"content section with {n_texts} text elements")

    # Background info
    bg_item = next(
        (item for item in cluster if item["type"] == "frame"
         and item["data"].get("background_colour")),
        None,
    )
    if bg_item:
        parts.append(f"background: {bg_item['data']['background_colour']}")

    return "; ".join(parts)
