import pygame
import sys
from boardAdjacencyList import BoardAdjacencyList
from dfs import depth_first_search
from uniformCost import uniform_cost_search

CELL_SIZE = 60
GRID_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
PATH_COLOR = (0, 0, 255)
CURRENT_COLOR = (255, 165, 0)
FONT_SIZE = 24

pygame.init()
font = pygame.font.SysFont('Arial', FONT_SIZE)


class JumpingMaze:
    def __init__(self, maze_file="input.txt"):
        self.mazes = []
        self.current_maze_index = 0
        self.load_mazes(maze_file)
        self.current_algorithm = "uniform"
        self.solution = None
        self.current_step = 0
        self.animation_speed = 500
        self.last_update = 0

        self.setup_window()

    def setup_window(self):
        if not self.mazes:
            print("No hay laberintos para mostrar.")
            sys.exit()

        maze = self.mazes[self.current_maze_index]
        rows, cols = len(maze._board), len(maze._board[0])
        self.width = cols * CELL_SIZE
        self.height = rows * CELL_SIZE + 100
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Laberinto Saltarin")

    def load_mazes(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()

            i = 0
            while i < len(lines):
                first_line = lines[i].strip()
                if first_line == "0":
                    break

                m, n, start_row, start_col, goal_row, goal_col = map(int, first_line.split())

                grid = []
                for j in range(i + 1, i + m + 1):
                    if j < len(lines):
                        row = list(map(int, lines[j].strip().split()))
                        grid.append(row)

                maze = BoardAdjacencyList(grid, (start_row, start_col), (goal_row, goal_col))
                self.mazes.append(maze)

                i += m + 1

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            sys.exit()

    def solve_current_maze(self):
        maze = self.mazes[self.current_maze_index]
        adjacent_list = maze.get_adjacency_list()
        start_pos = maze._start_pos
        goal_pos = maze._goal_pos

        if self.current_algorithm == "dfs":
            self.solution = depth_first_search(adjacent_list, start_pos, goal_pos)
            print(self.solution)
        else:
            self.solution = uniform_cost_search(adjacent_list, start_pos, goal_pos)
            print(self.solution)

        self.current_step = 0
        # Si hay solución, imprimimos el número de pasos
        if self.solution:
            print(f"Solución encontrada en {len(self.solution) - 1} pasos")
        else:
            print("No hay solución")
        return self.solution

    def get_solution_text(self):
        if not self.solution:
            return "No hay solución"
        return f"Solución: {len(self.solution) - 1} pasos"

    def get_current_position(self):
        if not self.solution or self.current_step == 0:
            return self.mazes[self.current_maze_index]._start_pos

        if self.current_step < len(self.solution):
            return self.solution[self.current_step]
        else:
            return self.solution[-1]

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)
        maze = self.mazes[self.current_maze_index]
        grid = maze._board
        rows, cols = len(grid), len(grid[0])

        # Dibujar el grid y los números
        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window, GRID_COLOR, rect, 1)

                text = font.render(str(grid[r][c]), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                self.window.blit(text, text_rect)

        # Dibujar posición inicial
        start_rect = pygame.Rect(maze._start_pos[1] * CELL_SIZE, maze._start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.window, START_COLOR, start_rect, 3)

        # Dibujar posición objetivo
        goal_rect = pygame.Rect(maze._goal_pos[1] * CELL_SIZE, maze._goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.window, GOAL_COLOR, goal_rect, 3)

        # Dibujar la solución hasta el paso actual
        if self.solution:
            # Dibujar el camino recorrido
            for i in range(1, min(self.current_step + 1, len(self.solution))):
                prev_pos = self.solution[i - 1]
                curr_pos = self.solution[i]

                prev_center = (prev_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                               prev_pos[0] * CELL_SIZE + CELL_SIZE // 2)
                curr_center = (curr_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                               curr_pos[0] * CELL_SIZE + CELL_SIZE // 2)

                pygame.draw.line(self.window, PATH_COLOR, prev_center, curr_center, 2)

            # Dibujar la posición actual
            current_pos = self.get_current_position()
            current_rect = pygame.Rect(current_pos[1] * CELL_SIZE, current_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.window, CURRENT_COLOR, current_rect, 3)

        # Dibujar información del algoritmo y solución
        info_text = f"Algoritmo: {'DFS' if self.current_algorithm == 'dfs' else 'Costo Uniforme'} | {self.get_solution_text()}"
        info_surface = font.render(info_text, True, TEXT_COLOR)
        self.window.blit(info_surface, (10, rows * CELL_SIZE + 20))

        # Dibujar instrucciones
        instructions = "Teclas: [D] DFS, [U] Costo Uniforme, [S] Resolver, [N] Siguiente laberinto, [A] Animar, [R] Reiniciar"
        instr_surface = font.render(instructions, True, TEXT_COLOR)
        self.window.blit(instr_surface, (10, rows * CELL_SIZE + 50))

        pygame.display.update()

    def animate_solution(self):
        if not self.solution:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            if self.current_step < len(self.solution) - 1:
                self.current_step += 1

    def run(self):
        running = True
        animating = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.current_algorithm = "dfs"
                        self.solution = None
                        self.current_step = 0
                    elif event.key == pygame.K_u:
                        self.current_algorithm = "uniform"
                        self.solution = None
                        self.current_step = 0
                    elif event.key == pygame.K_s:
                        self.solve_current_maze()
                    elif event.key == pygame.K_n:
                        self.current_maze_index = (self.current_maze_index + 1) % len(self.mazes)
                        self.setup_window()
                        self.solution = None
                        self.current_step = 0
                    elif event.key == pygame.K_a:
                        animating = not animating
                    elif event.key == pygame.K_r:
                        self.solution = None
                        self.current_step = 0

            if animating and self.solution and self.current_step < len(self.solution) - 1:
                self.animate_solution()

            self.draw()
            pygame.time.delay(50)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = JumpingMaze()
    game.run()