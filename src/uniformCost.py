import heapq

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