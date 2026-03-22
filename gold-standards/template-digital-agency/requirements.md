# Template Requirements: Denker Website

## Source
- **Figma File**: Denker Website
- **Figma Key**: oVr0KjvNH6e17ZjBelrPWo
- **Project**: Denker
- **Type**: Site

## Business Profile
- **Business Name**: Apex Architecture Studio
- **Industry**: Architecture & Interior Design
- **Tagline**: Spaces that inspire, structures that endure

## Brand Amendments

### Colours
- **Primary**: #2C2C2C
- **Secondary**: #6B6B6B
- **Accent**: #C8A96E
- **Background**: #FFFFFF
- **Text**: #1A1A1A

### Typography
- **Heading Font**: Cormorant Garamond
- **Body Font**: Raleway

### Logo
- **Logo Source**: `assets/logos/apex-architecture-studio-logo.svg`
- **Favicon**: `assets/logos/apex-architecture-studio-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Designing Spaces That Tell Your Story
- **Subheadline**: Award-winning architectural design for residential, commercial, and public spaces. From concept sketches to construction oversight.
- **CTA Button**: View Our Portfolio

### About Section
- **Description**: Apex Architecture Studio is a multidisciplinary design practice with a portfolio spanning luxury residences, boutique hotels, and civic buildings. Founded in 2012 by principal architect Nomsa Khumalo, we blend modernist principles with African materiality. Our projects have been featured in Architectural Digest SA and VISI Magazine.

### Contact
- **Email**: studio@apexarchitecture.co.za
- **Phone**: +27 21 422 0088
- **Address**: 78 Kloof Street, Gardens, Cape Town, 8001, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: video-background
- **Arrangement**: Cinematic architectural fly-through video with centered text overlay and scroll indicator

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: single-highlight
- **Footer Layout**: minimal-single-row

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Cormorant Garamond
- **Heading Weights**: 500, 700
- **Body Font**: Raleway
- **Body Weights**: 300, 400, 500
- **CTA Font**: Raleway

### Font Sizing
- **H1**: 60px / 3.75rem
- **H2**: 42px / 2.625rem
- **Body**: 16px / 1rem
- **CTA Button**: 14px / 0.875rem, uppercase, letter-spacing 2px

## Image Amendments

### Hero Background
- **Source**: `assets/images/apex-architecture-studio-hero-bg.jpg`
- **Alt Text**: Modern architectural facade with clean geometric lines against a clear sky
- **Overlay**: Dark gradient overlay at 55% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/apex-architecture-studio-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/blueprint.svg`, `assets/images/icons/interior-design.svg`, `assets/images/icons/construction-oversight.svg`
- **Team Photos**: `assets/images/team/principal-architect.jpg`
- **Gallery**: `assets/images/gallery/project-01.jpg`, `assets/images/gallery/project-02.jpg`, `assets/images/gallery/project-03.jpg`, `assets/images/gallery/project-04.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/apex-architecture-studio-logo.svg`
- **Alt Text**: "Apex Architecture Studio Logo"
- **Max Height**: 38px

### Footer Logo
- **Source**: `assets/logos/apex-architecture-studio-logo-white.svg`
- **Alt Text**: "Apex Architecture Studio"

### Favicon
- **Source**: `assets/logos/apex-architecture-studio-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Apex Architecture Studio — Spaces that inspire, structures that endure"
- **Description**: Apex Architecture Studio is an award-winning Cape Town design practice specialising in luxury residences, boutique hotels, and civic buildings.
- **OG Title**: Apex Architecture Studio — Spaces that inspire, structures that endure
- **OG Description**: Apex Architecture Studio is an award-winning Cape Town design practice specialising in luxury residences, boutique hotels, and civic buildings.
- **OG Image**: `assets/images/apex-architecture-studio-og.jpg`

### Structured Data
- **Type**: LocalBusiness
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
- **Staging URL Pattern**: `https://dev.apex-architecture-studio.preview.example.com`
- **S3 Prefix**: `staging/apex-architecture-studio/`
