# Manual Execution for Problems 1 and 2

## Small graph 1

Source file: `data/manual/directed_manual_1.txt`

Edges:
- 0 -> 1
- 0 -> 2
- 0 -> 3
- 1 -> 0
- 1 -> 3
- 1 -> 4
- 2 -> 1
- 2 -> 4
- 3 -> 2
- 4 -> 3

### Problem 1: forward BFS from 0 to 4

Queue and parent map:

| Step | Popped | Queue after step | New parents |
| --- | --- | --- | --- |
| 0 | - | 0 | `0: none` |
| 1 | 0 | 1, 2, 3 | `1: 0`, `2: 0`, `3: 0` |
| 2 | 1 | 2, 3, 4 | `4: 1` |
| 3 | 2 | 3, 4 | none |
| 4 | 3 | 4 | none |
| 5 | 4 | empty | stop |

Reconstructed path: `0 -> 1 -> 4`

Lowest length: `2`

### Problem 2: backward BFS from 0 to 4

Queue and next map:

| Step | Popped | Queue after step | New next vertices |
| --- | --- | --- | --- |
| 0 | - | 4 | `4: none` |
| 1 | 4 | 1, 2 | `1: 4`, `2: 4` |
| 2 | 1 | 2, 0 | `0: 1` |
| 3 | 2 | 0, 3 | `3: 2` |
| 4 | 0 | 3 | stop |

Reconstructed path from start: `0 -> 1 -> 4`

Lowest length: `2`

## Small graph 2

Source file: `data/manual/directed_manual_2.txt`

Edges:
- 0 -> 1
- 0 -> 4
- 1 -> 2
- 1 -> 4
- 2 -> 0
- 2 -> 3
- 2 -> 4
- 3 -> 1
- 4 -> 2
- 4 -> 3

### Problem 1: forward BFS from 3 to 0

Queue and parent map:

| Step | Popped | Queue after step | New parents |
| --- | --- | --- | --- |
| 0 | - | 3 | `3: none` |
| 1 | 3 | 1 | `1: 3` |
| 2 | 1 | 2, 4 | `2: 1`, `4: 1` |
| 3 | 2 | 4, 0 | `0: 2` |
| 4 | 4 | 0 | none |
| 5 | 0 | empty | stop |

Reconstructed path: `3 -> 1 -> 2 -> 0`

Lowest length: `3`

### Problem 2: backward BFS from 3 to 0

Queue and next map:

| Step | Popped | Queue after step | New next vertices |
| --- | --- | --- | --- |
| 0 | - | 0 | `0: none` |
| 1 | 0 | 2 | `2: 0` |
| 2 | 2 | 1, 4 | `1: 2`, `4: 2` |
| 3 | 1 | 4, 3 | `3: 1` |
| 4 | 4 | 3, 0 | none |
| 5 | 3 | 0 | stop |

Reconstructed path from start: `3 -> 1 -> 2 -> 0`

Lowest length: `3`

## Large graph results

The official datasets were run from the files in `data/large`.

### graph1k

Forward BFS:
- `1 -> 100`: length `6`, path `1 -> 5 -> 487 -> 175 -> 699 -> 624 -> 100`
- `100 -> 1`: length `5`, path `100 -> 416 -> 354 -> 865 -> 109 -> 1`

Backward BFS:
- `1 -> 100`: length `6`, path `1 -> 5 -> 487 -> 175 -> 699 -> 624 -> 100`
- `100 -> 1`: length `5`, path `100 -> 416 -> 354 -> 865 -> 109 -> 1`

### graph10k

Forward BFS:
- `1 -> 100`: length `8`, path `1 -> 3300 -> 2607 -> 523 -> 6311 -> 5359 -> 9794 -> 5173 -> 100`
- `100 -> 1`: length `7`, path `100 -> 2398 -> 3054 -> 5232 -> 8217 -> 2478 -> 7151 -> 1`

Backward BFS:
- `1 -> 100`: length `8`, path `1 -> 7317 -> 4118 -> 2404 -> 690 -> 1494 -> 739 -> 4722 -> 100`
- `100 -> 1`: length `7`, path `100 -> 5568 -> 2781 -> 1451 -> 4997 -> 528 -> 4260 -> 1`

### graph100k

Forward BFS:
- `1 -> 100`: length `8`, path `1 -> 17024 -> 27471 -> 14969 -> 3075 -> 4156 -> 32753 -> 14973 -> 100`
- `100 -> 1`: length `8`, path `100 -> 44340 -> 54527 -> 6606 -> 53263 -> 95930 -> 98655 -> 58288 -> 1`

Backward BFS:
- `1 -> 100`: length `8`, path `1 -> 17024 -> 27471 -> 14969 -> 3075 -> 4156 -> 32753 -> 14973 -> 100`
- `100 -> 1`: length `8`, path `100 -> 44340 -> 54527 -> 6606 -> 53263 -> 95930 -> 98655 -> 58288 -> 1`

Note: on `graph10k`, the forward and backward traversals return different paths for the same query, but the lengths are the same. That is valid because the graph has multiple shortest paths.
