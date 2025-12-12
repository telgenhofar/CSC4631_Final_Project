"""
File: visualizer.py
Author: Aiden Telgenhof
Description: This file contains all of the PyGame logic which is used to create a proper 
visualization of the simulation with a diease graph that shows infection spread and an 
opinion graph that shows opinion spread.
"""
import pygame
import time
from PIL import Image
import numpy as np

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
    """
    Handles rendering of simulation using PyGame, also saves simulation to GIF format
    """
    def __init__(self, env, positions, edges, step_delay=0.5, save_gif=True):
        """
        Initializes the PyGame window and settings
        """
        pygame.init()
        self.env = env
        self.positions = positions
        self.edges = edges
        self.delay = step_delay

        self.save_gif = save_gif
        self.frames =[]


        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Infection + Opinion Simulation")

        self.font = pygame.font.SysFont("Arial", 24)

        left_x = GRAPH_MARGIN
        right_x = GRAPH_MARGIN + GRAPH_SIZE + SMALL_GAP

        self.infection_positions = self._scale_positions(offset_x=left_x, offset_y=GRAPH_MARGIN)
        self.opinion_positions = self._scale_positions(offset_x=right_x, offset_y=GRAPH_MARGIN)

    def _scale_positions(self, offset_x, offset_y):
        """
        Converts positions for an 800x600 graph into whatever the graph settings are
        This was necessary when I started introducing more graphs to the visualizer
        """
        scaled = {}
        for i, (x, y) in self.positions.items():
            sx = offset_x + (x / 800) * GRAPH_SIZE
            sy = offset_y + (y / 600) * GRAPH_SIZE
            scaled[i] = (sx, sy)
        return scaled
    
    def run_simulation(self, steps=30):
        """
        Runs the pygame loop which will render each frame of the simulation
        """
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

        if self.save_gif and len(self.frames) > 0:
            gif_path = "simulation.gif"
            self.frames[0].save(
                gif_path,
                save_all=True,
                append_images=self.frames[1:],
                duration=int(self.delay*1000),
                loop=0
            )

        pygame.quit()

    def draw_frame(self, infected_edges, timestep):
        """
        Logic for drawing all of the pieces of a frame together
        """
        self.screen.fill(BACKGROUND_COLOR)

        self._draw_graph(self.infection_positions, infected_edges, infection_mode=True)
        label = self.font.render(f"Time Step: {timestep}", True, LABEL_COLOR)
        self.screen.blit(label, (10, 0))

        self._draw_graph(self.opinion_positions, infected_edges, infection_mode=False)

        if self.save_gif:
            frame = pygame.surfarray.array3d(self.screen)
            frame = np.transpose(frame, (1, 0, 2))
            img = Image.fromarray(frame)
            self.frames.append(img)

    def _draw_graph(self, positions, infected_edges, infection_mode=True):
        """
        Logic for drawing the two different graphs on screen
        """
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
            if node["vaccinated"]:
                v_label = self.font.render("V", True, LABEL_COLOR)
                self.screen.blit(v_label, (int(x) - 6, int(y) - 30))

    def opinion_to_color(self, opinion):
        """
        Logic for converting DeGroot model opinions to a color on an extreme scale
        to visualize differing opinions in the chart.
        """
        gamma = 2.2
        boosted = opinion ** gamma
        opposite_boosted = (1 - opinion) ** gamma

        r = int(255 * boosted)
        b = int(255 * opposite_boosted)
        g = 100
        return (r, g, b)