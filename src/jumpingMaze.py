import pygame
import sys
from boardAdjacencyList import BoardAdjacencyList
from dfs import depth_first_search
from uniformCost import uniform_cost_search

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_COLOR = (200, 200, 200)
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
PATH_COLOR = (0, 0, 255)
CURRENT_COLOR = (255, 165, 0)
NO_SOLUTION_COLOR = (255, 50, 50)
FONT_SIZE = 24
PADDING = 50

pygame.init()
font = pygame.font.SysFont('Arial', FONT_SIZE)
large_font = pygame.font.SysFont('Arial', FONT_SIZE * 2)


class JumpingMaze:
    def __init__(self, maze_file="input.txt"):
        self.mazes = []
        self.current_maze_index = 0
        self.load_mazes(maze_file)
        self.current_algorithm = "best"
        self.solution = None
        self.dfs_solution = None
        self.uniform_solution = None
        self.current_step = 0
        self.animation_speed = 500
        self.last_update = 0
        self.has_solution = True

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Laberinto Saltarin")

        self.solve_best_algorithm()

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

    def solve_dfs(self):
        maze = self.mazes[self.current_maze_index]
        adjacent_list = maze.get_adjacency_list()
        start_pos = maze._start_pos
        goal_pos = maze._goal_pos

        self.dfs_solution = depth_first_search(adjacent_list, start_pos, goal_pos)
        return self.dfs_solution

    def solve_uniform_cost(self):
        maze = self.mazes[self.current_maze_index]
        adjacent_list = maze.get_adjacency_list()
        start_pos = maze._start_pos
        goal_pos = maze._goal_pos

        self.uniform_solution = uniform_cost_search(adjacent_list, start_pos, goal_pos)
        return self.uniform_solution

    def solve_best_algorithm(self):
        self.solve_dfs()
        self.solve_uniform_cost()

        dfs_length = len(self.dfs_solution) - 1 if self.dfs_solution else float('inf')
        uniform_length = len(self.uniform_solution) - 1 if self.uniform_solution else float('inf')

        if dfs_length == float('inf') and uniform_length == float('inf'):
            self.current_algorithm = "best"
            self.solution = None
            self.has_solution = False
            return None

        self.has_solution = True

        if dfs_length <= uniform_length:
            self.current_algorithm = "dfs"
            self.solution = self.dfs_solution
        else:
            self.current_algorithm = "uniform"
            self.solution = self.uniform_solution

        self.current_step = 0
        return self.solution

    def solve_current_maze(self):
        if self.current_algorithm == "dfs":
            self.solution = self.solve_dfs()
        elif self.current_algorithm == "uniform":
            self.solution = self.solve_uniform_cost()
        else:
            self.solution = self.solve_best_algorithm()

        self.current_step = 0
        return self.solution

    def get_solution_text(self):
        if not self.solution:
            return "No hay solución"
        return f"Solución: {len(self.solution) - 1} pasos"

    def get_algorithm_text(self):
        if self.current_algorithm == "dfs":
            return "DFS"
        elif self.current_algorithm == "uniform":
            return "Costo Uniforme"
        else:
            if self.solution == self.dfs_solution:
                return "Mejor: DFS"
            elif self.solution == self.uniform_solution:
                return "Mejor: Costo Uniforme"
            else:
                return "Mejor algoritmo"

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

        info_height = 100
        available_height = self.height - info_height - 2 * PADDING
        available_width = self.width - 2 * PADDING

        cell_size_height = available_height / rows
        cell_size_width = available_width / cols

        cell_size = min(cell_size_height, cell_size_width)

        offset_x = (self.width - cols * cell_size) / 2
        offset_y = (self.height - info_height - rows * cell_size) / 2

        for r in range(rows):
            for c in range(cols):
                x = offset_x + c * cell_size
                y = offset_y + r * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.window, GRID_COLOR, rect, 1)

                font_size = int(min(cell_size * 0.5, FONT_SIZE))
                cell_font = pygame.font.SysFont('Arial', font_size)

                text = cell_font.render(str(grid[r][c]), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + cell_size / 2, y + cell_size / 2))
                self.window.blit(text, text_rect)

        start_x = offset_x + maze._start_pos[1] * cell_size
        start_y = offset_y + maze._start_pos[0] * cell_size
        start_rect = pygame.Rect(start_x, start_y, cell_size, cell_size)
        pygame.draw.rect(self.window, START_COLOR, start_rect, 3)

        goal_x = offset_x + maze._goal_pos[1] * cell_size
        goal_y = offset_y + maze._goal_pos[0] * cell_size
        goal_rect = pygame.Rect(goal_x, goal_y, cell_size, cell_size)
        pygame.draw.rect(self.window, GOAL_COLOR, goal_rect, 3)

        if not self.has_solution:
            no_solution_text = large_font.render("¡NO HAY SOLUCIÓN POSIBLE!", True, NO_SOLUTION_COLOR)
            text_rect = no_solution_text.get_rect(center=(self.width / 2, offset_y + available_height / 2 - 50))

            bg_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 10, text_rect.width + 40, text_rect.height + 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((255, 255, 255, 200))
            self.window.blit(bg_surface, (bg_rect.x, bg_rect.y))

            self.window.blit(no_solution_text, text_rect)

            hint_text = font.render("Prueba otro algoritmo o pasa al siguiente laberinto con [N]", True,
                                    NO_SOLUTION_COLOR)
            hint_rect = hint_text.get_rect(center=(self.width / 2, text_rect.bottom + 20))
            self.window.blit(hint_text, hint_rect)

        if self.solution:
            for i in range(1, min(self.current_step + 1, len(self.solution))):
                prev_pos = self.solution[i - 1]
                curr_pos = self.solution[i]

                prev_center = (offset_x + prev_pos[1] * cell_size + cell_size / 2,
                               offset_y + prev_pos[0] * cell_size + cell_size / 2)
                curr_center = (offset_x + curr_pos[1] * cell_size + cell_size / 2,
                               offset_y + curr_pos[0] * cell_size + cell_size / 2)

                pygame.draw.line(self.window, PATH_COLOR, prev_center, curr_center, max(2, int(cell_size / 15)))

            current_pos = self.get_current_position()
            current_x = offset_x + current_pos[1] * cell_size
            current_y = offset_y + current_pos[0] * cell_size
            current_rect = pygame.Rect(current_x, current_y, cell_size, cell_size)
            pygame.draw.rect(self.window, CURRENT_COLOR, current_rect, 3)

        info_y = self.height - info_height + 20

        info_text = f"Algoritmo: {self.get_algorithm_text()} | {self.get_solution_text()}"
        info_surface = font.render(info_text, True, TEXT_COLOR)
        self.window.blit(info_surface, (20, info_y))

        instructions = "Teclas: [D] DFS, [U] Costo Uniforme, [B] Mejor solución, [N] Siguiente, [A] Animar, [R] Reiniciar"
        instr_surface = font.render(instructions, True, TEXT_COLOR)
        self.window.blit(instr_surface, (20, info_y + 30))

        pygame.display.update()

    def animate_solution(self):
        if not self.solution:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            if self.current_step < len(self.solution) - 1:
                self.current_step += 1

    def next_maze(self):
        self.current_maze_index = (self.current_maze_index + 1) % len(self.mazes)
        self.solution = None
        self.dfs_solution = None
        self.uniform_solution = None
        self.current_step = 0
        self.solve_best_algorithm()

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
                        if not self.dfs_solution:
                            self.solve_dfs()
                        self.solution = self.dfs_solution
                        self.has_solution = self.solution is not None
                        self.current_step = 0
                    elif event.key == pygame.K_u:
                        self.current_algorithm = "uniform"
                        if not self.uniform_solution:
                            self.solve_uniform_cost()
                        self.solution = self.uniform_solution
                        self.has_solution = self.solution is not None
                        self.current_step = 0
                    elif event.key == pygame.K_b:
                        self.solve_best_algorithm()
                    elif event.key == pygame.K_n:
                        self.next_maze()
                    elif event.key == pygame.K_a:
                        animating = not animating
                    elif event.key == pygame.K_r:
                        self.solution = None
                        self.dfs_solution = None
                        self.uniform_solution = None
                        self.current_step = 0
                        self.solve_best_algorithm()

            if animating and self.solution and self.current_step < len(self.solution) - 1:
                self.animate_solution()

            self.draw()
            pygame.time.delay(50)

        pygame.quit()
        sys.exit()