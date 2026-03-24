# Template Customization Skill - Enhancement Proposal

**Based on:** Eval pack results (30 learnings, avg score 3.5/5)
**Skill file:** `skills/template_customization.skill.md`
**Version target:** v1.1.0

---

## 1. Current Issue Summary

| Issue | Frequency | Severity |
|-------|-----------|----------|
| Models paraphrase content instead of using exact text from requirements | Very High | Critical |
| Contact section not properly structured (should be dedicated section with cards) | High | High |
| JSON-LD structured data incomplete or missing | High | Medium |
| Meta tags (OG, description) not consistently added | Medium | Medium |
| Business name inconsistent across header, footer, meta, JSON-LD | High | High |

The most critical issue is content fidelity: when given specific text to use (e.g., a tagline, feature descriptions, about text), models rewrite or paraphrase it instead of using the exact text verbatim. The second most common issue is that the business name appears differently in different locations (e.g., "Acme Corp" in header, "Acme Corporation" in footer, "acme" in meta tags).

---

## 2. Proposed Additions

### Addition A: Verbatim Content Rule (Critical)

**WHERE:** Add as a new section immediately after "Content Injection Rules" (after line 214), before "Meta Tags Update".

```markdown
### Verbatim Content Rule (BLOCKING)

**CRITICAL:** When the user provides specific text content (headings, descriptions, taglines, feature text, about copy), you MUST use that text EXACTLY as provided. Do NOT:

- Paraphrase or reword the user's text
- "Improve" the phrasing
- Shorten or lengthen the text
- Change capitalisation
- Add words not in the original
- Replace specific terms with synonyms

**Examples:**

User provides: `"We craft digital experiences that drive growth"`

| Action | Text Used | Correct? |
|--------|----------|----------|
| Use verbatim | "We craft digital experiences that drive growth" | YES |
| Paraphrase | "Creating digital solutions for business growth" | NO |
| Shorten | "Digital experiences that drive growth" | NO |
| Expand | "We expertly craft innovative digital experiences that accelerate and drive sustainable growth" | NO |
| Synonym swap | "We build digital experiences that fuel growth" | NO |

**The ONLY acceptable modifications to user-provided text are:**
1. HTML entity escaping (`&` -> `&amp;`, `<` -> `&lt;`)
2. Wrapping in appropriate HTML tags (`<h1>`, `<p>`, etc.)
3. Adding `<br>` if the user explicitly indicates a line break

**If the user provides text in quotes, that text is SACRED. Use it character-for-character.**
```

---

### Addition B: Business Name Consistency Rule

**WHERE:** Add as a new section after the new "Verbatim Content Rule", before "Meta Tags Update".

```markdown
### Business Name Consistency Rule (BLOCKING)

**CRITICAL:** The business name MUST appear IDENTICALLY in ALL of the following locations. Use the EXACT casing and spelling provided by the user.

| Location | How It Appears | Example |
|----------|---------------|---------|
| `<title>` tag | `{BusinessName} - {Tagline}` | `Acme Corporation - Building Better Solutions` |
| `<meta name="description">` | Contains `{BusinessName}` | `Acme Corporation offers...` |
| `<meta property="og:title">` | `{BusinessName}` | `Acme Corporation` |
| `<meta property="og:site_name">` | `{BusinessName}` | `Acme Corporation` |
| Header/navbar logo alt text | `{BusinessName} Logo` | `Acme Corporation Logo` |
| Header/navbar logo link aria-label | `{BusinessName} Home` | `Acme Corporation Home` |
| Footer logo alt text | `{BusinessName} Logo` | `Acme Corporation Logo` |
| Footer copyright | `{Year} {BusinessName}` | `2026 Acme Corporation` |
| JSON-LD `"name"` | `{BusinessName}` | `"name": "Acme Corporation"` |
| JSON-LD `"legalName"` | `{BusinessName}` | `"legalName": "Acme Corporation"` |

**Verification step:** After customization, search the entire HTML for the business name. Every occurrence MUST match exactly. Common inconsistencies to check for:
- Header says "Acme Corp" but footer says "Acme Corporation"
- Meta tags use lowercase "acme corporation"
- JSON-LD uses a different variation
- Alt text still says "Company Logo" or placeholder text
```

---

### Addition C: Contact Section Structure Rule

**WHERE:** Add as a new section after "Form Configuration" (after line 340), before "Multi-Variant Generation".

```markdown
## Contact Section Structure (MANDATORY)

When the user requests a contact section, it MUST be structured as a dedicated `<section>` with contact info cards and an optional form. Do NOT scatter contact info across other sections or bury it in the footer only.

### Required Contact Section Structure

```html
<section class="contact" id="contact">
    <div class="container">
        <div class="section-header">
            <h2>Contact Us</h2>
            <p>{User's contact section subtitle, or "Get in touch with us"}</p>
        </div>
        <div class="contact-grid">
            <!-- Contact Info Cards -->
            <div class="contact-info">
                <div class="contact-card">
                    <div class="contact-card__icon">
                        <!-- Phone icon (SVG or font icon) -->
                    </div>
                    <h3>Phone</h3>
                    <p><a href="tel:{phone}">{phone}</a></p>
                </div>
                <div class="contact-card">
                    <div class="contact-card__icon">
                        <!-- Email icon -->
                    </div>
                    <h3>Email</h3>
                    <p><a href="mailto:{email}">{email}</a></p>
                </div>
                <div class="contact-card">
                    <div class="contact-card__icon">
                        <!-- Location icon -->
                    </div>
                    <h3>Address</h3>
                    <p>{address}</p>
                </div>
            </div>
            <!-- Contact Form (if enabled) -->
            <div class="contact-form-wrapper">
                <form class="contact-form" action="{FORM_ACTION}" method="POST">
                    <!-- form fields -->
                </form>
            </div>
        </div>
    </div>
</section>
```

```css
.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: start;
}

.contact-info {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.contact-card {
    background: var(--surface-color, #f8f9fa);
    border-radius: var(--border-radius, 8px);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
}

.contact-card__icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(var(--primary-rgb), 0.1);
    border-radius: 50%;
    color: var(--primary-color);
}

@media (max-width: 768px) {
    .contact-grid {
        grid-template-columns: 1fr;
    }
}
```

**Rules:**
- Phone numbers MUST be wrapped in `<a href="tel:...">` for click-to-call
- Email addresses MUST be wrapped in `<a href="mailto:...">` for click-to-email
- Each contact method gets its own card with an icon
- The contact section MUST have its own `id="contact"` and be listed in the nav
```

---

### Addition D: JSON-LD Structured Data Rule

**WHERE:** Add as a new section after the "Meta Tags Update" subsection (after line 227).

```markdown
### JSON-LD Structured Data (MANDATORY)

Every customized site MUST include a complete JSON-LD structured data block in `<head>` for search engine optimization. This is NOT optional.

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{BusinessName}",
    "legalName": "{BusinessName}",
    "url": "{website_url}",
    "logo": "{website_url}/images/logo.svg",
    "description": "{meta_description}",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "{street_address}",
        "addressLocality": "{city}",
        "addressRegion": "{state_or_province}",
        "postalCode": "{postal_code}",
        "addressCountry": "{country_code}"
    },
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "{phone}",
        "email": "{email}",
        "contactType": "customer service"
    },
    "sameAs": [
        "{facebook_url}",
        "{twitter_url}",
        "{linkedin_url}",
        "{instagram_url}"
    ]
}
</script>
```

**Rules:**
1. `"name"` MUST match the business name exactly (see Business Name Consistency Rule)
2. `"url"` should be the site's URL if known, otherwise use `"https://www.example.com"` as placeholder
3. `"sameAs"` array should only include social URLs that were provided — omit empty entries, do not include placeholder URLs
4. If the user provides an address, include the full `"address"` object. If not, omit the `"address"` field entirely (do not use placeholder addresses)
5. `"contactPoint"` MUST include phone and email if provided by the user
6. If the business type is more specific (e.g., restaurant, law firm, medical practice), use the appropriate `@type` instead of `Organization`
```

---

### Addition E: Complete Meta Tags Rule

**WHERE:** Add as an expansion of the existing "Meta Tags Update" subsection (replace lines 218-227 with this expanded version).

```markdown
### Meta Tags Update (MANDATORY)

Every customized site MUST include ALL of the following meta tags in `<head>`. Missing meta tags are a customization failure.

```html
<head>
    <!-- Basic Meta -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{BusinessName} - {Tagline}</title>
    <meta name="description" content="{150-160 character description of the business}">
    <meta name="author" content="{BusinessName}">

    <!-- Open Graph (Facebook, LinkedIn) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{BusinessName} - {Tagline}">
    <meta property="og:description" content="{Same as meta description}">
    <meta property="og:image" content="images/og-image.png">
    <meta property="og:url" content="{website_url}">
    <meta property="og:site_name" content="{BusinessName}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{BusinessName} - {Tagline}">
    <meta name="twitter:description" content="{Same as meta description}">
    <meta name="twitter:image" content="images/og-image.png">

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="images/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
</head>
```

**Rules:**
1. `<title>` format: `{BusinessName} - {Tagline}` (not just the business name)
2. `<meta name="description">` MUST be 150-160 characters, summarizing the business. Use the user's tagline/description if provided, otherwise compose a factual description
3. ALL `og:` tags MUST be present — they control how the site appears when shared on social media
4. `og:title`, `twitter:title`, and `<title>` MUST be consistent (same business name and tagline)
5. `og:description` and `twitter:description` MUST match `<meta name="description">`
6. If no OG image is provided, keep the placeholder reference but note it as a TODO
```

---

### Addition F: Anti-Pattern Table Additions

**WHERE:** Add these rows to the existing Anti-Patterns table (around line 416).

```markdown
| Paraphrasing user-provided text | User's carefully written copy is altered | Use user text VERBATIM — character for character |
| Business name varies across locations | Looks unprofessional, hurts SEO | Use EXACT same name in header, footer, meta, JSON-LD, alt text |
| Contact info scattered across footer only | No dedicated contact section, poor UX | Create a dedicated `<section id="contact">` with contact cards |
| Missing JSON-LD structured data | Poor search engine indexing | ALWAYS add JSON-LD `<script>` block in `<head>` |
| Missing or incomplete OG meta tags | Site looks ugly when shared on social media | Include ALL og: and twitter: meta tags |
| Meta description left as placeholder | SEO penalty, looks unprofessional in search results | Write a real 150-160 char description using business info |
```

---

## 3. Expected Impact

| Issue | Enhancement | Expected Resolution |
|-------|------------|---------------------|
| Content paraphrased | Addition A (Verbatim Content Rule) | Explicit examples of wrong vs right with "SACRED" emphasis |
| Contact section unstructured | Addition C (Contact Section Structure) | Complete HTML+CSS recipe for contact section with cards |
| JSON-LD missing/incomplete | Addition D (JSON-LD Rule) | Complete template with field-by-field rules |
| Meta tags inconsistent | Addition E (Complete Meta Tags Rule) | Full meta tag checklist with consistency rules |
| Business name inconsistent | Addition B (Business Name Consistency Rule) | Location-by-location verification table |

**Projected score improvement:** 3.5 -> 4.2+ (verbatim content rule addresses the single most common failure at ~40% of violations)
