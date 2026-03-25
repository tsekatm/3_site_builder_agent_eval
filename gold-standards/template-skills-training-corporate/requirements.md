# Template Requirements: CAPACITI Phase 1

## Source
- **Figma File**: CAPACITI Phase 1
- **Figma Key**: mS6hSPClkqlfRRWvTeTjDW
- **Project**: Capaciti
- **Type**: Site

## Business Profile
- **Business Name**: Vantage Robotics Academy
- **Industry**: Education Technology
- **Tagline**: Building the engineers of tomorrow

## Brand Amendments

### Colours
- **Primary**: #6C3CE1
- **Secondary**: #1F1B3D
- **Accent**: #FF6B35
- **Background**: #F8F7FC
- **Text**: #1D1D2C

### Typography
- **Heading Font**: Sora
- **Body Font**: DM Sans

### Logo
- **Logo Source**: `assets/logos/vantage-robotics-academy-logo.svg`
- **Favicon**: `assets/logos/vantage-robotics-academy-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Where Curiosity Meets Code
- **Subheadline**: Hands-on robotics and programming courses for learners aged 10 to 18. From beginner circuits to competition-ready autonomous systems.
- **CTA Button**: Explore Programmes

### About Section
- **Description**: Vantage Robotics Academy delivers STEM education through practical robotics workshops, coding bootcamps, and competitive league participation. Operating from campuses in Johannesburg and Durban, we have trained over 3,000 young engineers since 2018. Our curriculum aligns with international STEM standards while staying rooted in African innovation.

### Contact
- **Email**: admissions@vantagerobotics.co.za
- **Phone**: +27 31 266 4500
- **Address**: 8 Umhlanga Rocks Drive, Durban, 4319, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: asymmetric-grid
- **Arrangement**: Large headline left with robotic arm illustration right, angled divider

### Sections Layout
- **Features Section**: bento-grid
- **Testimonials Section**: grid-2col
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Sora
- **Heading Weights**: 600, 700
- **Body Font**: DM Sans
- **Body Weights**: 400, 500
- **CTA Font**: Sora

### Font Sizing
- **H1**: 56px / 3.5rem
- **H2**: 40px / 2.5rem
- **Body**: 16px / 1rem
- **CTA Button**: 18px / 1.125rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/vantage-robotics-academy-hero-bg.jpg`
- **Alt Text**: Young students assembling a robotic arm in a modern workshop
- **Overlay**: none (image sits alongside text)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/vantage-robotics-academy-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/circuit-board.svg`, `assets/images/icons/code-brackets.svg`, `assets/images/icons/robot-arm.svg`, `assets/images/icons/trophy.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/vantage-robotics-academy-logo.svg`
- **Alt Text**: "Vantage Robotics Academy Logo"
- **Max Height**: 48px

### Footer Logo
- **Source**: `assets/logos/vantage-robotics-academy-logo-white.svg`
- **Alt Text**: "Vantage Robotics Academy"

### Favicon
- **Source**: `assets/logos/vantage-robotics-academy-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Vantage Robotics Academy — Building the engineers of tomorrow"
- **Description**: Vantage Robotics Academy offers hands-on STEM education through robotics workshops and coding bootcamps for learners aged 10 to 18 in South Africa.
- **OG Title**: Vantage Robotics Academy — Building the engineers of tomorrow
- **OG Description**: Vantage Robotics Academy offers hands-on STEM education through robotics workshops and coding bootcamps for learners aged 10 to 18 in South Africa.
- **OG Image**: `assets/images/vantage-robotics-academy-og.jpg`

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
- **Staging URL Pattern**: `https://dev.vantage-robotics-academy.preview.example.com`
- **S3 Prefix**: `staging/vantage-robotics-academy/`

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
