"""
campus_data.py

This file defines the CampusNav graph.

WHY A DICT-OF-LISTS (ADJACENCY LIST)?
--------------------------------------
An adjacency list stores, for each node, only the neighbors it's
directly connected to (plus the edge weight/distance to each).

This is the natural fit here because:
- Our campus graph is SPARSE (13 nodes, only 13 edges) — most pairs
  of locations are NOT directly connected.
- Space complexity O(V + E) instead of O(V^2) for an adjacency matrix.
- Dijkstra needs to repeatedly ask "who are node X's neighbors?" —
  an adjacency list answers that directly in O(degree) time.

Each edge is stored in BOTH directions because campus paths are
walkable both ways (undirected graph). Weights are distances in
meters, estimated from the official GGSIPU East Delhi Campus map.
"""

CAMPUS_GRAPH = {
    "Gate01": {"BlockB": 100, "BlockG": 110},
    "Gate02": {"BlockE": 70},

    "BlockB": {"Gate01": 100, "BlockC": 40, "BlockG": 60},
    "BlockC": {"BlockB": 40, "BlockA": 40, "BlockD": 35},
    "BlockA": {"BlockC": 40, "BlockE": 120},
    "BlockD": {"BlockC": 35, "BoysHostel": 90},
    "BlockE": {"BlockA": 120, "Gate02": 70, "EastEndClub": 40},
    "BlockG": {"Gate01": 110, "BlockB": 60},

    "BoysHostel": {"BlockD": 90, "TeachersHostel": 50},
    "TeachersHostel": {"BoysHostel": 50, "GirlsHostel": 40},
    "GirlsHostel": {"TeachersHostel": 40, "Housing": 60},
    "Housing": {"GirlsHostel": 60},

    "EastEndClub": {"BlockE": 40},
}

# Human-readable labels, for display purposes only (not used by the algorithm)
LOCATION_NAMES = {
    "Gate01": "Gate 01 (Main Entrance)",
    "Gate02": "Gate 02",
    "BlockA": "Block A - USAR (Automation & Robotics)",
    "BlockB": "Block B - USDI (Design & Innovation)",
    "BlockC": "Block C - Central Library",
    "BlockD": "Block D - Administrative Block",
    "BlockE": "Block E - Auditorium",
    "BlockG": "Block G - Sports Hall",
    "BoysHostel": "Boy's Hostel",
    "GirlsHostel": "Girl's Hostel",
    "TeachersHostel": "Teacher's Hostel",
    "Housing": "Housing (Type II-V)",
    "EastEndClub": "East End Club",
}