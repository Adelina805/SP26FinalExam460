# Development Log – The Torchbearer

**Student Name:** Adelina Martinez
**Student ID:** 827822314

---

## Entry 1 – 5/11/26: Initial Plan

Finally getting started with initial plan and project setup. I started by reading the assignment and deciding what approach I want for each problem, as well as get started on the README answers (part 1-3) and filling DEVLOG Entry 1. My plan is to start with Dijkstra first, then use it to precompute the shortest costs from the entrance and each relic. After that I'll write a recursive search that tries different relic orders while tracking the best route found so far. Based on my experience with the midterm and practice in this class so far, I am assuming the hardest parts will be handling unreachable paths and keeping the README variable names consistent with the code. I plan on testing with small graphs so I can calculate the expected answers by hand, including the B/C/D example from the spec. Final assignment lets go!

---

## Entry 2 – 5/12/26: Search Design and Pruning Plan

Today I worked on README Parts 4-6 and focused on how the recursive search should be represented. I decided to keep the state simple: current location, visited relics, and fuel cost so far. I also decided to use a set for visited relics because checking, adding, and removing relics is straightforward for backtracking. For pruning, I am starting with best-so-far pruning because it is simple, safe, and easier to explain clearly.

---

## Entry 3 – 5/12/26: Directed Graph and Distance Table Testing

While implementing Dijkstra and precomputation, I initially thought about some paths as if they could be reversed, which treated the graph like it was undirected. This caused incorrect assumptions about reachability between nodes. I fixed this by making sure I only followed outgoing edges in the adjacency list and tested with small directed examples. I also verified that unreachable nodes correctly return infinity in the distance table.

---

## Entry 4 – 5/13/26: Post-Implementation Reflection

> Two to five sentences Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – 5/14/26: Time Estimate

| Part                           | Estimated Hours |
| ------------------------------ | --------------- |
| Part 1: Problem Analysis       | 1               |
| Part 2: Precomputation Design  |                 |
| Part 3: Algorithm Correctness  |                 |
| Part 4: Search Design          |                 |
| Part 5: State and Search Space |                 |
| Part 6: Pruning                |                 |
| Part 7: Implementation         |                 |
| README and DEVLOG writing      | 1.5             |
| **Total**                      |                 |
