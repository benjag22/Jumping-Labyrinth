from directions import Directions

class BoardAdjacencyList:
    _goal_pos: tuple[int, int]
    _start_pos: tuple[int, int]
    _board: list[list[int]]
    _cols: int
    _rows: int

    def __init__(self, board: list[list[int]], start_pos: tuple[int, int], goal_pos: tuple[int, int]):
        self._board = board
        self._rows = len(board)
        self._cols = len(board[0]) if self._rows > 0 else 0
        self._start_pos = start_pos

        self._goal_pos = goal_pos

        self.adj_list = self._build_adjacency_list()


    def _build_adjacency_list(self):
        adjacency_list = {}
        directions = [Directions.RIGHT, Directions.LEFT, Directions.UP, Directions.DOWN]

        for i in range(self._rows):
            for j in range(self._cols):

                position = (i,j)
                adjacency_list[position] = []

                if position == self._goal_pos:
                    continue
                jumps = self._board[i][j]

                for direction in directions:
                    x, y = direction.value

                    neighbor_of_position_i = i + x*jumps
                    neighbor_of_position_j = j + y*jumps

                    if 0 <= neighbor_of_position_i < self._rows and 0 <= neighbor_of_position_j < self._cols:
                        adjacency_list[position].append((neighbor_of_position_i,neighbor_of_position_j))

        return adjacency_list

    def get_adjacency_list(self):
        return self.adj_list

