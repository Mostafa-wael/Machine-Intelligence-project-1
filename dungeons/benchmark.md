## Approaches Comparison
Command: `python3 play_dungeon.py dungeons/dungeon1.txt -a astar -hf zero`
Command: `python3 play_dungeon.py dungeons/dungeon1.txt -a astar -hf waek`
Command: `python3 play_dungeon.py dungeons/dungeon1.txt -a astar -hf strong -c`
command: `python3 play_dungeon.py dungeons/dungeon4.txt -a gbfs -hf strong`

## A* Search
|Map| No Heuristic  | Weak Heuristic  | closestToExit Heuristic  | closestToOthers Heuristic | DP_closestToExit Heuristic  | DP_closestToOthers Heuristic |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Dungeon 1| 749 | 680 | 618 | 634 | 110 | 643 |
|Dungeon 2| 46 | 46 | 46 | 46 | 46 | 46|
|Dungeon 3| 21373 | 16246 | 15090 | 8939 | 155 | 11039 |
|Dungeon 4| ? | ? | ? | ? | ? | ? |

## Greedy Best First Search
|Map| No Heuristic  | Weak Heuristic  | closestToExit Heuristic  | closestToOthers Heuristic | DP_closestToExit Heuristic  | DP_closestToOthers Heuristic |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Dungeon 1| 749 | 600 | 437 | 83 | 64 | 70 |
|Dungeon 2| 46 | 27 | 14 | 14 | 14 | 14|
|Dungeon 3| 21373 | 23081 | 57729 | 149 | 111 | 188 |
|Dungeon 4| ? | ? | ? | 282 | ? | 597 |