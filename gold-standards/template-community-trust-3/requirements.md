# Template Requirements: Sibona Ilanga Trust Website

## Source
- **Figma File**: Sibona Ilanga Trust Website
- **Figma Key**: H6UTqg48VYc2UvZRYUY3Ml
- **Project**: Sibona Ilanga
- **Type**: Site

## Business Profile
- **Business Name**: Ubuntu Education Initiative
- **Industry**: Non-Profit / Education
- **Tagline**: Every child deserves a chance to learn

## Brand Amendments

### Colours
- **Primary**: #D63384
- **Secondary**: #4A0E2E
- **Accent**: #20C997
- **Background**: #FEF6FA
- **Text**: #21141D

### Typography
- **Heading Font**: Rubik
- **Body Font**: Nunito

### Logo
- **Logo Source**: `assets/logos/ubuntu-education-initiative-logo.svg`
- **Favicon**: `assets/logos/ubuntu-education-initiative-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Bridging the Education Gap, One School at a Time
- **Subheadline**: We build libraries, train teachers, and provide digital learning resources to under-resourced schools in rural South Africa.
- **CTA Button**: Donate Now

### About Section
- **Description**: Ubuntu Education Initiative is a Section 18A registered non-profit dedicated to improving educational outcomes in rural and township schools. We have equipped 120 schools with digital labs, trained 800 teachers in modern pedagogy, and established 45 community libraries. Our work reaches over 60,000 learners annually.

### Contact
- **Email**: info@ubuntueducation.org.za
- **Phone**: +27 41 373 2200
- **Address**: 12 Baakens Street, Central, Port Elizabeth, 6001, Eastern Cape

## Layout Amendments

### Hero Layout
- **Pattern**: split-screen
- **Arrangement**: Impactful headline and donate CTA left, school children photo right

### Sections Layout
- **Features Section**: card-grid-3col
- **Testimonials Section**: single-highlight
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Rubik
- **Heading Weights**: 500, 700
- **Body Font**: Nunito
- **Body Weights**: 300, 400, 600
- **CTA Font**: Rubik

### Font Sizing
- **H1**: 48px / 3rem
- **H2**: 36px / 2.25rem
- **Body**: 16px / 1rem
- **CTA Button**: 18px / 1.125rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/ubuntu-education-initiative-hero-bg.jpg`
- **Alt Text**: Children reading books in a brightly painted community library
- **Overlay**: none (split-screen with solid colour panel)

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/ubuntu-education-initiative-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/digital-lab.svg`, `assets/images/icons/teacher-training.svg`, `assets/images/icons/library.svg`, `assets/images/icons/learner-impact.svg`
- **Team Photos**: `assets/images/team/educators.jpg`
- **Gallery**: `assets/images/gallery/school-01.jpg`, `assets/images/gallery/library-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/ubuntu-education-initiative-logo.svg`
- **Alt Text**: "Ubuntu Education Initiative Logo"
- **Max Height**: 48px

### Footer Logo
- **Source**: `assets/logos/ubuntu-education-initiative-logo-white.svg`
- **Alt Text**: "Ubuntu Education Initiative"

### Favicon
- **Source**: `assets/logos/ubuntu-education-initiative-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Ubuntu Education Initiative — Every child deserves a chance to learn"
- **Description**: Ubuntu Education Initiative builds digital labs, trains teachers, and provides learning resources to under-resourced schools across rural South Africa.
- **OG Title**: Ubuntu Education Initiative — Every child deserves a chance to learn
- **OG Description**: Ubuntu Education Initiative builds digital labs, trains teachers, and provides learning resources to under-resourced schools across rural South Africa.
- **OG Image**: `assets/images/ubuntu-education-initiative-og.jpg`

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
- **Staging URL Pattern**: `https://dev.ubuntu-education-initiative.preview.example.com`
- **S3 Prefix**: `staging/ubuntu-education-initiative/`
