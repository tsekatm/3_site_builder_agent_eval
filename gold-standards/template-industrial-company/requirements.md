# Template Requirements: Forgeweld

## Source
- **Figma File**: Forgeweld
- **Figma Key**: EF5ayUwdHLWd0G8Wd7yEC3
- **Project**: Forgeweld
- **Type**: Site

## Business Profile
- **Business Name**: TitanCore Engineering
- **Industry**: Industrial Manufacturing
- **Tagline**: Engineered to perform, built to last

## Brand Amendments

### Colours
- **Primary**: #D4451A
- **Secondary**: #1C1C1C
- **Accent**: #F5A623
- **Background**: #F9F9F9
- **Text**: #212121

### Typography
- **Heading Font**: Oswald
- **Body Font**: Roboto

### Logo
- **Logo Source**: `assets/logos/titancore-engineering-logo.svg`
- **Favicon**: `assets/logos/titancore-engineering-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Precision Steel Fabrication for Africa's Biggest Projects
- **Subheadline**: Custom structural steel, heavy plate fabrication, and industrial welding services. ISO 3834 certified. Delivering across Sub-Saharan Africa.
- **CTA Button**: Request a Quote

### About Section
- **Description**: TitanCore Engineering is a steel fabrication and industrial services company based in Vanderbijlpark. We specialise in structural steelwork, pressure vessels, and mining equipment fabrication. With a 12,000m2 workshop and a team of 180 coded welders, we deliver large-scale projects on time and to specification.

### Contact
- **Email**: projects@titancoreeng.co.za
- **Phone**: +27 16 981 3000
- **Address**: 42 Steel Road, Vanderbijlpark, 1900, Gauteng, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: asymmetric-grid
- **Arrangement**: Bold headline left with industrial workshop photography right, angled steel-beam divider

### Sections Layout
- **Features Section**: timeline
- **Testimonials Section**: grid-2col
- **Footer Layout**: mega-footer

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Oswald
- **Heading Weights**: 500, 700
- **Body Font**: Roboto
- **Body Weights**: 300, 400, 500
- **CTA Font**: Oswald

### Font Sizing
- **H1**: 54px / 3.375rem
- **H2**: 38px / 2.375rem
- **Body**: 16px / 1rem
- **CTA Button**: 18px / 1.125rem, uppercase, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/titancore-engineering-hero-bg.jpg`
- **Alt Text**: Sparks flying from steel welding in an industrial fabrication workshop
- **Overlay**: Dark gradient overlay at 65% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: `assets/images/titancore-engineering-features-bg.jpg`
- **CTA Section**: `assets/images/titancore-engineering-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/structural-steel.svg`, `assets/images/icons/pressure-vessel.svg`, `assets/images/icons/mining-equipment.svg`, `assets/images/icons/iso-certified.svg`
- **Team Photos**: N/A
- **Gallery**: `assets/images/gallery/workshop-01.jpg`, `assets/images/gallery/project-steel-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/titancore-engineering-logo.svg`
- **Alt Text**: "TitanCore Engineering Logo"
- **Max Height**: 44px

### Footer Logo
- **Source**: `assets/logos/titancore-engineering-logo-white.svg`
- **Alt Text**: "TitanCore Engineering"

### Favicon
- **Source**: `assets/logos/titancore-engineering-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "TitanCore Engineering — Engineered to perform, built to last"
- **Description**: TitanCore Engineering provides precision steel fabrication, heavy plate welding, and industrial manufacturing services, ISO 3834 certified, across Sub-Saharan Africa.
- **OG Title**: TitanCore Engineering — Engineered to perform, built to last
- **OG Description**: TitanCore Engineering provides precision steel fabrication, heavy plate welding, and industrial manufacturing services, ISO 3834 certified, across Sub-Saharan Africa.
- **OG Image**: `assets/images/titancore-engineering-og.jpg`

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
- **Staging URL Pattern**: `https://dev.titancore-engineering.preview.example.com`
- **S3 Prefix**: `staging/titancore-engineering/`
