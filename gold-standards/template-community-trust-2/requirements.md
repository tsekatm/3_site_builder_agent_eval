# Template Requirements: Letsatsi Borutho Trust

## Source
- **Figma File**: Letsatsi Borutho Trust
- **Figma Key**: IJmiT1qtA0d7ET0R0VR5df
- **Project**: Sibona Ilanga
- **Type**: Site

## Business Profile
- **Business Name**: Khula Community Trust
- **Industry**: Non-Profit / Community Development
- **Tagline**: Growing communities from the ground up

## Brand Amendments

### Colours
- **Primary**: #4CAF50
- **Secondary**: #1B5E20
- **Accent**: #FFC107
- **Background**: #F5F9F5
- **Text**: #1A2B1A

### Typography
- **Heading Font**: Quicksand
- **Body Font**: Mulish

### Logo
- **Logo Source**: `assets/logos/khula-community-trust-logo.svg`
- **Favicon**: `assets/logos/khula-community-trust-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Sustainable Development Starts with People
- **Subheadline**: We partner with rural communities to build food gardens, early childhood centres, and skills training programmes that create lasting change.
- **CTA Button**: Get Involved

### About Section
- **Description**: Khula Community Trust is a development-focused NPO working in Limpopo, Mpumalanga, and the Eastern Cape. Our programmes address food security, early childhood development, and adult literacy. We work hand-in-hand with traditional leaders and local government to ensure our interventions are community-owned and sustainable.

### Contact
- **Email**: info@khulacommunity.org.za
- **Phone**: +27 15 297 4400
- **Address**: 88 Biccard Street, Polokwane, 0700, Limpopo, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: parallax-scroll
- **Arrangement**: Community garden photography with parallax depth, text overlay left-aligned

### Sections Layout
- **Features Section**: icon-list
- **Testimonials Section**: masonry
- **Footer Layout**: 3-column-centered

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Quicksand
- **Heading Weights**: 500, 700
- **Body Font**: Mulish
- **Body Weights**: 300, 400, 600
- **CTA Font**: Quicksand

### Font Sizing
- **H1**: 46px / 2.875rem
- **H2**: 32px / 2rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/khula-community-trust-hero-bg.jpg`
- **Alt Text**: Community members tending a vegetable garden with children watching
- **Overlay**: Dark gradient overlay at 40% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/khula-community-trust-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/food-garden.svg`, `assets/images/icons/early-childhood.svg`, `assets/images/icons/skills-training.svg`, `assets/images/icons/literacy.svg`
- **Team Photos**: `assets/images/team/field-workers.jpg`
- **Gallery**: `assets/images/gallery/garden-01.jpg`, `assets/images/gallery/classroom-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/khula-community-trust-logo.svg`
- **Alt Text**: "Khula Community Trust Logo"
- **Max Height**: 46px

### Footer Logo
- **Source**: `assets/logos/khula-community-trust-logo-white.svg`
- **Alt Text**: "Khula Community Trust"

### Favicon
- **Source**: `assets/logos/khula-community-trust-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Khula Community Trust — Growing communities from the ground up"
- **Description**: Khula Community Trust partners with rural communities in Limpopo, Mpumalanga, and Eastern Cape to build food gardens, ECD centres, and skills training programmes.
- **OG Title**: Khula Community Trust — Growing communities from the ground up
- **OG Description**: Khula Community Trust partners with rural communities in Limpopo, Mpumalanga, and Eastern Cape to build food gardens, ECD centres, and skills training programmes.
- **OG Image**: `assets/images/khula-community-trust-og.jpg`

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
- **Staging URL Pattern**: `https://dev.khula-community-trust.preview.example.com`
- **S3 Prefix**: `staging/khula-community-trust/`

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
