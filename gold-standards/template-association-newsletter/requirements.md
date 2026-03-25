# Template Requirements: Conference Newsletter

## Source
- **Figma File**: Conference Newsletter
- **Figma Key**: 26xc9wtLruW2LVMYnPOzmv
- **Project**: Hasa Main
- **Type**: Newsletter

## Business Profile
- **Business Name**: AfriAgri Summit
- **Industry**: Agriculture / Conference
- **Tagline**: Cultivating innovation in African agriculture

## Brand Amendments

### Colours
- **Primary**: #2E7D32
- **Secondary**: #1B4D1F
- **Accent**: #FF9800
- **Background**: #F9FBF2
- **Text**: #1A2B1D

### Typography
- **Heading Font**: Archivo
- **Body Font**: Source Serif Pro

### Logo
- **Logo Source**: `assets/logos/afriagri-summit-logo.svg`
- **Favicon**: `assets/logos/afriagri-summit-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: AfriAgri Summit 2026 Newsletter
- **Subheadline**: Your monthly update on speakers, sponsors, and programme highlights for Africa's largest agricultural innovation conference.
- **CTA Button**: Register Now

### About Section
- **Description**: The AfriAgri Summit brings together farmers, agri-tech startups, policymakers, and researchers to address food security challenges across the continent. Now in its 8th year, the summit features keynotes, field demonstrations, and a startup pitch competition. Join 2,500 delegates in Nairobi this September.

### Contact
- **Email**: newsletter@afriagrisummit.com
- **Phone**: +254 20 555 3300
- **Address**: Kenyatta International Convention Centre, Nairobi, Kenya

## Layout Amendments

### Hero Layout
- **Pattern**: full-width-overlay
- **Arrangement**: Agricultural field photography with centered newsletter title and registration CTA

### Sections Layout
- **Features Section**: timeline
- **Testimonials Section**: single-highlight
- **Footer Layout**: minimal-single-row

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Archivo
- **Heading Weights**: 500, 700
- **Body Font**: Source Serif Pro
- **Body Weights**: 400, 600
- **CTA Font**: Archivo

### Font Sizing
- **H1**: 44px / 2.75rem
- **H2**: 30px / 1.875rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/afriagri-summit-hero-bg.jpg`
- **Alt Text**: Expansive green agricultural field with drone technology monitoring crops
- **Overlay**: Dark gradient overlay at 50% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/afriagri-summit-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/speaker-podium.svg`, `assets/images/icons/field-demo.svg`, `assets/images/icons/startup-pitch.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/afriagri-summit-logo.svg`
- **Alt Text**: "AfriAgri Summit Logo"
- **Max Height**: 44px

### Footer Logo
- **Source**: `assets/logos/afriagri-summit-logo-white.svg`
- **Alt Text**: "AfriAgri Summit"

### Favicon
- **Source**: `assets/logos/afriagri-summit-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "AfriAgri Summit — Cultivating innovation in African agriculture"
- **Description**: Stay updated on the AfriAgri Summit 2026 with speaker announcements, programme highlights, and registration details for Africa's largest agri-innovation conference.
- **OG Title**: AfriAgri Summit — Cultivating innovation in African agriculture
- **OG Description**: Stay updated on the AfriAgri Summit 2026 with speaker announcements, programme highlights, and registration details for Africa's largest agri-innovation conference.
- **OG Image**: `assets/images/afriagri-summit-og.jpg`

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
- **Staging URL Pattern**: `https://dev.afriagri-summit.preview.example.com`
- **S3 Prefix**: `staging/afriagri-summit/`

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
