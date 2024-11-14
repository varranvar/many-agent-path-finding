# TODO

- [X] Basic visualization
- [X] Agent movement
- [X] Random Walk
- [X] Basic A Star
- [X] A Star, Naive Overlap Check, Single Goal
- [ ] A Star, Optimal Overlap Check, Singe Goal
- [ ] A Star, Optimal Overlap Check, Multiple Goals
- [ ] Corner Reduction
- [ ] A Star, Optimal Overlap Check, Multiple Goals, Corner Reduction
- [ ] Faster drawing for 100,000 agents (perhaps by drawing to a second surface then rendering to main screen)
- [ ] Maze generation
- [ ] Modifying the maze with mouse
- [ ] Data collection

# Notes on the algorithms

- algorithm for effecient many-agent many-goal optimal path finding:
  - do A* starting from both the start and the goal (two queues!)
  - once a new value is added to either queue, check if it's pairing with every value in the other queue already has a path saved
  - once a path is found, store every permutation of it
    - e.g. [1, 2, 3, 4] => (1, 2 -> 2), (1, 3 -> 2), (1, 3 -> 2), (1, 4 -> 2)
      - also the reverse, e.g. (4, 1 -> 3)
      - that way look-up for paths is O(1)
    - perhaps this can be a linked list kind of situation to reduce power
      - like best_move<(A, B)> = C, do C, then you can do best_ move<(C, B)> to get the next move
