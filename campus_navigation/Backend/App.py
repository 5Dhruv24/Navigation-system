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

from flask import Flask, jsonify, request
from flask_cors import CORS

from campus_data import CAMPUS_GRAPH, LOCATION_NAMES
from dijkstra import dijkstra

# static_folder points at the frontend directory (one level up, then into
# frontend/) so Flask can serve index.html and assets/campus_map.jpg
# directly. static_url_path="" means those files are served from the
# root URL (e.g. /index.html, /assets/campus_map.jpg) instead of /static/...
app = Flask(__name__, static_folder="../frontend", static_url_path="")
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)