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
    # Gate 01 sits beside Block E (Auditorium); Gate 02 is the entrance
    # near the Block B/C/A parking area. East End Club has been removed
    # per confirmed on-the-ground campus layout.
    "Gate01": {"BlockE": 60},
    "Gate02": {"BlockB": 80},

    "BlockB": {"Gate02": 80, "BlockC": 40, "BlockG": 60},
    "BlockC": {"BlockB": 40, "BlockA": 40, "BlockD": 35},
    "BlockA": {"BlockC": 40, "BlockE": 120},
    "BlockD": {"BlockC": 35, "BoysHostel": 90},
    "BlockE": {"BlockA": 120, "Gate01": 60},
    "BlockG": {"BlockB": 60},

    "BoysHostel": {"BlockD": 90, "TeachersHostel": 50},
    "TeachersHostel": {"BoysHostel": 50, "GirlsHostel": 40},
    "GirlsHostel": {"TeachersHostel": 40, "Housing": 60},
    "Housing": {"GirlsHostel": 60},
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
}

# ---------------------------------------------------------------
# Aliases for the natural-language query feature (nl_parser.py).
# Maps common ways a student might refer to a place -> its node
# code. Keys are lowercase; longer/more specific phrases are
# listed before shorter ones so greedy matching prefers them.
# ---------------------------------------------------------------
LOCATION_ALIASES = {
    "main entrance": "Gate01", "main gate": "Gate01", "gate 1": "Gate01",
    "gate01": "Gate01", "gate one": "Gate01",

    "gate 2": "Gate02", "gate02": "Gate02", "gate two": "Gate02",

    "automation": "BlockA", "robotics": "BlockA", "usar": "BlockA",
    "block a": "BlockA",

    "design": "BlockB", "innovation": "BlockB", "usdi": "BlockB",
    "block b": "BlockB",

    "library": "BlockC", "block c": "BlockC",

    "administrative": "BlockD", "admin block": "BlockD", "administration": "BlockD",
    "block d": "BlockD",

    "auditorium": "BlockE", "block e": "BlockE",

    "sports hall": "BlockG", "sports complex": "BlockG", "gym": "BlockG",
    "block g": "BlockG",

    "boys hostel": "BoysHostel", "boy's hostel": "BoysHostel", "boys": "BoysHostel",

    "girls hostel": "GirlsHostel", "girl's hostel": "GirlsHostel", "girls": "GirlsHostel",

    "teachers hostel": "TeachersHostel", "teacher's hostel": "TeachersHostel",
    "faculty hostel": "TeachersHostel", "teachers": "TeachersHostel",

    "housing": "Housing", "quarters": "Housing", "staff quarters": "Housing",
}