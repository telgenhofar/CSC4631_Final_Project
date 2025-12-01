import pygame
import time

INFECTED_COLOR = (255, 80, 80)
NOT_INFECTED_COLOR = (80, 160, 255)
INFECTED_EDGE_COLOR = (255, 0, 0)
NOT_INFECTED_EDGE_COLOR = (100, 100, 100)

LABEL_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (20, 20, 20)

LINE_THICKNESS = 1
NODE_RADIUS = 12

SCREEN_WIDTH = 1125
SCREEN_HEIGHT = 600
GRAPH_SIZE = 500
GRAPH_MARGIN = 50
SMALL_GAP = 25

class Visualizer:
    def __init__(self, env, positions, edges, step_delay=0.5):
        pygame.init()
        self.env = env
        self.positions = positions
        self.edges = edges
        self.delay = step_delay

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Infection + Opinion Simulation")

        self.font = pygame.font.SysFont("Arial", 24)

        left_x = GRAPH_MARGIN
        right_x = GRAPH_MARGIN + GRAPH_SIZE + SMALL_GAP

        self.infection_positions = self._scale_positions(offset_x=left_x, offset_y=GRAPH_MARGIN)
        self.opinion_positions = self._scale_positions(offset_x=right_x, offset_y=GRAPH_MARGIN)

    def _scale_positions(self, offset_x, offset_y):
        scaled = {}
        for i, (x, y) in self.positions.items():
            sx = offset_x + (x / 800) * GRAPH_SIZE
            sy = offset_y + (y / 600) * GRAPH_SIZE
            scaled[i] = (sx, sy)
        return scaled
    
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

        self._draw_graph(self.infection_positions, infected_edges, infection_mode=True)
        label = self.font.render(f"Time Step: {timestep}", True, LABEL_COLOR)
        self.screen.blit(label, (10, 0))

        self._draw_graph(self.opinion_positions, infected_edges, infection_mode=False)

    def _draw_graph(self, positions, infected_edges, infection_mode=True):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (positions[0][0]-GRAPH_MARGIN, positions[0][1]-GRAPH_MARGIN, GRAPH_SIZE, GRAPH_SIZE))

        for u, v in self.edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            if infection_mode and infected_edges is not None:
                color = INFECTED_EDGE_COLOR if (u, v) in infected_edges or (v, u) in infected_edges else NOT_INFECTED_EDGE_COLOR
            else:
                color = NOT_INFECTED_EDGE_COLOR
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), LINE_THICKNESS)

        for i, node in enumerate(self.env.nodes):
            x, y = positions[i]
            if infection_mode:
                color = INFECTED_COLOR if node["infected"] else NOT_INFECTED_COLOR
            else:
                color = self.opinion_to_color(node["opinion_risk"])
            pygame.draw.circle(self.screen, color, (int(x), int(y)), NODE_RADIUS)

    def opinion_to_color(self, opinion):
        gamma = 2.2
        boosted = opinion ** gamma
        opposite_boosted = (1 - opinion) ** gamma

        r = int(255 * boosted)
        b = int(255 * opposite_boosted)
        g = 100
        return (r, g, b)