# Template Requirements: Blog-Capaciti - Option 2

## Source
- **Figma File**: Blog-Capaciti - Option 2
- **Figma Key**: v3grhAxg6DsWUmudC5HneW
- **Project**: Capaciti
- **Type**: Blog

## Business Profile
- **Business Name**: Meridian Legal Partners
- **Industry**: Law Firm
- **Tagline**: Strategic counsel for complex challenges

## Brand Amendments

### Colours
- **Primary**: #1E3A5F
- **Secondary**: #8B6914
- **Accent**: #C9A84C
- **Background**: #FAFAF8
- **Text**: #2C2C2C

### Typography
- **Heading Font**: Playfair Display
- **Body Font**: Source Sans Pro

### Logo
- **Logo Source**: `assets/logos/meridian-legal-partners-logo.svg`
- **Favicon**: `assets/logos/meridian-legal-partners-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Legal Perspectives That Shape Business Strategy
- **Subheadline**: Expert analysis on corporate law, regulatory compliance, and dispute resolution from our team of senior partners.
- **CTA Button**: Browse Insights

### About Section
- **Description**: Meridian Legal Partners is a full-service commercial law firm with deep expertise in corporate governance, mergers and acquisitions, and regulatory affairs. Founded in 2009, we serve mid-market and listed companies across Southern Africa. Our blog shares thought leadership on the legal trends shaping business today.

### Contact
- **Email**: enquiries@meridianlegal.co.za
- **Phone**: +27 11 403 7700
- **Address**: 22 West Street, Sandton, Johannesburg, 2196, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Text left, featured article image right

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: single-highlight
- **Footer Layout**: 3-column-centered

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Playfair Display
- **Heading Weights**: 600, 700
- **Body Font**: Source Sans Pro
- **Body Weights**: 300, 400, 600
- **CTA Font**: Source Sans Pro

### Font Sizing
- **H1**: 52px / 3.25rem
- **H2**: 38px / 2.375rem
- **Body**: 17px / 1.0625rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/meridian-legal-partners-hero-bg.jpg`
- **Alt Text**: Elegant law library with leather-bound legal volumes and warm lighting
- **Overlay**: Dark gradient overlay at 50% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/meridian-legal-partners-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/corporate-law.svg`, `assets/images/icons/compliance.svg`, `assets/images/icons/dispute-resolution.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/meridian-legal-partners-logo.svg`
- **Alt Text**: "Meridian Legal Partners Logo"
- **Max Height**: 46px

### Footer Logo
- **Source**: `assets/logos/meridian-legal-partners-logo-white.svg`
- **Alt Text**: "Meridian Legal Partners"

### Favicon
- **Source**: `assets/logos/meridian-legal-partners-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Meridian Legal Partners — Strategic counsel for complex challenges"
- **Description**: Meridian Legal Partners is a full-service commercial law firm offering corporate governance, M&A, and regulatory advisory across Southern Africa.
- **OG Title**: Meridian Legal Partners — Strategic counsel for complex challenges
- **OG Description**: Meridian Legal Partners is a full-service commercial law firm offering corporate governance, M&A, and regulatory advisory across Southern Africa.
- **OG Image**: `assets/images/meridian-legal-partners-og.jpg`

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
- **Staging URL Pattern**: `https://dev.meridian-legal-partners.preview.example.com`
- **S3 Prefix**: `staging/meridian-legal-partners/`

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
