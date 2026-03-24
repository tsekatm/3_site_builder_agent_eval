# Logo Replacement Skill - Enhancement Proposal

**Based on:** Eval pack results (13 learnings, avg score 4.5/5)
**Skill file:** `skills/logo_replacement.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| Footer logo not replaced (only header logo updated) | Medium | Medium |
| Alt text not updated to match business name | Medium | Low |
| Logo sizing (`max-height`) not preserved after replacement | Low | Medium |
| Favicon not updated to match new brand | Low | Low |

This skill already scores well (4.5/5). The issues are edge-case omissions rather than fundamental misunderstandings. Models replace the header logo correctly but sometimes stop there, missing the footer logo, alt text, and favicon.

---

## 2. Proposed Additions

### Addition A: Mandatory Replacement Completeness Checklist

**WHERE:** Add immediately before the "Complete Replacement Workflow" section (before line 334), as a new section.

```markdown
## Mandatory Replacement Completeness Checklist (BLOCKING)

**CRITICAL:** A logo replacement is NOT complete until ALL of the following locations have been checked and updated. Do NOT stop after replacing the header logo.

| # | Location | Selector Pattern | Action Required |
|---|----------|-----------------|-----------------|
| 1 | **Header/Navbar logo** | `header img[src*="logo"]`, `.navbar-logo img`, `.header-logo img` | Replace `src`, update `alt` |
| 2 | **Footer logo** | `footer img[src*="logo"]`, `.footer-logo img` | Replace `src`, update `alt` |
| 3 | **Mobile nav logo** | `.mobile-nav img`, `.offcanvas img[src*="logo"]` | Replace `src`, update `alt` |
| 4 | **Alt text (ALL logos)** | Every `<img>` with "logo" in src or class | Set `alt="{BusinessName} Logo"` |
| 5 | **Aria-label (ALL logo links)** | Every `<a>` wrapping a logo `<img>` | Set `aria-label="{BusinessName} Home"` |
| 6 | **Favicon** | `<link rel="icon">`, `<link rel="shortcut icon">` | Update `href` to new favicon |
| 7 | **Apple touch icon** | `<link rel="apple-touch-icon">` | Update `href` |
| 8 | **OG image** | `<meta property="og:image">` | Update `content` if logo-based |

**Footer logo rule:** The footer logo MUST be replaced even if it uses a different filename (e.g., `footer-logo.png`, `logo-white.svg`, `logo-light.png`). Scan the entire `<footer>` element for ANY `<img>` tag, not just ones matching `logo` in the filename.

**Alt text rule:** After replacing logos, grep the entire HTML for every `<img>` whose `src` contains "logo". Every single one MUST have `alt="{BusinessName} Logo"` where `{BusinessName}` is the exact business name provided by the user.

**Sizing preservation rule:** When replacing an `<img>` src, do NOT modify or remove any of these attributes/CSS properties:
- `width` and `height` HTML attributes
- `max-height`, `max-width`, `height`, `width` in inline styles
- CSS classes that control sizing (`.logo-img`, `.logo-image`, etc.)
Only the `src` and `alt` attributes should change.
```

---

### Addition B: Footer Logo Detection Enhancement

**WHERE:** Add after the existing `LogoDetector.scan_html()` method (around line 155), as an additional detection note.

```markdown
### Footer Logo Detection — Extended Patterns

Footer logos may not always contain "logo" in their filename or class. Use these additional detection patterns:

```python
# Additional footer logo detection patterns
FOOTER_LOGO_PATTERNS = [
    # By location: any <img> inside <footer> that is NOT an icon
    "footer img:not([src*='icon'])",
    # By class on parent
    ".footer-brand img",
    ".footer-info img",
    ".footer-top img",
    # By src patterns
    "img[src*='logo-light']",
    "img[src*='logo-white']",
    "img[src*='logo-footer']",
    "img[src*='brand']",
]
```

**Rule:** After scanning with the standard `LogoDetector`, additionally scan the `<footer>` element for ANY `<img>` tag that could be a logo. If the footer contains an `<img>` that is not an icon (not < 32px wide, not an SVG icon), treat it as a footer logo and include it in the replacement list.
```

---

### Addition C: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 363).

```markdown
| Replacing only header logo, missing footer | Footer shows old brand, inconsistent | ALWAYS check header AND footer for logos |
| Leaving old alt text after logo replacement | Alt text says "Old Company Logo" | Update alt text on EVERY logo img to "{BusinessName} Logo" |
| Removing or modifying max-height/width when changing src | Logo appears oversized or distorted | Only change `src` and `alt`, preserve ALL sizing attributes |
| Skipping favicon update | Browser tab shows old brand icon | Always update `<link rel="icon">` in `<head>` |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| Footer logo missed | Addition A (checklist row 2) + Addition B (extended patterns) | Explicit instruction to check footer, with code patterns |
| Alt text not updated | Addition A (checklist rows 4-5, alt text rule) | Clear rule: grep for ALL logo imgs, update ALL alt text |
| Logo sizing broken | Addition A (sizing preservation rule) | Explicit list of attributes/properties to NOT touch |
| Favicon not updated | Addition A (checklist rows 6-7) | Included in the mandatory checklist |

**Projected score improvement:** 4.5 -> 4.8+ (already high, these are polish fixes)
