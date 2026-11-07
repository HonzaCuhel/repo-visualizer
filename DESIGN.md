---
name: Repo Visualizer
description: A quiet source workspace for inspecting component graphs.
colors:
  ink: '#151720'
  muted: '#5e6674'
  line: '#dce1e8'
  surface: '#f7f8fa'
  blue: '#2164c7'
  blue-light: '#eaf2ff'
  paper: '#fff'
  selected-ink: '#1558b7'
  blue-hover: '#184e9e'
  code-surface: '#f5f7fa'
  install-surface: '#f6f8fb'
  control-line: '#cbd3df'
  node-line: '#a9b2bf'
  edge-line: '#9da7b6'
typography:
  display:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: clamp(29px, 3.05vw, 44px)
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: -0.03em
  headline:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: clamp(25px, 2.2vw, 31px)
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: -0.025em
  title:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 18px
    fontWeight: 600
    letterSpacing: -0.01em
  body:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
  code:
    fontFamily: ui-monospace, monospace
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.7
  control:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 13px
    fontWeight: 400
  caption:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 12px
    fontWeight: 400
  source-identity:
    fontFamily: Menlo, ui-monospace, monospace
    fontSize: 10px
    fontWeight: 400
rounded:
  inset: 4px
  control: 5px
  primary: 6px
  container: 7px
  graph-group: 10px
  installation: 8px
spacing:
  tight: 4px
  small: 8px
  inset: 12px
  base: 16px
  pane-small: 18px
  pane: 24px
  pane-large: 28px
components:
  button-primary:
    backgroundColor: '{colors.blue}'
    textColor: '{colors.paper}'
    rounded: '{rounded.control}'
    padding: 8px 13px
  button-primary-hover:
    backgroundColor: '{colors.blue-hover}'
  button-view:
    textColor: '{colors.muted}'
    rounded: '{rounded.control}'
    padding: 6px 13px
  component-selected:
    backgroundColor: '{colors.blue-light}'
    textColor: '{colors.selected-ink}'
    rounded: '{rounded.control}'
    padding: 11px 10px
  search:
    textColor: '{colors.muted}'
    rounded: '{rounded.control}'
    padding: 7px 9px
  code:
    backgroundColor: '{colors.code-surface}'
    typography: '{typography.code}'
    rounded: '{rounded.inset}'
    padding: 12px
  command:
    backgroundColor: '{colors.paper}'
    rounded: '{rounded.container}'
    padding: 14px 16px
---

# Design System: Repo Visualizer

## Overview

**Creative North Star: "The Professional Source Workspace"**

A compact, extremely simple working environment puts the repository and its evidence first. White and cool near-white surfaces, charcoal text, a restrained blue and thin neutral rules carry the interface. The user-confirmed rejection is explicit: no childish orange 3D plates, glow, plastic surfaces, oversized gradient actions or neon instrument styling.

The interface is compact and conventional. Clear sans typography explains the work; monospaced text carries source paths, revisions and code. The graph is a flat, selectable representation of relationships. Its geometry belongs to the data rather than to decoration.

Version 0.2 applies the user-requested smaller type and controls, explicit installation CTA, light/dark/system appearance, English/Czech UI and restrained scroll reveals. This is a refinement of the professional source workspace.

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

### Dark appearance
Dark mode uses #10141b paper, #e7edf7 ink, #a8b4c5 supporting text, #303b4c rules, #8bb9ff links/selection strokes, #1c3150 selected surfaces and #306ac0 solid actions. Graph nodes, group bounds, source blocks and exported SVG/canvas all use the same theme tokens. The system preference is the default; user choice persists locally.

### Named Rules
**The Meaningful Blue Rule.** Blue marks an action, focus, selection or highlighted relationship; surrounding structure remains neutral.

## Typography

**Display Font:** Atkinson Hyperlegible Next, locally served under the family name Atkinson, with system-ui and sans-serif fallbacks.
**Body Font:** The same Atkinson family.
**Label/Mono Font:** Menlo with ui-monospace and monospace fallbacks for revision/path metadata; ui-monospace for source blocks, with SFMono-Regular additionally used in installation commands.

**Character:** One clear sans family provides hierarchy through weight, scale and restrained negative tracking. Monospace identifies literal code and source identity.

### Hierarchy
- **Display:** 29–44px with 1.12 line height; 36px on tablet and 30px on mobile.
- **Headline:** 25–31px section headings; 26px on mobile.
- **Title:** 18px example, guide and component-navigation headings. Inspector headings use 23px, becoming 22px on mobile.
- **Body:** root 16px; explanatory prose uses 15–17px, with 16px for mobile reading paragraphs.
- **Controls:** 13–14px for graph and primary actions; header preferences and secondary metadata use 11–12px. Search inputs use 16px on mobile to avoid focus zoom.
- **Source:** Menlo distinguishes paths/revisions; source blocks retain ui-monospace at 11px. Text may scroll inside its pane.
- **Graph:** SVG-coordinate titles remain 17px, kinds/relations 11px and groups 13px. Fitted scaling is independent of the surrounding typography.

### Named Rules
**The Source Identity Rule.** Keep source paths, revisions and literal code visually distinct through monospace; keep explanation in Atkinson.

## Layout

The desktop workspace is bounded at 1320px with 23% navigation, 50% graph and 27% evidence. It is 590px high, becoming 620px at wide viewports. Header controls are compact, with a 64px sticky site header. The installation action is repeated beside the introduction and in the command section so the primary task is immediately available.

At 900px and below, navigation and graph use 31% / 69% above the inspector. At 600px and below the panes stack, component navigation scrolls horizontally and the graph is 450px high. The mobile header keeps language and theme controls; the visible hero carries the primary installation CTA. Code and the command remain internally scrollable.

Standalone explanations cap the main heading at 30px (23px on mobile) and use a 14px short lead. Counts, duration and a seven-character commit are a separate 11px metadata row. An optional source-linked orientation row references existing components; long summaries are available in a disclosure.

Landing sections are bounded at 1200px with 64px vertical and 28px horizontal padding, becoming 44px / 20px on mobile. Examples and downloads are ruled rows. The installation block has one neutral surface and 8px corners. Guides and exports collapse to one column on mobile. Export-frame mode uses its fixed-frame composition rather than scrolling page layout.

## Elevation & Depth

The system is flat at rest. White and cool neutral fills, thin rules and selected outlines establish separation. The floating export menu uses the sole ambient shadow (`0 8px 22px #1d2b4514`). The inspector's selected tab uses a one-pixel blue box-shadow as an underline; it is a state rule, not elevation.

### Named Rules
**The Flat Workspace Rule.** Use borders and tone for persistent structure; reserve ambient shadow for the floating export menu.

## Shapes

Controls have small, practical curves: inset source blocks and icon buttons use the inset radius; searches, view controls and component selections use the control radius. The primary action and playback bar use the primary radius; workspace, command box, export menu and video use the container radius. SVG nodes share that container radius; group bounds use the larger graph-group radius. Rectilinear organization and thin rules dominate; there are no dimensional plates.

## Components

### Buttons
Compact, familiar actions.
- The installation action uses the primary variant, a matching blue border, semibold text and a darker hover fill. The hero action uses 14px text; the header uses 13px. Both share one action color.
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
Theme-aware nodes and thin neutral relationships sit within subtle group bounds. Edge sections are positioned relative to their declared ELK container, preserving endpoint attachment through nested groups. Active and selected nodes use pale blue interiors and stronger blue outlines; highlighted edges use the same blue. Inferred edges are dashed (`5 4`). Focus strengthens outlines further. Focus/path modes dim unrelated graph content to opacity 0.22. Labels and topology are data-derived.

Playback is an explicit interaction: a small pulse follows highlighted relationships, while a range control supports deterministic seeking. Below-fold sections reveal once on intersection over 460ms with a restrained 12px rise, opacity and 1px blur. Content is visible by default, and reduced motion skips the reveal. Scrolling does not start graph playback. The source reduces smooth page scrolling to automatic scrolling when reduced motion is requested; this does not establish a broader reduced-motion policy for every playback/export mode.

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
