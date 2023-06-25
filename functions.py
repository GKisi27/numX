import random
import math
from settings import *
import pygame
import sys


if debug == True:
    pass
else:
    # Retrieve the text content of the grid
    central_number = random.randint(27, 50)

def draw_game_board(grid, central_number):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell_x = GRID_OFFSET_X + col * GRID_TOTAL_SIZE
            cell_y = GRID_OFFSET_Y + row * GRID_TOTAL_SIZE

            draw_inner_rectangle(cell_x, cell_y, grid[row][col])
            if (row,col) not in exclude_grid:
                # Draw grid colors
                if row == col and row != 2 and col != 2:  # First diagonal grids
                    pygame.draw.rect(window, DIAGONAL1, (cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4),
                                    border_radius=BORDER_RADIUS)
                    draw_text(SHADOW, DIAGONAL1, pygame.Rect(cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4), grid[row][col])
                elif row + col == GRID_ROWS - 1 and row != 2 and col != 2:  # Second diagonal grids
                    pygame.draw.rect(window, DIAGONAL2, (cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4),
                                    border_radius=BORDER_RADIUS)
                    draw_text(SHADOW, DIAGONAL2, pygame.Rect(cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4), grid[row][col])
            elif row == 2 and col == 2:  # Central grid
                pygame.draw.rect(window, CENTRAL, (cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4),
                                 border_radius=BORDER_RADIUS)
                draw_text(SHADOW, CENTRAL, pygame.Rect(cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2), str(central_number))
            else:
                pygame.draw.rect(window, CENTRAL, (cell_x + 2, cell_y + 2, GRID_SIZE - 4, GRID_SIZE - 4), border_radius=BORDER_RADIUS)
                draw_text(SHADOW, CENTRAL, pygame.Rect(cell_x + 1, cell_y + 1, GRID_SIZE - 2, GRID_SIZE - 2), grid[row][col])

            # Exclude specific grids
            if grid[row][col] == -1:
                pygame.draw.rect(window, BACKGROUND, (cell_x, cell_y, GRID_SIZE, GRID_SIZE),
                                 border_radius=BORDER_RADIUS)
                
def render_and_display_text(screen, font, text, vertical_offset):
    text_lines = []
    words = text.split()

    line_width_limit = screen.get_width() - 80  # Adjust the padding as needed

    current_line = words[0]
    for word in words[1:]:
        if font.size(current_line + " " + word)[0] < line_width_limit:
            current_line += " " + word
        else:
            text_lines.append(current_line)
            current_line = word
    text_lines.append(current_line)

    line_height = font.get_linesize()
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in text_lines]
    text_rects = [text_surface.get_rect(center=(screen.get_width() // 2, 0)) for text_surface in text_surfaces]

    screen_center = screen.get_rect().center

    # Adjust the vertical position of the text
    for i, text_rect in enumerate(text_rects):
        text_rect.centery = screen_center[1] + vertical_offset + i * (line_height+10)

    for i in range(len(text_surfaces)):
        screen.blit(text_surfaces[i], text_rects[i])
    pygame.display.update()

def draw_text(shodow_color, main_color, rect, text):
    pygame.draw.rect(window, shodow_color, rect, border_radius=BORDER_RADIUS)
    pygame.draw.rect(window, main_color, pygame.Rect(rect.left + 2, rect.top + 2, rect.width - 4, rect.height - 4),
                     border_radius=BORDER_RADIUS)
    
    text_surface = font.render(str(text), True, BLACK)  # Convert text to a string explicitly
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

def draw_inner_rectangle(x, y, value):
    pygame.draw.rect(window, SHADOW, (x, y, GRID_SIZE, GRID_SIZE), border_radius=BORDER_RADIUS)
    pygame.draw.rect(window, DEFAULT, (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4), border_radius=BORDER_RADIUS)
    draw_text(SHADOW, DEFAULT, pygame.Rect(x+1, y+1, GRID_SIZE - 2, GRID_SIZE - 2), str(value))

def draw_elements(player1_score, current_player, player2_score, preview_grid_text):
    draw_text(SHADOW, CENTRAL, pygame.Rect(22, 22, 46, GRID_SIZE - 4), f"{player1_score}")
    draw_text(SHADOW, CENTRAL, pygame.Rect(112, 22, 126, GRID_SIZE - 4), f"Player{current_player}'s Turn")
    draw_text(SHADOW, CENTRAL, pygame.Rect(282, 22, 46, GRID_SIZE - 4), f"{player2_score}")
    draw_text(SHADOW, CENTRAL, pygame.Rect(12, 352, GRID_SIZE - 4, GRID_SIZE - 4), "R")
    draw_text(SHADOW, CENTRAL, pygame.Rect(62, 352, 230, GRID_SIZE - 4), preview_grid_text)
    draw_text(SHADOW, CENTRAL, pygame.Rect(300, 350, GRID_SIZE, GRID_SIZE), "GO")

def draw_player_tiles(tiles):
    for col in range(3):
        cell_x = GRID_OFFSET_X - (GRID_SIZE + GAP_BETWEEN_GRID) + col * GRID_TOTAL_SIZE
        cell_y = GRID_OFFSET_Y + 50 + (GRID_ROWS + 1) * GRID_TOTAL_SIZE
        tile_content = tiles[:3][col]
        if tile_content:
            draw_text(SHADOW, DEFAULT, pygame.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE), tile_content)

    for col in range(4):
        cell_x = GRID_OFFSET_X + 50 + (GRID_SIZE + GAP_BETWEEN_GRID) + col * GRID_TOTAL_SIZE
        cell_y = GRID_OFFSET_Y + 50 + (GRID_ROWS + 1) * GRID_TOTAL_SIZE
        tile_content = tiles[3:][col]
        if tile_content:
            draw_text(SHADOW, CENTRAL, pygame.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE), tile_content)

def draw_power_cards():
    for col in range(3):
        cell_x = GRID_OFFSET_X - 15 + col * GRID_TOTAL_SIZE * 2
        cell_y = GRID_OFFSET_Y + 110 + (GRID_ROWS + 1) * GRID_TOTAL_SIZE
        pygame.draw.rect(window, CENTRAL, (cell_x, cell_y, GRID_SIZE * 1.8, GRID_SIZE * 2.5),
                         border_radius=BORDER_RADIUS)
def quit_game():
    window.fill(BACKGROUND)
    pygame.quit()
    sys.exit()

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, [x,y])

def generate_random_player_tile():
    numbers = [str(i) for i in range(0, 10)]
    symbols = ["+", "-", "x", "÷"]
    random_symbols = random.sample(symbols, 3)
    random_numbers = random.sample(numbers, 4)
    return random_symbols+random_numbers

def get_numbers_from_diagonal(diagonal, grid):
    diagonal_values = []
    for cell in diagonal:
        row, col = cell
        cell_value = grid[row][col]  
        if cell_value.isdigit():
            diagonal_values.append(int(cell_value))
        else:
            diagonal_values.append(0)
    return diagonal_values

def check_diagonals(grid):
    global latest_score, exclude_grid

    total_score = 0

    for diagonal in main_diagonals:
        diagonal_values = get_numbers_from_diagonal(diagonal, grid)
        print(diagonal_values)
        if task == "Series":
            series_score = check_series(diagonal_values)
            if series_score:
                total_score = total_score +  series_score * 5
                return total_score,"Series score"
            
        elif task == "Same":
            equal_diagonal_score = same_numbers_on_diagonal(diagonal_values)
            if equal_diagonal_score:
                total_score = total_score +  equal_diagonal_score * 5
                return total_score, "Equal diagonal scores"
            
        elif task == "Fibonacci":
            fibonnacci_score = are_consecutive_fibonacci_series(diagonal_values)
            if fibonnacci_score:
                total_score = total_score +  fibonnacci_score * 5
                return total_score, "Fibonacci score"

        elif task == "Even":
            even_diagonal_score = are_consecutive_even_numbers(diagonal_values)
            if even_diagonal_score:
                total_score = total_score +  even_diagonal_score * 5
                return total_score, "Consecutive even diagonal scores"
            

        elif task == "Odd":
            odd_diagonal_score = are_consecutive_odd_numbers(diagonal_values)
            if odd_diagonal_score:
                total_score = total_score +  odd_diagonal_score * 5
                return total_score, "Consecutive odd diagonal scores"
            
        elif task == "Prime":
            prime_diagonal_score = are_consecutive_prime_numbers(diagonal_values)
            if prime_diagonal_score:
                total_score = total_score +  prime_diagonal_score * 5
                return total_score, "Consecutive prime diagonal scores"
        
        elif task.startswith('Multiple'):
            num = int(task[-1])
            multiple_in_diagonal_score = check_consecutive_multiples(diagonal_values, num)
            if multiple_in_diagonal_score:
                total_score = total_score +  multiple_in_diagonal_score * 5
                return total_score, f"multple of {num} in diagonal"

    for diagonal in medium_diagonals:
        diagonal_values = get_numbers_from_diagonal(diagonal, grid)
        equal_diagonal_score = same_numbers_on_diagonal(diagonal_values)
        if equal_diagonal_score:
            total_score = total_score +  equal_diagonal_score * 2
            for d in diagonal:
                exclude_grid.append(d)

    for diagonal in small_diagonals:
        diagonal_values = get_numbers_from_diagonal(diagonal, grid)
        equal_diagonal_score = same_numbers_on_diagonal(diagonal_values)
        if equal_diagonal_score:
            total_score += equal_diagonal_score
            for d in diagonal:
                exclude_grid.append(d)
    return total_score, False

def calculate_result(expression):
    try:
        expression = expression.replace("x", "*")
        expression = expression.replace("÷", "/")
        result = eval(expression)
        if math.isinf(result) or math.isnan(result):
            return ""
        return str(round(int(result)))
    except:
        return ""
    
def check_number(num):
    fibo = [13, 21, 34]
    if num < 2:
        return False #Number should be greater than or equal to 2.
    
    is_prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    
    multiples_count = {}
    for i in range(3, 10):
        multiples_count[i] = num // i if num % i == 0 else 0
    
    result = ["Series", "Same"]
    if num in fibo:
        result.append("Fibonacci")
    if is_prime:
        result.append("Prime") 
    if num % 2 == 0:
        result.append("Even") 
    else:
        result.append("Odd")
    
    for multiple, count in multiples_count.items():
        if count > 0:
            result.append(f"Multiple of {multiple}")
    
    return result

def check_series(numbers):
    if len(numbers) < 5:
        return False

    # Check if the numbers are consecutive in either ascending or descending order
    if all(numbers[i] == numbers[i-1] + 1 for i in range(1, len(numbers))) or \
       all(numbers[i] == numbers[i-1] - 1 for i in range(1, len(numbers))):
        return sum(numbers)

    return False

    
def same_numbers_on_diagonal(diagonal):
    all_zero = all(element == 0 for element in diagonal)
    if all_zero:
        return False
    
    first_value = diagonal[0]
    for number in diagonal:
        if number != first_value:
            return False

    return sum(diagonal)

def are_consecutive_even_numbers(numbers):
    # Check if there are 5 numbers:
    if len(numbers) < 5:
        return False

    # Determine the direction of the list (ascending or descending)
    diff = numbers[1] - numbers[0]
    is_ascending = diff > 0

    # Check if the first number is even
    if numbers[0] % 2 != 0:
        return False

    # Check if each subsequent number is consecutive and even
    for i in range(1, len(numbers)):
        if is_ascending:
            if numbers[i] != numbers[i-1] + diff:
                return False
        else:
            if numbers[i] != numbers[i-1] + diff:
                return False

        if numbers[i] % 2 != 0:
            return False

    return sum(numbers)


def are_consecutive_odd_numbers(numbers):
    # Check if there are 5 numbers:
    if len(numbers) < 5:
        return False

    # Determine the direction of the list (ascending or descending)
    diff = numbers[1] - numbers[0]
    is_ascending = diff > 0

    # Check if the first number is odd
    if numbers[0] % 2 == 0:
        return False

    # Check if each subsequent number is consecutive and odd
    for i in range(1, len(numbers)):
        if is_ascending:
            if numbers[i] != numbers[i-1] + diff:
                return False
        else:
            if numbers[i] != numbers[i-1] + diff:
                return False

        if numbers[i] % 2 == 0:
            return False

    return sum(numbers)

def check_consecutive_multiples(numbers, multiple):
    # Check if there are 5 numbers:
    if len(numbers) < 5:
        return False

    # Check if the first number is divisible by the given multiple
    if numbers[0] % multiple != 0:
        return False

    # Check if the numbers are consecutive multiples of the given multiple
    step = 1 if numbers[1] > numbers[0] else -1
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i-1] + step * multiple:
            return False

    return sum(numbers)

def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True

def are_consecutive_prime_numbers(numbers):
    # Check if there are 5 number:
    if len(numbers) < 5:
        return False
    # Check if each number is prime
    for number in numbers:
        if not is_prime(number):
            return False

    # Check if each number has a prime predecessor and no repeated prime numbers
    for i in range(1, len(numbers)):
        if not is_prime(numbers[i-1]) or numbers[i] == numbers[i-1]:
            return False

    return sum(numbers)


def are_consecutive_fibonacci_series(numbers):
    if len(numbers) < 5:
        return False

    # Check if the numbers form a Fibonacci series in either ascending or descending order
    if numbers[2] == numbers[1] + numbers[0]:
        step = 1  # Ascending order
    elif numbers[2] == numbers[0] - numbers[1]:
        step = -1  # Descending order
    else:
        return False

    a = numbers[0]
    b = numbers[1]
    for i in range(2, len(numbers)):
        c = a + (step * b)
        if numbers[i] != c:
            return False
        a = b
        b = c

    return sum(numbers)