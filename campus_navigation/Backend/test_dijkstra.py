"""
test_dijkstra.py

Quick manual tests to verify Dijkstra works correctly on our real
campus graph BEFORE we touch Flask or any frontend code.

Run this directly: python test_dijkstra.py
"""

from campus_data import CAMPUS_GRAPH, LOCATION_NAMES
from dijkstra import dijkstra


def show_result(start, end):
    path, total = dijkstra(CAMPUS_GRAPH, start, end)
    print(f"\nFrom: {LOCATION_NAMES.get(start, start)}")
    print(f"To:   {LOCATION_NAMES.get(end, end)}")

    if path is None:
        print("No route found.")
        return

    print("Route:")
    for i, node in enumerate(path):
        prefix = "  " if i == 0 else "  -> "
        print(f"{prefix}{LOCATION_NAMES.get(node, node)}")
    print(f"Total distance: {total} m")


if __name__ == "__main__":
    print("=" * 50)
    print("CampusNav - Dijkstra Test")
    print("=" * 50)

    # Test 1: A normal multi-hop route across campus
    show_result("Gate01", "Housing")

    # Test 2: A short, direct-ish route
    show_result("Gate01", "BlockA")

    # Test 3: A route to the far end of the hostel chain
    show_result("BlockA", "Housing")

    # Test 4: Same start and end (edge case, should be trivial)
    show_result("BlockC", "BlockC")

    # Test 5: A route via Gate02
    show_result("Gate02", "Housing")