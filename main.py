import pygame as pg

from time import perf_counter as pc

from typing import Final


class MyAntz():
    WINDOW_SIZE: Final[tuple[int, int]] = (800, 700)
    def __init__(self) -> None:
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode(self.WINDOW_SIZE)
        self.run: bool = True
        self.fps: int = 0

    def event_handler(self) -> None:
        """ Handles all the events. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
    
    def draw_window(self) -> None:
        """ Draws the window. """
        pg.display.set_caption(f"     MyAntz          FPS:{self.fps}")

    def main(self) -> None:
        """ The main method containing the loop. """
        time: float = pc()
        fps_counter: int = 0
        fps_timer: float = 0.0

        while self.run:
            old_time: float = time
            time = pc()
            dt: float = time - old_time
            # counting the frames
            fps_timer += dt
            fps_counter += 1
            if fps_timer >= 1:
                self.fps = fps_counter
                fps_counter = 0
                fps_timer = 0.0
            
            self.event_handler()
            self.draw_window()
            #fps break
            if dt < 1 / 60:
                pg.time.wait(round((1 / 60 - dt) * 1000))

pg.quit()


if __name__ == "__main__":
    my_antz = MyAntz()
    my_antz.main()