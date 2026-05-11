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

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component                | Variable name in code | Data type | Description |
| ------------------------ | --------------------- | --------- | ----------- |
| Current location         |                       |           |             |
| Relics already collected |                       |           |             |
| Fuel cost so far         |                       |           |             |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property                                    | Your answer      |
| ------------------------------------------- | ---------------- |
| Data structure chosen                       |                  |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected        | Time complexity: |
| Operation: unmark a relic (backtrack)       | Time complexity: |
| Why this structure fits                     |                  |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
