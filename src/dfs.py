
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