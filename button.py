
import pygame as pg
from typing import Final, TypedDict


class ButtonColors(TypedDict):
    main_color: tuple[int, int, int]
    hover_color: tuple[int, int, int]
    shadow_color: tuple[int, int, int]
    frame_color: tuple[int, int, int]


class Button:
    """ A button class that can be used to create buttons in the game. """

    BUTTON_COLORS: Final[dict[str, ButtonColors]] = {
    # Button colors including the hover, frame and shadow colors.
    'green': {'main_color': (56, 155, 60), 'hover_color': (76, 175, 80), 'shadow_color': (16, 115, 20), 'frame_color': (6, 95, 20)},
    'yellow': {'main_color': (235, 235, 0), 'hover_color': (255, 255, 50), 'shadow_color': (195, 195, 0), 'frame_color': (125, 125, 0)},
    'red': {'main_color': (235, 0, 0), 'hover_color': (255, 50, 50), 'shadow_color': (175, 0, 0), 'frame_color': (100, 0, 0)},
    'white': {'main_color': (235, 235, 235), 'hover_color': (255, 255, 255), 'shadow_color': (175, 175, 175), 'frame_color': (100, 100, 100)},
    'beige': {'main_color': (235, 220, 195), 'hover_color': (245, 230, 210), 'shadow_color': (185, 170, 145), 'frame_color': (120, 105, 80)}
    }
    BUTTON_FONT_SIZE: Final[int] = 20
    BUTTON_OFFSET: Final[int] = 5 
    
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str, color: str) -> None:
        """ Initializes a button object.
        Args:
        pos (tuple(int)): The topleft position of the button.
        size (tuple(int)): The size of the button.
        text (str): The text to be displayed on the button.
        color (str): The color of the button (green, yellow, red, white, beige)
        """
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.size: tuple[int, int] = size
        
        self.shadow_color: tuple[int, int, int] = self.BUTTON_COLORS[color]["shadow_color"]
        self.main_color: tuple[int, int, int] = self.BUTTON_COLORS[color]["main_color"]
        self.frame_color: tuple[int, int, int] = self.BUTTON_COLORS[color]["frame_color"]
        self.hover_color: tuple[int, int, int] = self.BUTTON_COLORS[color]["hover_color"]
        self.color: tuple[int, int, int] = self.main_color
        font: pg.font.Font = pg.font.SysFont("comicsans", self.BUTTON_FONT_SIZE)
        self.text: str = text
        self.text_surface: pg.Surface = font.render(self.text, True, "white")
        self.text_shadow: pg.Surface = font.render(self.text, True, "black")
        self.text_pos: tuple[int, int] = (int(self.pos.x + self.size[0] // 2 - self.text_surface.get_width() // 2),
                                     int(self.pos.y + self.size[1] // 2 - self.text_surface.get_height() // 2))
        self.clicked: bool = False
        self.offset: int = self.BUTTON_OFFSET
        self.rect: pg.Rect = self.create_rect()

    def check_clicked(self) -> None | bool:
        """ Checks if the button is clicked. """
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = self.hover_color
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
                self.offset = 0
            if not pg.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                self.offset = self.BUTTON_OFFSET

                return True
        else:
            self.color = self.main_color
            self.clicked = False

    def create_rect(self) -> pg.Rect:
        """ Creates a rectangle for the button. """
        return pg.Rect(self.pos.x, self.pos.y - self.offset, self.size[0], self.size[1])
    
    def get_value(self) -> int:
        """ Returns the value of the button. """
        return int(self.text)

    def render(self, surf: pg.Surface) -> None:
        """ Renders the button on the given surface.
        Args:
        surf (pg.Surface): the surface to render the button on
        """
        self.rect = self.create_rect()
        pg.draw.rect(surf, self.shadow_color, (self.pos.x, self.pos.y, self.size[0], self.size[1]), border_radius=5)
        pg.draw.rect(surf, self.color, self.rect, border_radius=5)
        pg.draw.rect(surf, self.frame_color, self.rect, width=3, border_radius=5)
        surf.blit(self.text_shadow, (self.text_pos[0], self.text_pos[1] - self.offset))
        surf.blit(self.text_surface, (self.text_pos[0] - 2, self.text_pos[1] - self.offset - 2))

