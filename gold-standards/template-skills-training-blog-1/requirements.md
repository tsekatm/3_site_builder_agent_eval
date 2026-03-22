# Template Requirements: Blog-Capaciti - Option 1

## Source
- **Figma File**: Blog-Capaciti - Option 1
- **Figma Key**: viH5HRCWleSJgKJxoGw8MK
- **Project**: Capaciti
- **Type**: Blog

## Business Profile
- **Business Name**: GreenPulse Analytics
- **Industry**: Environmental Technology
- **Tagline**: Data-driven insights for a sustainable future

## Brand Amendments

### Colours
- **Primary**: #1B7A3D
- **Secondary**: #2E4A3E
- **Accent**: #7CC47F
- **Background**: #F5FAF6
- **Text**: #1A1A2E

### Typography
- **Heading Font**: Space Grotesk
- **Body Font**: Inter

### Logo
- **Logo Source**: `assets/logos/greenpulse-analytics-logo.svg`
- **Favicon**: `assets/logos/greenpulse-analytics-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Insights That Power a Greener Tomorrow
- **Subheadline**: Our blog explores the intersection of environmental science and data analytics, bringing you actionable intelligence for sustainability leaders.
- **CTA Button**: Read Latest Articles

### About Section
- **Description**: GreenPulse Analytics is an environmental technology firm specialising in carbon footprint measurement and sustainability reporting. We help enterprises track, analyse, and reduce their environmental impact through advanced data platforms. Our team of data scientists and environmental engineers delivers clarity in a complex regulatory landscape.

### Contact
- **Email**: hello@greenpulseanalytics.co.za
- **Phone**: +27 21 555 0192
- **Address**: 45 Bree Street, Cape Town, 8001, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: full-width-overlay
- **Arrangement**: Centered text over background image with gradient overlay

### Sections Layout
- **Features Section**: card-grid-3col
- **Testimonials Section**: carousel
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Space Grotesk
- **Heading Weights**: 500, 700
- **Body Font**: Inter
- **Body Weights**: 300, 400, 500
- **CTA Font**: Space Grotesk

### Font Sizing
- **H1**: 48px / 3rem
- **H2**: 36px / 2.25rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/greenpulse-analytics-hero-bg.jpg`
- **Alt Text**: Aerial view of green forest canopy with data visualisation overlay
- **Overlay**: Dark gradient overlay at 60% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/greenpulse-analytics-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/carbon-tracker.svg`, `assets/images/icons/data-dashboard.svg`, `assets/images/icons/sustainability-report.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/greenpulse-analytics-logo.svg`
- **Alt Text**: "GreenPulse Analytics Logo"
- **Max Height**: 44px

### Footer Logo
- **Source**: `assets/logos/greenpulse-analytics-logo-white.svg`
- **Alt Text**: "GreenPulse Analytics"

### Favicon
- **Source**: `assets/logos/greenpulse-analytics-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "GreenPulse Analytics — Data-driven insights for a sustainable future"
- **Description**: GreenPulse Analytics delivers environmental data intelligence and carbon footprint measurement tools for enterprises committed to sustainability reporting.
- **OG Title**: GreenPulse Analytics — Data-driven insights for a sustainable future
- **OG Description**: GreenPulse Analytics delivers environmental data intelligence and carbon footprint measurement tools for enterprises committed to sustainability reporting.
- **OG Image**: `assets/images/greenpulse-analytics-og.jpg`

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
- **Staging URL Pattern**: `https://dev.greenpulse-analytics.preview.example.com`
- **S3 Prefix**: `staging/greenpulse-analytics/`
