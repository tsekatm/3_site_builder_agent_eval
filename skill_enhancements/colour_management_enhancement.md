# Colour Management Skill - Enhancement Proposal

**Based on:** Eval pack results (5 learnings, avg score 2.1/5)
**Skill file:** `skills/colour_management.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| Header background not updated to semi-transparent tint of `--background-color` | High | Medium |
| Gradient variable (`--gradient`) not updated when primary/secondary colours change | High | Medium |
| Hardcoded colour values used instead of CSS variables in some output | Medium | High |
| Dark text on dark backgrounds — overlay not applied on sections with background images | High | High |

Models update `:root` CSS variables correctly but fail to propagate colour changes to three critical areas: (1) the header/navbar background, which typically uses a semi-transparent version of the background colour, (2) gradient declarations that reference primary/secondary colours, and (3) sections with background images that need a colour overlay to maintain text readability.

---

## 2. Proposed Additions

### Addition A: Header Background Rule

**WHERE:** Add as a new subsection after "Step 5: Fix Hardcoded Colours" (after line 444), before "Step 6: Fix Hardcoded rgba() Values".

```markdown
### Step 5b: Update Header/Navbar Background

The header/navbar background MUST be updated when the colour palette changes. Most BigBeard templates use a semi-transparent version of the background colour for the header, not a solid colour.

**Rule (MANDATORY):** After updating `:root` variables, scan for and update the header/navbar background:

1. Find the header/navbar CSS rule (selectors: `header`, `.header`, `nav`, `.navbar`, `.nav-container`, `.site-header`)
2. If the background uses `rgba()` or a semi-transparent value, update it to use the new `--background-color` with the SAME alpha value
3. If the header has a `.scrolled` or `.sticky` variant, update that too

**Pattern — Header background tint:**
```css
/* CORRECT: Header uses semi-transparent tint of --background-color */
header,
.navbar {
    background: rgba(var(--background-rgb), 0.95);
}

/* CORRECT: Scrolled header uses slightly more opaque version */
header.scrolled,
.navbar.scrolled {
    background: rgba(var(--background-rgb), 0.98);
}
```

**Common mistake to avoid:**
```css
/* WRONG: Header background left as old colour after palette change */
header { background: rgba(26, 26, 46, 0.95); }  /* Old colour, not updated */

/* WRONG: Header background set to fully opaque, losing transparency */
header { background: var(--background-color); }  /* Lost the alpha channel */
```

**Implementation:** When generating the palette, ALWAYS include `--background-rgb` (comma-separated RGB of `--background-color`) so the header can use `rgba(var(--background-rgb), 0.95)`. Then replace any hardcoded `rgba(R, G, B, A)` in header rules with `rgba(var(--background-rgb), A)`, preserving the original alpha value.
```

---

### Addition B: Gradient Propagation Rule

**WHERE:** Add as a new subsection after the new "Step 5b" above, before "Step 6: Fix Hardcoded rgba() Values".

```markdown
### Step 5c: Update Gradient Declarations

**Rule (MANDATORY):** When primary or secondary colours change, ALL gradient declarations MUST be updated to reference the new colours.

**Scan for these gradient patterns and update them:**

1. **Hero/CTA gradients** — `linear-gradient(...)` using primary/secondary colours
2. **Button hover gradients** — gradient backgrounds on `.btn`, `.cta-button`
3. **Section dividers** — gradient borders or gradient overlays
4. **The `--gradient` CSS variable** (if present in `:root`)

**Pattern — Correct gradient update:**
```css
:root {
    /* When primary=#0693e3 and secondary=#9b51e0, the gradient MUST update too */
    --gradient: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    --gradient-reverse: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}

/* Section overlays using gradient */
.hero-overlay {
    background: linear-gradient(135deg, rgba(var(--primary-rgb), 0.7), rgba(var(--secondary-rgb), 0.5));
}
```

**Common mistake to avoid:**
```css
/* WRONG: --gradient left with old hardcoded values after palette change */
--gradient: linear-gradient(135deg, #F2DD10, #62A6A6);  /* Old colours! */

/* WRONG: Gradient uses var() for one colour but hardcodes the other */
--gradient: linear-gradient(135deg, var(--primary-color), #62A6A6);
```

**Implementation steps:**
1. After `apply_palette()`, scan CSS for ALL `linear-gradient`, `radial-gradient`, and `conic-gradient` declarations
2. For each gradient, check if it contains hardcoded hex values that match (or closely match) the OLD palette colours
3. Replace those hex values with the corresponding `var()` reference or the new hex value
4. If a `--gradient` variable exists in `:root`, update it to use `var(--primary-color)` and `var(--secondary-color)`
```

---

### Addition C: Background Image Overlay Contrast Rule

**WHERE:** Add as a new subsection at the end of "Colour Application" section (after Step 6, around line 487), before "WCAG Contrast Validation".

```markdown
### Step 6b: Ensure Overlay Contrast on Background Image Sections

**Rule (MANDATORY):** Any section with a background image MUST have an overlay that provides sufficient contrast for text readability. When the colour palette changes, overlay colours MUST be updated to use the new palette's RGB variables.

**Sections to check:** hero, CTA, testimonials, about, any section with `background-image` in CSS or an `<img>` with class containing `bg`.

**Pattern — Correct overlay using palette variables:**
```css
/* CORRECT: Overlay uses palette RGB variable */
.hero-overlay {
    background: rgba(var(--text-rgb), 0.6);
}

/* CORRECT: Gradient overlay using palette */
.cta-overlay {
    background: linear-gradient(
        to right,
        rgba(var(--primary-rgb), 0.85),
        rgba(var(--secondary-rgb), 0.65)
    );
}
```

**Common mistakes to avoid:**
```css
/* WRONG: No overlay at all — white text on a light image is unreadable */
.hero { background-image: url('hero.jpg'); color: white; }

/* WRONG: Overlay uses old hardcoded RGB values after palette change */
.hero-overlay { background: rgba(26, 26, 46, 0.7); }  /* Old palette! */

/* WRONG: Overlay div removed during colour change */
/* The .hero-overlay div was deleted from HTML — never do this */
```

**Implementation steps:**
1. After palette application, find all elements with `background-image` (CSS and inline)
2. For each, check if a sibling/child overlay element exists (class containing `overlay`)
3. If overlay exists: update its `rgba()` values to use new `--text-rgb` or `--primary-rgb` variable, preserving the alpha
4. If NO overlay exists: add one with `background: rgba(var(--text-rgb), 0.6)` and appropriate z-indexing
5. NEVER remove an existing overlay div from the HTML
```

---

### Addition D: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 586).

```markdown
| Leaving header background with old rgba() values | Header clashes with new palette | Update header rgba() to use `--background-rgb` |
| Not updating `--gradient` variable when colours change | Gradients show old palette colours | Always regenerate gradient from new primary/secondary |
| Removing overlay divs from background image sections | Text becomes unreadable on images | NEVER remove overlays; update their rgba() to new palette |
| Using hardcoded hex in output instead of var() references | Defeats the purpose of CSS variables | Every colour value in rules MUST use `var(--name)`, never raw hex |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| Header background not updated | Addition A (Header Background Rule) | Models will explicitly update header rgba() using `--background-rgb` |
| Gradient variable stale after colour change | Addition B (Gradient Propagation Rule) | Models will scan and update all gradient declarations |
| Hardcoded values in output | Addition D (Anti-Pattern reinforcement) | Explicit rule that every colour in CSS rules must use `var()` |
| Dark text on dark bg / missing overlay | Addition C (Overlay Contrast Rule) | Models will check and update overlays on all bg-image sections |

**Projected score improvement:** 2.1 -> 3.5+ (based on addressing the four highest-frequency failures)
