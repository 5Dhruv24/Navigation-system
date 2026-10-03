"""
app.py

Flask backend for CampusNav.

WHY FLASK?
-----------
Flask is a minimal Python web framework — it lets us expose our
already-tested Dijkstra function as a web API with just a few lines
of routing code, no heavy setup. The frontend (plain HTML/JS) will
call this API using fetch(), send a start + destination, and get
back JSON with the route and total distance.

ENDPOINTS:
-----------
GET /                       -> health check, confirms server is up
GET /locations               -> list of all valid location codes + names
                                 (used to populate the dropdowns)
GET /shortest-path?start=X&end=Y
                              -> runs Dijkstra, returns route as JSON

ERROR HANDLING:
-----------------
- Missing start/end params        -> 400 Bad Request
- start or end not a valid node   -> 400 Bad Request
- start == end                    -> handled by Dijkstra itself
                                      (returns trivial 1-node path, 0m)
- No path exists between nodes    -> 404 Not Found
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from campus_data import CAMPUS_GRAPH, LOCATION_NAMES
from dijkstra import dijkstra
from nl_parser import parse_query

# static_folder points at the frontend directory (one level up, then into
# frontend/) so Flask can serve index.html and assets/campus_map.jpg
# directly. static_url_path="" means those files are served from the
# root URL (e.g. /index.html, /assets/campus_map.jpg) instead of /static/...
#
# Built as an absolute path (based on this file's own location) rather
# than a relative one, so it resolves correctly both when run locally
# (python app.py) and when run by Vercel's serverless Python runtime,
# which may execute from a different working directory.
_FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Frontend")
app = Flask(__name__, static_folder=_FRONTEND_DIR, static_url_path="")
CORS(app)  # harmless now that everything is same-origin, kept for safety


@app.route("/")
def serve_frontend():
    """Serves the CampusNav web app itself at the root URL."""
    return app.send_static_file("index.html")


@app.route("/api/health")
def health_check():
    return jsonify({"status": "CampusNav backend is running"})


@app.route("/locations")
def get_locations():
    """Returns all valid location codes and their display names,
    so the frontend can populate the start/destination dropdowns."""
    locations = [
        {"code": code, "name": LOCATION_NAMES.get(code, code)}
        for code in CAMPUS_GRAPH
    ]
    return jsonify(locations)


@app.route("/shortest-path")
def shortest_path():
    start = request.args.get("start")
    end = request.args.get("end")

    # --- Error case 1: missing parameters ---
    if not start or not end:
        return jsonify({"error": "Both 'start' and 'end' parameters are required."}), 400

    # --- Error case 2: invalid location codes ---
    if start not in CAMPUS_GRAPH or end not in CAMPUS_GRAPH:
        return jsonify({"error": "Invalid start or end location."}), 400

    path, total_distance = dijkstra(CAMPUS_GRAPH, start, end)

    # --- Error case 3: no path exists (shouldn't happen on our
    #     connected campus graph, but Dijkstra handles it anyway) ---
    if path is None:
        return jsonify({"error": f"No route found between {start} and {end}."}), 404

    # Build a readable response with both codes and display names
    route = [
        {"code": node, "name": LOCATION_NAMES.get(node, node)}
        for node in path
    ]

    return jsonify({
        "start": start,
        "end": end,
        "path": route,
        "total_distance_m": total_distance,
    })


@app.route("/smart-route")
def smart_route():
    """
    AI-style natural-language routing. Takes a free-text query,
    e.g. /smart-route?query=how+do+i+get+to+the+library+from+gate+1
    extracts the start/end locations with nl_parser, then runs the
    exact same Dijkstra function as /shortest-path.
    """
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"error": "Please type a question, e.g. 'how do I get to the library from gate 1'."}), 400

    start, end = parse_query(query)

    if start is None or end is None:
        return jsonify({
            "error": "Couldn't identify two locations in that query. "
                     "Try mentioning a start and a destination clearly, "
                     "e.g. 'route from boys hostel to the auditorium'."
        }), 400

    path, total_distance = dijkstra(CAMPUS_GRAPH, start, end)

    if path is None:
        return jsonify({"error": f"No route found between {start} and {end}."}), 404

    route = [{"code": node, "name": LOCATION_NAMES.get(node, node)} for node in path]

    return jsonify({
        "query": query,
        "understood_start": {"code": start, "name": LOCATION_NAMES.get(start, start)},
        "understood_end": {"code": end, "name": LOCATION_NAMES.get(end, end)},
        "start": start,
        "end": end,
        "path": route,
        "total_distance_m": total_distance,
    })


if __name__ == "__main__":
    # Locally: runs on port 5000, same as always (python app.py).
    # On Render: the PORT environment variable is set automatically,
    # and the app must bind to 0.0.0.0 (not 127.0.0.1) to be reachable.
    # This does not change any app behavior — only where it listens.
    import os
    port = int(os.environ.get("PORT", 5000))
    debug_mode = "PORT" not in os.environ
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
