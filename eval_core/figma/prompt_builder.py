"""DesignPromptBuilder — formats DesignContext into model prompt.

Produces a structured prompt with:
- Section-by-section specs with verbatim text + image URLs
- Colour palette with semantic roles
- Typography system
- Layout descriptions
- Optional vision input (Figma screenshot)
"""

from __future__ import annotations

from eval_core.figma.extractor import DesignContext, Section


# ---------------------------------------------------------------------------
# Google Fonts substitution map
# ---------------------------------------------------------------------------

_FONT_SUBSTITUTES: dict[str, str] = {
    "Avenir": "Nunito Sans",
    "Avenir Next": "Nunito Sans",
    "Helvetica": "Inter",
    "Helvetica Neue": "Inter",
    "Arial": "Inter",
    "Futura": "Jost",
    "Gill Sans": "Lato",
    "Proxima Nova": "Montserrat",
    "SF Pro": "Inter",
    "SF Pro Display": "Inter",
    "Segoe UI": "Inter",
    "Roboto": "Roboto",
}


def _google_font(family: str) -> str:
    """Return Google Fonts-compatible name, substituting system fonts."""
    return _FONT_SUBSTITUTES.get(family, family)


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

class DesignPromptBuilder:
    """Formats a DesignContext into prompts for site generation models."""

    def build(self, context: DesignContext,
              include_screenshot: bool = True) -> dict:
        """Build the full prompt for a model.

        Returns:
            {
                "system_prompt": str,
                "user_content": str | list  (list for vision models)
            }
        """
        system = self._build_system_prompt()
        design_spec = self._build_design_spec(context)

        # For vision models: multipart content with screenshot + text
        if include_screenshot and context.screenshot_url:
            user_content = [
                {
                    "type": "image_url",
                    "image_url": {"url": context.screenshot_url},
                },
                {"type": "text", "text": design_spec},
            ]
        else:
            user_content = design_spec

        return {
            "system_prompt": system,
            "user_content": user_content,
        }

    def _build_system_prompt(self) -> str:
        return """You are a production website builder. You receive a complete design specification extracted from a Figma design and you generate a pixel-faithful HTML/CSS reproduction.

ABSOLUTE RULES:
1. Reproduce the design EXACTLY — same sections, same order, same layout
2. Use the EXACT text content provided — do NOT paraphrase, invent, summarise, or add text
3. Use the EXACT image URLs provided — do NOT substitute with other images or descriptions
4. Use the EXACT colours and fonts specified — do NOT change the colour scheme
5. ALL image src attributes MUST start with https:// — NEVER use descriptions or placeholders
6. White text on dark/image backgrounds — add rgba(0,0,0,0.5) overlay on background images minimum
7. Responsive design: 1024px and 768px breakpoints
8. Mobile hamburger menu with JS toggle
9. Smooth scroll for anchor links
10. Hover effects on buttons and cards

OUTPUT FORMAT:
Return the complete single-file HTML (with <style> and <script> inline):
===HTML===
(complete index.html with all CSS in <style> and all JS in <script>)
===END==="""

    def _build_design_spec(self, ctx: DesignContext) -> str:
        parts: list[str] = []

        # Header
        parts.append(f"## Design Specification: {ctx.file_name}")
        parts.append(f"Canvas: {int(ctx.dimensions.get('width', 0))}x{int(ctx.dimensions.get('height', 0))}px")
        parts.append("")

        # Colours
        parts.append(self._build_colours(ctx))
        parts.append("")

        # Typography
        parts.append(self._build_typography(ctx))
        parts.append("")

        # Sections
        parts.append("## Page Sections (reproduce ALL sections in this EXACT order)")
        parts.append("")

        for idx, section in enumerate(ctx.sections, 1):
            parts.append(self._build_section(idx, section, ctx))
            parts.append("")

        # Image manifest
        parts.append(self._build_image_manifest(ctx))
        parts.append("")

        # Generation rules
        parts.append(self._build_rules())

        return "\n".join(parts)

    def _build_colours(self, ctx: DesignContext) -> str:
        p = ctx.colours
        lines = ["## Colour Palette"]
        if p.primary:
            lines.append(f"- Primary: {p.primary}")
        if p.secondary:
            lines.append(f"- Secondary: {p.secondary}")
        if p.accent:
            lines.append(f"- Accent: {p.accent}")
        lines.append(f"- Background: {p.background}")
        lines.append(f"- Text: {p.text_primary}")
        if p.text_secondary:
            lines.append(f"- Text on dark: {p.text_secondary}")
        # All unique colours
        all_hex = sorted(set(c["hex"] for c in p.all_colours if not c["hex"].startswith("rgba")))
        if all_hex:
            lines.append(f"- All colours: {', '.join(all_hex)}")
        return "\n".join(lines)

    def _build_typography(self, ctx: DesignContext) -> str:
        t = ctx.typography
        heading = _google_font(t.heading_font) if t.heading_font else "serif"
        body = _google_font(t.body_font) if t.body_font else "sans-serif"
        lines = [
            "## Typography",
            f"- Headings: {heading} (Google Fonts)",
            f"- Body: {body} (Google Fonts)",
        ]
        # Show font scale
        sizes = sorted(set(s.get("font_size", 16) for s in t.all_styles), reverse=True)
        if sizes:
            lines.append(f"- Scale: {', '.join(str(int(s)) + 'px' for s in sizes[:8])}")
        return "\n".join(lines)

    def _build_section(self, idx: int, section: Section,
                       ctx: DesignContext) -> str:
        lines = [
            f"### Section {idx}: {section.name} [{section.semantic_role}]",
            f"Layout: {section.layout_description}",
        ]

        # Background
        if section.background:
            bg = section.background
            if bg["type"] == "colour":
                lines.append(f"Background: {bg['value']}")
            elif bg["type"] == "image":
                img = bg.get("image")
                if img and img.get("temp_url"):
                    lines.append(f"Background image: {img['temp_url']}")
                    lines.append("Apply dark overlay rgba(0,0,0,0.5) for text readability")
                else:
                    lines.append("Background: image (use nearest section image)")

        # Text content
        if section.texts:
            lines.append("")
            lines.append("Text content (use VERBATIM — do not change, paraphrase, or invent):")
            for t in section.texts:
                text = t.get("text", "")
                font = t.get("font_family", "")
                size = t.get("font_size", "")
                weight = t.get("font_weight", "")
                colour = t.get("text_colour", "")
                align = t.get("text_align", "LEFT")

                # Determine element type by font size
                size_val = int(size) if size else 16
                if size_val >= 40:
                    el_hint = "h1"
                elif size_val >= 30:
                    el_hint = "h2"
                elif size_val >= 24:
                    el_hint = "h3"
                elif size_val >= 20:
                    el_hint = "h4"
                else:
                    el_hint = "p"

                font_display = _google_font(font) if font else ""
                style_parts = []
                if font_display:
                    style_parts.append(font_display)
                if size:
                    style_parts.append(f"{int(size)}px")
                if weight:
                    style_parts.append(f"weight {int(weight)}")
                if colour:
                    style_parts.append(colour)
                if align and align != "LEFT":
                    style_parts.append(f"align {align}")

                style_str = f" [{', '.join(style_parts)}]" if style_parts else ""

                # Truncate very long text for prompt efficiency
                display_text = text if len(text) <= 300 else text[:300] + "..."

                lines.append(f'  <{el_hint}> "{display_text}"{style_str}')

        # Images
        if section.images:
            lines.append("")
            lines.append("Images (use these EXACT URLs — do NOT substitute):")
            for i, img in enumerate(section.images):
                name = img.get("node_name", f"image-{i+1}")
                url = img.get("temp_url", "")
                w = int(img.get("width", 0))
                h = int(img.get("height", 0))
                parent = img.get("parent_section", "")

                if url:
                    # Determine image role
                    if w > 1000:
                        role = "background-image (full width)"
                    elif w > 400:
                        role = "card/feature image"
                    else:
                        role = "icon/thumbnail"
                    lines.append(f"  - {name}: {url} ({w}x{h}, {role})")
                else:
                    lines.append(f"  - {name}: [no URL exported] ({w}x{h})")

        return "\n".join(lines)

    def _build_image_manifest(self, ctx: DesignContext) -> str:
        """Build a complete image manifest table."""
        lines = ["## Complete Image Manifest"]
        lines.append("| # | Name | Section | URL | Size |")
        lines.append("|---|------|---------|-----|------|")

        idx = 1
        for section in ctx.sections:
            for img in section.images:
                name = img.get("node_name", "unnamed")
                url = img.get("temp_url", "N/A")
                w = int(img.get("width", 0))
                h = int(img.get("height", 0))
                # Truncate URL for readability in table
                url_display = url[:60] + "..." if len(url) > 60 else url
                lines.append(f"| {idx} | {name} | {section.name} | {url_display} | {w}x{h} |")
                idx += 1

        if idx == 1:
            lines.append("| - | No images exported | - | - | - |")

        return "\n".join(lines)

    def _build_rules(self) -> str:
        return """## CRITICAL RULES
1. Use EXACT text from the specification — do NOT paraphrase, invent names, or add content
2. Use EXACT image URLs provided — every <img src> and background-image MUST use the URLs above
3. Reproduce ALL sections listed — do NOT skip any section
4. Use the exact colour palette — do NOT switch to a different colour scheme
5. Include Google Fonts <link> for the specified heading and body fonts
6. CSS variables for all colours: --primary, --secondary, --accent, --bg, --text
7. Dark overlay (rgba(0,0,0,0.5) minimum) on all background images for text readability
8. White text (#ffffff) on any dark or image background
9. Responsive: stack columns at 768px, adjust font sizes
10. Mobile menu: hamburger icon that toggles nav links via JS
11. Smooth scroll: html { scroll-behavior: smooth }
12. Hover states on all buttons (opacity/scale transition) and cards (shadow transition)
13. Footer: match the design's footer colour and layout exactly
14. Logo: use the logo image URL from the manifest, or create a text logo with the brand name
15. NAVIGATION MUST be a SEPARATE element ABOVE the hero — it must NOT overlay the hero image. The nav bar should have its own solid background (white/cream) so nav links are clearly readable. The hero section starts BELOW the navigation bar."""
