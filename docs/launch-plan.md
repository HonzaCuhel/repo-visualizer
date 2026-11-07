# Launch plan

The launch asset is the product doing one useful job: a real question, a nonlinear graph, one selected component with code evidence, and an exported animation. A polished screenshot alone does not demonstrate extraction or correctness.

## Before launch

- Publish a small, complete v0.1.0 skill with a checksum, clear dependencies and a tested fresh-install path for Codex and Claude Code. Record which agent tests actually ran.
- Ship an interactive public-source demo directly on GitHub Pages. A visitor should explore it without registration, then download its portable HTML or install the skill.
- Capture a 12–20 second MP4 and a compact README GIF from the same scene. Show a branch or retry loop, selection and a code reference. Keep labels legible on a phone.
- Use a public repository and preserve attribution. Private validation results stay local. Do not claim a static graph is a recorded runtime trace.
- Check project-subpath URLs, offline HTML, all downloads, keyboard controls, reduced motion and a real export from the packaged skill.

## Positioning to test

“Ask how a feature works. Get a component graph you can explore, verify against code, and share as HTML or video.”

The distinction is the combination of a local coding-agent workflow, one explicit graph model, readable nonlinear topology and source-grounded explanation. Existing tools already offer architecture diagrams, source links and videos; avoid “first ever” claims.

## First week

| When | Action for the author | Evidence to collect |
| --- | --- | --- |
| Before public launch | Invite 5–10 developers who are reading an unfamiliar repository to try one real question | Can they install, finish a graph and explain its main mechanism? |
| Release day | Publish the release, Pages demo and README animation; share one concrete example on the author's own channels | Demo visits, release downloads, meaningful questions |
| After initial feedback | Write one short walkthrough of an actual feature and its surprising failure/retry branch | Which part helped, and which claim was wrong? |
| When the demo is ready | Consider Show HN and one relevant community, follow current rules and stay available for discussion | Actual users trying the demo, not coordinated votes |
| Days 2–7 | Fix extraction or usability failures; add an attributed public example with permission | Successful first exports and repeat usage |

The user sends invitations and posts. No outreach or external posting is performed automatically. Hacker News currently requires human-authored text; prepare facts, then write the post and replies yourself. Recheck community rules on the day of posting. Do not ask for coordinated upvotes or use star gating.

## Facts for a human-written launch post

Use only facts verified in the actual release: supported agents, which repositories were tested, exported formats, whether the HTML works offline, exact installation command and limitations. Include one real question and the directly explorable result. Explain that the agent authors the semantic graph; the static inventory is a starting point, not automatic proof of architecture.

## Measure useful adoption

Initial experimental targets: 10 people try the output, 5 complete an export, 3 can explain the input, main branch and result after exploring it. These are learning targets, not predicted outcomes. Record wrong explanations as bugs.

Track release downloads, installations where available, successful first exports, meaningful issues and public examples contributed with permission. Stars and visits are secondary signals. GitHub traffic history is short; save snapshots if the author wants a launch comparison. A download does not prove an active user, and no strategy guarantees stars.

References: [Show HN guidelines](https://news.ycombinator.com/showhn.html), [HN guidelines](https://news.ycombinator.com/newsguidelines.html), [GitHub traffic](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository), [Agent Skills specification](https://agentskills.io/specification), [skills CLI](https://github.com/vercel-labs/skills). Research checked 7 November 2026; community rules and installation behavior should be rechecked at publication.
