import pygame as pg

from random import choice, randint

from typing import List


class Ant:
    FOOD_COLOR = (55, 123, 255)
    def __init__(self, app: object, field_size: tuple[int, int], pos: tuple[int, int]) -> None:
        """
        Initializes an ant object.
        Args:
        app (object): The main application
        pos (tuple[int, int]): the position of the ant.
        """
        self.pos: tuple[int, int] = pos
        self.field_size: tuple[int, int] = field_size
        self.direction: tuple[str, int] = (choice(["h", "v"]), choice([-1, 1]))
        self.old_direction: tuple[str, int] = self.direction
        self.color_count: int = 10

    def determine_direction(self, field: List[List[tuple[int, int, int]]], ants: List[object]) -> None:
        """ Sets the new direction depending on the field the ant is on and what is on the field she wants to go. """
        # white = turn right, black = turn left, colorful = no turn, go straight, another ant = turn 180
        if field[self.pos[0]][self.pos[1]][0] == 0:
            direction_0: str = "v" if self.direction[0] == "h" else "h"
            if self.direction[0] == "v" and self.direction[1] == -1:
                direction_1: int = -1
            elif self.direction[0] == "v" and self.direction[1] == 1:
                direction_1: int = 1
            elif self.direction[0] == "h" and self.direction[1] == -1:
                direction_1: int = 1
            elif self.direction[0] == "h" and self.direction[1] == 1:
                direction_1: int = -1

        elif field[self.pos[0]][self.pos[1]][0] == 255:
            direction_0: str = "v" if self.direction[0] == "h" else "h"
            if self.direction[0] == "v" and self.direction[1] == -1:
                direction_1: int = 1
            elif self.direction[0] == "v" and self.direction[1] == 1:
                direction_1: int = -1
            elif self.direction[0] == "h" and self.direction[1] == -1:
                direction_1: int = -1
            elif self.direction[0] == "h" and self.direction[1] == 1:
                direction_1: int = 1

        else:
            direction_0: str = self.direction[0]
            direction_1: int = self.direction[1]

        if self.direction[0] == "v":
            temp_new_pos: tuple[int, int] = (self.pos[0], self.pos[1] + direction_1)  # type: ignore
        else:
            temp_new_pos: tuple[int, int] = (self.pos[0] + direction_1, self.pos[1])  # type: ignore

        for ant in ants:
            if ant.pos == temp_new_pos:  # type:ignore
                direction_0: str = "v" if self.direction[0] == "h" else "h"

        self.direction = (direction_0, direction_1)  # type: ignore
        
        self.change_field(field)
    
    def get_rgb(self) -> tuple[int, int, int]:
        r: int = randint(1, 254)
        g: int = randint(0, 255)
        b: int = randint(0, 255)
        return r, g, b  

    def change_field(self, field) -> None:
        if self.color_count > 0:
            if field[self.pos[0]][self.pos[1]] == (0, 0, 0):
                field[self.pos[0]][self.pos[1]] = (255, 255, 255)
            elif field[self.pos[0]][self.pos[1]] == (255, 255, 255):
                field[self.pos[0]][self.pos[1]] = (0, 0, 0)
            else:
                r, g, b = self.get_rgb()
                field[self.pos[0]][self.pos[1]] = choice([(0, 0, 0), (255, 255, 255), (r, g, b)])
            self.color_count -= 1
        else:
            r, g, b = self.get_rgb()
            field[self.pos[0]][self.pos[1]] = (r, g, b)
            self.color_count = 10

    def move(self) -> None:
        """ Moves the ant. """
        pos_x: int = 0
        pos_y: int = 0
        if self.direction[0] == "h":
            pos_x: int = self.pos[0] + self.direction[1]
            pos_y: int = self.pos[1]
        elif self.direction[0] == "v":
            pos_x: int = self.pos[0]
            pos_y: int = self.pos[1] + self.direction[1]

        if pos_x > self.field_size[0] - 1:
            pos_x = 0
        if pos_x < 0:
            pos_x = self.field_size[0] - 1
        if pos_y > self.field_size[1] - 1:
            pos_y = 0
        if pos_y < 0:
            pos_y = self.field_size[1] - 1
        
        self.pos = (pos_x, pos_y)  # type: ignore

    def draw(self, surf: pg.Surface) -> None:
        """
        Draws the ant on the given surface.
        Args:
        surf (pg.Surface): The surface to draw the ant on.
        """
        pg.draw.rect(surf, "red", (self.pos[0] * 5, self.pos[1] * 5, 5, 5))