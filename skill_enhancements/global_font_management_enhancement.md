# Global Font Management Skill - Enhancement Proposal

**Based on:** Eval pack results (6 learnings, avg score 2.0/5)
**Skill file:** `skills/global_font_management.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| Google Fonts `<link>` URL not updated to match new font families | Very High | Critical |
| CSS font variables updated but old Google Fonts import left in HTML | Very High | Critical |
| Font fallback stack mismatch (serif font with sans-serif fallback or vice versa) | High | Medium |
| `font-display: swap` missing from Google Fonts URL `&display=swap` parameter | Medium | Medium |

The core failure mode is a disconnect between CSS and HTML: models correctly update `--font-heading` and `--font-body` CSS variables but leave the original Google Fonts `<link>` tag in `<head>` unchanged. The browser then cannot load the new fonts because they were never requested from Google Fonts. This is the single most impactful issue -- without the correct `<link>` tag, font changes are invisible.

---

## 2. Proposed Additions

### Addition A: Mandatory Font Change Checklist (Critical)

**WHERE:** Add immediately after the "Complete Font Replacement Workflow" section (after line 527), as a new top-level section titled "Mandatory Font Change Checklist".

```markdown
## Mandatory Font Change Checklist (BLOCKING)

**CRITICAL:** Every font change MUST complete ALL FOUR of these steps. Skipping any step results in broken fonts. This checklist is the single most important section of this skill.

When changing fonts, you MUST verify all four artifacts are updated IN THIS ORDER:

### Step 1: Update the Google Fonts `<link>` tag in `<head>` (HTML)

The `<link>` tag in `index.html` `<head>` is what tells the browser to DOWNLOAD the font files. If you change CSS variables but leave the old `<link>` tag, the new font will NOT load.

**MANDATORY actions:**
1. REMOVE the old Google Fonts `<link>` tag (and its preconnect tags)
2. INSERT a new `<link>` tag with the EXACT new font family names and weights
3. The `<link>` URL MUST include `&display=swap` parameter
4. Preconnect tags for `fonts.googleapis.com` and `fonts.gstatic.com` MUST be present

**Example — Changing from Poppins+Inter to Playfair Display+Lato:**

```html
<!-- REMOVE these old tags -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">

<!-- INSERT these new tags -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;500;600&display=swap" rel="stylesheet">
```

**Common mistakes to avoid:**
```html
<!-- WRONG: Old font still in <link>, new font only in CSS variables -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
<!-- CSS says --font-heading: 'Playfair Display' but Playfair Display is never loaded! -->

<!-- WRONG: Missing &display=swap causes Flash of Invisible Text -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700" rel="stylesheet">

<!-- WRONG: Spaces instead of + in font name -->
<link href="https://fonts.googleapis.com/css2?family=Playfair Display:wght@400;600;700&display=swap" rel="stylesheet">
```

### Step 2: Update CSS variables in `:root` (CSS)

Update `--font-heading`, `--font-body`, and `--font-cta` with the new font names AND correct fallback stacks.

### Step 3: Update fallback stacks to match font classification (CSS)

The fallback stack MUST match the font's classification:
- **Serif fonts** (Playfair Display, Merriweather, Lora, PT Serif, etc.) -> serif fallback: `'Georgia', 'Times New Roman', serif`
- **Sans-serif fonts** (Inter, Poppins, Lato, Open Sans, etc.) -> sans-serif fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Monospace fonts** -> monospace fallback: `'Fira Code', 'Consolas', 'Courier New', monospace`

**WRONG:** `--font-heading: 'Playfair Display', sans-serif;` (Playfair Display is a SERIF font)
**CORRECT:** `--font-heading: 'Playfair Display', 'Georgia', 'Times New Roman', serif;`

### Step 4: Replace hardcoded font-family declarations (CSS)

Any `font-family:` declaration outside `:root` that does NOT use `var()` must be updated.
```

---

### Addition B: Google Fonts URL Construction Reference

**WHERE:** Add after the new "Mandatory Font Change Checklist", as a reference subsection.

```markdown
### Google Fonts URL Construction Reference

The Google Fonts CSS2 API uses this URL format:

```
https://fonts.googleapis.com/css2?family={FontName}:wght@{weights}&family={FontName2}:wght@{weights2}&display=swap
```

**Rules:**
- Font name spaces are replaced with `+` (e.g., `Playfair+Display`)
- Multiple weights are separated by `;` (e.g., `wght@400;600;700`)
- Multiple font families are separated by `&family=`
- `&display=swap` MUST always be the last parameter
- Only request weights that are actually used in the template (typically 300, 400, 500, 600, 700)

**Quick reference — Common fonts and their correct URL encoding:**

| Font Name | URL Encoding | Classification |
|-----------|-------------|----------------|
| Playfair Display | `Playfair+Display` | Serif |
| Open Sans | `Open+Sans` | Sans-serif |
| Source Sans 3 | `Source+Sans+3` | Sans-serif |
| DM Sans | `DM+Sans` | Sans-serif |
| Nunito Sans | `Nunito+Sans` | Sans-serif |
| PT Serif | `PT+Serif` | Serif |
| Libre Baskerville | `Libre+Baskerville` | Serif |
| JetBrains Mono | `JetBrains+Mono` | Monospace |

**Complete example `<link>` tag for Playfair Display (heading) + Lato (body):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;500;600&display=swap" rel="stylesheet">
```
```

---

### Addition C: Font Classification Lookup Table

**WHERE:** Add to the existing `SERIF_FONTS` set in Step 5 (around line 406), expanding it and making it more prominent.

```markdown
### Font Classification Lookup (used for fallback stack selection)

**MANDATORY:** When setting `font-family`, the fallback stack MUST match the font's classification. Use this lookup:

**Serif fonts** (fallback: `'Georgia', 'Times New Roman', serif`):
Playfair Display, Merriweather, Lora, PT Serif, Libre Baskerville, Crimson Text, EB Garamond, Cormorant Garamond, Marcellus, Noto Serif, Source Serif 4, Bitter, Vollkorn, Alegreya, Zilla Slab

**Sans-serif fonts** (fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`):
Inter, Poppins, Lato, Open Sans, Roboto, Montserrat, Nunito Sans, DM Sans, Source Sans 3, Raleway, Work Sans, Manrope, Outfit, Plus Jakarta Sans, Rubik, Noto Sans, Barlow, Mulish, Figtree, Geist

**Monospace fonts** (fallback: `'Fira Code', 'Consolas', 'Courier New', monospace`):
JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono, Roboto Mono

**If a font is not in this list:** Check its Google Fonts page category (serif, sans-serif, display, handwriting, monospace). Display and handwriting fonts should use sans-serif fallbacks unless they are clearly serif-based.
```

---

### Addition D: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 542).

```markdown
| Updating CSS font variables but leaving the old Google Fonts `<link>` tag | New font never loads — browser uses fallback | ALWAYS update the `<link>` tag in HTML `<head>` FIRST, then CSS variables |
| Missing `&display=swap` in Google Fonts URL | Flash of Invisible Text (FOIT) — text disappears during font load | ALWAYS append `&display=swap` to the Google Fonts URL |
| Serif font with sans-serif fallback (or vice versa) | Layout shift when fallback activates — serif and sans-serif have very different metrics | Match fallback stack to font classification: serif fonts get serif fallbacks |
| Using spaces in Google Fonts URL instead of `+` | Font fails to load (404) | Replace spaces with `+` in the URL: `Playfair+Display`, not `Playfair Display` |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| Google Fonts `<link>` not updated | Addition A Step 1 (explicit before/after examples) | Models see the exact HTML they must produce, with wrong/right comparison |
| Old Google Fonts import left in HTML | Addition A Step 1 (REMOVE then INSERT instruction) | Explicit two-step: remove old, insert new |
| Fallback stack mismatch | Addition C (Font Classification Lookup Table) | Models can look up any font and find the correct fallback |
| Missing `font-display: swap` | Addition A Step 1 + Addition B (URL construction) | URL format reference always includes `&display=swap` |

**Projected score improvement:** 2.0 -> 3.8+ (the `<link>` tag issue alone accounts for ~60% of failures)
