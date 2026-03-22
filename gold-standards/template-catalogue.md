# Gold Standard Template Catalogue

**Total Templates**: 21 (20 existing + 1 pending: HASA CRMP)
**Source Templates**: `bigbeard-templates/` (anonymised, reusable skeletons)
**Source Designs**: Figma Team — Big Beard Web Solutions (ID: 1163841941862231068)
**Date Catalogued**: 2026-03-22

---

## Eval Pipeline (Corrected)

Templates already exist as anonymised skeletons in `bigbeard-templates/`. The eval tests an agent's ability to **customise** these templates to match business requirements.

| Stage | Agent Task | Input | Output |
|-------|-----------|-------|--------|
| 1 | Customise template (colours, fonts, logos, images, text, layout, SEO, a11y) | Template skeleton + requirements.md | Customised output folder |
| 2 | Site generation (optimise, validate, package) | Customised template | Deployment-ready folder |
| 3 | Deploy to staging (S3 + CloudFront preview) | Deployment-ready folder | Live staging URL + config |

---

## Template Mapping

| # | bigbeard-templates Path | Figma Source | Figma Key | Industry | Eval Business |
|---|------------------------|-------------|-----------|----------|---------------|
| 1 | `education/skills-training-blog-1` | Blog-Capaciti Option 1 | `viH5HRCWleSJgKJxoGw8MK` | Education | GreenPulse Analytics |
| 2 | `education/skills-training-blog-2` | Blog-Capaciti Option 2 | `v3grhAxg6DsWUmudC5HneW` | Education | Meridian Legal Partners |
| 3 | `education/skills-training-corporate` | CAPACITI Phase 1 | `mS6hSPClkqlfRRWvTeTjDW` | Education | Vantage Robotics Academy |
| 4 | `education/skills-training-landing` | CAPACITI Phase 2 | `YCkggAfrxrn1EATvGFWSfj` | Education | Solaris Wealth Advisors |
| 5 | `technology/saas-product` | Catalyst App Landing Page | `EQYDubJjrnkn4IEDwNQauV` | Technology | FleetPulse |
| 6 | `technology/ai-page-builder` | Chirrup | `W6Ngo1qUBpo5tkNlcD87fR` | Technology | Nourish Kitchen Collective |
| 7 | `marketing/digital-agency` | Denker Website | `oVr0KjvNH6e17ZjBelrPWo` | Marketing | Apex Architecture Studio |
| 8 | `hospitality/safari-lodge` | Etali Safari Website | `mhMK6el5GzzYOJASq0wXZu` | Hospitality | Karoo Starlight Lodge |
| 9 | `energy/solar-provider` | Industry Landing Page | `rdvPurH4MH0bPHP4gyTIQY` | Energy | SunVolt Energy |
| 10 | `manufacturing/industrial-company` | Forgeweld | `EF5ayUwdHLWd0G8Wd7yEC3` | Manufacturing | TitanCore Engineering |
| 11 | `manufacturing/creative-factory` | Fuse Factory | `0Yo1PO6Zyuc2cdmqjSuTYc` | Manufacturing | Pixel & Grain Creative |
| 12 | `healthcare/association-corporate` | HASA Main Redesign V3 | `4diRrKJRYjAbA93vpLHIpN` | Healthcare | Institute of Chartered Accountants SA |
| 13 | `healthcare/association-gala-event` | Gala Page | `odkLDVy7HFYAs09dLc47JT` | Healthcare | Masiyavana Heritage Gala |
| 14 | `healthcare/association-newsletter` | Conference Newsletter | `26xc9wtLruW2LVMYnPOzmv` | Healthcare | AfriAgri Summit |
| 15 | `healthcare/association-policy` | HASA NHI | `L6L024r4UcygQifA3fppG0` | Healthcare | ClearPath Insurance Brokers |
| 16 | `finance/investment-company` | Metis | `kFAqZfGpRIwFyFLAKk2GoJ` | Finance | Quantum Consulting Group |
| 17 | `nonprofit/community-trust-1` | Amandla Omoya Trust | `3ucuFVI3JQRDyVRlKngRQe` | Nonprofit | Thrive Africa Foundation |
| 18 | `nonprofit/community-trust-2` | Letsatsi Borutho Trust | `IJmiT1qtA0d7ET0R0VR5df` | Nonprofit | Khula Community Trust |
| 19 | `nonprofit/community-trust-3` | Sibona Ilanga Trust | `H6UTqg48VYc2UvZRYUY3Ml` | Nonprofit | Ubuntu Education Initiative |
| 20 | `blank/blank-site` | SoSimple | `7mL5yd7JmNs3UFqUgxqlmI` | General | CloudNest Digital |
| 21 | **PENDING** (user adding) | HASA CRMP Wireframes | `VArIfUwbcqQLmlglPoVsTe` | App | MediTrack Connect |

---

## Templates NOT Mapped (excluded from eval)

| Figma Source | Reason |
|-------------|--------|
| Chirrup Mobile | Mobile-specific design, separate eval track |
| Etali Safari Landing Page | Duplicate coverage (safari-lodge covers Etali) |
| HASA Main Redesign V2 | V3 supersedes V2 |
| HASA Main Holiday Banner | Banner only, not a full site |
| Experience Madikwe | No direct bigbeard-template match found |
| Uvu Africa | Empty Figma project (no files) |

---

## Notes

- `bigbeard-templates/` contains the anonymised skeletons (input to eval)
- `gold-standards/template-*/` will contain the expected customised output (what perfect agent output looks like)
- HASA CRMP will be added to `bigbeard-templates/` by user for app/wireframe variation
- Mapping above is approximate — verify by visually comparing each template to its Figma source
