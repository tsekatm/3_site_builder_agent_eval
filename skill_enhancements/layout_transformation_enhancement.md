# Layout Transformation Skill - Enhancement Proposal

**Based on:** Eval pack results (16 learnings, avg score 0.8/5)
**Skill file:** `skills/layout_transformation.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| HTML structure broken during layout changes | Very High | Critical |
| Responsive breakpoints not maintained for features section | Very High | Critical |
| Parallax not implemented (just changes background) | High | High |
| 4-column footer grid not reliably created | High | High |
| Content (text, images, links) lost during layout changes | High | Critical |
| Alternating rows pattern (flexbox row/row-reverse) not understood | High | High |

This is the worst-performing skill (0.8/5). Models attempt layout changes but produce broken HTML, lose content, and ignore responsive design. The root cause is that the skill provides layout CSS patterns but lacks explicit HTML transformation rules showing exactly how to restructure HTML without losing content, and how to ensure responsive breakpoints are present.

---

## 2. Proposed Additions

### Addition A: Content Preservation Protocol (Critical)

**WHERE:** Add as a new top-level section immediately after "Output Specification" (after line 49), before "Layout Catalogue".

```markdown
## Content Preservation Protocol (BLOCKING)

**CRITICAL:** Layout transformation is ONLY about restructuring HTML containers and updating CSS layout rules. It MUST NEVER add, remove, modify, or paraphrase any content.

### The Golden Rule

Before transforming a layout, extract ALL content from the source section. After transforming, verify ALL content is present in the target section. Content means:

| Content Type | Must Be Preserved EXACTLY |
|-------------|--------------------------|
| Heading text | Every `<h1>`-`<h6>` text node |
| Paragraph text | Every `<p>` text node |
| Link text and href | Every `<a>` text + `href` attribute |
| Button text and href | Every `<a class="btn">` or `<button>` text + `href` |
| Image src and alt | Every `<img>` `src` + `alt` attribute |
| List items | Every `<li>` text node |
| Icon classes | Every `<i>` or `<span>` with icon classes |
| Data attributes | All `data-*` attributes |
| ARIA attributes | All `aria-*` attributes |

### Content Extraction Procedure

Before changing ANY layout, follow this exact procedure:

**Step 1: Extract content inventory from source HTML**
```python
def extract_section_content(section_html: str) -> dict:
    """Extract all content from a section BEFORE layout transformation."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(section_html, 'html.parser')

    content = {
        "headings": [],
        "paragraphs": [],
        "links": [],
        "images": [],
        "list_items": [],
        "buttons": [],
    }

    for h in soup.find_all(['h1','h2','h3','h4','h5','h6']):
        content["headings"].append({"tag": h.name, "text": h.get_text(strip=True), "html": str(h)})

    for p in soup.find_all('p'):
        content["paragraphs"].append({"text": p.get_text(strip=True), "html": str(p)})

    for a in soup.find_all('a'):
        content["links"].append({"text": a.get_text(strip=True), "href": a.get('href',''), "classes": a.get('class',[])})

    for img in soup.find_all('img'):
        content["images"].append({"src": img.get('src',''), "alt": img.get('alt','')})

    for btn in soup.find_all(class_=lambda c: c and 'btn' in ' '.join(c)):
        content["buttons"].append({"text": btn.get_text(strip=True), "href": btn.get('href',''), "html": str(btn)})

    return content
```

**Step 2: After transformation, verify all content is present**
```python
def verify_content_preserved(original_content: dict, new_section_html: str) -> list:
    """Verify all original content exists in the transformed section."""
    new_content = extract_section_content(new_section_html)
    missing = []

    for h in original_content["headings"]:
        if not any(h["text"] in nh["text"] for nh in new_content["headings"]):
            missing.append(f"MISSING HEADING: {h['text']}")

    for p in original_content["paragraphs"]:
        if p["text"] and not any(p["text"][:50] in np["text"] for np in new_content["paragraphs"]):
            missing.append(f"MISSING PARAGRAPH: {p['text'][:80]}...")

    for img in original_content["images"]:
        if not any(img["src"] == ni["src"] for ni in new_content["images"]):
            missing.append(f"MISSING IMAGE: {img['src']}")

    for btn in original_content["buttons"]:
        if not any(btn["text"] in nb["text"] for nb in new_content["buttons"]):
            missing.append(f"MISSING BUTTON: {btn['text']}")

    return missing  # Empty list = all content preserved
```

**If verification finds missing content, the transformation has FAILED.** Restore from backup and retry.
```

---

### Addition B: Responsive Breakpoint Mandatory Rules

**WHERE:** Add as a new section after the new "Content Preservation Protocol", before "Layout Catalogue".

```markdown
## Responsive Breakpoint Rules (BLOCKING)

**CRITICAL:** Every layout transformation MUST include responsive breakpoints. A layout without responsive rules is broken on mobile devices.

### Mandatory Breakpoints

Every layout transformation MUST include CSS rules for these three breakpoints:

```css
/* Desktop (default) — write desktop CSS first for layout transforms */
.section-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* Multi-column on desktop */
}

/* Tablet */
@media (max-width: 1024px) {
    .section-grid {
        grid-template-columns: repeat(2, 1fr);  /* 2 columns on tablet */
    }
}

/* Mobile */
@media (max-width: 768px) {
    .section-grid {
        grid-template-columns: 1fr;  /* Single column on mobile */
    }
}
```

### Responsive Patterns by Layout Type

| Layout | Desktop | Tablet (<=1024px) | Mobile (<=768px) |
|--------|---------|-------------------|------------------|
| 2-column split | `1fr 1fr` | `1fr 1fr` | `1fr` (stacked) |
| 3-column features | `repeat(3, 1fr)` | `repeat(2, 1fr)` | `1fr` |
| 4-column footer | `repeat(4, 1fr)` | `repeat(2, 1fr)` | `1fr` |
| Bento grid | `repeat(4, 1fr)` | `repeat(2, 1fr)` | `1fr` |
| Sidebar | `250px 1fr` | `200px 1fr` | `1fr` (sidebar hidden/collapsed) |
| Card grid | `repeat(auto-fit, minmax(300px, 1fr))` | Same (auto-adjusts) | Same |
| Timeline | Alternating left/right | Alternating left/right | Single column left-aligned |

**Rule:** If the transformed CSS does not contain `@media (max-width: 768px)` with layout adjustments, the transformation is INCOMPLETE. Go back and add mobile breakpoints.
```

---

### Addition C: Specific Layout Transformation Recipes

**WHERE:** Add after the existing "Layout Transformation Templates" section (around line 590), expanding the section with detailed recipes for the most-failed layouts.

```markdown
## Detailed Transformation Recipes

These recipes address the most commonly failed layout transformations with exact HTML and CSS.

### Recipe 1: Features Section — 3-Column Card Grid

**Source pattern (any):** Features as a list, vertical stack, or 2-column layout
**Target:** 3-column responsive card grid

```html
<!-- Target HTML structure -->
<section class="features" id="features">
    <div class="container">
        <div class="section-header">
            <h2>{PRESERVE: original heading text}</h2>
            <p>{PRESERVE: original subtitle text}</p>
        </div>
        <div class="features-grid">
            <!-- Repeat for EACH feature item from the original -->
            <div class="feature-card">
                <div class="feature-icon">{PRESERVE: original icon}</div>
                <h3>{PRESERVE: original feature title}</h3>
                <p>{PRESERVE: original feature description}</p>
            </div>
            <!-- ... more cards ... -->
        </div>
    </div>
</section>
```

```css
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
}

.feature-card {
    background: var(--surface-color, #f8f9fa);
    border-radius: var(--border-radius, 8px);
    padding: 2rem;
    text-align: center;
}

@media (max-width: 1024px) {
    .features-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .features-grid {
        grid-template-columns: 1fr;
    }
}
```

### Recipe 2: Hero — Parallax Background

**Target:** True parallax scrolling effect (not just a background change)

```html
<section class="hero hero--parallax" id="hero">
    <div class="hero-bg hero-bg--parallax">
        <img src="{PRESERVE: original image src}" alt="{PRESERVE: original alt}" class="hero-bg__img">
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1>{PRESERVE: original heading}</h1>
        <p>{PRESERVE: original subtitle}</p>
        <a href="{PRESERVE: original CTA href}" class="btn">{PRESERVE: original CTA text}</a>
    </div>
</section>
```

```css
.hero--parallax {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.hero-bg--parallax {
    position: absolute;
    inset: -20% 0;  /* Extra height for parallax movement */
    z-index: 0;
}

.hero-bg--parallax .hero-bg__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    z-index: 1;
    background: rgba(0, 0, 0, 0.5);
}

.hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    color: #ffffff;
}

/* Parallax scroll effect via JavaScript */
```

```javascript
// Add to main.js — Parallax scroll handler
window.addEventListener('scroll', () => {
    const parallaxBg = document.querySelector('.hero-bg--parallax');
    if (parallaxBg) {
        const scrolled = window.pageYOffset;
        parallaxBg.style.transform = `translateY(${scrolled * 0.4}px)`;
    }
});
```

**Key requirement:** Parallax MUST include the JavaScript scroll handler. Without it, the image is static and there is no parallax effect. CSS-only `background-attachment: fixed` is an acceptable alternative:

```css
/* CSS-only parallax alternative */
.hero--parallax-css {
    background-image: url('images/hero-bg.jpg');
    background-attachment: fixed;
    background-position: center;
    background-size: cover;
    min-height: 100vh;
}
```

### Recipe 3: Footer — 4-Column Grid

**Target:** Footer with 4 equal columns (About, Links, Services, Contact)

```html
<footer class="site-footer" id="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>{PRESERVE: column 1 heading, e.g., "About Us"}</h4>
                <p>{PRESERVE: about text}</p>
            </div>
            <div class="footer-col">
                <h4>{PRESERVE: column 2 heading, e.g., "Quick Links"}</h4>
                <ul class="footer-links">
                    <!-- PRESERVE: all original links -->
                    <li><a href="{href}">{link text}</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>{PRESERVE: column 3 heading, e.g., "Services"}</h4>
                <ul class="footer-links">
                    <!-- PRESERVE: all original links -->
                    <li><a href="{href}">{link text}</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>{PRESERVE: column 4 heading, e.g., "Contact"}</h4>
                <!-- PRESERVE: all contact info -->
                <p>{phone}</p>
                <p>{email}</p>
                <p>{address}</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>{PRESERVE: copyright text}</p>
        </div>
    </div>
</footer>
```

```css
.footer-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    padding: 3rem 0;
}

.footer-col h4 {
    margin-bottom: 1rem;
    font-size: 1.125rem;
    color: var(--text-color, #ffffff);
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: var(--text-secondary, #b8c0d4);
    text-decoration: none;
}

.footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1.5rem;
    text-align: center;
}

@media (max-width: 1024px) {
    .footer-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .footer-grid {
        grid-template-columns: 1fr;
    }
}
```

### Recipe 4: Alternating Content Rows (Z-Pattern)

**Target:** Content sections alternate between text-left/image-right and image-left/text-right

```html
<section class="content-rows" id="about">
    <div class="container">
        <!-- Row 1: Text Left, Image Right -->
        <div class="content-row">
            <div class="content-row__text">
                <h3>{PRESERVE: heading}</h3>
                <p>{PRESERVE: description}</p>
            </div>
            <div class="content-row__image">
                <img src="{PRESERVE: image src}" alt="{PRESERVE: alt}">
            </div>
        </div>
        <!-- Row 2: Image Left, Text Right (REVERSED) -->
        <div class="content-row content-row--reverse">
            <div class="content-row__text">
                <h3>{PRESERVE: heading}</h3>
                <p>{PRESERVE: description}</p>
            </div>
            <div class="content-row__image">
                <img src="{PRESERVE: image src}" alt="{PRESERVE: alt}">
            </div>
        </div>
        <!-- Row 3: Text Left, Image Right (same as row 1) -->
        <!-- ... pattern continues ... -->
    </div>
</section>
```

```css
.content-row {
    display: flex;
    align-items: center;
    gap: 3rem;
    margin-bottom: 4rem;
}

/* CRITICAL: row-reverse flips the visual order without changing HTML order */
.content-row--reverse {
    flex-direction: row-reverse;
}

.content-row__text {
    flex: 1;
}

.content-row__image {
    flex: 1;
}

.content-row__image img {
    width: 100%;
    border-radius: var(--border-radius, 8px);
    object-fit: cover;
}

@media (max-width: 768px) {
    .content-row,
    .content-row--reverse {
        flex-direction: column;  /* Stack vertically on mobile */
    }
}
```

**Key concept:** The alternating pattern uses `flex-direction: row-reverse` on even rows. The HTML order stays the same (text first, image second) but the CSS reverses the visual order. This ensures correct reading order for screen readers while creating the visual zigzag pattern.
```

---

### Addition D: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 622).

```markdown
| Deleting content elements during restructuring | User's text, images, links are lost forever | Extract content BEFORE transforming, verify AFTER |
| Writing layout CSS without mobile breakpoints | Site broken on mobile (50%+ of traffic) | EVERY layout MUST have `@media (max-width: 768px)` rules |
| Parallax: only changing background-image, no scroll effect | Not parallax, just a background image change | Parallax requires JS scroll handler OR `background-attachment: fixed` |
| 4-column footer: using flex instead of grid | Columns don't align, unequal widths | Use `grid-template-columns: repeat(4, 1fr)` for equal columns |
| Alternating rows: swapping HTML order instead of using CSS | Breaks screen reader order, duplicates content errors | Use `flex-direction: row-reverse`, keep HTML order unchanged |
| Bento grid: all items same size | Not a bento grid, just a regular grid | Bento requires `span 2` on featured items via `grid-column: span 2` |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| HTML structure broken | Addition A (Content Preservation Protocol) | Extract-transform-verify procedure prevents content loss |
| No responsive breakpoints | Addition B (Responsive Breakpoint Rules) | Mandatory breakpoint table per layout type |
| Parallax not implemented | Addition C Recipe 2 (complete parallax code) | Full HTML + CSS + JS recipe with parallax scroll handler |
| 4-column footer fails | Addition C Recipe 3 (complete footer grid) | Copy-paste ready 4-column grid with responsive breakpoints |
| Content lost | Addition A (verification function) | Automated check catches missing content before completion |
| Alternating rows broken | Addition C Recipe 4 (flexbox row-reverse) | Explicit explanation of row-reverse pattern |

**Projected score improvement:** 0.8 -> 2.8+ (this skill needs the most improvement; additions target every failure mode)
