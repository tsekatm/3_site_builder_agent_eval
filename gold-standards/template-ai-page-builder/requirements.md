# Template Requirements: Chirrup

## Source
- **Figma File**: Chirrup
- **Figma Key**: W6Ngo1qUBpo5tkNlcD87fR
- **Project**: Chirrup
- **Type**: Site

## Business Profile
- **Business Name**: Nourish Kitchen Collective
- **Industry**: Restaurant / Food & Beverage
- **Tagline**: Farm-fresh flavours, crafted with care

## Brand Amendments

### Colours
- **Primary**: #B85C38
- **Secondary**: #5C3D2E
- **Accent**: #E8D5B7
- **Background**: #FDF8F3
- **Text**: #2D2A26

### Typography
- **Heading Font**: Fraunces
- **Body Font**: Lato

### Logo
- **Logo Source**: `assets/logos/nourish-kitchen-collective-logo.svg`
- **Favicon**: `assets/logos/nourish-kitchen-collective-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Seasonal Menus. Local Ingredients. Unforgettable Meals.
- **Subheadline**: A modern bistro celebrating South African produce through globally inspired dishes. Dine in, take away, or book us for your next event.
- **CTA Button**: View Our Menu

### About Section
- **Description**: Nourish Kitchen Collective is a farm-to-table restaurant group with locations in Stellenbosch and Franschhoek. We partner directly with smallholder farmers to source seasonal, organic ingredients. Our menus change monthly, reflecting what the land offers and what our chefs dream up.

### Contact
- **Email**: reservations@nourishkitchen.co.za
- **Phone**: +27 21 880 1234
- **Address**: 14 Church Street, Stellenbosch, 7600, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: parallax-scroll
- **Arrangement**: Full-bleed food photography background with centered text overlay and scroll-triggered parallax

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: masonry
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Fraunces
- **Heading Weights**: 600, 800
- **Body Font**: Lato
- **Body Weights**: 300, 400, 700
- **CTA Font**: Lato

### Font Sizing
- **H1**: 54px / 3.375rem
- **H2**: 38px / 2.375rem
- **Body**: 16px / 1rem
- **CTA Button**: 17px / 1.0625rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/nourish-kitchen-collective-hero-bg.jpg`
- **Alt Text**: Beautifully plated farm-to-table dish on a rustic wooden table
- **Overlay**: Dark gradient overlay at 45% opacity

### Section Backgrounds
- **About Section**: `assets/images/nourish-kitchen-collective-about-bg.jpg`
- **Features Section**: none
- **CTA Section**: `assets/images/nourish-kitchen-collective-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/seasonal-menu.svg`, `assets/images/icons/local-farm.svg`, `assets/images/icons/wine-glass.svg`, `assets/images/icons/event-catering.svg`
- **Team Photos**: `assets/images/team/head-chef.jpg`
- **Gallery**: `assets/images/gallery/dish-01.jpg`, `assets/images/gallery/dish-02.jpg`, `assets/images/gallery/dish-03.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/nourish-kitchen-collective-logo.svg`
- **Alt Text**: "Nourish Kitchen Collective Logo"
- **Max Height**: 50px

### Footer Logo
- **Source**: `assets/logos/nourish-kitchen-collective-logo-white.svg`
- **Alt Text**: "Nourish Kitchen Collective"

### Favicon
- **Source**: `assets/logos/nourish-kitchen-collective-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Nourish Kitchen Collective — Farm-fresh flavours, crafted with care"
- **Description**: Nourish Kitchen Collective is a farm-to-table restaurant in Stellenbosch and Franschhoek offering seasonal menus crafted from locally sourced organic ingredients.
- **OG Title**: Nourish Kitchen Collective — Farm-fresh flavours, crafted with care
- **OG Description**: Nourish Kitchen Collective is a farm-to-table restaurant in Stellenbosch and Franschhoek offering seasonal menus crafted from locally sourced organic ingredients.
- **OG Image**: `assets/images/nourish-kitchen-collective-og.jpg`

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
- **Staging URL Pattern**: `https://dev.nourish-kitchen-collective.preview.example.com`
- **S3 Prefix**: `staging/nourish-kitchen-collective/`
