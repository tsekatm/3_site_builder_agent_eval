# Template Requirements: HASA - NHI

## Source
- **Figma File**: HASA - NHI
- **Figma Key**: L6L024r4UcygQifA3fppG0
- **Project**: Hasa Main
- **Type**: Page

## Business Profile
- **Business Name**: ClearPath Insurance Brokers
- **Industry**: Insurance / Financial Services
- **Tagline**: Protection made personal

## Brand Amendments

### Colours
- **Primary**: #0D6EFD
- **Secondary**: #0A3D91
- **Accent**: #198754
- **Background**: #F4F8FD
- **Text**: #0F172A

### Typography
- **Heading Font**: Urbanist
- **Body Font**: Assistant

### Logo
- **Logo Source**: `assets/logos/clearpath-insurance-brokers-logo.svg`
- **Favicon**: `assets/logos/clearpath-insurance-brokers-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Understanding Your Health Insurance Options
- **Subheadline**: Independent guidance on medical aid, gap cover, and health insurance products. We help individuals and businesses find the right cover at the right price.
- **CTA Button**: Get Expert Advice

### About Section
- **Description**: ClearPath Insurance Brokers is an independent insurance advisory firm specialising in health, life, and business insurance. We represent over 30 insurers and medical schemes, giving our clients unbiased comparisons and tailored recommendations. Our team of 25 qualified brokers serves clients across all nine provinces.

### Contact
- **Email**: advice@clearpathbrokers.co.za
- **Phone**: +27 11 325 6600
- **Address**: 2nd Floor, Illovo Edge, 6 Rivonia Road, Illovo, Johannesburg, 2196

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Reassuring headline and advice CTA left, family healthcare photo right

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: grid-2col
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Urbanist
- **Heading Weights**: 500, 700
- **Body Font**: Assistant
- **Body Weights**: 300, 400, 600
- **CTA Font**: Urbanist

### Font Sizing
- **H1**: 46px / 2.875rem
- **H2**: 34px / 2.125rem
- **Body**: 16px / 1rem
- **CTA Button**: 17px / 1.0625rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/clearpath-insurance-brokers-hero-bg.jpg`
- **Alt Text**: Family smiling during a consultation with an insurance advisor in a bright office
- **Overlay**: none (split-screen with solid blue panel)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/clearpath-insurance-brokers-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/medical-aid.svg`, `assets/images/icons/gap-cover.svg`, `assets/images/icons/life-insurance.svg`, `assets/images/icons/business-cover.svg`
- **Team Photos**: `assets/images/team/broker-team.jpg`
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/clearpath-insurance-brokers-logo.svg`
- **Alt Text**: "ClearPath Insurance Brokers Logo"
- **Max Height**: 42px

### Footer Logo
- **Source**: `assets/logos/clearpath-insurance-brokers-logo-white.svg`
- **Alt Text**: "ClearPath Insurance Brokers"

### Favicon
- **Source**: `assets/logos/clearpath-insurance-brokers-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "ClearPath Insurance Brokers — Protection made personal"
- **Description**: ClearPath Insurance Brokers provides independent health, life, and business insurance advice with unbiased comparisons across 30+ insurers and medical schemes.
- **OG Title**: ClearPath Insurance Brokers — Protection made personal
- **OG Description**: ClearPath Insurance Brokers provides independent health, life, and business insurance advice with unbiased comparisons across 30+ insurers and medical schemes.
- **OG Image**: `assets/images/clearpath-insurance-brokers-og.jpg`

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
- **Staging URL Pattern**: `https://dev.clearpath-insurance-brokers.preview.example.com`
- **S3 Prefix**: `staging/clearpath-insurance-brokers/`

## Interactivity Requirements

### Mobile Menu
- **Hamburger toggle**: Visible below 768px, toggles nav with aria-expanded
- **Animation**: Smooth slide or fade transition

### Scroll Behavior
- **Smooth scroll**: All anchor links scroll smoothly to target
- **Scroll indicator**: "Scroll to explore" or down-arrow on hero (optional)

### Hover States
- **Buttons**: Scale up slightly (transform: scale(1.02)) with shadow on hover
- **Cards**: Lift effect (translateY(-4px)) with shadow transition
- **Links**: Colour change or underline on hover
- **Nav items**: Subtle colour/opacity change

### Card Interactions
- **Feature cards**: Hover lift effect with shadow
- **Testimonial cards**: Subtle border or shadow change on hover
- **Gallery items**: Overlay with zoom icon on hover (if gallery present)

### Animations
- **Hero**: Parallax scroll on background image (respect prefers-reduced-motion)
- **Sections**: Fade-in on scroll (IntersectionObserver)
- **prefers-reduced-motion**: Disable all animations when user prefers reduced motion
