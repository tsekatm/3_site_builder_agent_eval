# Template Requirements: Blank Site

## Source
- **Figma File**: SoSimple
- **Figma Key**: 7mL5yd7JmNs3UFqUgxqlmI
- **Project**: SoSimple
- **Type**: General / Blank

## Business Profile
- **Business Name**: CloudNest Digital
- **Industry**: Cloud Hosting / SaaS
- **Tagline**: Simple cloud infrastructure for modern teams

## Brand Amendments

### Colours
- **Primary**: #6366F1
- **Secondary**: #312E81
- **Accent**: #A5B4FC
- **Background**: #F8F9FE
- **Text**: #1E1B4B

### Typography
- **Heading Font**: Plus Jakarta Sans
- **Body Font**: Inter

### Logo
- **Logo Source**: `assets/logos/cloudnest-digital-logo.svg`
- **Favicon**: `assets/logos/cloudnest-digital-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Deploy, Scale, Relax.
- **Subheadline**: CloudNest gives your team simple, reliable cloud hosting with zero DevOps headaches. From startup to enterprise, we scale with you.
- **CTA Button**: Start Free Trial

### About Section
- **Description**: CloudNest Digital provides managed cloud infrastructure for development teams. We handle the servers, networking, and scaling so you can focus on shipping code. Trusted by 2,000+ teams across Africa and Europe.

### Contact
- **Email**: hello@cloudnest.digital
- **Phone**: +27 11 450 7890
- **Address**: 44 Rivonia Road, Sandton, 2196, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: centered-minimal
- **Arrangement**: Centered headline and subheadline with gradient background, no hero image

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
- **Heading Font**: Plus Jakarta Sans
- **Heading Weights**: 600, 700
- **Body Font**: Inter
- **Body Weights**: 300, 400, 500
- **CTA Font**: Inter

### Font Sizing
- **H1**: 48px / 3rem
- **H2**: 36px / 2.25rem
- **Body**: 16px / 1rem
- **CTA Button**: 16px / 1rem, semibold

## Image Amendments

### Hero Background
- **Source**: none (gradient background only)
- **Alt Text**: N/A
- **Overlay**: N/A

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/cloudnest-digital-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/deploy.svg`, `assets/images/icons/scale.svg`, `assets/images/icons/monitor.svg`
- **Team Photos**: N/A
- **Gallery**: N/A

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/cloudnest-digital-logo.svg`
- **Alt Text**: "CloudNest Digital Logo"
- **Max Height**: 40px

### Footer Logo
- **Source**: `assets/logos/cloudnest-digital-logo-white.svg`
- **Alt Text**: "CloudNest Digital"

### Favicon
- **Source**: `assets/logos/cloudnest-digital-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "CloudNest Digital — Simple cloud infrastructure for modern teams"
- **Description**: CloudNest Digital provides managed cloud hosting for development teams. Zero DevOps headaches, auto-scaling, trusted by 2,000+ teams across Africa and Europe.
- **OG Title**: CloudNest Digital — Simple cloud infrastructure for modern teams
- **OG Description**: CloudNest Digital provides managed cloud hosting for development teams. Zero DevOps headaches, auto-scaling, trusted by 2,000+ teams across Africa and Europe.
- **OG Image**: `assets/images/cloudnest-digital-og.jpg`

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
- **Staging URL Pattern**: `https://dev.cloudnest-digital.preview.example.com`
- **S3 Prefix**: `staging/cloudnest-digital/`
