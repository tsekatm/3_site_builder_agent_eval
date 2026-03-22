# Template Requirements: Industry Landing Page

## Source
- **Figma File**: Industry landing page
- **Figma Key**: rdvPurH4MH0bPHP4gyTIQY
- **Project**: Industry Landing Page
- **Type**: Landing Page

## Business Profile
- **Business Name**: SunVolt Energy
- **Industry**: Renewable Energy / Solar
- **Tagline**: Powering progress with clean energy

## Brand Amendments

### Colours
- **Primary**: #F59E0B
- **Secondary**: #1E3A2F
- **Accent**: #10B981
- **Background**: #FFFDF5
- **Text**: #1A1A1A

### Typography
- **Heading Font**: Montserrat
- **Body Font**: Poppins

### Logo
- **Logo Source**: `assets/logos/sunvolt-energy-logo.svg`
- **Favicon**: `assets/logos/sunvolt-energy-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Solar Solutions for Homes, Farms, and Businesses
- **Subheadline**: Reduce your electricity costs by up to 80%. Expert solar installation, battery storage, and energy management systems across South Africa.
- **CTA Button**: Get a Free Quote

### About Section
- **Description**: SunVolt Energy is a solar energy company providing turnkey photovoltaic installations for residential, agricultural, and commercial clients. We handle everything from site assessment and system design to installation and ongoing maintenance. With over 2,500 installations completed, we are one of the fastest-growing solar providers in the country.

### Contact
- **Email**: quotes@sunvoltenergy.co.za
- **Phone**: +27 21 100 4488
- **Address**: Unit 12, Sunnydale Business Park, Noordhoek, Cape Town, 7979

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Bold headline and quote form left, solar panel installation photo right

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
- **Heading Font**: Montserrat
- **Heading Weights**: 600, 800
- **Body Font**: Poppins
- **Body Weights**: 300, 400, 500
- **CTA Font**: Montserrat

### Font Sizing
- **H1**: 50px / 3.125rem
- **H2**: 36px / 2.25rem
- **Body**: 16px / 1rem
- **CTA Button**: 18px / 1.125rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/sunvolt-energy-hero-bg.jpg`
- **Alt Text**: Solar panel array on a residential rooftop with clear blue sky
- **Overlay**: none (split-screen layout with solid colour panel)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/sunvolt-energy-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/solar-panel.svg`, `assets/images/icons/battery-storage.svg`, `assets/images/icons/energy-monitor.svg`, `assets/images/icons/maintenance.svg`
- **Team Photos**: N/A
- **Gallery**: `assets/images/gallery/installation-01.jpg`, `assets/images/gallery/installation-02.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/sunvolt-energy-logo.svg`
- **Alt Text**: "SunVolt Energy Logo"
- **Max Height**: 44px

### Footer Logo
- **Source**: `assets/logos/sunvolt-energy-logo-white.svg`
- **Alt Text**: "SunVolt Energy"

### Favicon
- **Source**: `assets/logos/sunvolt-energy-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "SunVolt Energy — Powering progress with clean energy"
- **Description**: SunVolt Energy provides expert solar panel installation, battery storage, and energy management systems for homes, farms, and businesses across South Africa.
- **OG Title**: SunVolt Energy — Powering progress with clean energy
- **OG Description**: SunVolt Energy provides expert solar panel installation, battery storage, and energy management systems for homes, farms, and businesses across South Africa.
- **OG Image**: `assets/images/sunvolt-energy-og.jpg`

### Structured Data
- **Type**: LocalBusiness
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
- **Staging URL Pattern**: `https://dev.sunvolt-energy.preview.example.com`
- **S3 Prefix**: `staging/sunvolt-energy/`
