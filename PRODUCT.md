# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated: the user leaves implementation choices to the agent and prioritizes exceptional visual quality. Use a static HTML/CSS/JavaScript player and GitHub Pages site, a small Python builder, and Playwright-based export. Keep runtime dependencies out of generated HTML.

## Users

People opening an unfamiliar repository who want to understand how it works, especially how one named feature goes from input to result.

## Product Purpose

An open agent skill that extracts relevant repository components and relationships into an explicit source-grounded graph, then visualizes that same graph professionally. Interactive HTML, animated paths, video and static exports are projections of the graph.

## Operating Context

The user confirmed Codex and Claude Code as first-release targets. The skill works with the repository context available to the coding agent. Its output is viewed in a browser, shared as a file, or embedded as an animated GIF.

## Capabilities and Constraints

- Primary artifact: a component graph with inspectable sources, branches, cycles, parallel relationships and groups. A selected feature can have an animated path through that graph; a path is optional and does not determine the graph's topology.
- Users can choose a visualization and an export format; animated GIF is an explicit requirement.
- Map, Focus and Path use one shared graph model. HTML, PNG, SVG, GIF, MP4 and WebM are supported; HyperFrames is an optional adapter.
- The requested public presentation is GitHub Pages. The user wants a release prepared for 8 November 2026.
- Research, proposals, and joint selection precede the final implementation.
- Repo Visualizer is the product name. Original code is MIT-licensed with separately licensed vendored assets. The public repository is HonzaCuhel/repo-visualizer; private test examples are not authorized for publication.

## Brand Commitments

The user asks for an extremely simple, professional product with exceptional visual quality, using stack-diagram and stacks.caru.moe as references for craft and ease of adoption. They explicitly rejected the orange exploded-plate concept as scam-like and childish. Preserve flat diagrams, disciplined typography, quiet colors, conventional compact controls and readable code. Do not use playful 3D plates, glow, plastic surfaces, large gradient buttons or a neon instrument costume. The user selected composition B (Story and source), with the explicit refinement that its linear chain must become a potentially complex component graph. Keep its navigation/component area, central graph and source detail; topology follows the repository rather than the comp's five-step example.

## Evidence on Hand

- Research: reports/Vizuální průvodce fungováním repozitáře.md.
- Structural comparison: concepts/view-comparison-preview.html uses clearly labeled synthetic data.
- Reference source snapshots: concepts/reference-source/, from caru-ini/stack-diagram commit 1ed53e3e9525364ae5d82e0430f2bb3f7ef4c838, with MIT attribution.
- Three authorized repositories are used for local validation. Their source snapshots and generated graphs stay outside the public distribution.
- Private repository internals are excluded from the public showcase and distribution.

## Product Principles

- Answer the user's question about behavior with a small, readable story.
- Tie important claims to source code; distinguish interpretation from observed execution.
- Keep the same meaning across interactive and exported outputs.
- Make installation and first use simple across the two confirmed coding agents.
