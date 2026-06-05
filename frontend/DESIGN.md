---
name: Obsidian Flux
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#38393a'
  surface-container-lowest: '#0d0e0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#292a2a'
  surface-container-highest: '#343535'
  on-surface: '#e3e2e2'
  on-surface-variant: '#c3c9b2'
  inverse-surface: '#e3e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#8d937e'
  outline-variant: '#434938'
  surface-tint: '#a4d64c'
  primary: '#fefff1'
  on-primary: '#233600'
  primary-container: '#bef264'
  on-primary-container: '#4b6e00'
  inverse-primary: '#476800'
  secondary: '#c8c6c5'
  on-secondary: '#303030'
  secondary-container: '#474746'
  on-secondary-container: '#b7b5b4'
  tertiary: '#fcffff'
  on-tertiary: '#313030'
  tertiary-container: '#e4e1e0'
  on-tertiary-container: '#646363'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#bff365'
  primary-fixed-dim: '#a4d64c'
  on-primary-fixed: '#131f00'
  on-primary-fixed-variant: '#354e00'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474746'
  background: '#121414'
  on-background: '#e3e2e2'
  surface-variant: '#343535'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 1.5rem
  margin-x: 2rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

The design system is engineered for professional client management, emphasizing efficiency, clarity, and a premium "command center" aesthetic. The brand personality is authoritative yet streamlined, utilizing a high-performance dark mode that reduces eye strain during long working sessions.

The visual style leans heavily into **Modern Minimalism** with a **Tonal Layering** approach. It avoids unnecessary decoration, instead using subtle value shifts and precise typography to establish hierarchy. The interface evokes a sense of calm control, where the data is the hero, supported by a vibrant, high-energy accent color that signals action and vitality.

## Colors

This design system utilizes a sophisticated grayscale foundation paired with a singular "Electric Lime" primary accent. 

- **Primary:** A high-vibrancy lime used sparingly for active states, primary CTAs, and status indicators. It is the sole source of "light" in the interface.
- **Surface Tiers:** The background is an deep, ink-black (`#0A0A0A`). Secondary surfaces (cards) use a slightly lighter neutral (`#171717`), and tertiary surfaces (inputs/search) use a mid-gray (`#262626`) to pull elements forward.
- **Typography Colors:** Pure white (`#FFFFFF`) is reserved for high-priority headings and buttons. Muted gray (`#A3A3A3`) is used for secondary metadata and body text to maintain a comfortable reading contrast.

## Typography

The typography strategy focuses on precision. **Hanken Grotesk** provides a sharp, contemporary feel for headings, while **Inter** ensures maximum legibility for dense client data. **JetBrains Mono** is introduced for small labels and metadata to reinforce the technical, "pro-tool" nature of the product.

- Use high-contrast white for headers.
- Use reduced-opacity neutrals for supporting text (e.g., email addresses, project counts).
- Status labels should utilize the `label-caps` style for distinct visual separation from body content.

## Layout & Spacing

The system follows a **Fluid Grid** with fixed constraints on larger screens to maintain readability. 

- **Grid:** A 12-column layout on desktop, transitioning to 2 columns for tablets and 1 column for mobile.
- **Card-Based Architecture:** Information is encapsulated in cards with consistent internal padding of `1.5rem`.
- **Rhythm:** A 4px/8px baseline grid is used to maintain vertical rhythm. Larger gaps (`2rem`) separate major sections like "Stat Summaries" from the "Client List."
- **Desktop:** 2rem side margins.
- **Mobile:** 1rem side margins with full-width cards.

## Elevation & Depth

Depth is achieved through **Tonal Layers** rather than heavy shadows. In this design system, the Z-axis is communicated by color value: the lighter the gray, the "closer" the element is to the user.

- **Level 0 (Background):** Pure black or `#0A0A0A`.
- **Level 1 (Cards/Surfaces):** Deep gray `#171717`.
- **Level 2 (Active/Hover/Inputs):** Mid-gray `#262626`.
- **Outlines:** Subtle, low-opacity borders (`rgba(255, 255, 255, 0.08)`) define the edges of cards and inputs, ensuring separation without visual clutter.
- **No Shadows:** Shadows are omitted to maintain the crisp, flat aesthetic characteristic of the professional dashboard style.

## Shapes

The design system utilizes **Rounded** shapes (`0.5rem` base) to soften the technical edge of the dark theme. This creates a friendly, approachable atmosphere within a professional context.

- **Primary Radius:** 8px (0.5rem) for cards and buttons.
- **Secondary Radius:** 16px (1rem) for larger container groups.
- **Avatars:** Circular (pill) shapes are used to contrast against the predominantly rectangular card grid.

## Components

### Buttons & CTAs
- **Primary:** Solid background in the accent color (`#BEF264`) with black text.
- **Secondary:** Ghost style with a subtle white border or a dark gray surface (`#262626`) with white text.
- **Action Icons:** Encapsulated in small square buttons with 8px radius.

### Input Fields
- **Search Bar:** Full-width, `#262626` background, with placeholder text in the neutral-gray tone. No border by default; focus state adds a subtle accent-colored ring.

### Cards
- **Client Cards:** Split into a header section (Avatar + Title) and a footer section (Action buttons). Use a subtle horizontal divider (`1px solid rgba(255, 255, 255, 0.05)`) to separate content from card actions.

### Chips & Status Indicators
- **Active Pills:** A soft green background with a dark green text/dot icon to indicate status. The pill should be highly rounded (32px).

### Lists & Metadata
- Group metadata (Email, Project Count, Date) using small icons paired with `body-sm` text in the neutral color palette.