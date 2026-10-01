"""
dijkstra.py

WHY DIJKSTRA (not BFS)?
------------------------
BFS finds the shortest path in terms of NUMBER OF EDGES — it assumes
every edge costs the same (1 hop = 1 hop). That's wrong for us,
because "Block A -> Block E" (120m) is not the same cost as
"Block C -> Block D" (35m).

Our campus graph has WEIGHTED edges (real distances in meters), so we
need an algorithm that accounts for those weights. Dijkstra's
algorithm finds the shortest weighted path from a single source to
all other nodes (or a specific destination), as long as all weights
are non-negative — which distances always are.

HOW IT WORKS (high level):
1. Keep a "distance so far" for every node; start = 0, everything
   else = infinity.
2. Always expand the unvisited node with the smallest known distance
   (a min-priority-queue makes this fast).
3. For each neighbor of that node, check if going through the current
   node gives a shorter path than what we currently know. If so,
   update it ("relax" the edge).
4. Repeat until every node is visited, or we've reached the
   destination.
5. Reconstruct the path by walking backwards through "previous node"
   pointers we recorded along the way.

COMPLEXITY:
- Time: O((V + E) log V) using a binary heap, where V = number of
  nodes (13 here) and E = number of edges (13 here).
- Space: O(V + E) for the graph, distances, and previous-node map.
  For our small campus graph this is instant, but the same code
  scales to a campus with hundreds of nodes.
"""

import heapq


def dijkstra(graph: dict, start: str, end: str):
    """
    Find the shortest path between `start` and `end` in `graph`.

    graph: adjacency list, e.g. {"A": {"B": 5, "C": 2}, ...}
    start, end: node names (must exist in graph)

    Returns:
        (path, total_distance) where path is a list of node names
        from start to end, e.g. ["Gate01", "BlockB", "BlockC"].
        Returns (None, None) if no path exists.
    """
    if start not in graph or end not in graph:
        return None, None

    # distances[node] = shortest known distance from start to node
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    # previous[node] = the node we came from on the shortest path
    previous = {node: None for node in graph}

    # Min-heap of (distance, node). Python's heapq is a min-heap by
    # default, which is exactly what Dijkstra needs: always process
    # the closest unvisited node next.
    priority_queue = [(0, start)]
    visited = set()

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue  # already finalized, skip stale queue entry
        visited.add(current_node)

        if current_node == end:
            break  # shortest path to destination found, stop early

        for neighbor, weight in graph[current_node].items():
            if neighbor in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_dist, neighbor))

    if distances[end] == float("inf"):
        return None, None  # end is unreachable from start

    # Reconstruct path by walking backwards from end to start
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return path, distances[end]