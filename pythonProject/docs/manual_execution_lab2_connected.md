# Manual Execution for Problems 3 and 4

## Graph with 3 connected components

Source file: `data/manual/undirected_components_1.txt`

Vertices: `0 1 2 3 4 5 6 7`

Edges:
- 0 -- 1
- 1 -- 2
- 2 -- 3
- 3 -- 0
- 0 -- 2
- 4 -- 5
- 5 -- 6
- 4 -- 6

Vertex `7` is isolated.

### Problem 3: DFS connected components

Traversal:

| Step | Stack before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 1 | 0 | 0 | `0` |
| 2 | 3, 2, 1 | 1 | `0, 1` |
| 3 | 3, 2, 3, 2 | 2 | `0, 1, 2` |
| 4 | 3, 2, 3, 3 | 3 | `0, 1, 2, 3` |

First component: `{0, 1, 2, 3}`

Restart from the smallest unvisited vertex:

| Step | Stack before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 5 | 4 | 4 | `0, 1, 2, 3, 4` |
| 6 | 6, 5 | 5 | `0, 1, 2, 3, 4, 5` |
| 7 | 6, 6 | 6 | `0, 1, 2, 3, 4, 5, 6` |

Second component: `{4, 5, 6}`

Restart again:

| Step | Stack before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 8 | 7 | 7 | `0, 1, 2, 3, 4, 5, 6, 7` |

Third component: `{7}`

### Problem 4: BFS connected components

Traversal:

| Step | Queue before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 1 | 0 | 0 | `0, 1, 2, 3` |
| 2 | 1, 2, 3 | 1 | `0, 1, 2, 3` |
| 3 | 2, 3 | 2 | `0, 1, 2, 3` |
| 4 | 3 | 3 | `0, 1, 2, 3` |

First component: `{0, 1, 2, 3}`

Restart from `4`:

| Step | Queue before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 5 | 4 | 4 | `0, 1, 2, 3, 4, 5, 6` |
| 6 | 5, 6 | 5 | `0, 1, 2, 3, 4, 5, 6` |
| 7 | 6 | 6 | `0, 1, 2, 3, 4, 5, 6` |

Second component: `{4, 5, 6}`

Restart from `7`:

| Step | Queue before pop | Popped | Visited after step |
| --- | --- | --- | --- |
| 8 | 7 | 7 | `0, 1, 2, 3, 4, 5, 6, 7` |

Third component: `{7}`

## Graph with 1 connected component

Source file: `data/manual/undirected_components_2.txt`

Edges:
- 0 -- 1
- 1 -- 2
- 2 -- 3
- 3 -- 4
- 4 -- 5
- 5 -- 0
- 0 -- 2
- 1 -- 4

### Problem 3: DFS connected components

Starting from `0`, the traversal reaches every vertex:

`0 -> 1 -> 2 -> 3 -> 4 -> 5`

Connected components: `{0, 1, 2, 3, 4, 5}`

### Problem 4: BFS connected components

Starting from `0`, the queue expands in this order:

`0 -> 1 -> 2 -> 5 -> 3 -> 4`

Connected components: `{0, 1, 2, 3, 4, 5}`
