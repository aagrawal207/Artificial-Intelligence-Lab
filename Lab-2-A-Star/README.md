# Assignment 2

Implementing the A* algorithm

### Dependency

You will require `PrettyTable` module to print the data as required. Please install it if not done already using the following command: `pip install PrettyTable`

### Usage

#### Run

There are two python programs: `eight_puzzle_all_heuristics.py` and `eight_puzzle_heuristic_comparison.py`. We wrote these programs using python3.

Run these programs using the command: `python <program-name> <input-file-relative-path>`. Please use python3 command respective to your system.

#### Input format

All the input should be in the following format:

```
Start State:
8 3 5
4 1 6
2 7 0

Goal State:
1 2 3
8 0 4
7 6 5

// Consider 0 as blank
```

Example input files are present in the folder `input`. You can put the input file anywhere but you will be require to put the relative path in command line while running the programs.

#### Sample output

For `eight_puzzle_all_heuristics.py`:

```
$ python3 eight_puzzle_all_heuristics.py input/input_solvable.txt
1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Large Heuristic (h(n) > h*(n)).
5. Displaced tile heuristic with blank tile cost included
6. Manhattand distance heuristic with blank tile cost included
7. Compare all the above and show in table format.
Enter choice: 7
+---------------------------+-----------------------+----------------------------------+-------------------+-------------------------+---------------------------------+
|         Heuristic         | Total states explored | Total states on the optimal path | Optimal path cost | Total time taken (secs) | Monotonic restriction satisfied |
+---------------------------+-----------------------+----------------------------------+-------------------+-------------------------+---------------------------------+
|        No Heuristic       |         110699        |                24                |         23        |    10.601903805974871   |               True              |
|      Displaced tiles      |         13738         |                24                |         23        |     1.65170287003275    |               True              |
|         Manhattan         |          1658         |                24                |         23        |   0.21324810897931457   |               True              |
|      Large Heuristic      |          1715         |               102                |        101        |    0.1782806320115924   |              False              |
| Displaced with blank tile |         14427         |                24                |         23        |    1.4462313030380756   |              False              |
| Manhattan with blank tile |          1700         |                24                |         23        |    0.2286340210121125   |              False              |
+---------------------------+-----------------------+----------------------------------+-------------------+-------------------------+---------------------------------+
```

For `eight_puzzle_heuristic_comparison.py`:

```
$ python3 eight_puzzle_heuristic_comparison.py input/input_solvable.txt
1. Zero Heuristic.
2. Displced tiles Heuristic.
3. Manhattan distance Heuristic.
4. Large Heuristic (h(n) > h*(n)).
5. Displaced tiles heuristic with blank tile cost included.
6. Manhattan distance heuristic with blank tile cost included
Enter choice 1 for comparison: 2
Enter choice 2 for comparison: 3
+-----------------+---------------------+--------------------------------+-------------------+---------------------+---------------------------------+
|    Heuristic    | No. states explored | No. states on the optimal path | Optimal path cost |  Time taken (secs)  | Monotonic restriction satisfied |
+-----------------+---------------------+--------------------------------+-------------------+---------------------+---------------------------------+
| Displaced Tiles |        13738        |               24               |         23        |  1.4306556159863248 |               True              |
|    Manhattan    |         1658        |               24               |         23        | 0.20955026207957417 |               True              |
+-----------------+---------------------+--------------------------------+-------------------+---------------------+---------------------------------+

Displaced Tiles visits all nodes visited by Manhattan plus extra
```
