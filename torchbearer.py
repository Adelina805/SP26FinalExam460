"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Adelina Martinez
Student ID: 827822314

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return """
    Why a single shortest-path run from S is not enough: For the torchbearer problem, a single Dijkstra run from S only gives the shortest distance from the entrance to other nodes, but it does not choose how to visit all relics and reach the exit. It also cannot decide on the order of relic to visit to achieve the minimum total cost.
    What decision remains after all inter-location costs are known: After all the inter-location costs are known, the remaining decision is to choose the order of what relic to visit all of them before going to the exit.
    Why this requires a search over orders (one sentence): This requires a search over orders because choosing different visiting orders of the relics can cause different total fuel costs.
    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    # Collect all nodes we need shortest paths from: spawn and each relic
    sources = []

    # Include the starting node
    if spawn not in sources:
        sources.append(spawn)

    # Include each relic as a source for later route segments
    for relic in relics:
        if relic not in sources: # add each relic if not already in sources
            sources.append(relic)

    return sources # return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    # Initialize all known nodes with infinite distance
    dist = {node: float('inf') for node in graph}

    # Ensure the source exists and starts at distance 0
    if source not in dist:
        dist[source] = float('inf')
    dist[source] = 0

    # Min-heap storing (current_cost, node)
    heap = [(0, source)]

    while heap:
        cur_cost, u = heapq.heappop(heap)

        # Ignore outdated entries that are no longer optimal
        if cur_cost > dist.get(u, float('inf')):
            continue

        # Explore outgoing edges from current node (if u has no outgoing edges, use empty list)
        for v, w in graph.get(u, []):
            # Add neighbor to dist if it was not originally a key in graph
            if v not in dist:
                dist[v] = float('inf')

            new_cost = cur_cost + w

            # Relax edge if a shorter path is found
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    # Select all nodes we need shortest paths FROM (S and each relic)
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {} # dist_table[src][v] will store shortest distance from src to v
    for src in sources: # Run Dijkstra from each source node to compute all outgoing distances
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return """
    Part 3: Algorithm Correctness

    Part 3a: What the Invariant Means

    For nodes already finalized (in S):
    The shortest path distance to these nodes is already final and will never change.

    For nodes not yet finalized (not in S):
    Their current distance is the shortest known path so far using only finalized nodes and still has the chance to improve / find a shorter path.

    Part 3b: Why Each Phase Holds

    Initialization : why the invariant holds before iteration 1:
    For initialization, the invariant holds before iteration 1 because only the source has a distance of 0 and is correct because no shorter path exists.
    All the other nodes start at infinity which means no paths have been discovered yet.

    Maintenance : why finalizing the min-dist node is always correct:
    For maintenance, finalizing the node with the smallest distance is always correct because no shorter path can reach it later. It is the best possible choice.
    This is guaranteed because all edge weights are nonnegative so any new path would only increase the distance positively.

    Termination : what the invariant guarantees when the algorithm ends:
    For termination, the algorithm's completion guarantees that all reachable nodes have been finalized with their true shortest distances.

    Part 3c: Why This Matters for the Route Planner
    This matters for the route planner because it will rely on these distances being correct so it can accurately compare the different relic visit orders and choose the minimum cost route.
    """

# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return """
    Part 4: Search Design

    Why Greedy Fails

    - The failure mode: picking the closest next relic can create a bad route later.
    - Counter-example setup: S starts, relics are A and B, and T is the exit with costs: S -> A = 1, S -> B = 2, A -> B = 100, A -> T = 1, B -> A = 1, B -> T = 1
    - What greedy picks: from S, greedy picks A because cost is 1. Then the most likely route is S -> A -> B -> T = 1 + 100 + 1 = 102
    - What optimal picks: The optimal route is S -> B -> A -> T = 2 + 1 + 1 = total cost 4
    - Why greedy loses: Greedy loses because it doesn't consider all possible relic orders and only picks the closest relic which leads to a worse route later than the optimal solution.

    What the Algorithm Must Explore

    The algorithm must explore all possible relic orders, because the locally cheapest next relic may not lead to the globally cheapest full route.
    """

# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    # Initialize best as a mutable container so _explore can update it
    best = [float('inf'), []]

    # Use a set for relics_remaining as required by the README
    relics_remaining = set(relics)
    relics_visited_order = []
    cost_so_far = 0

    # Start recursive exploration from the spawn
    _explore(dist_table, spawn, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best)

    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    # Pruning: if current partial cost already exceeds best, stop exploring.
    # Because all future edge costs are nonnegative, this branch can only get more expensive.
    # So if it already costs at least best[0], it cannot become the optimal route.
    if cost_so_far >= best[0]:
        return

    # Base case: no relics left to visit, try to go to the exit
    if not relics_remaining:
        exit_cost = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total_cost = cost_so_far + exit_cost
        # If exit is reachable and this route is better, update best
        if exit_cost != float('inf') and total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    # Recursive case: try visiting each remaining relic next
    for relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(relic, float('inf'))
        # Skip unreachable relic from current location
        if travel_cost == float('inf'):
            continue

        # Choose this relic and recurse
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)

        _explore(dist_table, relic, relics_remaining, relics_visited_order,
                 cost_so_far + travel_cost, exit_node, best)

        # Backtrack
        relics_visited_order.pop()
        relics_remaining.add(relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    # Precompute shortest distances from spawn and each relic
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    # Find the optimal route using the recursive search
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")

if __name__ == "__main__":
    _run_tests()