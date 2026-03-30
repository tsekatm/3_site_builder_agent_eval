# THINK Blocks — Draft for Skill Injection

**Date**: 2026-03-30
**Status**: DRAFT — Awaiting approval before injecting into skills
**Target**: 8 actions across 6 skill files (~42 lines total)

---

## P0: apply-sections-layout (avg gap: -10.2)

**Inject into**: `skills/layout_transformation.skill.md`
**Root cause**: Models edit CSS without inventorying what exists. They add new grid rules that conflict with existing ones, breaking responsive behaviour and removing content.

```markdown
## THINK before transforming section layout:
1. LIST every grid/flex container in the current CSS and count its children
2. NOTE which CSS classes control responsive breakpoints (768px, 1024px)
3. IDENTIFY which content elements will move — will any be hidden or orphaned?
4. WRITE the new layout using ONLY existing class names — do NOT invent new ones
5. VERIFY section count before and after — no sections removed
6. TEST: at 768px, all content still stacks to single column
```

---

## P0: apply-hero-layout (avg gap: -5.4)

**Inject into**: `skills/layout_transformation.skill.md`
**Root cause**: Models remove hero child elements (subheading, CTA) when restructuring, or break the background image overlay.

```markdown
## THINK before transforming hero layout:
1. FIND the hero element and LIST all its children (heading, subtext, CTA, image)
2. NOTE the current background-image URL and overlay opacity
3. PLAN the new layout — which children move, which stay?
4. APPLY layout changes WITHOUT removing any child elements
5. VERIFY background image URL is unchanged and overlay opacity ≥ 0.5
6. CHECK text colour is white (#fff) on the overlay
```

---

## P1: apply-colours (avg gap: -3.3)

**Inject into**: `skills/colour_management.skill.md`
**Root cause**: Models change colour values at usage sites instead of in CSS variable declarations, creating inconsistencies. Or they skip the CSS variables entirely.

```markdown
## THINK before applying brand colours:
1. FIND :root {} or CSS custom property declarations (--primary, --secondary, etc.)
2. MAP each new brand colour to an existing variable name — one-to-one
3. CHANGE only the :root declarations — NEVER edit colour values at usage sites
4. CHECK text-on-background contrast for every pairing (min 4.5:1 ratio)
5. VERIFY buttons use --accent or --primary, not --background
```

---

## P1: replace-section-bgs (avg gap: -2.8)

**Inject into**: `skills/background_image_changer.skill.md`
**Root cause**: Models write image descriptions as URLs, or remove the dark overlay when replacing the image.

```markdown
## THINK before replacing section backgrounds:
1. FIND every section with a background-image CSS property
2. NOTE the current overlay (linear-gradient or ::before pseudo-element)
3. REPLACE the image URL only — keep the overlay rule unchanged
4. VERIFY every new URL starts with https:// (never a description)
5. CHECK text is still readable — overlay opacity ≥ 0.5 on all image sections
```

---

## P1: update-contact (avg gap: -2.7)

**Inject into**: `skills/template_customization.skill.md`
**Root cause**: Models invent contact details instead of using the exact values from requirements. Or they restructure the contact section layout.

```markdown
## THINK before updating contact details:
1. FIND the contact section in the HTML (look for email, phone, address)
2. MAP each requirement field to an existing HTML element
3. REPLACE text content only — do NOT change the section structure or styling
4. VERIFY email, phone, and address match requirements EXACTLY (copy-paste)
```

---

## P2: replace-hero-bg (avg gap: -2.3)

**Inject into**: `skills/background_image_changer.skill.md`
**Root cause**: Same as section-bgs — image hallucination and overlay removal.

```markdown
## THINK before replacing hero background:
1. FIND the hero background-image declaration (inline style or CSS class)
2. NOTE the overlay element (gradient, ::before, or rgba background)
3. REPLACE the URL only — do NOT touch the overlay
4. VERIFY new URL starts with https:// and is a real image URL
5. CHECK hero text is white on dark overlay (contrast ≥ 4.5:1)
```

---

## P2: swap-fonts (avg gap: -2.4)

**Inject into**: `skills/global_font_management.skill.md`
**Root cause**: Models change the font-family in some places but miss others (nav, footer, CTA buttons). Or they break the Google Fonts import.

```markdown
## THINK before swapping fonts:
1. FIND the Google Fonts <link> or @import in <head>
2. LIST every font-family declaration in CSS (headings, body, nav, footer, buttons)
3. UPDATE the Google Fonts URL to load the new families + weights
4. REPLACE every font-family declaration — miss NONE
5. VERIFY: search CSS for old font name — should return 0 results
```

---

## P2: replace-footer-logo (avg gap: -2.5)

**Inject into**: `skills/logo_replacement.skill.md`
**Root cause**: Models can't find the footer logo element, or they replace the wrong image.

```markdown
## THINK before replacing footer logo:
1. FIND the <footer> element in the HTML
2. LOCATE the logo <img> inside the footer (may be in a nested div)
3. NOTE the current src, alt, width, and height attributes
4. REPLACE src with the new logo URL — keep width/height unchanged
5. UPDATE alt text to match the new brand name
```

---

## Summary

| Action | Steps | Lines | Skill File |
|--------|-------|-------|-----------|
| apply-sections-layout | 6 | 7 | layout_transformation.skill.md |
| apply-hero-layout | 6 | 7 | layout_transformation.skill.md |
| apply-colours | 5 | 6 | colour_management.skill.md |
| replace-section-bgs | 5 | 6 | background_image_changer.skill.md |
| update-contact | 4 | 5 | template_customization.skill.md |
| replace-hero-bg | 5 | 6 | background_image_changer.skill.md |
| swap-fonts | 5 | 6 | global_font_management.skill.md |
| replace-footer-logo | 5 | 6 | logo_replacement.skill.md |
| **Total** | **41** | **49** | **6 files** |

49 lines of surgical THINK blocks. Not 1,191 lines of explanations.
