# Background Image Changer Skill - Enhancement Proposal

**Based on:** Eval pack results (11 learnings, avg score 3.5/5)
**Skill file:** `skills/background_image_changer.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| Local file paths used instead of working URLs (e.g., Unsplash) | High | Critical |
| Dark overlay not applied when changing background images | High | High |
| Text colour not adjusted for contrast after background image change | Medium | High |
| Overlay div removed when replacing background images | Medium | Critical |

Models understand the mechanics of image replacement but fail on three fronts: (1) they use local filesystem paths or placeholder paths instead of working web URLs, (2) they forget to add or preserve dark overlays, and (3) they change the background image without checking whether the overlaid text remains readable.

---

## 2. Proposed Additions

### Addition A: Image Source URL Rule (Critical)

**WHERE:** Add as a new section after "Input Specification" (after line 42), before "Output Specification".

```markdown
## Image Source Rules (MANDATORY)

### Rule 1: NEVER use local file system paths as image sources

When a background image needs to be replaced and no user-provided file is available, you MUST use a working web URL from a free stock photo service. NEVER use a local filesystem path, a placeholder path, or a broken URL.

**WRONG examples (will result in broken images):**
```
/Users/john/Desktop/hero.jpg          <-- Local filesystem path
./images/new-hero.jpg                 <-- File doesn't exist in template
images/placeholder-hero.jpg           <-- Placeholder that doesn't exist
C:\Users\john\Pictures\hero.jpg       <-- Windows local path
```

**CORRECT examples (working web URLs):**
```
https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&h=800&fit=crop
https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1920&h=800&fit=crop
```

### Rule 2: Unsplash URL format for background images

When using Unsplash as the image source, use this URL format to get correctly sized images:

```
https://images.unsplash.com/photo-{PHOTO_ID}?w={WIDTH}&h={HEIGHT}&fit=crop&auto=format
```

**Recommended dimensions by section:**

| Section | URL Parameters | Example |
|---------|---------------|---------|
| Hero background | `?w=1920&h=800&fit=crop` | Full-width hero banner |
| Section background | `?w=1920&h=600&fit=crop` | About, CTA sections |
| Card image | `?w=600&h=400&fit=crop` | Feature cards, blog cards |
| Team member | `?w=400&h=400&fit=crop` | Circular headshots |

### Rule 3: When user provides a file path

If the user provides an actual file path to a local image:
1. Copy the file into the template's `images/` directory
2. Reference it as `images/{filename}` (relative path from template root)
3. NEVER reference the original absolute path in the HTML/CSS
```

---

### Addition B: Overlay Preservation and Creation Rule (Critical)

**WHERE:** Add as a new subsection after the existing "Overlay Preservation" section (after line 454), expanding on it.

```markdown
### Overlay Mandatory Rules (BLOCKING)

These rules are INVIOLABLE. Violating them causes unreadable text.

**Rule 1: NEVER remove an overlay div from the HTML.**

When replacing a background image, the overlay `<div>` MUST remain in the HTML. Do not delete it, comment it out, or replace it with the new image.

**Template overlay structure (DO NOT MODIFY):**
```html
<!-- This structure MUST be preserved during image replacement -->
<section class="hero" id="hero">
    <div class="hero-bg">
        <img src="images/hero-bg.jpg" alt="">  <!-- ONLY change the src here -->
    </div>
    <div class="hero-overlay"></div>             <!-- NEVER remove this div -->
    <div class="hero-content">                   <!-- NEVER modify this div -->
        <h1>Headline</h1>
    </div>
</section>
```

**Rule 2: If an overlay does NOT exist, ADD one.**

When adding a background image to a section that previously had no background image (e.g., solid colour background), you MUST add an overlay div to ensure text readability.

**Pattern for adding a missing overlay:**
```html
<!-- Before: Section with solid background, no overlay needed -->
<section class="about" id="about">
    <div class="about-content">
        <h2>About Us</h2>
        <p>Description text...</p>
    </div>
</section>

<!-- After: Background image added, overlay MUST be added too -->
<section class="about" id="about" style="position: relative;">
    <div class="about-bg" style="position: absolute; inset: 0; z-index: 0;">
        <img src="images/about-bg.jpg" alt="" style="width: 100%; height: 100%; object-fit: cover;">
    </div>
    <div class="about-overlay" style="position: absolute; inset: 0; z-index: 1; background: rgba(0, 0, 0, 0.5);"></div>
    <div class="about-content" style="position: relative; z-index: 2;">
        <h2>About Us</h2>
        <p>Description text...</p>
    </div>
</section>
```

**Rule 3: Overlay opacity guidance based on image brightness.**

| Image Type | Overlay Recommendation |
|-----------|----------------------|
| Dark image (night sky, dark interior) | `rgba(0, 0, 0, 0.3)` — lighter overlay |
| Medium image (landscapes, offices) | `rgba(0, 0, 0, 0.5)` — medium overlay |
| Light/bright image (white walls, sky) | `rgba(0, 0, 0, 0.6)` — darker overlay |
| Colourful/busy image (markets, crowds) | `rgba(0, 0, 0, 0.65)` — strong overlay to calm visual noise |

When in doubt, use `rgba(0, 0, 0, 0.5)` as the default.
```

---

### Addition C: Text Contrast Adjustment Rule

**WHERE:** Add after the new overlay rules above, as a subsection.

```markdown
### Text Colour Contrast After Background Change

**Rule (MANDATORY):** When adding or changing a background image on a section, check that text within that section has sufficient contrast against the overlay.

**Decision tree:**

1. Does the section have a dark overlay (opacity >= 0.4)?
   - YES -> Text colour should be LIGHT: `color: #ffffff` or `color: var(--text-color)` (if theme is dark)
   - NO -> Text colour should match the existing theme

2. Was the section previously a light solid background with dark text?
   - YES -> After adding a dark background image + overlay, change text to WHITE
   - Update: headings, paragraphs, labels, links, and button text in that section

**Pattern:**
```css
/* Section with background image needs light text */
.hero-content h1,
.hero-content p,
.hero-content .btn {
    color: #ffffff;
}

.hero-content .btn {
    border-color: #ffffff;
}
```

**Common mistake to avoid:**
```css
/* WRONG: Dark text left unchanged on dark background image + overlay */
.hero-content h1 { color: #1a1a2e; }  /* Invisible on dark overlay! */
```
```

---

### Addition D: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 521).

```markdown
| Using local filesystem paths (e.g., `/Users/.../image.jpg`) as image sources | Image appears broken in browser | Use web URLs (Unsplash) or copy file to template `images/` directory |
| Not adding an overlay when placing a background image on a previously solid section | Text becomes unreadable | ALWAYS add an overlay div with `rgba(0,0,0,0.5)` when adding bg images |
| Changing background image but leaving dark text on dark overlay | Text is invisible | Update text colour to white/light when section has a dark overlay |
| Deleting the overlay div to "simplify" the HTML | Text loses contrast, becomes unreadable | NEVER remove overlay divs — they exist for readability |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| Local file paths instead of URLs | Addition A (Image Source Rules) | Clear wrong/right examples with Unsplash URL format |
| Missing dark overlay | Addition B (Overlay Mandatory Rules) | Explicit rules with code patterns for preserving and adding overlays |
| Text colour not adjusted | Addition C (Text Contrast Rule) | Decision tree for when to change text to white |
| Overlay div removed | Addition B Rule 1 | Explicit "NEVER remove" instruction with preserved HTML structure |

**Projected score improvement:** 3.5 -> 4.3+ (image URL issue alone accounts for ~30% of failures)
