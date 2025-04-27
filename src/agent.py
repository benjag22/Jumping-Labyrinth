from boardAdjacencyList import BoardAdjacencyList
from dfs import depth_first_search
from uniformCost import uniform_cost_search

board1 = [

    [3, 4, 1, 3, 1],
    [3, 3, 3, "G", 2],
    [3, 1, 2, 2, 3],
    [4, 2, 3, 3, 3],
    [4, 1, 4, 3, 2]
]
board2 = [
    [3, 3, 2, 4, 4],
    [2, 2, 2, 1, 1],
    [4, 3, 1, 3, 4],
    [2, 3, 1, 1, 3],
    [1, 1, 3, 2, 'G']
]

graph = BoardAdjacencyList(board2, (0, 0))

print(depth_first_search(graph.get_adjacency_list(), (0, 0), graph._goal_pos))
print(uniform_cost_search(graph.get_adjacency_list(), (0, 0), graph._goal_pos))