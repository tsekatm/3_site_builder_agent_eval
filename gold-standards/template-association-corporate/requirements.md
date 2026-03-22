# Template Requirements: HASA Main Site Redesign - V3

## Source
- **Figma File**: HASA Main Site Redesign - V3
- **Figma Key**: 4diRrKJRYjAbA93vpLHIpN
- **Project**: Hasa Main
- **Type**: Site

## Business Profile
- **Business Name**: Institute of Chartered Accountants SA
- **Industry**: Professional Accounting Body
- **Tagline**: Setting the standard in financial excellence

## Brand Amendments

### Colours
- **Primary**: #2B4C7E
- **Secondary**: #0F2440
- **Accent**: #5DADE2
- **Background**: #F5F7FA
- **Text**: #1C1C28

### Typography
- **Heading Font**: Merriweather
- **Body Font**: Hind

### Logo
- **Logo Source**: `assets/logos/institute-chartered-accountants-sa-logo.svg`
- **Favicon**: `assets/logos/institute-chartered-accountants-sa-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Shaping the Future of the Accounting Profession
- **Subheadline**: Professional development, regulatory guidance, and advocacy for over 50,000 chartered accountants and auditors in Southern Africa.
- **CTA Button**: Join the Institute

### About Section
- **Description**: The Institute of Chartered Accountants SA is the premier professional body for accountants, auditors, and financial professionals in the region. We set ethical standards, deliver world-class examinations, and provide lifelong learning programmes. Our members are trusted leaders in business, government, and the non-profit sector.

### Contact
- **Email**: info@icasa.org.za
- **Phone**: +27 11 621 6600
- **Address**: Integritas Building, 7 Zulberg Close, Bruma Lake, Johannesburg, 2198

## Layout Amendments

### Hero Layout
- **Pattern**: centered-minimal
- **Arrangement**: Clean centered headline on light background with professional crest and CTA below

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: single-highlight
- **Footer Layout**: mega-footer

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Merriweather
- **Heading Weights**: 400, 700
- **Body Font**: Hind
- **Body Weights**: 300, 400, 500
- **CTA Font**: Hind

### Font Sizing
- **H1**: 46px / 2.875rem
- **H2**: 34px / 2.125rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/institute-chartered-accountants-sa-hero-bg.jpg`
- **Alt Text**: Professional accountants at a conference in a modern auditorium
- **Overlay**: Light gradient overlay at 20% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/institute-chartered-accountants-sa-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/examination.svg`, `assets/images/icons/ethics-standard.svg`, `assets/images/icons/lifelong-learning.svg`, `assets/images/icons/member-directory.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/institute-chartered-accountants-sa-logo.svg`
- **Alt Text**: "Institute of Chartered Accountants SA Logo"
- **Max Height**: 52px

### Footer Logo
- **Source**: `assets/logos/institute-chartered-accountants-sa-logo-white.svg`
- **Alt Text**: "Institute of Chartered Accountants SA"

### Favicon
- **Source**: `assets/logos/institute-chartered-accountants-sa-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Institute of Chartered Accountants SA — Setting the standard in financial excellence"
- **Description**: The Institute of Chartered Accountants SA provides professional development, examinations, and ethical standards for over 50,000 chartered accountants in Southern Africa.
- **OG Title**: Institute of Chartered Accountants SA — Setting the standard in financial excellence
- **OG Description**: The Institute of Chartered Accountants SA provides professional development, examinations, and ethical standards for over 50,000 chartered accountants in Southern Africa.
- **OG Image**: `assets/images/institute-chartered-accountants-sa-og.jpg`

### Structured Data
- **Type**: Organization
- **Schema.org**: JSON-LD in head

### Heading Hierarchy
- **H1**: One per page (hero headline)
- **H2**: Section headings
- **H3**: Subsection headings
- No skipped levels

## Performance Requirements

### Images
- **Format**: WebP with JPEG fallback
- **Max File Size**: 200KB per image (hero max 500KB)
- **Lazy Loading**: All images below the fold
- **Responsive**: srcset for 1x, 2x

### Fonts
- **font-display**: swap on all declarations
- **Preconnect**: `<link rel="preconnect" href="https://fonts.googleapis.com">`
- **Max Families**: 2 (heading + body)

### CSS
- **CSS Variables**: All colours and fonts via :root variables
- **No Inline Styles**: All styling via external CSS

## Accessibility Requirements

### Images
- **Alt Text**: All images must have descriptive alt text
- **Decorative Images**: Use `alt=""` and `role="presentation"`

### Navigation
- **Skip Link**: "Skip to main content" as first focusable element
- **ARIA Labels**: All nav elements labelled

### Colour Contrast
- **Body Text**: WCAG AA minimum (4.5:1 ratio)
- **Large Text**: WCAG AA minimum (3:1 ratio)
- **CTA Buttons**: WCAG AA minimum against button background

## Deployment
- **Staging URL Pattern**: `https://dev.institute-chartered-accountants-sa.preview.example.com`
- **S3 Prefix**: `staging/institute-chartered-accountants-sa/`
