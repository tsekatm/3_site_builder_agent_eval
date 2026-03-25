# Template Requirements: Fuse Factory

## Source
- **Figma File**: Fuse Factory
- **Figma Key**: 0Yo1PO6Zyuc2cdmqjSuTYc
- **Project**: Fuse Factory
- **Type**: Site

## Business Profile
- **Business Name**: Pixel & Grain Creative
- **Industry**: Creative Agency / Branding
- **Tagline**: Ideas that move people

## Brand Amendments

### Colours
- **Primary**: #FF3366
- **Secondary**: #1A0033
- **Accent**: #FFD166
- **Background**: #FFFBF5
- **Text**: #1A1A2E

### Typography
- **Heading Font**: Clash Display
- **Body Font**: General Sans

### Logo
- **Logo Source**: `assets/logos/pixel-and-grain-creative-logo.svg`
- **Favicon**: `assets/logos/pixel-and-grain-creative-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: We Build Brands That People Remember
- **Subheadline**: Full-service creative agency specialising in brand identity, digital campaigns, and motion design. From strategy to execution, we make brands unforgettable.
- **CTA Button**: See Our Work

### About Section
- **Description**: Pixel & Grain Creative is a Johannesburg-based branding and design agency working with startups, corporates, and cultural organisations. We believe great design is a business advantage. Our services span visual identity, packaging, digital marketing, and video production, delivered by a diverse team of strategists, designers, and storytellers.

### Contact
- **Email**: hello@pixelandgrain.co.za
- **Phone**: +27 11 447 2900
- **Address**: 44 Stanley Avenue, Milpark, Johannesburg, 2092, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: asymmetric-grid
- **Arrangement**: Oversized headline left with colourful portfolio mosaic collage right

### Sections Layout
- **Features Section**: bento-grid
- **Testimonials Section**: carousel
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Clash Display
- **Heading Weights**: 600, 700
- **Body Font**: General Sans
- **Body Weights**: 300, 400, 500
- **CTA Font**: Clash Display

### Font Sizing
- **H1**: 64px / 4rem
- **H2**: 44px / 2.75rem
- **Body**: 17px / 1.0625rem
- **CTA Button**: 16px / 1rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/pixel-and-grain-creative-hero-bg.jpg`
- **Alt Text**: Vibrant collage of brand identity projects and packaging designs
- **Overlay**: none (solid gradient background)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/pixel-and-grain-creative-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/brand-identity.svg`, `assets/images/icons/digital-campaign.svg`, `assets/images/icons/motion-design.svg`, `assets/images/icons/packaging.svg`
- **Team Photos**: `assets/images/team/creative-team.jpg`
- **Gallery**: `assets/images/gallery/project-branding-01.jpg`, `assets/images/gallery/project-digital-01.jpg`, `assets/images/gallery/project-motion-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/pixel-and-grain-creative-logo.svg`
- **Alt Text**: "Pixel & Grain Creative Logo"
- **Max Height**: 42px

### Footer Logo
- **Source**: `assets/logos/pixel-and-grain-creative-logo-white.svg`
- **Alt Text**: "Pixel & Grain Creative"

### Favicon
- **Source**: `assets/logos/pixel-and-grain-creative-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Pixel & Grain Creative — Ideas that move people"
- **Description**: Pixel & Grain Creative is a Johannesburg branding and design agency specialising in visual identity, digital campaigns, motion design, and packaging.
- **OG Title**: Pixel & Grain Creative — Ideas that move people
- **OG Description**: Pixel & Grain Creative is a Johannesburg branding and design agency specialising in visual identity, digital campaigns, motion design, and packaging.
- **OG Image**: `assets/images/pixel-and-grain-creative-og.jpg`

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
- **Staging URL Pattern**: `https://dev.pixel-and-grain-creative.preview.example.com`
- **S3 Prefix**: `staging/pixel-and-grain-creative/`

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
