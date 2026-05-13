# The Torchbearer

**Student Name:** Adelina Martinez
**Student ID:** 827822314
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- ## **Why a single shortest-path run from S is not enough:**
- For the torchbearer problem, a single Dijkstra run from S only gives the shortest distance from the entrance to other nodes, but it does not choose how to visit all relics and reach the exit. It also cannot decide on the order of relic to visit to achieve the minimum total cost.

- ## **What decision remains after all inter-location costs are known:**
- After all the inter-location costs are known, the remaining decision is to choose the order of what relic to visit all of them before going to the exit.

- ## **Why this requires a search over orders (one sentence):**
- This requires a search over orders because choosing different visiting orders of the relics can cause different total fuel costs.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| Entrance node S  | The route starts here, so the planner needs shortest costs from S to each relic.                        |
| Relic chambers   | After collecting a relic, the planner may need shortest costs from that relic to another relic or to T. |

### Part 2b: Distance Storage

| Property                    | Your answer                                           |
| --------------------------- | ----------------------------------------------------- |
| Data structure name         | Nested dictionary                                     |
| What the keys represent     | outer key = source node; inner key = destination node |
| What the values represent   | Shortest fuel cost from source to destination         |
| Lookup time complexity      | O(1) average case                                     |
| Why O(1) lookup is possible | Python dictionary lookups use hashing                 |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1
- **Cost per run:** O(m log n)
- **Total complexity:** O((k + 1)m log n)
- **Justification (one line):** Dijkstra runs once from S and once from each of the k relics.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
- The shortest path distance to these nodes is already final and will never change.

- **For nodes not yet finalized (not in S):**
- Their current distance is the shortest known path so far using only finalized nodes and still has the chance to improve / find a shorter path.

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
- For initialization, the invariant holds before iteration 1 because only the source has a distance of 0 and is correct because no shorter path exists.
- All the other nodes start at infinity which means no paths have been discovered yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
- For maintenance, finalizing the node with the smallest distance is always correct because no shorter path can reach it later. It is the best possible choice.
- This is guaranteed because all edge weights are nonnegative so any new path would only increase the distance positively.

- **Termination : what the invariant guarantees when the algorithm ends:**
- For termination, the algorithm's completion guarantees that all reachable nodes have been finalized with their true shortest distances.

### Part 3c: Why This Matters for the Route Planner

- This matters for the route planner because it will rely on these distances being correct so it can accurately compare the different relic visit orders and choose the minimum cost route.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** picking the closest next relic can create a bad route later.
- **Counter-example setup:** S starts, relics are A and B, and T is the exit with costs: S -> A = 1, S -> B = 2, A -> B = 100, A -> T = 1, B -> A = 1, B -> T = 1
- **What greedy picks:** from S, greedy picks A because cost is 1. Then the most likely route is S -> A -> B -> T = 1 + 100 + 1 = 102
- **What optimal picks:** The optimal route is S -> B -> A -> T = 2 + 1 + 1 = total cost 4
- **Why greedy loses:** Greedy loses because it doesn't consider all possible relic orders and only picks the closest relic which leads to a worse route later than the optimal solution.

### What the Algorithm Must Explore

- The algorithm must explore all possible relic orders, because the locally cheapest next relic may not lead to the globally cheapest full route.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component                | Variable name in code | Data type  | Description                                       |
| ------------------------ | --------------------- | ---------- | ------------------------------------------------- |
| Current location         | current_loc           | node label | The node where the search currently is.           |
| Relics already collected | relics_visited_order  | list       | The relics collected so far in the current route. |
| Fuel cost so far         | cost_so_far           | number     | The total fuel used by the current partial route. |

### Part 5b: Data Structure for Visited Relics

| Property                                    | Your answer                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------------- |
| Data structure chosen                       | set                                                                                   |
| Operation: check if relic already collected | Time complexity: O(1) average                                                         |
| Operation: mark a relic as collected        | Time complexity: O(1) average                                                         |
| Operation: unmark a relic (backtrack)       | Time complexity: O(1) average                                                         |
| Why this structure fits                     | A set makes it simple to check, add, and remove relics during recursive backtracking. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** k!
- **Why:** With k relics, the search may need to try every possible ordering of the relics.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** The algorithm tracks the best completed route cost found so far.
- **When it is used:** It is used during the recursive search before continuing to explore a new branch.
- **What it allows the algorithm to skip:** It allows the algorithm to skip exploring any branch where the current fuel cost is already greater than or equal to the best known cost.

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** The current location, the list of visited relics, the remaining relics, and the fuel cost so far.
- **What the lower bound accounts for:** The lower bound is based on the fuel cost so far, which represents the minimum possible cost of the current partial route.
- **Why it never overestimates:** It never overestimates because all edge weights are nonnegative, so the total cost can only increase from the current fuel cost.

### Part 6c: Pruning Correctness

- Pruning is safe because if the current fuel cost is already greater than or equal to the best known complete route, adding more nonnegative costs cannot make it any better. Therefore, pruning this branch cannot remove the optimal solution.

---

## References

- Lecture notes only.
