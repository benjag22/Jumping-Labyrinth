from boardAdjacencyList import BoardAdjacencyList
import heapq

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


def uniform_cost_search(adjacent_list, init_pos, goal_pos):
    if not goal_pos:
        return None

    priority_queue = [(0, init_pos)]

    cost_so_far = {init_pos: 0}

    parent = {init_pos: None}

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_node == goal_pos:
            path = []

            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return path[::-1]

        for neighbor in adjacent_list[current_node]:
            new_cost = current_cost + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(priority_queue, (new_cost, neighbor))
                parent[neighbor] = current_node

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

    print(depth_first_search(graph.get_adjacency_list(), (0, 0), graph.goal_pos))
    print(uniform_cost_search(graph.get_adjacency_list(), (0, 0), graph.goal_pos))

