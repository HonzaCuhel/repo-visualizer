(() => {
  "use strict";
  const $ = (id) => document.getElementById(id),
    baseStory = JSON.parse($("repo-data").textContent),
    NS = "http://www.w3.org/2000/svg";
  const t = (key, values) => window.repoAppearance.t(key, values);
  function localizedStory() {
    const value = JSON.parse(JSON.stringify(baseStory));
    const display = baseStory.translations?.[window.repoAppearance.language];
    if (!display) return value;
    for (const [key, translated] of Object.entries(display)) {
      if (["nodes", "edges", "groups", "steps", "scenarios"].includes(key)) {
        for (const item of value[key])
          Object.assign(item, translated[item.id] || {});
      } else if (key === "overview") {
        value.overview = { ...value.overview, ...translated };
      } else value[key] = translated;
    }
    value.language = window.repoAppearance.language;
    return value;
  }
  let S = localizedStory();
  const nodes = new Map(S.nodes.map((n) => [n.id, n])),
    edges = new Map(S.edges.map((e) => [e.id, e])),
    sources = new Map(S.sources.map((s) => [s.id, s])),
    steps = new Map(S.steps.map((s) => [s.id, s]));
  const diagram = $("diagram"),
    positions = new Map(),
    nodeLines = new Map(),
    edgeElements = new Map(),
    nodeElements = new Map();
  let inspectedKey = null;
  let layout = null,
    bounds = null,
    camera = null,
    view = S.default_view || "map",
    selected = { type: "node", id: S.nodes[0].id },
    scenarioId = S.scenarios[0]?.id || "tour",
    current = 0,
    playing = false,
    codeMode = false,
    exporting = false,
    cancelled = false;
  const iconPaths = {
    module: "M4 4h16v16H4zM4 9h16M9 9v11",
    function: "M8 5H6L3 12l3 7h2M16 5h2l3 7-3 7h-2",
    service: "M4 4h16v6H4zM4 14h16v6H4zM7 7h.1M7 17h.1",
    store:
      "M4 6c0-4 16-4 16 0v12c0 4-16 4-16 0zM4 6c0 4 16 4 16 0M4 12c0 4 16 4 16 0",
    queue: "M4 6h16M4 12h16M4 18h16",
    decision: "m12 2 10 10-10 10L2 12z",
    external: "M14 3h7v7M21 3l-10 10M10 4H4v16h16v-6",
    input: "M10 4h10v16H10M3 12h12M10 7l5 5-5 5",
    output: "M14 4H4v16h10M10 12h11M16 7l5 5-5 5",
    actor: "M16 6a4 4 0 1 1-8 0 4 4 0 0 1 8 0M4 21v-3c0-6 16-6 16 0v3",
    artifact: "M5 3h9l5 5v13H5zM14 3v6h5",
    process: "M4 6h16v12H4zM8 10h8M8 14h5",
  };
  const playerIcons = {
    play: '<path d="m8 5 11 7-11 7z"/>',
    pause: '<path d="M8 5v14M16 5v14"/>',
    previous: '<path d="M6 5v14m12-14-9 7 9 7z"/>',
    next: '<path d="M18 5v14M6 5l9 7-9 7z"/>',
  };
  function icon(name) {
    return (
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' +
      (iconPaths[name] || iconPaths.module) +
      '"/></svg>'
    );
  }
  function setPlayIcon() {
    $("play").innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true">' +
      playerIcons[playing ? "pause" : "play"] +
      "</svg>";
    $("play").setAttribute("aria-label", playing ? t("pause") : t("play"));
  }
  $("previous").innerHTML =
    '<svg viewBox="0 0 24 24" aria-hidden="true">' +
    playerIcons.previous +
    "</svg>";
  $("next").innerHTML =
    '<svg viewBox="0 0 24 24" aria-hidden="true">' +
    playerIcons.next +
    "</svg>";
  setPlayIcon();
  function text(tag, value, className) {
    const el = document.createElement(tag);
    el.textContent = value ?? "";
    if (className) el.className = className;
    return el;
  }
  function svg(tag, attributes = {}, value) {
    const el = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attributes)) el.setAttribute(k, v);
    if (value !== undefined) el.textContent = value;
    return el;
  }
  function slug() {
    return (
      S.title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "")
        .slice(0, 70) || "repository-graph"
    );
  }
  function status(message) {
    $("player-status").textContent = message;
  }
  function tour() {
    if (scenarioId === "tour" || !S.scenarios.length)
      return orderedNodes().map((n) => ({
        id: "tour-" + n.id,
        title: n.label,
        description: n.description,
        node_ids: [n.id],
        edge_ids: [],
        source_ids: n.source_ids,
        duration_ms: 2200,
        tour: true,
      }));
    const scenario = S.scenarios.find((s) => s.id === scenarioId);
    return scenario.step_ids.map((id) => steps.get(id));
  }
  function duration() {
    return tour().reduce((a, s) => a + s.duration_ms, 0);
  }
  function activeAt(ms) {
    const ts = tour();
    let start = 0,
      index = 0;
    for (; index < ts.length - 1; index++) {
      if (ms < start + ts[index].duration_ms) break;
      start += ts[index].duration_ms;
    }
    return {
      step: ts[index],
      index,
      progress: Math.min(1, Math.max(0, (ms - start) / ts[index].duration_ms)),
      start,
    };
  }
  function time(ms) {
    const sec = Math.floor(ms / 1000);
    return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2, "0");
  }
  function refreshIntro() {
    if (window.REPO_LANDING) return;
    $("page-title").removeAttribute("data-i18n");
    $("page-title").textContent = S.title;
    const full = S.summary || S.question;
    const first = full.split(/(?<=[.!?])\s+/)[0];
    let lead = S.overview?.lead || (full.length > 220 ? first : full);
    if (lead.length > 240)
      lead = lead.slice(0, 237).replace(/\s+\S*$/, "") + "…";
    $("page-description").textContent = lead;
    $("intro-details").hidden = full === lead;
    $("intro-details-copy").textContent = full;
    const meta = $("intro-metadata");
    meta.hidden = false;
    meta.replaceChildren();
    meta.append(
      text(
        "span",
        t("counts", { nodes: S.nodes.length, edges: S.edges.length }),
      ),
    );
    meta.append(
      text(
        "span",
        t("path") +
          ": " +
          new Intl.NumberFormat(window.repoAppearance.language, {
            maximumFractionDigits: 1,
          }).format(duration() / 1000) +
          " s",
      ),
    );
    meta.append(text("span", t("staticAnalysis")));
    if (S.repo.commit) {
      const revision = text("code", S.repo.commit.slice(0, 7));
      revision.title = S.repo.commit;
      meta.append(revision);
    }
    const list = $("overview-path");
    list.replaceChildren();
    list.hidden = !S.overview?.path?.length;
    list.setAttribute("aria-label", t("overview"));
    for (const [index, part] of (S.overview?.path || []).entries()) {
      const item = text("li", "");
      if (index)
        item.insertAdjacentHTML(
          "beforeend",
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16m-6-6 6 6-6 6"/></svg>',
        );
      const button = text(
        "button",
        part.label || nodes.get(part.node_id).label,
      );
      button.title = nodes.get(part.node_id).description;
      button.addEventListener("click", () => {
        select("node", part.node_id);
        $("workspace").scrollIntoView({ block: "start" });
      });
      item.append(button);
      list.append(item);
    }
  }
  function configureTimeline() {
    const select = $("scenario");
    select.replaceChildren();
    for (const sc of S.scenarios) {
      const option = text("option", sc.label);
      option.value = sc.id;
      select.append(option);
    }
    const option = text("option", t("tour"));
    option.value = "tour";
    select.append(option);
    select.value = scenarioId;
    $("seek").max = String(duration());
    $("tour-note").textContent =
      scenarioId === "tour" ? t("tourNote") : t("pathNote");
    refreshIntro();
  }
  function select(type, id, { fromTimeline = false, announce = true } = {}) {
    if (
      type === "node" ? !nodes.has(id) : type === "edge" ? !edges.has(id) : true
    )
      throw Error("Unknown graph selection: " + type + " " + id);
    if (!fromTimeline) pause();
    selected = { type, id };
    paint();
    inspect();
    if (dialog.open && !fromTimeline) ensureReadable(true);
    if (announce)
      status(
        t(type === "node" ? "selectedNode" : "selectedEdge", {
          label:
            type === "node"
              ? nodes.get(id).label
              : edges.get(id).label || edges.get(id).relation,
        }),
      );
  }
  function adjacency(id) {
    const found = new Set([id]);
    for (const e of S.edges)
      if (e.from === id || e.to === id) {
        found.add(e.from);
        found.add(e.to);
      }
    return found;
  }
  function paint(active = null) {
    if (!layout) return;
    const highlight = active || activeAt(current);
    const ids = new Set(
      view === "path"
        ? highlight.step.node_ids
        : selected.type === "node"
          ? [selected.id]
          : [edges.get(selected.id).from, edges.get(selected.id).to],
    );
    const near = selected.type === "node" ? adjacency(selected.id) : ids;
    for (const [id, el] of nodeElements) {
      el.classList.toggle(
        "is-selected",
        selected.type === "node" && selected.id === id,
      );
      el.classList.toggle("is-active", view === "path" && ids.has(id));
      el.classList.toggle(
        "is-dimmed",
        view === "focus"
          ? !near.has(id)
          : view === "path"
            ? !ids.has(id)
            : false,
      );
    }
    for (const [id, el] of edgeElements) {
      const e = edges.get(id),
        activeEdge = view === "path" && highlight.step.edge_ids.includes(id);
      el.classList.toggle(
        "is-selected",
        selected.type === "edge" && selected.id === id,
      );
      el.classList.toggle("is-active", activeEdge);
      el.classList.toggle(
        "is-dimmed",
        view === "focus"
          ? !(e.from === selected.id || e.to === selected.id)
          : view === "path"
            ? !activeEdge
            : false,
      );
      const pulse = el.querySelector(".edge-pulse"),
        path = el.querySelector(".edge-line");
      pulse.setAttribute("visibility", activeEdge ? "visible" : "hidden");
      if (activeEdge && path.getTotalLength()) {
        const p = path.getPointAtLength(
          path.getTotalLength() * highlight.progress,
        );
        pulse.setAttribute("cx", p.x);
        pulse.setAttribute("cy", p.y);
      }
    }
    for (const button of $("component-list").querySelectorAll("button"))
      button.setAttribute(
        "aria-pressed",
        String(selected.type === "node" && button.dataset.node === selected.id),
      );
  }
  function inspect() {
    const key = selected.type + ":" + selected.id + ":" + codeMode;
    if (key === inspectedKey) return;
    inspectedKey = key;
    const item =
      selected.type === "node"
        ? nodes.get(selected.id)
        : edges.get(selected.id);
    $("selection-meta").textContent =
      (selected.type === "node"
        ? t(item.kind)
        : t("relationship") + " · " + item.relation) +
      (item.evidence === "inferred"
        ? " · " + t("inferred")
        : " · " + t("grounded"));
    $("selection-title").textContent =
      selected.type === "node" ? item.label : item.label || item.relation;
    const description =
      selected.type === "node"
        ? item.description
        : nodes.get(item.from).label + " → " + nodes.get(item.to).label;
    $("selection-description").textContent =
      (description || t("inspectSource")) +
      (item.evidence === "inferred" ? " " + t("inference") + item.reason : "");
    const connections = $("connections");
    connections.replaceChildren();
    for (const edge of selected.type === "node"
      ? S.edges.filter((e) => e.from === selected.id || e.to === selected.id)
      : []) {
      const button = document.createElement("button");
      button.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h18m-6-6 6 6-6 6"/></svg>';
      const other =
        edge.from === selected.id ? nodes.get(edge.to) : nodes.get(edge.from);
      button.append(
        text(
          "span",
          (edge.from === selected.id ? "" : t("from")) +
            other.label +
            " · " +
            (edge.label || edge.relation),
        ),
      );
      button.addEventListener("click", () => select("edge", edge.id));
      connections.append(button);
    }
    const container = $("source-content");
    container.replaceChildren();
    for (const id of item.source_ids) {
      const source = sources.get(id),
        entry = text("section", "", "source-entry"),
        head = text("div", "", "source-heading"),
        open = text(
          "button",
          source.path + " · L" + source.start + "–" + source.end,
        );
      open.title = t("showCode");
      open.addEventListener("click", () => setCodeMode(!codeMode));
      head.append(open);
      if (source.url) {
        const a = text("a", t("openSource") + " ");
        a.insertAdjacentHTML(
          "beforeend",
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>',
        );
        a.href = source.url;
        a.target = "_blank";
        a.rel = "noopener";
        head.append(a);
      }
      entry.append(head);
      const pre = document.createElement("pre"),
        code = document.createElement("code");
      code.textContent = source.excerpt;
      pre.append(code);
      pre.hidden = !codeMode;
      entry.append(pre);
      const revision = text(
        "p",
        (source.revision === "commit"
          ? source.commit.slice(0, 7)
          : t("workingTree")) +
          " · SHA256 " +
          source.sha256.slice(0, 12),
        "source-revision",
      );
      revision.hidden = !codeMode;
      entry.append(revision);
      container.append(entry);
    }
    if (!item.source_ids.length)
      container.append(text("p", t("noSource"), "source-revision"));
    $("overview-content").hidden = codeMode;
    $("overview-tab").setAttribute("aria-pressed", String(!codeMode));
    $("code-tab").setAttribute("aria-pressed", String(codeMode));
  }
  function setCodeMode(value) {
    codeMode = value;
    inspect();
  }
  function fillComponents() {
    const list = $("component-list");
    list.replaceChildren();
    const query = $("component-search").value.trim().toLowerCase();
    const levels = S.presentation?.levels;
    for (const n of orderedNodes().filter((n) =>
      (n.label + " " + n.kind + " " + n.description)
        .toLowerCase()
        .includes(query),
    )) {
      const b = document.createElement("button");
      b.className = "component-item";
      b.dataset.node = n.id;
      if (levels) {
        const rank = levels.findIndex((row) => row.includes(n.id));
        b.dataset.level = rank;
        const badge = text("span", rank + 1, "component-order");
        badge.setAttribute("aria-hidden", "true");
        b.append(badge);
        b.title =
          t("mechanismPhase", { number: rank + 1 }) +
          (levels[rank].length > 1 ? " · " + t("parallelComponents") : "");
      }
      b.setAttribute(
        "aria-pressed",
        String(selected.type === "node" && selected.id === n.id),
      );
      const mark = text("span", "", "component-mark");
      mark.innerHTML = icon(n.kind);
      b.append(mark, text("span", n.label, "component-label"));
      b.addEventListener("click", () => select("node", n.id));
      list.append(b);
    }
    $("no-components").hidden = Boolean(list.childElementCount);
  }
  function orderedNodes() {
    const levels = S.presentation?.levels;
    if (levels) return levels.flat().map((id) => nodes.get(id));
    return [...S.nodes].sort((a, b) => {
      const left = positions.get(a.id),
        right = positions.get(b.id);
      if (!left || !right) return 0;
      return Math.abs(left.y - right.y) > 16
        ? left.y - right.y
        : left.x - right.x;
    });
  }
  function setView(value) {
    if (!["map", "focus", "path"].includes(value))
      throw Error("Unknown graph view");
    view = value;
    for (const button of document.querySelectorAll("[data-view]"))
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.view === value),
      );
    paint();
    status(
      value === "focus"
        ? t("focusStatus")
        : value === "path"
          ? t("pathStatus")
          : t("mapStatus"),
    );
  }
  function pathFromPoints(points) {
    if (points.length < 2) return "";
    let d = "M" + points[0].x + " " + points[0].y;
    for (let i = 1; i < points.length - 1; i++) {
      const a = points[i - 1],
        b = points[i],
        c = points[i + 1],
        ab = Math.hypot(b.x - a.x, b.y - a.y),
        bc = Math.hypot(c.x - b.x, c.y - b.y),
        r = Math.min(7, ab / 2, bc / 2);
      if (!ab || !bc) continue;
      const p = {
          x: b.x + ((a.x - b.x) * r) / ab,
          y: b.y + ((a.y - b.y) * r) / ab,
        },
        q = {
          x: b.x + ((c.x - b.x) * r) / bc,
          y: b.y + ((c.y - b.y) * r) / bc,
        };
      d +=
        " L" + p.x + " " + p.y + " Q" + b.x + " " + b.y + " " + q.x + " " + q.y;
    }
    const last = points[points.length - 1];
    return d + " L" + last.x + " " + last.y;
  }
  let layoutSerial = 0;
  async function layOut() {
    const serial = ++layoutSerial,
      measurements = new Map();
    const groupMap = new Map(
      S.groups.map((g) => [
        g.id,
        {
          id: g.id,
          children: [],
          layoutOptions: {
            "elk.direction": "DOWN",
            "elk.padding": "[top=42,left=24,bottom=24,right=24]",
            "elk.spacing.nodeNode": "36",
            "elk.layered.spacing.nodeNodeBetweenLayers": "20",
          },
        },
      ]),
    );
    const children = [];
    for (const g of S.groups) {
      const item = groupMap.get(g.id);
      if (g.parent) groupMap.get(g.parent).children.push(item);
      else children.push(item);
    }
    for (const n of S.nodes) {
      const data = window.repoDiagram.measureNode(n, t(n.kind)),
        item = { id: n.id, width: data.width, height: data.height };
      measurements.set(n.id, data);
      if (n.group) groupMap.get(n.group).children.push(item);
      else children.push(item);
    }
    const model = {
      id: "__repo-root",
      layoutOptions: {
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
        "elk.hierarchyHandling": "INCLUDE_CHILDREN",
        "elk.edgeRouting": "ORTHOGONAL",
        "elk.randomSeed": "42",
        "elk.spacing.nodeNode": "36",
        "elk.layered.spacing.nodeNodeBetweenLayers": "36",
        "elk.spacing.edgeNode": "22",
        "elk.padding": "[top=18,left=18,bottom=18,right=18]",
      },
      children,
      edges: S.edges.map((e) => ({
        id: e.id,
        sources: [e.from],
        targets: [e.to],
        labels: e.label
          ? [{ text: e.label, ...window.repoDiagram.measureEdge(e) }]
          : [],
      })),
    };
    let nextLayout;
    if (window.REPO_PRECOMPUTED_LAYOUT) {
      nextLayout = JSON.parse(JSON.stringify(window.REPO_PRECOMPUTED_LAYOUT));
      if (nextLayout.typography) {
        measurements.clear();
        for (const [id, data] of Object.entries(nextLayout.typography))
          measurements.set(id, data);
      }
    } else {
      nextLayout = await window.repoDiagram.layOut(
        model,
        S,
        {
          width: $("graph-stage").clientWidth,
          height: $("graph-stage").clientHeight,
          pageWidth: innerWidth,
        },
        measurements,
        (id) => t(nodes.get(id).kind),
      );
    }
    if (serial !== layoutSerial) return;
    nextLayout.typography = Object.fromEntries(measurements);
    layout = nextLayout;
    nodeLines.clear();
    for (const [id, data] of measurements) nodeLines.set(id, data);
    diagram.dataset.layout = layout.layoutMode || "layered";
    draw();
    fillComponents();
    fit();
    $("loading").hidden = true;
    paint();
  }
  function draw() {
    diagram.replaceChildren();
    positions.clear();
    edgeElements.clear();
    nodeElements.clear();
    const defs = svg("defs");
    for (const [id, color] of [
      ["arrow", "var(--edge-line)"],
      ["arrow-active", "var(--blue)"],
    ]) {
      const marker = svg("marker", {
        id,
        viewBox: "0 0 10 10",
        refX: 9,
        refY: 5,
        markerWidth: 6,
        markerHeight: 6,
        orient: "auto-start-reverse",
        markerUnits: "strokeWidth",
      });
      marker.append(svg("path", { d: "M1 1 9 5 1 9z", fill: color }));
      defs.append(marker);
    }
    diagram.append(
      defs,
      svg("rect", {
        class: "diagram-frame",
        x: -10,
        y: -10,
        width: layout.width + 20,
        height: layout.height + 20,
        rx: 16,
      }),
    );
    const groupsLayer = svg("g"),
      edgeLayer = svg("g"),
      nodeLayer = svg("g");
    diagram.append(groupsLayer, edgeLayer, nodeLayer);
    const routed = [];
    const containerPositions = new Map();
    function walk(item, ox = 0, oy = 0) {
      const x = ox + (item.x || 0),
        y = oy + (item.y || 0);
      containerPositions.set(item.id, { x, y });
      if (item !== layout) {
        if (nodes.has(item.id)) {
          positions.set(item.id, {
            x,
            y,
            width: item.width,
            height: item.height,
          });
        } else if (S.groups.some((g) => g.id === item.id)) {
          const group = S.groups.find((g) => g.id === item.id),
            g = svg("g", { class: "graph-group" });
          g.append(
            svg("rect", {
              x,
              y,
              width: item.width,
              height: item.height,
              rx: 10,
            }),
            svg("text", { x: x + 16, y: y + 23 }, group?.label || item.id),
          );
          groupsLayer.append(g);
        }
      }
      for (const edge of item.edges || []) routed.push({ edge, x, y });
      for (const child of item.children || []) walk(child, x, y);
    }
    walk(layout);
    for (const routedEdge of routed) {
      const { edge } = routedEdge;
      // ELK can return an edge on the root while expressing its section and
      // label coordinates in a nested container's coordinate system.
      const { x, y } = containerPositions.get(edge.container) || routedEdge;
      const e = edges.get(edge.id);
      if (!e) continue;
      const g = svg("g", {
        class: "graph-edge" + (e.evidence === "inferred" ? " is-inferred" : ""),
        "data-edge": e.id,
        role: "button",
        tabindex: 0,
        "aria-label":
          nodes.get(e.from).label +
          " " +
          (e.label || e.relation) +
          " " +
          nodes.get(e.to).label,
      });
      for (const section of edge.sections || []) {
        const points = [
          section.startPoint,
          ...(section.bendPoints || []),
          section.endPoint,
        ].map((p) => ({ x: p.x + x, y: p.y + y }));
        const d = pathFromPoints(points);
        g.append(
          svg("path", { class: "edge-hit", d }),
          svg("path", { class: "edge-line", d, "marker-end": "url(#arrow)" }),
        );
      }
      for (const label of edge.labels || []) {
        const lines = window.repoDiagram.measureEdge(e).lines;
        const value = svg("text", {
          x: x + label.x + label.width / 2,
          y: y + label.y + 14,
          "text-anchor": "middle",
        });
        lines.forEach((line, i) =>
          value.append(
            svg(
              "tspan",
              { x: x + label.x + label.width / 2, dy: i ? 18 : 0 },
              line,
            ),
          ),
        );
        g.append(value);
      }
      g.append(svg("title", {}, e.label || e.relation));
      g.append(
        svg("circle", { class: "edge-pulse", r: 3, visibility: "hidden" }),
      );
      g.addEventListener("click", () => select("edge", e.id));
      g.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          select("edge", e.id);
        }
      });
      edgeLayer.append(g);
      edgeElements.set(e.id, g);
    }
    for (const n of S.nodes) {
      const p = positions.get(n.id);
      if (!p) throw Error("Layout did not return component " + n.id);
      const g = svg("g", {
        class:
          "graph-node" +
          ([
            ...(S.presentation?.top || []),
            ...(S.presentation?.bottom || []),
          ].includes(n.id)
            ? " shared-band"
            : ""),
        transform: `translate(${p.x},${p.y})`,
        "data-node": n.id,
        role: "button",
        tabindex: 0,
        "aria-label": n.label + " · " + t(n.kind),
      });
      g.append(svg("rect", { width: p.width, height: p.height, rx: 9 }));
      const data = nodeLines.get(n.id);
      const label = svg("text", {
        class: "node-title",
        x: p.width / 2,
        y: 36,
        "text-anchor": "middle",
      });
      data.title.forEach((line, i) =>
        label.append(svg("tspan", { x: p.width / 2, dy: i ? 24 : 0 }, line)),
      );
      g.append(label);
      if (data.caption.length) {
        const caption = svg("text", {
          class: "node-caption",
          x: p.width / 2,
          y: 36 + (data.title.length - 1) * 24 + 28,
          "text-anchor": "middle",
        });
        data.caption.forEach((line, i) =>
          caption.append(
            svg("tspan", { x: p.width / 2, dy: i ? 19 : 0 }, line),
          ),
        );
        g.append(caption);
      }
      if (data.inferred)
        g.append(
          svg(
            "text",
            {
              class: "node-kind",
              x: p.width / 2,
              y: p.height - 12,
              "text-anchor": "middle",
            },
            t("inferred"),
          ),
        );
      g.append(
        svg(
          "title",
          {},
          n.label + "\n" + (n.description || n.caption || t(n.kind)),
        ),
      );
      g.addEventListener("click", () => select("node", n.id));
      g.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          select("node", n.id);
        }
      });
      nodeLayer.append(g);
      nodeElements.set(n.id, g);
    }
    bounds = { x: -10, y: -10, w: layout.width + 20, h: layout.height + 20 };
    $("graph-count").textContent = t("counts", {
      nodes: S.nodes.length,
      edges: S.edges.length,
    });
  }
  function applyCamera() {
    if (camera)
      diagram.setAttribute(
        "viewBox",
        [camera.x, camera.y, camera.w, camera.h].join(" "),
      );
  }
  function fit() {
    if (!bounds) return;
    if ($("diagram-hint")) $("diagram-hint").hidden = true;
    camera = { ...bounds };
    applyCamera();
  }
  function zoom(factor) {
    if (!camera) return;
    readabilityRequested = false;
    const w = Math.max(bounds.w / 8, Math.min(bounds.w * 2, camera.w * factor)),
      h = (w * camera.h) / camera.w;
    camera = {
      x: camera.x + (camera.w - w) / 2,
      y: camera.y + (camera.h - h) / 2,
      w,
      h,
    };
    applyCamera();
  }
  function renderAt(ms) {
    const total = duration();
    current = Math.max(
      0,
      Math.min(total - 0.001, Number.isFinite(Number(ms)) ? Number(ms) : 0),
    );
    const active = activeAt(current),
      previousSelection = selected.id;
    selected = { type: "node", id: active.step.node_ids[0] };
    $("seek").value = String(current);
    $("elapsed").textContent = time(current) + " / " + time(total);
    $("step-count").textContent = active.index + 1 + " / " + tour().length;
    paint(active);
    inspect();
    if (readableDetail && previousSelection !== selected.id)
      ensureReadable(true);
    return {
      timeMs: current,
      durationMs: total,
      index: active.index,
      nodeIds: active.step.node_ids,
      edgeIds: active.step.edge_ids,
    };
  }
  window.renderAt = renderAt;
  function pause() {
    window.repoClock?.pause();
    playing = false;
    setPlayIcon();
  }
  function togglePlay() {
    if (!exporting) window.repoClock?.toggle();
  }
  function skip(offset) {
    pause();
    const active = activeAt(current),
      ts = tour(),
      next = Math.max(0, Math.min(ts.length - 1, active.index + offset));
    renderAt(ts.slice(0, next).reduce((a, s) => a + s.duration_ms, 0));
  }
  function setScenario(id) {
    if (id !== "tour" && !S.scenarios.some((s) => s.id === id))
      throw Error("Unknown scenario: " + id);
    pause();
    scenarioId = id;
    configureTimeline();
    renderAt(0);
  }
  const workspace = $("workspace"),
    dialog = $("diagram-dialog"),
    expandButton = $("expand-diagram");
  const graphDock = document.createElement("template");
  graphDock.id = "graph-dock";
  workspace.before(graphDock);
  let savedCamera = null,
    resizingDiagram = false;
  let readabilityRequested = false,
    readableDetail = false;
  function ensureReadable(force = false) {
    if (!dialog.open || !readabilityRequested || !camera || !bounds) return;
    let stage = $("graph-stage").getBoundingClientRect();
    const scale = Math.min(stage.width / camera.w, stage.height / camera.h);
    if (!force && scale >= 0.55) return;
    $("diagram-hint").hidden = false;
    stage = $("graph-stage").getBoundingClientRect();
    const id =
      selected.type === "node" ? selected.id : edges.get(selected.id)?.from;
    const node = positions.get(id) || positions.values().next().value;
    const w = stage.width,
      h = stage.height;
    const clamp = (center, size, start, total) =>
      size >= total
        ? start + (total - size) / 2
        : Math.max(start, Math.min(start + total - size, center - size / 2));
    camera = {
      x: clamp(node.x + node.width / 2, w, bounds.x, bounds.w),
      y: clamp(node.y + node.height / 2, h, bounds.y, bounds.h),
      w,
      h,
    };
    readableDetail = true;
    applyCamera();
  }
  function expansionIcon() {
    const expanded = dialog.open,
      key = expanded ? "collapseGraph" : "expandGraph";
    expandButton.dataset.i18nAria = expandButton.dataset.i18nTitle = key;
    expandButton.setAttribute("aria-label", t(key));
    expandButton.title = t(key);
    expandButton.setAttribute("aria-expanded", String(expanded));
    expandButton.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' +
      (expanded
        ? "M9 3v6H3m12-6v6h6M9 21v-6H3m12 6v-6h6"
        : "M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6") +
      '"/></svg>';
    const caption = text("span", t(key), "expand-label");
    caption.dataset.i18n = key;
    expandButton.append(caption);
  }
  async function toggleDiagram(force) {
    if (resizingDiagram) return;
    await window.repoReady;
    if (resizingDiagram) return;
    const open = force ?? !dialog.open;
    if (open === dialog.open) return;
    resizingDiagram = true;
    expandButton.disabled = true;
    try {
      if (open) {
        savedCamera = camera ? { ...camera } : null;
        readabilityRequested = true;
        readableDetail = false;
        dialog.append(workspace);
        dialog.showModal();
        document.body.classList.add("diagram-open");
      } else {
        dialog.close();
        readabilityRequested = readableDetail = false;
        $("diagram-hint").hidden = true;
        graphDock.after(workspace);
        document.body.classList.remove("diagram-open");
      }
      expansionIcon();
      await new Promise(requestAnimationFrame);
      await layOut();
      if (open) ensureReadable();
      if (!open && savedCamera) {
        camera = savedCamera;
        applyCamera();
      }
    } finally {
      resizingDiagram = false;
      expandButton.disabled = false;
      (open ? $("close-workspace") : expandButton).focus({
        preventScroll: true,
      });
    }
  }
  let resizeTimer;
  if ("ResizeObserver" in window)
    new ResizeObserver(() => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (
          !layout ||
          exporting ||
          resizingDiagram ||
          window.REPO_PRECOMPUTED_LAYOUT
        )
          return;
        if (
          window.repoDiagram.mode(
            S,
            $("graph-stage").getBoundingClientRect(),
          ) !== (layout.layoutMode || "layered") ||
          (layout.layoutMode === "flow" && layout.flowDirection !== "DOWN")
        )
          layOut().then(() => ensureReadable());
        else if (dialog.open) ensureReadable();
      }, 120);
    }).observe($("graph-stage"));
  expansionIcon();
  expandButton.addEventListener("click", () => toggleDiagram());
  $("close-workspace").addEventListener("click", () => toggleDiagram(false));
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    toggleDiagram(false);
  });
  $("inspect-expanded").addEventListener("click", async () => {
    $("code-tab").click();
    $("code-tab").focus();
  });
  function exportSVG() {
    const copy = diagram.cloneNode(true);
    copy.removeAttribute("id");
    copy.setAttribute("xmlns", NS);
    copy.setAttribute(
      "viewBox",
      [bounds.x, bounds.y, bounds.w, bounds.h].join(" "),
    );
    copy.setAttribute("width", Math.ceil(bounds.w));
    copy.setAttribute("height", Math.ceil(bounds.h));
    copy.setAttribute("role", "img");
    const style = svg(
      "style",
      {},
      $("player-style").textContent.replace(
        "url(assets/AtkinsonHyperlegibleNext.ttf)",
        "url(data:font/ttf;base64," +
          JSON.parse($("repo-font").textContent) +
          ")",
      ),
    );
    copy.insertBefore(style, copy.firstChild);
    const computed = getComputedStyle(document.documentElement);
    const tokenValues = [...computed]
      .filter((key) => key.startsWith("--"))
      .map((key) => key + ":" + computed.getPropertyValue(key))
      .join(";");
    style.textContent += "\nsvg{" + tokenValues + "}";
    copy.setAttribute("data-theme", window.repoAppearance.resolvedTheme);
    const background = svg("rect", {
      x: bounds.x,
      y: bounds.y,
      width: bounds.w,
      height: bounds.h,
      fill: getComputedStyle(document.documentElement)
        .getPropertyValue("--paper")
        .trim(),
    });
    copy.insertBefore(background, style.nextSibling);
    copy.prepend(svg("title", {}, S.question));
    copy.append(
      svg(
        "metadata",
        {},
        JSON.stringify({
          title: S.title,
          repo: S.repo,
          licenses: document.querySelector(".player-footer details").innerText,
          source: "https://github.com/HonzaCuhel/repo-visualizer",
        }),
      ),
    );
    return new XMLSerializer().serializeToString(copy);
  }
  function download(blob, name) {
    const url = URL.createObjectURL(blob),
      a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function rasterFrame(ms, width = 960, height = 640) {
    renderAt(ms);
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = getComputedStyle(document.documentElement)
      .getPropertyValue("--paper")
      .trim();
    ctx.fillRect(0, 0, width, height);
    const image = new Image(),
      url = URL.createObjectURL(
        new Blob([exportSVG()], { type: "image/svg+xml;charset=utf-8" }),
      );
    try {
      await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = () => reject(Error(t("rasterFailed")));
        image.src = url;
      });
      const scale = Math.min(
          (width - 48) / bounds.w,
          (height - 135) / bounds.h,
        ),
        w = bounds.w * scale,
        h = bounds.h * scale;
      ctx.drawImage(image, (width - w) / 2, 70 + (height - 135 - h) / 2, w, h);
      ctx.fillStyle = getComputedStyle(document.documentElement)
        .getPropertyValue("--ink")
        .trim();
      ctx.font = "600 22px Atkinson";
      ctx.fillText(S.title, 24, 33, width - 48);
      const active = activeAt(current);
      ctx.font = "16px Atkinson";
      ctx.fillStyle = getComputedStyle(document.documentElement)
        .getPropertyValue("--selected-ink")
        .trim();
      ctx.fillText(active.step.title, 24, height - 36, width - 48);
      ctx.font = "11px Atkinson";
      ctx.fillStyle = getComputedStyle(document.documentElement)
        .getPropertyValue("--muted")
        .trim();
      ctx.fillText(
        (scenarioId === "tour" ? t("tourNote") : t("pathNote")) +
          "   " +
          time(ms) +
          " / " +
          time(duration()),
        24,
        height - 15,
        width - 48,
      );
      return canvas;
    } finally {
      URL.revokeObjectURL(url);
    }
  }
  async function browserExport(format) {
    if (exporting) return;
    const old = { time: current, view, selected: { ...selected } };
    pause();
    exporting = true;
    cancelled = false;
    document.body.classList.add("export-busy");
    $("export-progress").hidden = false;
    const message = (value) => ($("export-message").textContent = value);
    try {
      if (format === "html") {
        const copy = document.documentElement.cloneNode(true);
        const copiedWorkspace = copy.querySelector("#workspace"),
          copiedDock = copy.querySelector("#graph-dock");
        copiedDock.after(copiedWorkspace);
        copy.querySelector("#graph-dock")?.remove();
        copy.querySelector("#diagram-dialog").removeAttribute("open");
        copy.querySelector("body").classList.remove("diagram-open");
        copy.querySelector("#diagram-hint").hidden = true;
        const copiedExpand = copy.querySelector("#expand-diagram");
        copiedExpand.setAttribute("aria-expanded", "false");
        copiedExpand.dataset.i18nAria = copiedExpand.dataset.i18nTitle =
          "expandGraph";
        copy
          .querySelector("body")
          .classList.remove("export-busy", "export-frame", "landing");
        copy.querySelector("body").classList.add("standalone");
        copy.querySelector("#export-progress").hidden = true;
        copy
          .querySelectorAll(
            ".landing-section,.landing-only,#site-script,#site-style,#site-locales",
          )
          .forEach((el) => el.remove());
        const settings = JSON.parse(
          copy.querySelector("#appearance-config").textContent,
        );
        settings.landing = false;
        settings.preference = {
          language: window.repoAppearance.language,
          theme: window.repoAppearance.resolvedTheme,
        };
        copy.querySelector("#appearance-config").textContent = JSON.stringify(
          settings,
        ).replace(/</g, "\\u003c");
        const documentText = copy.outerHTML
          .replace(
            "url(assets/AtkinsonHyperlegibleNext.ttf)",
            "url(data:font/ttf;base64," +
              JSON.parse($("repo-font").textContent) +
              ")",
          )
          .replace("window.REPO_LANDING=true;", "window.REPO_LANDING=false;");
        download(
          new Blob(["<!doctype html>\n" + documentText], { type: "text/html" }),
          slug() + ".html",
        );
      } else if (format === "json") {
        const data = JSON.parse(JSON.stringify(baseStory));
        download(
          new Blob([JSON.stringify(data, null, 2) + "\n"], {
            type: "application/json",
          }),
          slug() + ".json",
        );
      } else if (format === "svg")
        download(
          new Blob([exportSVG()], { type: "image/svg+xml" }),
          slug() + ".svg",
        );
      else if (format === "png") {
        message(t("exportPng"));
        const canvas = await rasterFrame(current, 1440, 960);
        const blob = await new Promise((resolve) =>
          canvas.toBlob(resolve, "image/png"),
        );
        if (!blob) throw Error(t("pngFailed"));
        download(blob, slug() + ".png");
      } else if (format === "gif") {
        setView("path");
        const fps = 8,
          count = Math.ceil((duration() / 1000) * fps);
        if (count > 960) throw Error(t("longGif"));
        const gif = Gifenc.GIFEncoder();
        for (let i = 0; i < count; i++) {
          if (cancelled) throw Error(t("cancelled"));
          message(t("renderGif", { percent: Math.round((i / count) * 100) }));
          const canvas = await rasterFrame((i * 1000) / fps, 800, 540),
            ctx = canvas.getContext("2d"),
            rgba = ctx.getImageData(0, 0, 800, 540).data,
            palette = Gifenc.quantize(rgba, 128),
            indexed = Gifenc.applyPalette(rgba, palette);
          gif.writeFrame(indexed, 800, 540, {
            palette,
            delay:
              Math.round(((i + 1) * 100) / fps) * 10 -
              Math.round((i * 100) / fps) * 10,
            repeat: 0,
          });
          await new Promise((resolve) => setTimeout(resolve, 0));
        }
        gif.finish();
        download(
          new Blob([gif.bytes()], { type: "image/gif" }),
          slug() + ".gif",
        );
      } else {
        const mime =
          format === "mp4"
            ? "video/mp4;codecs=avc1.42001f"
            : "video/webm;codecs=vp9";
        if (!window.MediaRecorder || !MediaRecorder.isTypeSupported(mime))
          throw Error(t("videoUnavailable", { format: format.toUpperCase() }));
        setView("path");
        const fps = 12,
          canvas = document.createElement("canvas");
        canvas.width = 960;
        canvas.height = 640;
        const ctx = canvas.getContext("2d"),
          stream = canvas.captureStream(0),
          track = stream.getVideoTracks()[0],
          chunks = [],
          recorder = new MediaRecorder(stream, {
            mimeType: mime,
            videoBitsPerSecond: 4000000,
          });
        const done = new Promise((resolve, reject) => {
          recorder.ondataavailable = (e) => {
            if (e.data.size) chunks.push(e.data);
          };
          recorder.onstop = resolve;
          recorder.onerror = () => reject(Error(t("videoFailed")));
        });
        recorder.start();
        try {
          for (let ms = 0; ms < duration(); ms += 1000 / fps) {
            if (cancelled) throw Error(t("cancelled"));
            message(
              t("recordVideo", {
                format: format.toUpperCase(),
                percent: Math.round((ms / duration()) * 100),
              }),
            );
            ctx.drawImage(await rasterFrame(ms), 0, 0);
            track.requestFrame();
            await new Promise((resolve) => setTimeout(resolve, 1000 / fps));
          }
        } finally {
          recorder.stop();
          await done;
          stream.getTracks().forEach((t) => t.stop());
        }
        download(
          new Blob(chunks, { type: recorder.mimeType }),
          slug() + "." + format,
        );
      }
      status(t("exported", { format: format.toUpperCase() }));
    } catch (error) {
      status(error.message);
      throw error;
    } finally {
      exporting = false;
      document.body.classList.remove("export-busy");
      $("export-progress").hidden = true;
      setView(old.view);
      renderAt(old.time);
      selected = old.selected;
      paint();
      inspect();
    }
  }
  window.repoPlayer = {
    get durationMs() {
      return duration();
    },
    get timeMs() {
      return current;
    },
    _setPlaying(value) {
      playing = value;
      setPlayIcon();
    },
    get graph() {
      return S;
    },
    get layout() {
      return layout;
    },
    get view() {
      return view;
    },
    get selection() {
      return { ...selected };
    },
    get isPlaying() {
      return playing;
    },
    setScenario,
    setView,
    selectNode: (id) => select("node", id),
    selectEdge: (id) => select("edge", id),
    exportSVG,
    renderFrame: rasterFrame,
    export: browserExport,
    fit,
    pause,
  };
  $("play").addEventListener("click", togglePlay);
  $("previous").addEventListener("click", () => skip(-1));
  $("next").addEventListener("click", () => skip(1));
  $("seek").addEventListener("input", () => {
    pause();
    renderAt(Number($("seek").value));
  });
  $("scenario").addEventListener("change", (event) =>
    setScenario(event.target.value),
  );
  $("component-search").addEventListener("input", fillComponents);
  $("overview-tab").addEventListener("click", () => setCodeMode(false));
  $("code-tab").addEventListener("click", () => setCodeMode(true));
  for (const b of document.querySelectorAll("[data-view]"))
    b.addEventListener("click", () => setView(b.dataset.view));
  for (const b of document.querySelectorAll("[data-export]"))
    b.addEventListener("click", () => {
      document.querySelector(".export-menu").open = false;
      browserExport(b.dataset.export).catch(() => {});
    });
  $("cancel-export").addEventListener("click", () => {
    cancelled = true;
  });
  $("zoom-out").addEventListener("click", () => zoom(1.25));
  $("zoom-in").addEventListener("click", () => zoom(0.8));
  $("zoom-fit").addEventListener("click", () => {
    readabilityRequested = readableDetail = false;
    fit();
  });
  let drag = null;
  diagram.addEventListener("pointerdown", (event) => {
    if (event.target.closest(".graph-node,.graph-edge") || !camera) return;
    readabilityRequested = false;
    drag = { x: event.clientX, y: event.clientY, camera: { ...camera } };
    diagram.setPointerCapture(event.pointerId);
  });
  diagram.addEventListener("pointermove", (event) => {
    if (!drag) return;
    const r = diagram.getBoundingClientRect(),
      scale = Math.max(camera.w / r.width, camera.h / r.height);
    camera = {
      ...drag.camera,
      x: drag.camera.x - (event.clientX - drag.x) * scale,
      y: drag.camera.y - (event.clientY - drag.y) * scale,
    };
    applyCamera();
  });
  diagram.addEventListener("pointerup", () => (drag = null));
  diagram.addEventListener("pointercancel", () => (drag = null));
  diagram.addEventListener(
    "wheel",
    (event) => {
      if (event.ctrlKey || event.metaKey) {
        event.preventDefault();
        zoom(event.deltaY > 0 ? 1.1 : 0.9);
      }
    },
    { passive: false },
  );
  document.addEventListener("keydown", (event) => {
    if (
      event.target.closest(
        "input,select,textarea,button,a,summary,[role=button]",
      ) ||
      exporting
    )
      return;
    if (event.key === " ") {
      event.preventDefault();
      togglePlay();
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      skip(1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      skip(-1);
    } else if (event.key === "Escape") {
      if (dialog.open) {
        event.preventDefault();
        toggleDiagram(false);
        return;
      }
      pause();
      setView("map");
      document.querySelector(".export-menu").open = false;
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause();
  });
  document.addEventListener("click", (event) => {
    const menu = document.querySelector(".export-menu");
    if (!menu.contains(event.target)) menu.open = false;
  });
  $("repo-name").textContent = S.title;
  $("repo-revision").textContent = S.repo.commit?.slice(0, 7) || t("local");
  $("question").textContent = S.question;
  if (!window.REPO_LANDING) {
    $("page-title").removeAttribute("data-i18n");
    $("page-title").textContent = S.title;
    $("page-description").textContent = S.summary || S.question;
    document.querySelector(".site-nav").hidden = true;

    document.querySelector(".install-button").dataset.i18n = "exploreSource";
    document.querySelector(".install-button").textContent = t("exploreSource");
    document.querySelector(".install-button").href = "#workspace";
  }
  for (const note of S.uncertainties)
    $("uncertainties").append(text("li", note));
  configureTimeline();
  fillComponents();
  renderAt(0);
  document.addEventListener("repo-language-change", () => {
    if (exporting) return;
    window.repoLocaleReady = (async () => {
      await window.repoReady;
      pause();
      const previous = { ...selected };
      S = localizedStory();
      for (const [collection, map] of [
        [S.nodes, nodes],
        [S.edges, edges],
        [S.steps, steps],
      ]) {
        map.clear();
        for (const item of collection) map.set(item.id, item);
      }
      inspectedKey = null;
      $("question").textContent = S.question;
      $("repo-name").textContent = S.title;
      $("uncertainties").replaceChildren(
        ...S.uncertainties.map((note) => text("li", note)),
      );
      if (!window.REPO_LANDING) {
        $("page-title").textContent = S.title;
        $("page-description").textContent = S.summary || S.question;
      }
      configureTimeline();
      fillComponents();
      await layOut();
      renderAt(current);
      select(previous.type, previous.id, { announce: false });
      setPlayIcon();
      if (dialog.open) ensureReadable();
      status(t("ready", { nodes: S.nodes.length, edges: S.edges.length }));
    })();
  });
  window.repoReady = (async () => {
    await document.fonts.ready;
    await layOut();
    setView(S.default_view || "map");
    status(t("ready", { nodes: S.nodes.length, edges: S.edges.length }));
    return true;
  })().catch((error) => {
    $("loading").textContent = t("layoutFailed") + error.message;
    status("Layout failed: " + error.message);
    throw error;
  });
})();
