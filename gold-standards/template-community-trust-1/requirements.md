# Template Requirements: Amandla Omoya Trust

## Source
- **Figma File**: Amandla Omoya Trust
- **Figma Key**: 3ucuFVI3JQRDyVRlKngRQe
- **Project**: Sibona Ilanga
- **Type**: Site

## Business Profile
- **Business Name**: Thrive Africa Foundation
- **Industry**: Non-Profit / Youth Development
- **Tagline**: Empowering young Africans to lead

## Brand Amendments

### Colours
- **Primary**: #E07A2F
- **Secondary**: #3B1F0B
- **Accent**: #2EC4B6
- **Background**: #FFF9F3
- **Text**: #1F1A15

### Typography
- **Heading Font**: Bitter
- **Body Font**: Cabin

### Logo
- **Logo Source**: `assets/logos/thrive-africa-foundation-logo.svg`
- **Favicon**: `assets/logos/thrive-africa-foundation-favicon.png`

## Content Amendments

### Hero Section
- **Headline**: Investing in the Next Generation of African Leaders
- **Subheadline**: Scholarships, mentorship programmes, and entrepreneurship incubators for young people in underserved communities across Southern Africa.
- **CTA Button**: Support Our Mission

### About Section
- **Description**: Thrive Africa Foundation is a registered non-profit organisation focused on youth education, leadership development, and economic empowerment. Since 2014, we have awarded over 1,200 bursaries and supported 85 youth-led startups through our accelerator programme. We operate in South Africa, Mozambique, and Zambia.

### Contact
- **Email**: connect@thriveafrica.org
- **Phone**: +27 11 234 5678
- **Address**: 10 Melle Street, Braamfontein, Johannesburg, 2001, South Africa

## Layout Amendments

### Hero Layout
- **Pattern**: full-width-overlay
- **Arrangement**: Inspirational youth photography background with centered headline and donation CTA

### Sections Layout
- **Features Section**: alternating-rows
- **Testimonials Section**: carousel
- **Footer Layout**: 4-column

### Responsive Breakpoints
- **Mobile**: 375px (single column, stacked sections)
- **Tablet**: 768px (2-column where applicable)
- **Desktop**: 1024px+ (full layout as designed)

## Font Amendments

### Font Pairing
- **Heading Font**: Bitter
- **Heading Weights**: 500, 700
- **Body Font**: Cabin
- **Body Weights**: 400, 500
- **CTA Font**: Cabin

### Font Sizing
- **H1**: 48px / 3rem
- **H2**: 34px / 2.125rem
- **Body**: 16px / 1rem
- **CTA Button**: 17px / 1.0625rem, bold

## Image Amendments

### Hero Background
- **Source**: `assets/images/thrive-africa-foundation-hero-bg.jpg`
- **Alt Text**: Smiling young African students in a classroom raising their hands
- **Overlay**: Dark gradient overlay at 45% opacity

### Section Backgrounds
- **About Section**: none
- **Features Section**: none
- **CTA Section**: `assets/images/thrive-africa-foundation-cta-bg.jpg`

### Content Images
- **Feature Icons**: `assets/images/icons/scholarship.svg`, `assets/images/icons/mentorship.svg`, `assets/images/icons/incubator.svg`, `assets/images/icons/community.svg`
- **Team Photos**: `assets/images/team/foundation-team.jpg`
- **Gallery**: `assets/images/gallery/graduation-01.jpg`, `assets/images/gallery/workshop-01.jpg`

## Logo Amendments

### Header Logo
- **Source**: `assets/logos/thrive-africa-foundation-logo.svg`
- **Alt Text**: "Thrive Africa Foundation Logo"
- **Max Height**: 48px

### Footer Logo
- **Source**: `assets/logos/thrive-africa-foundation-logo-white.svg`
- **Alt Text**: "Thrive Africa Foundation"

### Favicon
- **Source**: `assets/logos/thrive-africa-foundation-favicon.png`
- **Sizes**: 16x16, 32x32, 180x180 (Apple Touch)

## SEO Requirements

### Meta Tags
- **Title**: "Thrive Africa Foundation — Empowering young Africans to lead"
- **Description**: Thrive Africa Foundation provides scholarships, mentorship, and entrepreneurship incubators for young people in underserved communities across Southern Africa.
- **OG Title**: Thrive Africa Foundation — Empowering young Africans to lead
- **OG Description**: Thrive Africa Foundation provides scholarships, mentorship, and entrepreneurship incubators for young people in underserved communities across Southern Africa.
- **OG Image**: `assets/images/thrive-africa-foundation-og.jpg`

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
- **Staging URL Pattern**: `https://dev.thrive-africa-foundation.preview.example.com`
- **S3 Prefix**: `staging/thrive-africa-foundation/`
