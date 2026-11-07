---
name: Repo Visualizer
description: A quiet source workspace for inspecting component graphs.
colors:
  ink: "#151720"
  muted: "#5e6674"
  line: "#dce1e8"
  surface: "#f7f8fa"
  blue: "#2164c7"
  blue-light: "#eaf2ff"
  paper: "#fff"
  selected-ink: "#1558b7"
  blue-hover: "#184e9e"
  code-surface: "#f5f7fa"
  install-surface: "#f6f8fb"
  control-line: "#cbd3df"
  node-line: "#a9b2bf"
  edge-line: "#9da7b6"
typography:
  display:
    fontFamily: "Atkinson, system-ui, sans-serif"
    fontSize: "clamp(32px, 3.71vw, 62px)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Atkinson, system-ui, sans-serif"
    fontSize: "clamp(29px, 2.55vw, 43px)"
    fontWeight: 650
    lineHeight: 1.14
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Atkinson, system-ui, sans-serif"
    fontSize: "25px"
    fontWeight: 600
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Atkinson, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "Atkinson, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
  code:
    fontFamily: "ui-monospace, monospace"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  inset: "4px"
  control: "5px"
  primary: "6px"
  container: "7px"
  graph-group: "10px"
spacing:
  tight: "4px"
  small: "8px"
  inset: "12px"
  base: "16px"
  pane-small: "18px"
  pane: "24px"
  pane-large: "28px"
components:
  button-primary:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.paper}"
    rounded: "{rounded.primary}"
    padding: "0.35em 0.8em"
  button-primary-hover:
    backgroundColor: "{colors.blue-hover}"
  button-view:
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
    padding: "6px 13px"
  component-selected:
    backgroundColor: "{colors.blue-light}"
    textColor: "{colors.selected-ink}"
    rounded: "{rounded.control}"
    padding: "11px 10px"
  search:
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
    padding: "7px 9px"
  code:
    backgroundColor: "{colors.code-surface}"
    typography: "{typography.code}"
    rounded: "{rounded.inset}"
    padding: "12px"
  command:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.container}"
    padding: "14px 16px"
---

# Design System: Repo Visualizer

## Overview

**Creative North Star: "The Professional Source Workspace"**

A bright, extremely simple working environment puts the repository and its evidence first. White and cool near-white surfaces, charcoal text, a restrained blue and thin neutral rules carry the interface. The user-confirmed rejection is explicit: no childish orange 3D plates, glow, plastic surfaces, oversized gradient actions or neon instrument styling.

The interface is compact and conventional. Clear sans typography explains the work; monospaced text carries source paths, revisions and code. The graph is a flat, selectable representation of relationships. Its geometry belongs to the data rather than to decoration.

**Key Characteristics:**
- White and cool-neutral surfaces with charcoal text.
- Restrained blue for selection, links, focus and the primary action.
- Thin rules and compact, gently rounded controls.
- Clear prose paired with readable source code.
- Flat diagrams with explicit selection and inferred relationships.

## Colors

One restrained primary accent sits within a cool neutral working palette. Frontmatter values describe the built source; subtle one-off helper colors are not promoted into a larger brand scale.

### Primary
- **Working Blue** (`blue`): primary installation action, links, keyboard outlines, active graph strokes and playback accents.
- **Pale Selection Blue** (`blue-light`): selected components and graph nodes; export-option hover.
- **Selected Blue Ink** (`selected-ink`): selected component navigation text.
- **Deep Action Blue** (`blue-hover`): installation action hover.

### Neutral
- **Charcoal Ink** (`ink`): main prose, headings and navigation.
- **Slate Text** (`muted`): supporting prose, metadata and inactive controls.
- **Fine Rule** (`line`): pane boundaries, rows and control borders.
- **Cool Surface** (`surface`): a source-defined neutral primitive; retain its name without forcing it onto surfaces that use specific colors.
- **White Paper** (`paper`): main canvas, buttons, node interiors and floating export menu.
- **Code Paper** (`code-surface`): inset source excerpts.
- **Installation Paper** (`install-surface`): installation section background.
- **Control Rule** (`control-line`): installation controls and command container.
- **Node Rule** (`node-line`) and **Relationship Rule** (`edge-line`): unselected diagram structure.

### Named Rules
**The Meaningful Blue Rule.** Blue marks an action, focus, selection or highlighted relationship; surrounding structure remains neutral.

## Typography

**Display Font:** Atkinson Hyperlegible Next, locally served under the family name Atkinson, with system-ui and sans-serif fallbacks.
**Body Font:** The same Atkinson family.
**Label/Mono Font:** Menlo with ui-monospace and monospace fallbacks for revision/path metadata; ui-monospace for source blocks, with SFMono-Regular additionally used in installation commands.

**Character:** One clear sans family provides hierarchy through weight, scale and restrained negative tracking. Monospace identifies literal code and source identity.

### Hierarchy
- **Display:** the frontmatter display role is the wide-layout page heading. At widths up to 900px it becomes 38px; up to 600px it becomes 34px with line-height 1.08.
- **Headline:** landing section headings use the frontmatter headline role; up to 700px they become 32px.
- **Title:** example and guide headings use the frontmatter title role; up to 700px they become 23px. Inspector and component-pane headings have their own responsive clamps in the source.
- **Body:** the frontmatter body role is the root baseline. Explanatory landing prose uses 17–20px and 1.5–1.65 line height, with recurring 65–70ch reading measures.
- **Label:** compact search and button text uses the label role; graph-view/export controls use 16px on wide layouts and 14px on narrower layouts.
- **Code:** the frontmatter code role describes inset source excerpts. Installation commands use 15px and 1.6 line height, reducing to 13px and then 12px at the landing breakpoints.
- **Graph labels:** SVG titles use 17px at weight 600; kind and relationship labels use 11px, and group labels use 13px at weight 600. These are SVG-coordinate values; fitted viewport scale changes their apparent size.

### Named Rules
**The Source Identity Rule.** Keep source paths, revisions and literal code visually distinct through monospace; keep explanation in Atkinson.

## Layout

The explorer uses bounded, independently scrollable working panes and a dominant graph area. Wide-layout columns are 22.3%, 51.6% and the remaining width; workspace width is 98.74%, height is 38.15vw bounded by 530px and 760px. At 1800px and above it has a 1900px maximum width. These describe the explorer, not a required composition for every future surface.

At up to 1200px the explorer uses 23% / 49% / 28% columns and a 570px minimum height. At up to 900px the inspector moves below the navigation and graph; its content becomes two columns. At up to 600px all panes stack, component navigation becomes a horizontal scroller, the inspector returns to block flow, and the graph pane keeps a 455px height. The graph SVG reserves a 42px strip for navigation controls outside its drawable area.

Landing sections use a 1672px maximum width and 76px vertical padding; up to 700px this becomes 48px with 20px horizontal padding. Example and download collections use ruled rows, not decorative card grids. Guide and export layouts collapse to one column on small screens. The landing also has an intermediate 1100px breakpoint.

Spacing is contextual rather than a rigid mathematical scale. The extracted recurring steps cover small control gaps, code insets and 18–28px pane padding. Large landing-section spacing remains specific to that content hierarchy. Export-frame mode intentionally fits the same explorer into a fixed viewport and omits page-level navigation and introduction.

## Elevation & Depth

The system is flat at rest. White and cool neutral fills, thin rules and selected outlines establish separation. The floating export menu uses the sole ambient shadow (`0 8px 22px #1d2b4514`). The inspector's selected tab uses a one-pixel blue box-shadow as an underline; it is a state rule, not elevation.

### Named Rules
**The Flat Workspace Rule.** Use borders and tone for persistent structure; reserve ambient shadow for the floating export menu.

## Shapes

Controls have small, practical curves: inset source blocks and icon buttons use the inset radius; searches, view controls and component selections use the control radius. The primary action and playback bar use the primary radius; workspace, command box, export menu and video use the container radius. SVG nodes share that container radius; group bounds use the larger graph-group radius. Rectilinear organization and thin rules dominate; there are no dimensional plates.

## Components

### Buttons
Compact, familiar actions.
- The installation action uses the primary variant, a matching blue border, semibold text and a darker hover fill. Mobile overrides use 14px text and 6px 10px padding.
- View controls use neutral text, transparent default backgrounds and a quiet selected fill; selection also strengthens the text weight.
- Export summaries use a thin neutral border, white background and the control radius. Menu rows highlight with pale selection blue.
- Keyboard focus uses a two-pixel blue outline with a three-pixel offset; search uses focus-within with a one-pixel offset. Disabled buttons reduce opacity to 0.5 and use a waiting cursor.
- Icon actions use authored stroke SVG. Mathematical zoom signs remain text operators.

### Chips / Component Navigation
Component choices are full-width, left-aligned rows on desktop. Hover adds a cool near-white fill; selected state uses pale blue, blue text and weight 600. On mobile they become bordered, horizontally scrolling compact choices. Selected state is carried by `aria-pressed` rather than color alone.

### Cards / Containers
The workspace and command container are restrained white, ruled containers with the container radius. Code excerpts use a cool inset fill, the inset radius, source whitespace and overflow scrolling. Example and download lists remain open rows divided by rules.

### Inputs / Fields
Search is a thin-bordered control with an inline stroke SVG and a transparent input. It uses a blue caret and explicit focus-within outline. The playback range uses the same blue accent; time labels use tabular numerals. Scenario selection is a compact conventional select. No distinct field-error visual treatment is established by this build.

### Navigation
The main navigation is text-based, charcoal and unadorned until hover underlines it. It disappears at the 600px breakpoint while the primary installation action remains. Inspector tabs use muted text and a thin blue active underline. The component list is the working navigation and follows the responsive behavior above.

### Component Graph
White nodes and thin neutral relationships sit within pale group bounds. Active and selected nodes use pale blue interiors and stronger blue outlines; highlighted edges use the same blue. Inferred edges are dashed (`5 4`). Focus strengthens outlines further. Focus/path modes dim unrelated graph content to opacity 0.22. Labels and topology are data-derived.

Playback is an explicit interaction: a small pulse follows highlighted relationships, while a range control supports deterministic seeking. No decorative entrance-transition vocabulary is established. The source reduces smooth page scrolling to automatic scrolling when reduced motion is requested; this does not establish a broader reduced-motion policy for every playback/export mode.

## Do's and Don'ts

### Do:
- **Do** use restrained blue to identify actions, keyboard focus and graph selection.
- **Do** preserve thin neutral rules, cool white surfaces and compact conventional controls.
- **Do** use Atkinson for explanation and monospace for literal code and source identity.
- **Do** reflow the working panes and allow code and component navigation to scroll where the source does.
- **Do** preserve selection, inferred-relationship styling and source meaning across projections.

### Don't:
- **Don't** introduce orange 3D plates, glow, plastic surfaces, oversized gradient actions or neon instrument styling.
- **Don't** replace authored action SVG with Unicode arrow icon substitutes.
- **Don't** impose a linear chain on graph data that contains branches, parallel relationships or cycles.
- **Don't** turn tiny helper metadata, SVG-coordinate label sizes or isolated colors into a universal body-text or palette scale.
