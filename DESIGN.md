---
name: Repo Visualizer
description: A landscape invitation into a quiet, source-grounded graph workspace.
colors:
  paper: '#fff'
  ink: '#151720'
  muted: '#5e6674'
  line: '#dce1e8'
  surface: '#f7f8fa'
  hover: '#f1f4f8'
  blue: '#2164c7'
  blue-light: '#eaf2ff'
  selected-ink: '#1558b7'
  action-hover: '#184e9e'
  group-fill: '#fafbfd'
  code-surface: '#f5f7fa'
  control-line: '#cbd3df'
  node-line: '#a9b2bf'
  edge-line: '#8490a1'
  landing-action: '#0854e5'
  landing-action-hover: '#0645be'
  landing-selected-ink: '#0649cd'
  dark-paper: '#10141b'
  dark-ink: '#e7edf7'
  dark-muted: '#a8b4c5'
  dark-line: '#303b4c'
  dark-surface: '#181f2a'
  dark-hover: '#202a38'
  dark-blue: '#8bb9ff'
  dark-blue-light: '#1c3150'
  dark-selected-ink: '#b4d3ff'
  dark-action: '#306ac0'
  dark-action-hover: '#3978d1'
  dark-group-fill: '#171e29'
  dark-code-surface: '#19222f'
  dark-control-line: '#3c4b60'
  dark-node-line: '#687992'
  dark-edge-line: '#b9c4d3'
  landing-dark-selected-ink: '#bcd7ff'
  diagram-surface: '#fbfcfe'
  diagram-band: '#edf2f7'
  dark-diagram-surface: '#141b23'
  dark-diagram-band: '#1c2732'
typography:
  standalone-display:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: clamp(23px, 2vw, 30px)
    fontWeight: 700
    lineHeight: 1.24
    letterSpacing: -0.02em
  landing-display:
    fontFamily: Rethink, Atkinson, sans-serif
    fontSize: clamp(40px, 3.468vw, 64px)
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: -0.03em
  landing-headline:
    fontFamily: Rethink, Atkinson, sans-serif
    fontSize: clamp(26px, 2.3vw, 34px)
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: -0.025em
  standalone-body:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.45
  landing-body:
    fontFamily: Rethink, Atkinson, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.45
  standalone-control:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 13px
    fontWeight: 400
  landing-control:
    fontFamily: Rethink, Atkinson, sans-serif
    fontSize: 13px
    fontWeight: 400
  public-detail-control:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.3
  diagram-title:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 20px
    fontWeight: 600
    lineHeight: 24px
  diagram-caption:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 19px
  diagram-edge:
    fontFamily: Atkinson, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 18px
  code:
    fontFamily: ui-monospace, monospace
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.7
  source-identity:
    fontFamily: Menlo, ui-monospace, monospace
    fontSize: 10px
    fontWeight: 400
  landing-command:
    fontFamily: Menlo, ui-monospace, monospace
    fontSize: 14px
    lineHeight: 1.5
rounded:
  inset: 4px
  control: 5px
  primary: 6px
  container: 7px
  landing-action: 8px
  landing-command: 9px
  diagram-node: 9px
  graph-group: 10px
  diagram-dialog: 14px
  diagram-frame: 16px
  landing-video: 12px
  landing-installation: 14px
  landing-workspace-mobile: 17px
  landing-theme: 20px
  landing-workspace: 22px
spacing:
  tight: 4px
  small: 8px
  inset: 12px
  base: 16px
  pane-small: 18px
  pane: 24px
  pane-large: 28px
  landing-gutter: clamp(24px, 3.53vw, 56px)
components:
  diagram-node:
    backgroundColor: '{colors.paper}'
    textColor: '{colors.ink}'
    typography: '{typography.diagram-title}'
    rounded: '{rounded.diagram-node}'
  diagram-dialog:
    backgroundColor: '{colors.paper}'
    textColor: '{colors.ink}'
    rounded: '{rounded.diagram-dialog}'
    padding: 0
    width: calc(100% - 32px)
    height: calc(100% - 32px)
  public-detail-source:
    backgroundColor: transparent
    textColor: '{colors.ink}'
    typography: '{typography.public-detail-control}'
    rounded: '{rounded.primary}'
    padding: 7px 12px
  landing-button-primary:
    backgroundColor: '{colors.landing-action}'
    textColor: '{colors.paper}'
    rounded: '{rounded.landing-action}'
    padding: 10px 20px
  landing-button-primary-hover:
    backgroundColor: '{colors.landing-action-hover}'
  button-view:
    textColor: '{colors.muted}'
    rounded: '{rounded.control}'
    padding: 6px 13px
  component-selected:
    backgroundColor: '{colors.blue-light}'
    textColor: '{colors.selected-ink}'
    rounded: '{rounded.control}'
    padding: 9px 8px
  landing-component-selected:
    backgroundColor: '{colors.blue-light}'
    textColor: '{colors.landing-selected-ink}'
    rounded: '{rounded.control}'
    padding: 5px 6px
  search:
    textColor: '{colors.muted}'
    rounded: '{rounded.control}'
    padding: 7px 9px
  code:
    backgroundColor: '{colors.code-surface}'
    typography: '{typography.code}'
    rounded: '{rounded.inset}'
    padding: 12px
  landing-command:
    backgroundColor: '#fffffff0'
    textColor: '{colors.ink}'
    typography: '{typography.landing-command}'
    rounded: '{rounded.landing-command}'
    padding: 0 16px 0 20px
    height: 45px
---

# Design System: Repo Visualizer

## Overview

**Creative North Star: "The Professional Source Workspace, Open to the Landscape"**

The shared visual system is a compact, professional source workspace: flat component graphs, quiet neutral panes, restrained blue actions and inspectable evidence. Clear prose and literal code have distinct typographic roles. The graph's geometry follows repository relationships, including branches and cycles.

The public landing adds the user-selected landscape world: an original sunlit mountain valley supplies atmosphere and spatial depth while a complete working explorer supplies proof. Rethink Sans carries the landing interface; the standalone skill player retains Atkinson. This is a scoped public presentation, not a new photographic requirement for every generated explanation. The user rejected childish orange 3D plates, glow, plastic surfaces, oversized gradient actions and neon instrument styling.

**Key Characteristics:**
- Flat, source-grounded diagrams with explicit selection and inferred relationships.
- Cool neutral surfaces, charcoal text and purposeful blue actions.
- A photographic landscape on the public landing, with the tooling kept flat.
- Rethink for the public interface, Atkinson for standalone explanations and graph labels, monospace for source identity.
- Compact controls, five bundled interface languages and explicit appearance choices.

## Colors

The frontmatter records observed light and dark primitives. Landing-prefixed tokens apply only to the public surface; unprefixed values preserve the standalone workspace. These labels document existing values rather than installing a new CSS token scale.

### Primary
- **Working Blue** (`blue`): standalone actions, focus, links and highlighted relationships. **Deep Action Blue** (`action-hover`) carries standalone action hover.
- **Landing Cobalt** (`landing-action`): the public action fill, links and selected graph strokes in light mode. **Deep Landing Cobalt** (`landing-action-hover`) carries action hover.
- **Pale Selection Blue** (`blue-light`) and **Selected Blue Ink** (`selected-ink`, `landing-selected-ink`): selected working navigation and graph states.
- **Night Blue** (`dark-blue`, `dark-blue-light` and the scoped selected-ink tokens): dark links and selection. Solid standalone dark actions use `dark-action` and `dark-action-hover`; landing action fills retain their scoped cobalt.

### Neutral
- **White Paper**, **Charcoal Ink** and **Slate Text** (`paper`, `ink`, `muted`): canvas, main copy and supporting metadata.
- **Fine Rule**, **Cool Surface** and **Quiet Hover** (`line`, `surface`, `hover`): boundaries, installation surfaces and neutral interaction states.
- **Source Paper** and **Group Paper** (`code-surface`, `group-fill`): inset code and subtle graph group regions.
- **Control Rule**, **Node Rule** and **Relationship Rule** (`control-line`, `node-line`, `edge-line`): control boundaries and unselected graph structure.
- **Diagram Paper** and **Shared Band** (`diagram-surface`, `diagram-band`): the neutral diagram frame and sourced shared-component bands. Light nodes use white paper; dark frames and nodes share dark-diagram-surface while bands use dark-diagram-band. The dark relationship rule is lighter to preserve route readability.
- The corresponding `dark-*` tokens carry the same roles on a charcoal canvas. The landing landscape darkens with brightness and saturation filtering while the working panes use the shared theme.

### Named Rules
**The Meaningful Blue Rule.** Blue marks an action, focus, selection or highlighted relationship; surrounding structure remains neutral.

**The Scoped Landscape Rule.** Nature supplies depth on the public landing; source evidence and graph geometry remain live interface elements rather than rasterized decoration.

## Typography

**Display Font:** Locally served Rethink Sans under `Rethink` on the landing; locally bundled Atkinson Hyperlegible Next under `Atkinson` in standalone explanations.
**Body Font:** Inherits the surface's family. The root uses the standalone-body role; the landing overrides the family.
**Label/Mono Font:** Menlo with ui-monospace and monospace fallbacks for source paths, revisions and the hero command; ui-monospace for source excerpts.

### Hierarchy
- **Landing display:** the landing-display role; at phone widths it becomes `clamp(30px, 7.8vw, 39px)`, line height 1.1 and an 18ch measure. The centered subtitle uses `clamp(19px, 1.514vw, 27px)` and becomes 17px with 1.45 line height on phones.
- **Standalone display:** the standalone-display role with a 58ch cap, becoming 23px on phones. The short lead remains 14px; counts and duration use 11px and a short revision uses 10px.
- **Landing section headline:** the landing-headline role. Example and guide titles use 18px. Landing explorer navigation uses 20px titles and 13px component rows; its inspector uses 24px headings and 15px descriptions, with contextual responsive overrides.
- **Standalone explorer:** navigation headings use 18px, rows 14px, inspector headings 23px and descriptions 15px. Phone rows become 12px while search uses 16px.
- **Controls:** compact 13px graph controls in both surfaces. Landing hero actions use 16px, becoming 14px on phones. Tiny metadata and source-coordinate text are contextual, not a general reading-size standard.
- **Graph:** labels retain Atkinson even on the Rethink landing. Measured SVG titles use the diagram-title role; short responsibility captions use diagram-caption with at most two lines and explicit ellipsis. Edge labels use diagram-edge with at most three measured lines. Group labels remain 13px and the separate inferred marker remains 11px. These are graph-coordinate sizes; camera fitting controls displayed size. Full descriptions remain available in the inspector and tooltip.

### Named Rules
**The Source Identity Rule.** Keep source paths, revisions and literal code visually distinct through monospace; use the surface's sans family for explanations and Atkinson for graph labels.

## Layout

The standalone desktop workspace caps at 1320px with 23% navigation, 50% graph and 27% evidence. It is 590px high, becoming 620px from 1600px. At 900px and below, navigation and graph use 31% / 69% above the inspector; at 600px and below the working panes stack, navigation becomes horizontally scrollable and the shared graph pane now grows intrinsically with zero minimum height while its stage is 420px high. Standalone introductions stay compact; optional orientation choices reference actual graph components and long summaries use disclosure.

The public landing centers its introduction above the real explorer. Header, workspace, selection status and footer share a 1480px maximum frame with the landing-gutter spacing on each side. The transparent header stays between 56px and 64px high. The introduction caps at 1280px wide, with a height of `clamp(320px, 23.077vw, 366px)`. The desktop workspace retains 21.6% / 51.8% / 26.6% columns with a height of `clamp(510px, 35.44vw, 600px)`. The landscape height is capped at 800px. The thick paper frame has an inset rule; it separates the working surface from the image without adding a shadow. The actual first viewport, not a percentage from the mockup, governs review.

At 1200px the landing uses 23% / 49% / 28% columns. At 1000px and below it switches to 29% / 71% over a full-width inspector: workspace height is automatic, both rows are intrinsic (`auto auto`), and the first two panes have a 510px minimum height. The inspector retains its source-defined internal grid at tablet widths where that shared rule applies. At 600px and below the workspace becomes a block stack; component navigation becomes a horizontal strip, the graph pane has automatic height and zero minimum height, and its stage alone is 420px high. The mobile graph toolbar grows naturally from a 51px minimum height, wraps with an 8px gap and 8px vertical padding, and keeps the view group and export control from shrinking. Export stays right-aligned and moves to a second row when translated labels need the room. Playback, caption, inspector and later content follow in normal flow. Do not restore a fixed graph-pane height to the mobile landing.

The public command scrolls internally on wide screens; on phones its text wraps anywhere, the command container grows naturally and only the copy icon remains visible. At 600px and below the shared landing gutter becomes 12px, the introduction grows intrinsically and the working frame remains aligned with the status and footer. The compact flag and sun/moon/system controls remain in the header; text navigation disappears at 1000px. At 360px and below the locale code also hides.

Landing sections cap at 1240px with 76px vertical padding, becoming 46px at 600px. Example/download rows use thin dividers; the installation surface caps at 1184px with 40px padding. Guides and exports collapse at their source-defined 700px breakpoint. Export-frame mode retains its separate fixed-frame composition. An expanded diagram uses a native modal dialog inset by 16px, reducing to 6px on phones; the graph stage fills the available dialog height instead of retaining its phone-stage height.

## Elevation & Depth

Persistent working surfaces are flat: thin rules, tonal fills and selected outlines communicate structure. The public landscape carries photographic depth outside the explorer. Its light overlay fades into the paper canvas; dark mode filters the image and fades into dark paper. Floating export and language menus share the ambient shadow (`0 8px 22px #1d2b4514`). The diagram frame and shared-component bands add quiet neutral layering inside the graph. The expanded native dialog uses a dark translucent backdrop (`#08101a99`), a thin control rule and no new shadow tier. The inspector tab's one-pixel blue box-shadow is an active-state underline, not an elevation tier.

### Named Rules
**The Flat Workspace Rule.** Use borders and tone for persistent tooling structure; reserve ambient shadow for floating menus.

## Shapes

Small practical curves define the shared tools: inset code, conventional controls, a gently rounded workspace and graph nodes, and larger group bounds. The public presentation uses broader curves for its 22px explorer frame, 17px phone frame, 9px hero command, 8px hero actions, 14px installation surface and 12px video. The shared header theme switch is a 20px capsule with 16px selected segments in every generated HTML, including raw skill, ZIP-built, offline and public examples. These are scoped component shapes, not a universal pill-button rule. Diagram nodes use 9px corners, the neutral diagram frame 16px and the expanded dialog 14px. Thin rectilinear rules remain the organizing device inside the workspace.

## Components

### Brand mark and landscape

The mark is a crisp graph of three connected components: one filled node and two outlined nodes. Its canonical SVG and shared header stylesheet live in the installed skill assets. The core builder embeds the mark, favicon and stylesheet in every generated HTML, including raw skill output, ZIP-built artifacts, offline files and public examples. The public builder adds its page-specific content and preferences without a duplicate brand-style or mark wrapper. The README shares the same mark. The GitHub mark is the separately attributed Bootstrap Icons asset.

The landscape is original generated atmosphere, not a claim about a named real place. It has no UI painted into it. Shipping raster provenance records the generation prompt for generated imagery or the origin/render inputs for derived media. Diagram PNG, SVG, GIF and MP4 exports are rendered from the canonical SVG scene by Repo Visualizer, with committed source-HTML identity and source/artifact fingerprints; these exports are derived renders, not image-generation assets or recordings of target-code execution. Preserve those records when replacing or rebuilding media.

### Buttons

Compact, conventional actions have distinct selected and focus states. The public primary action is cobalt with white text; its secondary explore action is a thin dark border over translucent paper. Both have a 44px minimum height. Standalone headers use the compact neutral source-jump action; blue continues to identify graph selection, focus and links. Neutral view controls use a quiet hover fill and stronger selected text; export summaries use a thin rule. Keyboard focus uses a two-pixel blue outline with three-pixel offset; search uses focus-within with one-pixel offset. Disabled actions reduce opacity to 0.5 with a waiting cursor. Authored stroke SVG supplies action icons; mathematical zoom operators remain text.

### Chips / Component Navigation

Desktop component choices are left-aligned rows; hover adds a quiet neutral surface and selection adds blue tone, stronger ink and weight 600. `aria-pressed` preserves state beyond color. Mobile choices are bordered compact items in a horizontally scrollable strip. Source-linked orientation choices are optional standalone explanation controls, not an arbitrary linear replacement for the graph.

### Cards / Containers

The explorer, source blocks and commands are ruled containers with contextual corner sizes. Source excerpts preserve literal whitespace and scroll internally. The public copy command keeps its text and copy action in one translucent paper row; clipboard failure selects the text and exposes feedback. Examples and downloads stay open, ruled rows rather than a card grid. The current public gallery links to the Codex loop, Codex shell execution, Superpowers workflow, Whisper transcription and a focused Whisper decoder loop; repository identity, pinned source attribution and the explore action remain legible parts of each example pattern.

### Inputs / Fields

Search combines an authored stroke icon with a transparent input, thin border and blue caret. Its public desktop text is compact (11px), becoming 12px on the phone landing; this does not replace the standalone phone search's 16px rule. The playback range uses the surface accent and tabular time labels. Scenario choice uses a conventional compact select. No separate field-error visual system is established.

### Navigation and Appearance

Public landing navigation uses content-sized flex links with equal 28px gaps, reducing to 20px at 1200px and below; translation changes link width without imposing fixed columns. Links are quiet text over the sky with hover underlines. Component navigation and inspector tabs remain the working navigation; the active inspector tab has a thin blue underline. Every core-generated HTML shares the flag-plus-locale-code trigger and the sun/moon/system capsule, including the landing, public details, raw skill output and ZIP-built or offline artifacts. The trigger opens a keyboard-operable listbox with a visible selected check. Appearance-group spacing is 24px, reducing to 12px at 1200px, 8px on phones and 6px at 360px. Theme segments are 40px wide, becoming 26px on phones and 24px at 360px; the locale code also hides at that narrowest breakpoint. English, Czech, German, French and Spanish UI catalogs are bundled; graph translation availability is separate and a notice explains mismatches. The current Superpowers and Whisper gallery graphs each include display translations in all five languages while source paths and revision-pinned references retain their literal identity.

Sun, moon and system buttons explicitly select light, dark or operating-system appearance, with accessible labels and `aria-pressed`. Query choices precede stored choices, then artifact preferences and the fallback. The public build supplies English and light preferences to both landing and branded detail pages; a saved or queried choice wins. The raw installed skill player retains the user or graph language behavior and system theme fallback unless its artifact carries a preference. Choices persist locally. Exported standalone HTML embeds its player, shared brand mark/header styles, favicon, fonts, interface catalogs and graph/source data for offline viewing and removes the public landscape styles and landing-only content.

Every standalone HTML keeps an understated source-jump action in the desktop header: neutral transparent fill, a thin control rule, 13px medium text, 7px by 12px padding, 6px corners and a 36px minimum height. Hover uses the quiet surface; the action hides at 600px and below. The existing public-detail-control and public-detail-source token names now describe this shared core component as well. Public detail pages additionally place a translated Back to examples link above the detail heading, with an authored 16px arrow, 13px medium text and a 36px minimum height. Back and the wordmark preserve the selected interface language and theme in their destination query. Back targets the examples anchor; an offline file uses the canonical public URL as its fallback. Both the public back link and standalone header source action hide in export-frame mode. These public additions do not change raw skill language selection or the exported graph framing.

### Component Graph and Motion

Nodes and neutral relationships sit within a quiet diagram frame; grouped graphs retain their subtle group bounds. Measured node titles are followed by short responsibility captions: authored captions are limited to 180 characters, including translations, and render in at most two lines with an explicit ellipsis when clipped. Without an authored caption, the description or kind supplies the fallback. Full text remains in the inspector and tooltip. Edge labels are measured and wrapped to at most three lines; a diagram-surface stroke behind text keeps routes readable. Node and relationship identities, evidence and selection remain canonical. Selection and active paths use blue outlines and pale blue interiors; inferred edges retain dashed (`5 4`) styling and inferred nodes retain their separate marker. Focus strengthens outlines; Focus and Path modes dim unrelated graph content to 0.22 opacity.

Presentation selects geometry rather than inventing topology. Automatic flow is limited to an ungrouped acyclic chain of 3–6 components with enough available width; other graphs retain layered layout. Explicit flow supports 1–8 main components plus up to two top and two bottom shared components, each an existing sourced node ID used in only one band. Bands cannot be combined with groups or layered hints. Flow follows physical page width: below 800px the main components run downward, while wider pages run left to right; expanding the dialog does not substitute pane width for this page-width decision. Main-flow layer spacing is 24px. On narrow pages, shared-band title and caption measurement is clamped to the available text width, with a 204px minimum, so long shared bars do not create excessively wide text lines. Orthogonal routing keeps shared-component relationships out of node bodies while preserving branches, cycles, parallel edges and self-edges. Nested layered relationships retain their declared container geometry.

The expand control moves the existing graph pane into a native modal dialog rather than creating a second SVG. Selection persists, geometry is recalculated for the new space, and collapse restores the pane and its previous camera. If the expanded fit would scale below 0.55, it opens a readable detail centered on the selected node, targeting one logical diagram unit per screen pixel, instead of reducing every label to a tiny overview. A short pan hint explains how to explore and return to the full graph. Explicit pan, zoom and Fit choices take precedence over automatic readable-detail framing; Fit restores the overview. The phone expand control includes a visible translated label, and expanded graph actions wrap within the available width. Escape collapses the dialog and restores the expand control's focus. Inspect selection collapses it and focuses the source-code tab for the selected component or relationship. Full-graph Fit is an overview on a narrow phone; reading individual captions uses the expanded detail and panning. Cached-layout projections retain their measured typography alongside geometry so captions and titles use the same line measurements as the cached nodes. HTML downloaded while expanded normalizes the pane back into the workspace, closes the dialog and resets expansion state. Export-frame controls hide the expand and expanded-inspection actions.

Playback is explicit and supports deterministic seeking; scrolling does not start graph playback. On the landing, the background moves by 0.075 times scroll distance, capped at 700px of input scroll (52.5px translation). Section headings, example rows, the installation surface, guide articles, the export showcase and the privacy note reveal according to scroll progress. Between 94% and 68% of viewport height, each pending element moves from 20px below its resting position to zero while opacity rises from 0.22 to 1. There is no timed reveal or blur. On reaching full progress the element is completed and its transient styles are removed. Keyboard focus or navigation to an anchor completes the relevant reveal immediately. Scroll and resize updates use animation frames with geometry reads batched before writes.

Content is visible by default without scripts. Reduced motion completes pending reveals, stops landscape translation, removes the loading spinner animation and changes smooth scrolling to automatic; the stylesheet also forces reveal content fully visible without translation. This does not claim a universal reduced-motion policy for every animated export.

## Do's and Don'ts

### Do:
- **Do** use purposeful blue for actions, focus and graph selection within the surface's documented palette.
- **Do** preserve flat thin-ruled tooling over the public landscape and keep photographic styling scoped to that public surface.
- **Do** retain Rethink on the landing, Atkinson in standalone explanations and graph labels, and monospace for literal code and source identity.
- **Do** preserve intrinsic landing tablet rows and the automatic mobile graph-pane height so controls and evidence remain in flow.
- **Do** retain five bundled interface languages, explicit appearance choices, keyboard states and distinct graph-language availability.
- **Do** preserve source meaning and offline assets across interactive and exported projections.
- **Do** retain prompt or origin provenance for every shipping raster.

### Don't:
- **Don't** introduce childish orange 3D plates, glow, plastic surfaces, oversized gradient actions or neon instrument styling.
- **Don't** bake the graph, controls or source evidence into a photographic asset.
- **Don't** impose a linear chain on graph data that contains branches, parallel relationships or cycles.
- **Don't** replace authored action SVG with Unicode arrow icon substitutes.
- **Don't** turn tiny helper metadata, SVG-coordinate labels, the hero composition or isolated colors into universal design rules.
- **Don't** describe static source explanations as runtime recordings or treat design documentation as a closed build gate or publication receipt.
