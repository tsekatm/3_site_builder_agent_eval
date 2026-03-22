# Template Requirements: Catalyst App Landing Page

## Source
- **Figma File**: Catalyst App Landing Page
- **Figma Key**: EQYDubJjrnkn4IEDwNQauV
- **Project**: Catalyst App Landing Page
- **Type**: Landing Page

## Business Profile
- **Business Name**: FleetPulse
- **Industry**: Logistics Technology
- **Tagline**: Real-time fleet intelligence at your fingertips

## Brand Amendments

### Colours
- **Primary**: #E84430
- **Secondary**: #2B2D42
- **Accent**: #FF8C42
- **Background**: #FEFEFE
- **Text**: #1B1B2F

### Typography
- **Heading Font**: Outfit
- **Body Font**: Work Sans

### Logo
- **Logo Source**: `assets/logos/fleetpulse-logo.svg`
- **Favicon**: `assets/logos/fleetpulse-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Track Every Vehicle. Optimise Every Route.
- **Subheadline**: FleetPulse gives logistics managers real-time GPS tracking, fuel analytics, and driver behaviour scoring in one powerful mobile app.
- **CTA Button**: Download the App

### About Section
- **Description**: FleetPulse is a logistics SaaS platform that helps fleet operators reduce costs and improve delivery performance. Our mobile-first solution integrates with existing telematics hardware and provides instant visibility across your entire fleet. Trusted by over 200 transport companies in Sub-Saharan Africa.

### Contact
- **Email**: sales@fleetpulse.io
- **Phone**: +27 10 900 3344
- **Address**: 5th Floor, The Link, 173 Oxford Road, Rosebank, Johannesburg, 2196

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Text left with app mockup phone frame right

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
- **Heading Font**: Outfit
- **Heading Weights**: 600, 700
- **Body Font**: Work Sans
- **Body Weights**: 300, 400, 500
- **CTA Font**: Outfit

### Font Sizing
- **H1**: 52px / 3.25rem
- **H2**: 36px / 2.25rem
- **Body**: 16px / 1rem
- **CTA Button**: 18px / 1.125rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/fleetpulse-hero-bg.jpg`
- **Alt Text**: Fleet of delivery trucks on a highway with GPS tracking overlay graphic
- **Overlay**: none (solid colour background with app mockup)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/fleetpulse-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/gps-tracking.svg`, `assets/images/icons/fuel-analytics.svg`, `assets/images/icons/driver-score.svg`, `assets/images/icons/route-optimise.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/fleetpulse-logo.svg`
- **Alt Text**: "FleetPulse Logo"
- **Max Height**: 40px

### Footer Logo
- **Source**: `assets/logos/fleetpulse-logo-white.svg`
- **Alt Text**: "FleetPulse"

### Favicon
- **Source**: `assets/logos/fleetpulse-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "FleetPulse — Real-time fleet intelligence at your fingertips"
- **Description**: FleetPulse provides real-time GPS tracking, fuel analytics, and driver behaviour scoring for logistics managers across Sub-Saharan Africa.
- **OG Title**: FleetPulse — Real-time fleet intelligence at your fingertips
- **OG Description**: FleetPulse provides real-time GPS tracking, fuel analytics, and driver behaviour scoring for logistics managers across Sub-Saharan Africa.
- **OG Image**: `assets/images/fleetpulse-og.jpg`

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
- **Staging URL Pattern**: `https://dev.fleetpulse.preview.example.com`
- **S3 Prefix**: `staging/fleetpulse/`
