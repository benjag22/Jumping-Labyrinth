from directions import Directions

class BoardAdjacencyList:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0
        self.adj_list = self._build_adjacency_list()

    def _build_adjacency_list(self):
        adjacency_list = {}
        directions = [Directions.RIGHT,Directions.LEFT,Directions.UP,Directions.DOWN]

        for i in range(self.rows):
            for j in range(self.cols):

                position = (i,j)
                adjacency_list[position] = []

                for x, y in directions:

                    neighbor_of_position_i = i + x
                    neighbor_of_position_j = j + y

                    if 0 <= neighbor_of_position_i < self.rows and 0 <= neighbor_of_position_j < self.cols:

                        adjacency_list[position].append((neighbor_of_position_i,neighbor_of_position_j))
        return adjacency_list