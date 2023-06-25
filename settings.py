import pygame

debug = False


# Window settings
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 600


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("numX")

# Load the image
image = pygame.image.load("numX.png")  # Replace "path_to_your_image.jpg" with the actual path to your image file

# Calculate the scaled dimensions while maintaining aspect ratio
screen_ratio = window.get_width() / window.get_height()
image_ratio = image.get_width() / image.get_height()

if screen_ratio > image_ratio:
    # Fit based on height
    scaled_height = window.get_height()
    scaled_width = int(scaled_height * image_ratio)
else:
    # Fit based on width
    scaled_width = window.get_width()-200
    scaled_height = int(scaled_width / image_ratio)

# Resize the image
image = pygame.transform.scale(image, (scaled_width, scaled_height))

# Calculate the position to center the image on the screen
x = (window.get_width() - image.get_width()) // 2
y = (window.get_height() - image.get_height()) // 3

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 22)

# Grid settings
GRID_SIZE = 40  # Size of each grid cell
GAP_BETWEEN_GRID = 5  # Gap between each grid
GRID_ROWS = 5  # Number of rows in the grid
GRID_COLS = 5  # Number of columns in the grid
BORDER_RADIUS = 6
PLAYER_TILES = 7

if debug == True:
    #To Debug Only
    task = "Same"
    if task == "Series":
        central_number = 5
        grid = [['3', '', '', '', ''], ['', '4', '', '', ''], ['', '', '5', '', ''], ['', '', '', '6', ''], ['', '', '', '', '']]
    elif task == "Same":
        central_number = 5
        grid = [['5', '', '', '', ''], ['', '5', '', '', ''], ['', '', '5', '', ''], ['', '', '', '5', ''], ['', '', '', '', '']]
    elif task == "Fibonacci":
        central_number = 5
        grid = [['2', '', '', '', ''], ['', '3', '', '', ''], ['', '', '5', '', ''], ['', '', '', '8', ''], ['', '', '', '', '']]
    elif task == "Prime":
        central_number = 5
        grid = [['2', '', '', '', ''], ['', '3', '', '', ''], ['', '', '5', '', ''], ['', '', '', '7', ''], ['', '', '', '', '']]
    elif task == "Even":
        central_number = 6
        grid = [['2', '', '', '', ''], ['', '4', '', '', ''], ['', '', '6', '', ''], ['', '', '', '8', ''], ['', '', '', '', '']]
    elif task == "Odd":
        central_number = 5
        grid = [['1', '', '', '', ''], ['', '3', '', '', ''], ['', '', '5', '', ''], ['', '', '', '7', ''], ['', '', '', '', '']]
    elif task == "Multiple of 3":
        central_number = 9
        grid = [['3', '', '', '', ''], ['', '6', '', '', ''], ['', '', '9', '', ''], ['', '', '', '12', ''], ['', '', '', '', '']]
    elif task == "Multiple of 4":
        central_number = 12
        grid = [['4', '', '', '', ''], ['', '8', '', '', ''], ['', '', '12', '', ''], ['', '', '', '16', ''], ['', '', '', '', '']]
    elif task == "Multiple of 5":
        central_number = 15
        grid = [['5', '', '', '', ''], ['', '10', '', '', ''], ['', '', '15', '', ''], ['', '', '', '20', ''], ['', '', '', '', '']]
    elif task == "Multiple of 6":
        central_number = 18
        grid = [['6', '', '', '', ''], ['', '12', '', '', ''], ['', '', '18', '', ''], ['', '', '', '24', ''], ['', '', '', '', '']]
    elif task == "Multiple of 7":
        central_number = 21
        grid = [['7', '', '', '', ''], ['', '14', '', '', ''], ['', '', '21', '', ''], ['', '', '', '28', ''], ['', '', '', '', '']]
    elif task == "Multiple of 8":
        central_number = 24
        grid = [['8', '', '', '', ''], ['', '16', '', '', ''], ['', '', '24', '', ''], ['', '', '', '32', ''], ['', '', '', '', '']]
    elif task == "Multiple of 9":
        central_number = 27
        grid = [['9', '', '', '', ''], ['', '18', '', '', ''], ['', '', '27', '', ''], ['', '', '', '36', ''], ['', '', '', '', '']]

else:
    # Create a 2D grid to track the state of each cell
    grid = [[""] * GRID_COLS for _ in range(GRID_ROWS)]
    task = ""

# Color settings
BACKGROUND = (33, 53, 85)
DIAGONAL1 = (46, 176, 134)
DIAGONAL2 = (249, 102, 102)
CENTRAL = (249, 245, 246)
DEFAULT = (249, 224, 187)
SHADOW = (40, 40, 40)  # Shadow color
WHITE = (255, 255, 255)  # White for Text
BLACK = (0, 0, 0)  # Black for Text

# Calculate total grid size including gaps
GRID_TOTAL_SIZE = GRID_SIZE + GAP_BETWEEN_GRID

# Calculate grid offset to center the grid
GRID_OFFSET_X = (WINDOW_WIDTH - (GRID_TOTAL_SIZE * GRID_COLS - GAP_BETWEEN_GRID)) // 2
GRID_OFFSET_Y = 100

excluded_cells = [(0, 2), (2, 0), (2, 4), (4, 2)]

player1_restricted_tiles = [(0, 4), (1, 3), (3, 1), (4, 0)]
player2_restricted_tiles = [(0, 0), (1, 1), (3, 3), (4, 4)]

# Define progress bar variables
progress_bar_height = 5
progress_bar_x = 0
progress_bar_y = 70

# Define circle variables
circle_radius = 2
circle_spacing = 5
circle_start_x = 0
circle_y = 90

exclude_grid = [(2,2)]

main_diagonals = [
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
    [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]
    ]
medium_diagonals = [
    [(3,0), (1,2), (2,1), (0,3)],
    [(4,1), (3,2), (2,3), (1,4)],
    [(1,0), (2,1), (3,2), (4,3)],
    [(0,1), (1,2), (2,3), (3,4)]
    ]

small_diagonals = [
    [(1, 0), (0,1)],
    [(4,3), (3,4)],
    [(3,0), (4,1)],
    [(0,3), (1,4)]
]





