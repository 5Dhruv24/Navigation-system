# DECISIONS.md — CampusNav

This file records the key product and technical decisions made while
building CampusNav, including why alternatives were rejected.

---

## 1. Combining both assignments into one project

**Decision:** Build a single Campus Navigation web app that satisfies
both the "campus utility app" brief and the "graph + shortest path"
brief, instead of two separate projects.

**Why:** A weighted-graph shortest-path finder *is* a genuine,
practical campus utility (helping students navigate an unfamiliar
campus). Splitting it into two unrelated projects would have meant
either a shallow utility app or a shortest-path solver with no real
UI — building one real thing satisfies both rubrics without padding.

---

## 2. Graph representation: adjacency list, not adjacency matrix

**Decision:** Represent the campus graph as a Python dict of dicts
(`{node: {neighbor: weight}}`) rather than a 2D adjacency matrix.

**Why:** The graph is sparse — 12 nodes, 11 edges, when a complete
graph would have 66 possible edges. An adjacency list costs
O(V + E) space and lets Dijkstra look up a node's neighbors directly,
instead of scanning an entire row of mostly-zero entries as a matrix
would require.

---

## 3. Algorithm: Dijkstra, not BFS

**Decision:** Use Dijkstra's algorithm, not plain BFS.

**Why:** BFS assumes every edge costs the same (counts hops, not
distance). Our edges carry real-world walking distances in meters,
which vary edge to edge (35m to 120m) — BFS would therefore return
the path with the *fewest buildings crossed*, not the *shortest
distance*, which can disagree. Dijkstra correctly accounts for edge
weights and is appropriate since all weights (distances) are
non-negative.

---

## 4. Edge weights: estimated, not surveyed

**Decision:** Distances between campus locations are estimated from
the official GGSIPU East Delhi Campus location map and satellite
imagery, not measured with survey equipment.

**Why:** Survey-grade accuracy isn't the point of this project —
demonstrating correct graph construction and shortest-path
computation is. Estimates are proportionally reasonable and
consistent with the real campus layout, which is sufficient to prove
the algorithm works correctly on realistic data.

---

## 5. Tech stack: Python/Flask backend + plain HTML/JS frontend

**Decision:** Flask for the API, vanilla HTML/CSS/JS for the
frontend (no React/Vue, no database).

**Why:** The project needed to stay explainable end-to-end in a
viva. Flask exposes the Dijkstra function as a couple of simple
routes with minimal boilerplate. A plain frontend avoids a build
step, a framework learning curve, or dependencies unrelated to the
actual assignment goals (the graph algorithm). The graph itself is
small and static, so no database was needed — it lives directly in
`campus_data.py`.

**Revision during development:** Originally the frontend was served
as a separate static file opened directly in the browser, with the
Flask API on a different port. This was later merged so Flask serves
the frontend too (`/` returns `index.html`), so the whole app runs
from one URL and one command (`python app.py`) — simpler to run and
demo.

---

## 6. Visual map: real satellite imagery, not an abstract diagram

**Decision:** The visual-map bonus overlays the graph (nodes, edges,
highlighted shortest path) directly on top of a real satellite
screenshot of the actual campus, rather than an abstract node-link
diagram or the official architectural location-map graphic.

**Why:** This makes the connection between "the graph" and "the real
place" immediate and concrete for anyone evaluating the project —
the shortest path is visibly drawn over real buildings and roads,
not an abstraction. Node pixel positions were calibrated against the
official campus map and corrected twice based on first-hand
knowledge of the campus (gate positions were initially swapped; East
End Club was removed as it isn't a real routing node on this
campus).

---

## 7. Natural-language query: rule-based parsing, not an external AI API

**Decision:** The "Ask CampusNav" feature (e.g. "library from gate
1") is parsed with a custom rule-based matcher (`nl_parser.py`)
using regex sentence patterns and an alias dictionary, rather than
calling an external LLM/AI API.

**Why:**
- The app runs entirely locally with no API key configured, so an
  external AI call would be a dependency that can silently fail.
- A rule-based parser is fully transparent — every match can be
  explained line by line in a viva, unlike a black-box model call.
- It costs nothing and has no network dependency or latency.

This was a deliberate trade-off: the parser only understands a
specific, limited pattern (two location mentions, optionally framed
as "from X to Y"), not open-ended conversation. That limitation is
acceptable since the feature's job is narrow (extract a start and
destination), not general chat.

---

## 8. Error handling

**Decision:** Errors are handled at both the backend and frontend:

- Backend (`app.py`): missing parameters (400), invalid/unknown
  location codes (400), no path found (404) — even though the
  current graph is fully connected, so this case is defensive.
- Frontend (`index.html`): empty dropdown selection, identical
  start/destination, and an unreachable backend (connection
  failure) are all caught before or around the API call, with a
  clear message shown to the user rather than a silent failure or
  raw error.

**Why:** Both layers matter — frontend checks give instant feedback
without a network round-trip; backend checks protect the API from
being called directly or incorrectly (e.g. via the `/smart-route`
natural-language path, which can't pre-validate input the way the
dropdowns do).
