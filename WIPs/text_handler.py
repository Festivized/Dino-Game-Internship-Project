import pygame
# Setup
pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
clock.tick(10)

# window display settings
pygame.display.set_icon(pygame.image.load("../assets/graphics/egg/egg_1.png"))
pygame.display.set_caption("Placeholder")

if __name__ == "__main__":
    raise RuntimeError("chat can we not run this individually ty <3")

list_texts = []
def textobject_init(coords: tuple[int,int], #workin with evan's repo, and the way he modulized the code to hopefully make it more efficient to add the additional menus
               hexcode: str,
               fontsize: int,
               text: str) -> int:
    """Registers a new text object

    Args:
        coords (tuple[float, float]): Text coordinates.
        hexcode (str): Text color hex code
        fontsize (int): Text font size
        text (str): Text string

    Returns:
        int: The text object's index in the list
    """
    font = pygame.font.Font(pygame.font.get_default_font(), fontsize)
    list_texts.append([coords, hexcode, font, text]) # at index 4 of the list is the drawable toggle
    return len(list_texts)-1


# oh shit this is really smart, add index into
# list_texts = []
# def textobject(coords: tuple[int,int],
#                color: string,
#                font_size: int
#                text: str) -> int:
#     # stole the idea from evan, this is stupid compared to objects but sure why not
#     font = pygame.font.Font(pygame.font.get_default_font(), font_size)
#     _registered_texts.append([text_center, colour, font, text, False])
#     return len(_registered_texts)-1

# evans textreg code
# def register_text(text_center: tuple[float, float],
#                   colour: tuple[int, int, int],
#                   font_size: int,
#                   text: str) -> int:
#     """Registers a new text object
#
#     Args:
#         text_center (tuple[float, float]): The text's center.
#         colour (tuple[int, int, int]): The text's colour
#         font_size (int): The font size of the text
#         text (str): The text itself
#
#     Returns:
#         int: The text object's ID
#     """
#     # Construct the font now to save time rendering
#     font = pygame.font.Font(pygame.font.get_default_font(), font_size)
#
#     _registered_texts.append([text_center, colour, font, text, False])
#     return len(_registered_texts)-1

