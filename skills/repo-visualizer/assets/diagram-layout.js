/* Presentation only: every component and relationship keeps its canonical id. */
(() => {
  const context = document.createElement("canvas").getContext("2d");
  function wrap(value, width, font, limit = Infinity) {
    context.font = font;
    const lines = [];
    let current = "";
    for (let word of String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .split(" ")) {
      if (!word) continue;
      while (context.measureText(word).width > width) {
        if (current) {
          lines.push(current);
          current = "";
        }
        const letters = Array.from(word);
        let cut = letters.length - 1;
        while (
          cut > 1 &&
          context.measureText(letters.slice(0, cut).join("")).width > width
        )
          cut--;
        lines.push(letters.slice(0, cut).join(""));
        word = letters.slice(cut).join("");
      }
      const next = current ? current + " " + word : word;
      if (context.measureText(next).width > width) {
        lines.push(current);
        current = word;
      } else current = next;
    }
    if (current) lines.push(current);
    if (lines.length > limit) {
      lines.length = limit;
      let last = lines[limit - 1];
      while (last && context.measureText(last + "…").width > width)
        last = last.slice(0, -1);
      lines[limit - 1] = last.replace(/\s+\S*$/, "") + "…";
    }
    return lines;
  }
  function textWidth(value, font) {
    context.font = font;
    return context.measureText(value).width;
  }
  function measureNode(
    node,
    fallback,
    width = 240,
    band = false,
    textWidth = width - 36,
  ) {
    const title = wrap(node.label, textWidth, "600 20px Atkinson");
    const caption = wrap(
      node.caption || node.description || fallback,
      textWidth,
      "400 14px Atkinson",
      2,
    );
    const inferred = node.evidence === "inferred";
    return {
      width,
      height: Math.max(
        band ? 88 : 112,
        36 +
          title.length * 24 +
          (caption.length ? 8 + caption.length * 19 : 0) +
          (inferred ? 18 : 0),
      ),
      title,
      caption,
      inferred,
    };
  }
  function measureEdge(edge) {
    const lines = wrap(edge.label || "", 128, "400 14px Atkinson", 3);
    return {
      lines,
      width:
        Math.max(
          1,
          ...lines.map((line) => textWidth(line, "400 14px Atkinson")),
        ) + 12,
      height: Math.max(18, lines.length * 18),
    };
  }
  function mode(story, viewport) {
    const hints = story.presentation || {},
      bands = [...(hints.top || []), ...(hints.bottom || [])];
    if (hints.layout === "layered" || story.groups.length) return "layered";
    if (hints.layout === "flow" || bands.length) return "flow";
    // Automatic flow is deliberately limited to a single small acyclic chain,
    // and only when its labels would remain readable at the available width.
    const count = story.nodes.length;
    if (
      count < 3 ||
      count > 6 ||
      story.edges.length !== count - 1 ||
      viewport.width /
        (count * 240 +
          (count - 1) * 64 +
          story.edges.reduce((sum, e) => sum + measureEdge(e).width, 0) +
          40) <
        0.55
    )
      return "layered";
    const incoming = new Map(story.nodes.map((n) => [n.id, 0])),
      outgoing = new Map(story.nodes.map((n) => [n.id, []]));
    for (const e of story.edges) {
      incoming.set(e.to, incoming.get(e.to) + 1);
      outgoing.get(e.from).push(e.to);
    }
    if (
      [...incoming.values()].some((n) => n > 1) ||
      [...outgoing.values()].some((a) => a.length > 1)
    )
      return "layered";
    const starts = [...incoming].filter(([, n]) => !n);
    if (starts.length !== 1) return "layered";
    const seen = new Set();
    let cursor = starts[0][0];
    while (cursor && !seen.has(cursor)) {
      seen.add(cursor);
      cursor = outgoing.get(cursor)[0];
    }
    return seen.size === count ? "flow" : "layered";
  }
  const intersects = (a, b) =>
    a.x < b.x + b.width - 0.1 &&
    a.x + a.width > b.x + 0.1 &&
    a.y < b.y + b.height - 0.1 &&
    a.y + a.height > b.y + 0.1;
  function clearSegment(a, b, obstacles) {
    return !obstacles.some((r) =>
      a.x === b.x
        ? a.x > r.x + 0.1 &&
          a.x < r.x + r.width - 0.1 &&
          Math.max(a.y, b.y) > r.y + 0.1 &&
          Math.min(a.y, b.y) < r.y + r.height - 0.1
        : a.y > r.y + 0.1 &&
          a.y < r.y + r.height - 0.1 &&
          Math.max(a.x, b.x) > r.x + 0.1 &&
          Math.min(a.x, b.x) < r.x + r.width - 0.1,
    );
  }
  function simplify(points) {
    const out = [];
    for (const p of points) {
      if (out.length && p.x === out.at(-1).x && p.y === out.at(-1).y) continue;
      while (
        out.length > 1 &&
        ((out.at(-2).x === out.at(-1).x && out.at(-1).x === p.x) ||
          (out.at(-2).y === out.at(-1).y && out.at(-1).y === p.y))
      )
        out.pop();
      out.push(p);
    }
    return out;
  }
  // Orthogonal visibility grid keeps shared-service routes out of component bodies.
  function route(start, end, obstacles, width, height) {
    const xs = [
      ...new Set([
        start.x,
        end.x,
        12,
        width - 12,
        ...obstacles.flatMap((r) => [r.x, r.x + r.width]),
      ]),
    ].sort((a, b) => a - b);
    const ys = [
      ...new Set([
        start.y,
        end.y,
        12,
        height - 12,
        ...obstacles.flatMap((r) => [r.y, r.y + r.height]),
      ]),
    ].sort((a, b) => a - b);
    const key = (x, y, d) => x + ":" + y + ":" + d,
      queue = [],
      best = new Map(),
      previous = new Map();
    const sx = xs.indexOf(start.x),
      sy = ys.indexOf(start.y),
      tx = xs.indexOf(end.x),
      ty = ys.indexOf(end.y);
    const first = key(sx, sy, 0);
    queue.push({ x: sx, y: sy, d: 0, c: 0, k: first });
    best.set(first, 0);
    let finish;
    while (queue.length) {
      queue.sort((a, b) => b.c - a.c);
      const at = queue.pop();
      if (at.c !== best.get(at.k)) continue;
      if (at.x === tx && at.y === ty) {
        finish = at;
        break;
      }
      for (const [dx, dy, d] of [
        [-1, 0, 1],
        [1, 0, 1],
        [0, -1, 2],
        [0, 1, 2],
      ]) {
        const x = at.x + dx,
          y = at.y + dy;
        if (x < 0 || y < 0 || x >= xs.length || y >= ys.length) continue;
        const a = { x: xs[at.x], y: ys[at.y] },
          b = { x: xs[x], y: ys[y] };
        if (!clearSegment(a, b, obstacles)) continue;
        const c =
            at.c +
            Math.abs(a.x - b.x) +
            Math.abs(a.y - b.y) +
            (at.d && at.d !== d ? 24 : 0),
          k = key(x, y, d);
        if (c >= (best.get(k) ?? Infinity)) continue;
        best.set(k, c);
        previous.set(k, at);
        queue.push({ x, y, d, c, k });
      }
    }
    if (!finish)
      throw Error("No clear route for a shared-component relationship");
    const points = [];
    for (let at = finish; at; at = previous.get(at.k))
      points.push({ x: xs[at.x], y: ys[at.y] });
    return simplify(points.reverse());
  }
  async function layOut(model, story, viewport, nodeSizes, fallback) {
    const chosen = mode(story, viewport),
      elk = new ELK();
    if (chosen === "layered") {
      const result = await elk.layout(model);
      result.layoutMode = "layered";
      return result;
    }
    const hints = story.presentation || {},
      top = hints.top || [],
      bottom = hints.bottom || [],
      bandIds = new Set([...top, ...bottom]);
    const bandEdges = model.edges.filter(
      (e) => bandIds.has(e.sources[0]) || bandIds.has(e.targets[0]),
    );
    const narrow = (viewport.pageWidth || viewport.width) < 800;
    const inner = await elk.layout({
      id: "__flow-main",
      layoutOptions: {
        ...model.layoutOptions,
        "elk.direction": narrow ? "DOWN" : "RIGHT",
        "elk.spacing.nodeNode": "44",
        "elk.layered.spacing.nodeNodeBetweenLayers": "24",
        "elk.padding": "[top=20,left=20,bottom=20,right=20]",
      },
      children: model.children.filter((n) => !bandIds.has(n.id)),
      edges: model.edges.filter((e) => !bandEdges.includes(e)),
    });
    const width = Math.max(narrow ? 320 : 960, inner.width + 48),
      gap = 144,
      children = [];
    let y = 24;
    for (const id of top) {
      const data = measureNode(
        story.nodes.find((n) => n.id === id),
        fallback(id),
        width - 48,
        true,
        narrow
          ? Math.max(204, Math.min(width - 84, viewport.width - 36))
          : width - 84,
      );
      nodeSizes.set(id, data);
      children.push({ id, x: 24, y, width: data.width, height: data.height });
      y += data.height + 28;
    }
    if (top.length) y += gap - 28;
    inner.x = (width - inner.width) / 2;
    inner.y = y;
    children.push(inner);
    y += inner.height;
    if (bottom.length) y += gap;
    for (const id of bottom) {
      const data = measureNode(
        story.nodes.find((n) => n.id === id),
        fallback(id),
        width - 48,
        true,
        narrow
          ? Math.max(204, Math.min(width - 84, viewport.width - 36))
          : width - 84,
      );
      nodeSizes.set(id, data);
      children.push({ id, x: 24, y, width: data.width, height: data.height });
      y += data.height + 28;
    }
    const result = {
      id: model.id,
      width,
      height: y + 24,
      children,
      edges: [],
      layoutMode: "flow",
      flowDirection: narrow ? "DOWN" : "RIGHT",
    };
    const boxes = new Map();
    function collect(item, ox = 0, oy = 0) {
      const x = ox + (item.x || 0),
        y = oy + (item.y || 0);
      if (story.nodes.some((n) => n.id === item.id))
        boxes.set(item.id, { x, y, width: item.width, height: item.height });
      for (const c of item.children || []) collect(c, x, y);
    }
    collect(result);
    const faces = new Map(),
      faceKey = (id, face) => id + ":" + face;
    const connections = bandEdges.map((e) => {
      const a = boxes.get(e.sources[0]),
        b = boxes.get(e.targets[0]),
        down = a.y + a.height / 2 <= b.y + b.height / 2;
      const record = {
        e,
        a,
        b,
        af: down ? "bottom" : "top",
        bf: down ? "top" : "bottom",
      };
      if (e.sources[0] === e.targets[0]) record.af = record.bf = "bottom";
      for (const [id, face] of [
        [e.sources[0], record.af],
        [e.targets[0], record.bf],
      ]) {
        const k = faceKey(id, face);
        if (!faces.has(k)) faces.set(k, []);
        faces.get(k).push(record);
      }
      return record;
    });
    const labelBoxes = [];
    function labels(item, ox = 0, oy = 0) {
      const x = ox + (item.x || 0),
        y = oy + (item.y || 0);
      for (const e of item.edges || [])
        for (const l of e.labels || [])
          labelBoxes.push({
            x: x + l.x,
            y: y + l.y,
            width: l.width,
            height: l.height,
          });
      for (const c of item.children || []) labels(c, x, y);
    }
    labels(inner);
    for (const connection of connections) {
      const { e, a, b, af, bf } = connection;
      function port(id, box, face, other, endPort = false) {
        const list = faces.get(faceKey(id, face)),
          index =
            endPort && id === other.id
              ? list.lastIndexOf(connection)
              : list.indexOf(connection);
        let x =
          box.x + 18 + ((box.width - 36) * (index + 1)) / (list.length + 1);
        if (bandIds.has(id) && !bandIds.has(other.id))
          x = Math.max(
            box.x + 24,
            Math.min(
              box.x + box.width - 24,
              other.x + other.width / 2 + (index - (list.length - 1) / 2) * 18,
            ),
          );
        return { x, y: face === "top" ? box.y : box.y + box.height };
      }
      const start = port(e.sources[0], a, af, { ...b, id: e.targets[0] }),
        end = port(e.targets[0], b, bf, { ...a, id: e.sources[0] }, true);
      const escapeA = { x: start.x, y: start.y + (af === "top" ? -20 : 20) },
        escapeB = { x: end.x, y: end.y + (bf === "top" ? -20 : 20) };
      const obstacles = [...boxes].map(([id, r]) => {
        const pad = id === e.sources[0] || id === e.targets[0] ? 0 : 12;
        return {
          x: r.x - pad,
          y: r.y - pad,
          width: r.width + pad * 2,
          height: r.height + pad * 2,
        };
      });
      const labelObstacles = labelBoxes.filter(
        (r) =>
          ![escapeA, escapeB].some(
            (p) =>
              p.x > r.x &&
              p.x < r.x + r.width &&
              p.y > r.y &&
              p.y < r.y + r.height,
          ),
      );
      const points = simplify([
        start,
        ...route(
          escapeA,
          escapeB,
          [...obstacles, ...labelObstacles],
          result.width,
          result.height,
        ),
        end,
      ]);
      const rendered = {
        ...e,
        sections: [
          {
            startPoint: points[0],
            endPoint: points.at(-1),
            bendPoints: points.slice(1, -1),
          },
        ],
        labels: [],
      };
      if (e.labels?.length) {
        const original = e.labels[0],
          candidates = [];
        for (let i = 1; i < points.length; i++) {
          const a = points[i - 1],
            b = points[i],
            horizontal = a.y === b.y;
          for (const fraction of [0.5, 0.25, 0.75])
            for (const side of [-1, 1]) {
              const x = a.x + (b.x - a.x) * fraction,
                y = a.y + (b.y - a.y) * fraction;
              const box = {
                x: horizontal
                  ? x - original.width / 2
                  : x + (side > 0 ? 10 : -original.width - 10),
                y: horizontal
                  ? y + (side > 0 ? 10 : -original.height - 10)
                  : y - original.height / 2,
                width: original.width,
                height: original.height,
              };
              if (
                box.x >= 16 &&
                box.y >= 16 &&
                box.x + box.width <= result.width - 16 &&
                (horizontal
                  ? Math.abs(b.x - a.x) >= original.width + 12
                  : Math.abs(b.y - a.y) >= original.height + 12) &&
                ![...boxes.values(), ...labelBoxes].some((r) =>
                  intersects(box, r),
                )
              )
                candidates.push(box);
            }
        }
        const label = candidates[0] || {
          x: result.width + 16,
          y: 24 + labelBoxes.length * 56,
          width: original.width,
          height: original.height,
        };
        rendered.labels = [{ ...original, ...label }];
        labelBoxes.push(label);
      }
      result.edges.push(rendered);
    }
    result.width = Math.max(
      result.width,
      ...labelBoxes.map((r) => r.x + r.width + 24),
    );
    result.height = Math.max(
      result.height,
      ...labelBoxes.map((r) => r.y + r.height + 24),
    );
    return result;
  }
  window.repoDiagram = { measureNode, measureEdge, layOut, wrap, mode };
})();
