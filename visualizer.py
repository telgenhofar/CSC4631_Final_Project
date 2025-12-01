import pygame
import time

INFECTED_COLOR = (255, 80, 80)
NOT_INFECTED_COLOR = (80, 160, 255)
LABEL_COLOR = (255, 255, 255)
INFECTED_EDGE_COLOR = (255, 0, 0)
NOT_INFECTED_EDGE_COLOR = (100, 100, 100)
LINE_THICKNESS = 1
BACKGROUND_COLOR = (20, 20, 20)

class Visualizer:
    def __init__(self, env, positions, edges, step_delay=0.5):
        pygame.init()
        self.env = env
        self.positions = positions
        self.edges = edges
        self.delay = step_delay

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Infection Simulation")

        self.font = pygame.font.SysFont("Arial", 24)

    def run_simulation(self, steps=30):
        running = True
        clock = pygame.time.Clock()

        for t in range(steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            infected_edges = self.env.step()

            self.draw_frame(infected_edges, timestep=t)
            pygame.display.flip()
            time.sleep(self.delay)

            if not running:
                break

        pygame.quit()

    def draw_frame(self, infected_edges, timestep):
        self.screen.fill(BACKGROUND_COLOR)

        for (u, v) in self.edges:
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]

            color = INFECTED_EDGE_COLOR if (u, v) in infected_edges or (v, u) in infected_edges else NOT_INFECTED_EDGE_COLOR

            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), LINE_THICKNESS)

        for i, node in enumerate(self.env.nodes):
            x, y = self.positions[i]
            if node["infected"]:
                pygame.draw.circle(self.screen, INFECTED_COLOR, (int(x), int(y)), 10)
            else:
                pygame.draw.circle(self.screen, NOT_INFECTED_COLOR, (int(x), int(y)), 10)

        label = self.font.render(f"Time Step: {timestep}", True, LABEL_COLOR)
        self.screen.blit(label, (20, 20))