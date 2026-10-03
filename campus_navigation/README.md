# CampusNav — Smart Campus Navigation App

A web app that finds the shortest walking route between locations on
the USAR, GGSIPU East Delhi Campus, using Dijkstra's algorithm on a
real weighted graph of the campus — with the route drawn live on top
of actual satellite imagery.

Built as a combined submission for:
- **Campus Utility App** assignment (practical student-facing app)
- **Campus Navigation System** assignment (graph + shortest path)

---

## Features

- Real campus graph: 12 locations, 11 weighted edges (distances in
  meters), built from the official campus location map and
  satellite imagery
- Shortest-path routing via **Dijkstra's algorithm**, implemented
  from scratch (`dijkstra.py`)
- Interactive map UI with the route drawn live over real satellite
  imagery of the campus
- **"Ask CampusNav"** — type a plain-English request like *"library
  from gate 1"* and it parses out the start/destination and routes
  automatically (rule-based parser, no external AI API)
- Error handling for invalid input, identical start/destination, and
  unreachable locations
- Single command to run — Flask serves both the API and the frontend

---

## Project structure

```
campus_navigation/
├── backend/
│   ├── app.py              # Flask server: API routes + serves the frontend
│   ├── campus_data.py       # The graph (nodes, edges, distances, aliases)
│   ├── dijkstra.py          # Dijkstra's algorithm implementation
│   ├── nl_parser.py         # Rule-based parser for "Ask CampusNav"
│   └── test_dijkstra.py     # Standalone tests for the algorithm
├── frontend/
│   ├── index.html            # The entire web app (UI + map overlay)
│   └── assets/
│       └── campus_map.jpg    # Real satellite screenshot used as the map
├── DECISIONS.md
└── README.md
```

---

## How to run

**Requirements:** Python 3, Flask, flask-cors

```bash
pip install flask flask-cors
cd backend
python app.py
```

Then open your browser to:

```
http://127.0.0.1:5000/
```

That's it — one command, one URL. The frontend, API, and map are all
served from the same Flask process.

---

## How it works

1. The campus is modeled as a **weighted, undirected graph**
   (`campus_data.py`), stored as an adjacency list — each location
   maps to its directly-connected neighbors and the walking distance
   to each.
2. When a user picks a start and destination (or types a natural-
   language query), the Flask backend runs **Dijkstra's algorithm**
   (`dijkstra.py`) to compute the shortest path and total distance.
3. The frontend draws the full path as a highlighted line over a
   real satellite image of campus, with every node positioned at its
   actual real-world location.

---

## Algorithm choice: why Dijkstra, not BFS

BFS finds the path with the **fewest edges**, which is only correct
if every edge costs the same. Our edges represent real walking
distances that vary (35m–120m), so the path with fewest hops is not
necessarily the shortest in meters. Dijkstra correctly accounts for
edge weights and is guaranteed correct here since all distances are
non-negative.

---

## Complexity analysis

Using a binary heap (Python's `heapq`) as the priority queue:

| | Complexity |
|---|---|
| **Time** | O((V + E) log V) |
| **Space** | O(V + E) |

Where **V** = number of nodes (12) and **E** = number of edges (11).

- Each node is pushed/popped from the heap at most once per edge
  relaxation — O(log V) per heap operation, O(E) relaxations total
  → O(E log V), plus O(V log V) for the initial pushes.
- Space is dominated by the adjacency list (O(V + E)), the distance
  map, and the previous-node map (both O(V)).

With 12 nodes and 11 edges, this runs effectively instantly — but
the same implementation scales correctly to a campus graph with
hundreds of nodes without any code changes.

---

## Known limitations

- Edge distances are estimated from map imagery, not surveyed —
  reasonable for demonstrating the algorithm, not survey-grade
  accurate.
- The "Ask CampusNav" parser only recognizes a specific set of
  location aliases and sentence patterns — it is not a general
  conversational interface.
- The satellite image used is a single screenshot; a couple of
  real-world distances (particularly around Gate 02) are
  approximate rather than measured.

See `DECISIONS.md` for the reasoning behind these and other design
choices.
