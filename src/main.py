from src.boardAdjacencyList import BoardAdjacencyList


def main():
    mazes = []
    while True:
        first_line = input().strip()
        first_line_list = first_line.split()

        if len(first_line_list) == 1 and first_line_list[0] == "0":
            break

        n = int(first_line_list[0])
        m = int(first_line_list[1])
        init_pos = (int(first_line_list[2]), int(first_line_list[3]))
        goal_pos = (int(first_line_list[4]), int(first_line_list[5]))

        matrix = []

        for i in range(n):
            i_line = input().strip().split()
            if len(i_line) < m:
                exit(1)
            matrix.append(i_line)
        mazes.append(BoardAdjacencyList(matrix, init_pos, goal_pos))

if __name__ == "__main__":
    main()