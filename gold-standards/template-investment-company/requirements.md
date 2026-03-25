# Template Requirements: Metis

## Source
- **Figma File**: Metis
- **Figma Key**: kFAqZfGpRIwFyFLAKk2GoJ
- **Project**: Metis
- **Type**: Site

## Business Profile
- **Business Name**: Quantum Consulting Group
- **Industry**: Management Consulting
- **Tagline**: Transforming complexity into competitive advantage

## Brand Amendments

### Colours
- **Primary**: #5B2C8E
- **Secondary**: #2A1052
- **Accent**: #00E5A0
- **Background**: #FAF8FD
- **Text**: #1C1528

### Typography
- **Heading Font**: Satoshi
- **Body Font**: Cabinet Grotesk

### Logo
- **Logo Source**: `assets/logos/quantum-consulting-group-logo.svg`
- **Favicon**: `assets/logos/quantum-consulting-group-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Strategy. Operations. Growth.
- **Subheadline**: We partner with executive teams to solve their most pressing business challenges. From digital transformation to market entry, we deliver results that matter.
- **CTA Button**: Talk to a Partner

### About Section
- **Description**: Quantum Consulting Group is a boutique management consultancy advising blue-chip companies, state-owned enterprises, and high-growth startups across Africa. Our practice areas include corporate strategy, operational excellence, and organisational design. With offices in Johannesburg and Nairobi, we bring both local depth and pan-African reach.

### Contact
- **Email**: engage@quantumconsulting.co.za
- **Phone**: +27 11 506 7700
- **Address**: The Campus, 57 Sloane Street, Bryanston, Johannesburg, 2021

## Layout Amendments

### Hero Layout
- **Pattern**: full-width-overlay
- **Arrangement**: Abstract geometric background with centered bold headline and partner CTA

### Sections Layout
- **Features Section**: bento-grid
- **Testimonials Section**: grid-2col
- **Footer Layout**: 3-column-centered

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Satoshi
- **Heading Weights**: 500, 700
- **Body Font**: Cabinet Grotesk
- **Body Weights**: 400, 500
- **CTA Font**: Satoshi

### Font Sizing
- **H1**: 52px / 3.25rem
- **H2**: 38px / 2.375rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/quantum-consulting-group-hero-bg.jpg`
- **Alt Text**: Executive boardroom with city skyline visible through floor-to-ceiling windows
- **Overlay**: Dark gradient overlay at 70% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/quantum-consulting-group-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/strategy.svg`, `assets/images/icons/operations.svg`, `assets/images/icons/digital-transform.svg`, `assets/images/icons/org-design.svg`
- **Team Photos**: `assets/images/team/partners.jpg`
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/quantum-consulting-group-logo.svg`
- **Alt Text**: "Quantum Consulting Group Logo"
- **Max Height**: 40px

### Footer Logo
- **Source**: `assets/logos/quantum-consulting-group-logo-white.svg`
- **Alt Text**: "Quantum Consulting Group"

### Favicon
- **Source**: `assets/logos/quantum-consulting-group-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Quantum Consulting Group — Transforming complexity into competitive advantage"
- **Description**: Quantum Consulting Group is a boutique management consultancy advising blue-chip companies and high-growth startups on strategy, operations, and digital transformation across Africa.
- **OG Title**: Quantum Consulting Group — Transforming complexity into competitive advantage
- **OG Description**: Quantum Consulting Group is a boutique management consultancy advising blue-chip companies and high-growth startups on strategy, operations, and digital transformation across Africa.
- **OG Image**: `assets/images/quantum-consulting-group-og.jpg`

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
- **Staging URL Pattern**: `https://dev.quantum-consulting-group.preview.example.com`
- **S3 Prefix**: `staging/quantum-consulting-group/`

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
