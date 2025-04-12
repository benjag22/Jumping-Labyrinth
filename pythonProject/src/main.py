from boardAdjacencyList import BoardAdjacencyList


def depth_first_search(adjacent_list, init_pos, goal_pos):
    if not goal_pos:
        return None

    visited_nodes = set()
    stack = [init_pos]
    parent = {init_pos: None}

    while stack:
        node = stack.pop()

        if node == goal_pos:
            path = []
            current = node
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if node not in visited_nodes:
            visited_nodes.add(node)

            for neighbor in adjacent_list[node]:

                if neighbor not in visited_nodes:
                    stack.append(neighbor)

                    if neighbor not in parent:
                        parent[neighbor] = node

    return None

if __name__ == "__main__":
    board = [
        [3, 4, 1, 3, 1],
        [3, 3, 3, "G", 2],
        [3, 1, 2, 2, 3],
        [4, 2, 3, 3, 3],
        [4, 1, 4, 3, 2]
    ]

    graph = BoardAdjacencyList(board, (0, 0))
    print(len(depth_first_search(graph.get_adjacency_list(), (0, 0), (1, 3))))
    print(depth_first_search(graph.get_adjacency_list(), (0, 0), (1, 3)))

