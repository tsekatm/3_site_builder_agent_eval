# Template Requirements: Etali Safari Website

## Source
- **Figma File**: Etali Safari Website
- **Figma Key**: mhMK6el5GzzYOJASq0wXZu
- **Project**: Etali Safari
- **Type**: Site

## Business Profile
- **Business Name**: Karoo Starlight Lodge
- **Industry**: Eco-Tourism / Lodge
- **Tagline**: Under African skies, find yourself again

## Brand Amendments

### Colours
- **Primary**: #8B5E3C
- **Secondary**: #3D2B1F
- **Accent**: #E6C87A
- **Background**: #FAF6F1
- **Text**: #2B2218

### Typography
- **Heading Font**: Bodoni Moda
- **Body Font**: Karla

### Logo
- **Logo Source**: `assets/logos/karoo-starlight-lodge-logo.svg`
- **Favicon**: `assets/logos/karoo-starlight-lodge-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: A Sanctuary in the Heart of the Karoo
- **Subheadline**: Luxury eco-lodge offering stargazing experiences, guided nature walks, and farm-to-table dining in the Great Karoo, South Africa.
- **CTA Button**: Plan Your Stay

### About Section
- **Description**: Karoo Starlight Lodge is a 12-suite eco-lodge set on a 5,000-hectare private conservancy near Graaff-Reinet. We are a certified Dark Sky accommodation, offering world-class stargazing alongside hiking, mountain biking, and wildlife encounters. Our lodge runs entirely on solar energy and harvested rainwater.

### Contact
- **Email**: reservations@karoostarlight.co.za
- **Phone**: +27 49 891 0055
- **Address**: Farm Doornhoek, Graaff-Reinet, 6280, Eastern Cape, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: video-background
- **Arrangement**: Slow-pan aerial video of Karoo landscape at dusk with centered text and scroll indicator

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
- **Heading Font**: Bodoni Moda
- **Heading Weights**: 400, 700
- **Body Font**: Karla
- **Body Weights**: 300, 400, 500
- **CTA Font**: Karla

### Font Sizing
- **H1**: 56px / 3.5rem
- **H2**: 40px / 2.5rem
- **Body**: 16px / 1rem
- **CTA Button**: 15px / 0.9375rem, uppercase, letter-spacing 1.5px

## Image Amendments

### Hero Background
- **Source**: `assets/images/karoo-starlight-lodge-hero-bg.jpg`
- **Alt Text**: Star-filled night sky over the Karoo landscape with lodge silhouette
- **Overlay**: Dark gradient overlay at 50% opacity

### Section Backgrounds
- **About Section**: `assets/images/karoo-starlight-lodge-about-bg.jpg`
- **Features Section**: none
- **CTA Section**: `assets/images/karoo-starlight-lodge-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/stargazing.svg`, `assets/images/icons/hiking-trail.svg`, `assets/images/icons/farm-dining.svg`, `assets/images/icons/solar-energy.svg`
- **Team Photos**: N/A
- **Gallery**: `assets/images/gallery/suite-01.jpg`, `assets/images/gallery/landscape-01.jpg`, `assets/images/gallery/dining-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/karoo-starlight-lodge-logo.svg`
- **Alt Text**: "Karoo Starlight Lodge Logo"
- **Max Height**: 52px

### Footer Logo
- **Source**: `assets/logos/karoo-starlight-lodge-logo-white.svg`
- **Alt Text**: "Karoo Starlight Lodge"

### Favicon
- **Source**: `assets/logos/karoo-starlight-lodge-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Karoo Starlight Lodge — Under African skies, find yourself again"
- **Description**: Karoo Starlight Lodge is a luxury eco-lodge in the Great Karoo offering world-class stargazing, guided nature walks, and farm-to-table dining on solar power.
- **OG Title**: Karoo Starlight Lodge — Under African skies, find yourself again
- **OG Description**: Karoo Starlight Lodge is a luxury eco-lodge in the Great Karoo offering world-class stargazing, guided nature walks, and farm-to-table dining on solar power.
- **OG Image**: `assets/images/karoo-starlight-lodge-og.jpg`

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
- **Staging URL Pattern**: `https://dev.karoo-starlight-lodge.preview.example.com`
- **S3 Prefix**: `staging/karoo-starlight-lodge/`
