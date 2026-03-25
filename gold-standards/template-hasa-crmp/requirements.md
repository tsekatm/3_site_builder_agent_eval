# Template Requirements: HASA CRMP - Low Fidelity Wireframes

## Source
- **Figma File**: HASA CRMP — Low Fidelity Wireframes
- **Figma Key**: VArIfUwbcqQLmlglPoVsTe
- **Project**: HASA CRMP
- **Type**: Wireframe

## Business Profile
- **Business Name**: MediTrack Connect
- **Industry**: Healthcare / Patient Management
- **Tagline**: Smarter patient journeys, better outcomes

## Brand Amendments

### Colours
- **Primary**: #0077B6
- **Secondary**: #023E73
- **Accent**: #48CAE4
- **Background**: #F0F7FB
- **Text**: #0A1628

### Typography
- **Heading Font**: IBM Plex Sans
- **Body Font**: Noto Sans

### Logo
- **Logo Source**: `assets/logos/meditrack-connect-logo.svg`
- **Favicon**: `assets/logos/meditrack-connect-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Patient Relationship Management, Reimagined
- **Subheadline**: A unified platform for managing patient records, appointment scheduling, referrals, and clinical communications across multi-site healthcare practices.
- **CTA Button**: Request a Demo

### About Section
- **Description**: MediTrack Connect is a cloud-based patient relationship management system designed for private healthcare practices, day hospitals, and specialist groups. We streamline administrative workflows so clinicians can focus on care. Compliant with POPIA and HPCSA guidelines, our platform is trusted by over 400 practices across South Africa.

### Contact
- **Email**: info@meditrackconnect.co.za
- **Phone**: +27 11 783 5500
- **Address**: 3rd Floor, MedCity Building, 15 Fredman Drive, Sandton, 2196

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Text left with dashboard UI mockup screenshot right

### Sections Layout
- **Features Section**: card-grid-3col
- **Testimonials Section**: single-highlight
- **Footer Layout**: 3-column-centered

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: IBM Plex Sans
- **Heading Weights**: 500, 700
- **Body Font**: Noto Sans
- **Body Weights**: 300, 400, 500
- **CTA Font**: IBM Plex Sans

### Font Sizing
- **H1**: 46px / 2.875rem
- **H2**: 34px / 2.125rem
- **Body**: 15px / 0.9375rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/meditrack-connect-hero-bg.jpg`
- **Alt Text**: Healthcare professional reviewing patient records on a tablet in a modern clinic
- **Overlay**: none (light solid background with UI mockup)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/meditrack-connect-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/patient-record.svg`, `assets/images/icons/appointment-calendar.svg`, `assets/images/icons/referral-network.svg`, `assets/images/icons/clinical-comms.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/meditrack-connect-logo.svg`
- **Alt Text**: "MediTrack Connect Logo"
- **Max Height**: 40px

### Footer Logo
- **Source**: `assets/logos/meditrack-connect-logo-white.svg`
- **Alt Text**: "MediTrack Connect"

### Favicon
- **Source**: `assets/logos/meditrack-connect-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "MediTrack Connect — Smarter patient journeys, better outcomes"
- **Description**: MediTrack Connect is a cloud-based patient relationship management platform for healthcare practices, offering scheduling, records, and referrals in one system.
- **OG Title**: MediTrack Connect — Smarter patient journeys, better outcomes
- **OG Description**: MediTrack Connect is a cloud-based patient relationship management platform for healthcare practices, offering scheduling, records, and referrals in one system.
- **OG Image**: `assets/images/meditrack-connect-og.jpg`

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
- **Staging URL Pattern**: `https://dev.meditrack-connect.preview.example.com`
- **S3 Prefix**: `staging/meditrack-connect/`

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
