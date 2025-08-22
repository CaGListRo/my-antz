from ant import Ant
from button import Button

import pygame as pg

from time import perf_counter as pc
from random import randint as ri
from random import choice

from typing import Final, List


class MyAntz():
    WINDOW_SIZE: Final[tuple[int, int]] = (1600, 1000)
    DIVIDER: Final[int] = 5
    FIELD_SIZE: Final[tuple[int, int]] = (int(WINDOW_SIZE[0] / DIVIDER), int((WINDOW_SIZE[1] - 100) / 5))
    # button section
    SPACING: int = 10  # spacing for the buttons
    TOP_ROW: int = WINDOW_SIZE[1] - 100 + SPACING

    def __init__(self) -> None:
        pg.init()
        self.screen: pg.Surface = pg.display.set_mode(self.WINDOW_SIZE)
        self.run: bool = True
        self.fps: int = 0
        self.ants: List[object] = []
        # create the field and fill it with all white
        self.field: List[List[tuple[int, int, int]]] = []
        self.start: int = -1

        self.create_buttons()

    def check_button(self) -> None:
        """ Checks if the button are clicked. """
        if self.start_stop_button.check_clicked():
            if self.start < 0:
                self.start = 1
            else:
                self.start = -1
        if self.create_ants_button.check_clicked():
            self.create_ants()
        if self.delete_ants_button.check_clicked():
            self.delete_ants()
        if self.fill_black_button.check_clicked():
            self.fill_field_black()
        if self.fill_white_button.check_clicked():
            self.fill_field_white()
        if self.fill_black_and_white_button.check_clicked():
            self.fill_field_black_and_white()
        if self.fill_random_button.check_clicked():
            self.fill_field_random()

    def create_ants(self, amount: int = 10) -> None:
        """ Creates all the ants and stores them in a list. """
        list_of_positions: List[tuple[int, int]] = []
        for _ in range(amount):
            while True:
                x: int = ri(0, self.FIELD_SIZE[0] - 1)
                y: int = ri(0, self.FIELD_SIZE[1] - 1)
                if (x, y) not in list_of_positions:
                    list_of_positions.append((x, y))
                    break
            self.create_one_ant((x, y))

    def create_one_ant(self, pos: tuple[int, int]) -> None:
        """
        Creates an ant at the given position.
        Args:
        pos (tuple(int, int)): The position of the ant
        """
        self.ants.append(Ant(app=self, field_size=self.FIELD_SIZE, pos=pos))
    
    def create_buttons(self) -> None:
        """ Creates all the buttons. """
        self.start_stop_button: Button = Button(pos=(self.SPACING, self.TOP_ROW), size=(180, 35), text="Start/Stop", color="green")
        self.create_ants_button: Button = Button(pos=(200, self.TOP_ROW), size=(180, 35), text="Make Antz", color="beige")
        self.delete_ants_button: Button = Button(pos=(1200, self.TOP_ROW), size=(180, 35), text="Delete Antz", color="red")
        self.fill_black_button: Button = Button(pos=(400, self.TOP_ROW), size=(180, 35), text="Fill black", color="beige")
        self.fill_white_button: Button = Button(pos=(600, self.TOP_ROW), size=(180, 35), text="Fill white", color="beige")
        self.fill_black_and_white_button: Button = Button(pos=(800, self.TOP_ROW), size=(180, 35), text="Fill B/W", color="beige")
        self.fill_random_button: Button = Button(pos=(1000, self.TOP_ROW), size=(180, 35), text="Fill random", color="beige")

    def delete_ants(self, amount: int = 10) -> None:
        """ Deletes the amount of ants from the ant list. """
        if len(self.ants) >= amount:
            for _ in range(amount):
                ant_to_delete: int = ri(0, len(self.ants) - 1)
                self.ants.pop(ant_to_delete)

    def event_handler(self) -> None:
        """ Handles all the events. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False

    def fill_field_white(self) -> None:
        """ Fills the field all white. """
        self.field = [[(255, 255, 255) for _ in range(self.FIELD_SIZE[1])] for _ in range(self.FIELD_SIZE[0])]
    
    def fill_field_black(self) -> None:
        """ Fills the field all black. """
        self.field = [[(0, 0, 0) for _ in range(self.FIELD_SIZE[1])] for _ in range(self.FIELD_SIZE[0])]
    
    def fill_field_black_and_white(self) -> None:
        """ Fills the field random with back and white. """
        self.field = [[choice([(0, 0, 0), (255, 255, 255)]) for _ in range(self.FIELD_SIZE[1])] for _ in range(self.FIELD_SIZE[0])]

    def fill_field_random(self) -> None:
        """ Fills the field completely random. """
        self.field = [[choice([(0, 0, 0), (ri(1, 254), ri(0, 255), ri(0, 255)),(255, 255, 255)]) for _ in range(self.FIELD_SIZE[1])] for _ in range(self.FIELD_SIZE[0])]

    def draw_window(self) -> None:
        """ Draws the window. """
        pg.display.set_caption(f"     MyAntz          FPS:{self.fps}")
        # reset the screen
        self.screen.fill("black")
        # draw the field
        for i, column in enumerate(self.field):
            for j, element in enumerate(column):
                pg.draw.rect(self.screen, element, (0 + i * self.DIVIDER, 0 + j * self.DIVIDER, self.DIVIDER, self.DIVIDER))
        # draw the ants
        for ant in self.ants:
            ant.draw(self.screen)  # type:ignore
        # draw the buttons
        self.start_stop_button.render(self.screen)
        self.create_ants_button.render(self.screen)
        self.delete_ants_button.render(self.screen)
        self.fill_black_button.render(self.screen)
        self.fill_white_button.render(self.screen)
        self.fill_black_and_white_button.render(self.screen)
        self.fill_random_button.render(self.screen)

        pg.display.update()

    def main(self) -> None:
        """ The main method containing the loop. """
        time: float = pc()
        fps_counter: int = 0
        fps_timer: float = 0.0
        self.fill_field_black()
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
            
            self.check_button()
            self.event_handler()
            # move ants
            if self.start > 0 and len(self.ants) > 0:
                for ant in self.ants:
                    ant.determine_direction(self.field, self.ants)  # type:ignore
                    ant.move()                                      # type:ignore
        
            self.draw_window()
            #fps break
            # speed_limiter = pc() - speed_limiter
            # if speed_limiter < 1 / 60:
            #     pg.time.wait(round((1 / 60 - speed_limiter) * 1000))

pg.quit()


if __name__ == "__main__":
    my_antz = MyAntz()
    my_antz.main()