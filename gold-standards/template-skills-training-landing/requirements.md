# Template Requirements: CAPACITI Phase 2

## Source
- **Figma File**: CAPACITI Phase 2
- **Figma Key**: YCkggAfrxrn1EATvGFWSfj
- **Project**: Capaciti
- **Type**: Site

## Business Profile
- **Business Name**: Solaris Wealth Advisors
- **Industry**: Financial Planning
- **Tagline**: Clarity in every financial decision

## Brand Amendments

### Colours
- **Primary**: #0A5C5A
- **Secondary**: #1A1A2E
- **Accent**: #D4A843
- **Background**: #F4F7F6
- **Text**: #222233

### Typography
- **Heading Font**: Libre Baskerville
- **Body Font**: Nunito Sans

### Logo
- **Logo Source**: `assets/logos/solaris-wealth-advisors-logo.svg`
- **Favicon**: `assets/logos/solaris-wealth-advisors-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Your Wealth, Strategically Managed
- **Subheadline**: Personalised financial planning and investment management for individuals, families, and business owners across Africa.
- **CTA Button**: Book a Consultation

### About Section
- **Description**: Solaris Wealth Advisors is an independent financial advisory firm offering holistic wealth management, retirement planning, and estate structuring. With R2.4 billion in assets under advice, our certified financial planners deliver fiduciary-first guidance. We operate from offices in Pretoria, Cape Town, and Windhoek.

### Contact
- **Email**: advisory@solariswealthadvisors.co.za
- **Phone**: +27 12 348 9100
- **Address**: 120 Dyer Street, Hillcrest Office Park, Pretoria, 0083, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: centered-minimal
- **Arrangement**: Centered headline and subheadline with subtle background pattern, CTA below

### Sections Layout
- **Features Section**: icon-list
- **Testimonials Section**: single-highlight
- **Footer Layout**: 3-column-centered

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Libre Baskerville
- **Heading Weights**: 400, 700
- **Body Font**: Nunito Sans
- **Body Weights**: 300, 400, 600
- **CTA Font**: Nunito Sans

### Font Sizing
- **H1**: 44px / 2.75rem
- **H2**: 34px / 2.125rem
- **Body**: 16px / 1rem
- **CTA Button**: 17px / 1.0625rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/solaris-wealth-advisors-hero-bg.jpg`
- **Alt Text**: Modern office with panoramic city skyline view at golden hour
- **Overlay**: Light gradient overlay at 30% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/solaris-wealth-advisors-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/wealth-growth.svg`, `assets/images/icons/retirement-plan.svg`, `assets/images/icons/estate-shield.svg`, `assets/images/icons/tax-advisory.svg`
- **Team Photos**: `assets/images/team/advisory-team.jpg`
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/solaris-wealth-advisors-logo.svg`
- **Alt Text**: "Solaris Wealth Advisors Logo"
- **Max Height**: 42px

### Footer Logo
- **Source**: `assets/logos/solaris-wealth-advisors-logo-white.svg`
- **Alt Text**: "Solaris Wealth Advisors"

### Favicon
- **Source**: `assets/logos/solaris-wealth-advisors-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Solaris Wealth Advisors — Clarity in every financial decision"
- **Description**: Solaris Wealth Advisors provides personalised financial planning, investment management, and estate structuring for individuals and families across Africa.
- **OG Title**: Solaris Wealth Advisors — Clarity in every financial decision
- **OG Description**: Solaris Wealth Advisors provides personalised financial planning, investment management, and estate structuring for individuals and families across Africa.
- **OG Image**: `assets/images/solaris-wealth-advisors-og.jpg`

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
- **Staging URL Pattern**: `https://dev.solaris-wealth-advisors.preview.example.com`
- **S3 Prefix**: `staging/solaris-wealth-advisors/`

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
