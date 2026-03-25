# Template Requirements: Gala Page

## Source
- **Figma File**: Gala Page
- **Figma Key**: odkLDVy7HFYAs09dLc47JT
- **Project**: Hasa Main
- **Type**: Event Page

## Business Profile
- **Business Name**: Masiyavana Heritage Gala
- **Industry**: Arts & Culture / Fundraising Event
- **Tagline**: Celebrating heritage, funding futures

## Brand Amendments

### Colours
- **Primary**: #9B1B30
- **Secondary**: #2D0A10
- **Accent**: #D4AF37
- **Background**: #FDF5F7
- **Text**: #1A0A0F

### Typography
- **Heading Font**: Playfair Display
- **Body Font**: Crimson Pro

### Logo
- **Logo Source**: `assets/logos/masiyavana-heritage-gala-logo.svg`
- **Favicon**: `assets/logos/masiyavana-heritage-gala-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: The 5th Annual Masiyavana Heritage Gala
- **Subheadline**: An evening of music, art, and culture to raise funds for heritage preservation and arts education in South Africa. 14 November 2026, The Venue, Melrose Arch.
- **CTA Button**: Purchase Tickets

### About Section
- **Description**: The Masiyavana Heritage Gala is an annual black-tie fundraising event celebrating South African arts, music, and cultural heritage. Proceeds fund arts education bursaries and the restoration of heritage sites. Past galas have featured performances by leading South African artists and raised over R12 million for cultural programmes.

### Contact
- **Email**: gala@masiyavanafoundation.org.za
- **Phone**: +27 11 684 1900
- **Address**: The Venue, Melrose Arch, Johannesburg, 2196, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: video-background
- **Arrangement**: Slow-motion gala highlights reel with elegant centered headline and ticket CTA

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
- **Heading Font**: Playfair Display
- **Heading Weights**: 600, 800
- **Body Font**: Crimson Pro
- **Body Weights**: 300, 400, 600
- **CTA Font**: Crimson Pro

### Font Sizing
- **H1**: 56px / 3.5rem
- **H2**: 40px / 2.5rem
- **Body**: 17px / 1.0625rem
- **CTA Button**: 18px / 1.125rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/masiyavana-heritage-gala-hero-bg.jpg`
- **Alt Text**: Elegantly decorated gala ballroom with warm gold lighting and cultural art installations
- **Overlay**: Dark gradient overlay at 60% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/masiyavana-heritage-gala-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/music-note.svg`, `assets/images/icons/art-palette.svg`, `assets/images/icons/heritage-site.svg`
- **Team Photos**: N/A
- **Gallery**: `assets/images/gallery/gala-2025-01.jpg`, `assets/images/gallery/gala-2025-02.jpg`, `assets/images/gallery/gala-2025-03.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/masiyavana-heritage-gala-logo.svg`
- **Alt Text**: "Masiyavana Heritage Gala Logo"
- **Max Height**: 52px

### Footer Logo
- **Source**: `assets/logos/masiyavana-heritage-gala-logo-white.svg`
- **Alt Text**: "Masiyavana Heritage Gala"

### Favicon
- **Source**: `assets/logos/masiyavana-heritage-gala-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Masiyavana Heritage Gala — Celebrating heritage, funding futures"
- **Description**: Join the 5th Annual Masiyavana Heritage Gala on 14 November 2026 at Melrose Arch for an evening of music, art, and culture supporting heritage preservation.
- **OG Title**: Masiyavana Heritage Gala — Celebrating heritage, funding futures
- **OG Description**: Join the 5th Annual Masiyavana Heritage Gala on 14 November 2026 at Melrose Arch for an evening of music, art, and culture supporting heritage preservation.
- **OG Image**: `assets/images/masiyavana-heritage-gala-og.jpg`

### Structured Data
- **Type**: Event
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
- **Staging URL Pattern**: `https://dev.masiyavana-heritage-gala.preview.example.com`
- **S3 Prefix**: `staging/masiyavana-heritage-gala/`

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
