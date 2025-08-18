from ant import Ant

import pygame as pg

from time import perf_counter as pc
from random import randint as ri
from random import choice

from typing import Final, List


class MyAntz():
    WINDOW_SIZE: Final[tuple[int, int]] = (800, 700)
    def __init__(self) -> None:
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode(self.WINDOW_SIZE)
        self.run: bool = True
        self.fps: int = 0
        self.ants: List[object] = []
        # create the field and fill it with all white
        self.field: List[List[tuple[int, int, int]]] = [[(255, 255, 255) for _ in range(int((self.WINDOW_SIZE[1] - 100) / 5))] for _ in range(int((self.WINDOW_SIZE[0]) / 5))]
        print(len(self.field))
        print(len(self.field[0]))


    def create_ant(self, pos: tuple[int, int]) -> None:
        """
        Creates an ant at the given position.
        Args:
        pos (tuple(int, int)): The position of the ant
        """
        self.ants.append(Ant(app=self, pos=pos))
        
    def event_handler(self) -> None:
        """ Handles all the events. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
    
    def draw_window(self) -> None:
        """ Draws the window. """
        pg.display.set_caption(f"     MyAntz          FPS:{self.fps}")
        # reset the screen
        self.screen.fill("black")
        # draw the field
        for i, column in enumerate(self.field):
            for j, element in enumerate(column):
                pg.draw.rect(self.screen, element, (0 + i * 5, 0 + j * 5, 5, 5))
        # draw the ants
        for ant in self.ants:
            ant.draw(self.screen)
        # draw the buttons
        # buttons here

        pg.display.update()

    def main(self) -> None:
        """ The main method containing the loop. """
        time: float = pc()
        fps_counter: int = 0
        fps_timer: float = 0.0
        
        list_of_positions: List[tuple[int, int]] = []
        for _ in range(2):
            while True:
                x: int = ri(10, int(self.WINDOW_SIZE[0] / 5) - 10)
                y: int = ri(10, int(self.WINDOW_SIZE[1] / 5) - 10)
                if (x, y) not in list_of_positions:
                    list_of_positions.append((x, y))
                    break
            self.create_ant((x, y))

        while self.run:
            old_time: float = time
            time = pc()
            speed_limiter: float = time
            dt: float = time - old_time
            # counting the frames
            fps_timer += dt
            fps_counter += 1
            if fps_timer >= 1:
                self.fps = fps_counter
                fps_counter = 0
                fps_timer = 0.0
            
            self.event_handler()
            # move ants
            for ant in self.ants:
                ant.determine_direction(self.field, self.ants)
                ant.move(self.field)
        
            self.draw_window()
            #fps break
            speed_limiter = pc() - speed_limiter
            if speed_limiter < 1 / 60:
                pg.time.wait(round((1 / 60 - speed_limiter) * 1000))

pg.quit()


if __name__ == "__main__":
    my_antz = MyAntz()
    my_antz.main()