from directions import Directions

class BoardAdjacencyList:
    def __init__(self, board, start_pos, goal_marker= "G"):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0
        self.start_pos = start_pos

        self.goal_pos = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == goal_marker:
                    self.goal_pos = (i, j)
                    break
            if self.goal_pos:
                break

        self.adj_list = self._build_adjacency_list()


    def _build_adjacency_list(self):
        adjacency_list = {}
        directions = [Directions.RIGHT, Directions.LEFT, Directions.UP, Directions.DOWN]

        for i in range(self.rows):
            for j in range(self.cols):

                position = (i,j)
                adjacency_list[position] = []

                if position == self.goal_pos:
                    continue
                jumps = self.board[i][j]

                for direction in directions:
                    x, y = direction.value

                    neighbor_of_position_i = i + x*jumps
                    neighbor_of_position_j = j + y*jumps

                    if 0 <= neighbor_of_position_i < self.rows and 0 <= neighbor_of_position_j < self.cols:
                        adjacency_list[position].append((neighbor_of_position_i,neighbor_of_position_j))

        return adjacency_list

    def get_adjacency_list(self):
        return self.adj_list

    def print_adjacency_list(self):
        for pos, neighbors in self.adj_list.items():
            i, j = pos
            value = self.board[i][j]
            neighbors_with_values = [(neighbor, self.board[neighbor[0]][neighbor[1]]) for neighbor in neighbors]
            print(f"({i},{j}) [Valor: {value}] -> {neighbors_with_values}")