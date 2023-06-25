import pygame
import sys
from settings import *
from functions import *
import copy

def welcome_screen():
    global task
    space_pressed_count = 0
    exit_game = False
    if debug == True:
        pass
    else:
        number_properties = check_number(central_number) 
        task = random.choice(number_properties)
        print(task)
    if task == "Series":
        text = "Match Series of Number Diagonally. For example, if the number on the center of the grid is 25, you should create a diagonal of 23,24,25,26,27"
    elif task == "Same":
        text = "Fill the main diagonal with equal numbers. For example, if the number on the center of the grid is 25, you should create a diagonal of 25,25,25,25,25"
    elif task == "Fibonacci":
        text = "Fill the main diagonal with fibonacci series. For example, if the number on the center of the grid is 21, you should create a diagonal of 8,13,21,34,55"
    elif task == "Prime":
        text = "Fill the main diagonal with prime numbers. For example, if the number on the center of the grid is 17, you should create a diagonal of 11,13,17,19,23"
    elif task == "Even":
        text = "Fill the main diagonal with consecutive even numbers. For example, if the number on the center of the grid is 12, you should create a diagonal of 8,10,12,14,16"
    elif task == "Odd":
        text = "Fill the main diagonal with consecutive odd numbers. For example, if the number on the center of the grid is 15, you should create a diagonal of 11,13,15,17,19"
    elif task.startswith("Multiple"):
        num = int(task[-1])
        result = f"{', '.join(str(num * i) for i in range(1, 6))}"
        text = f"Fill the main diagonal with consecutive mutliples of {num}. For example, if the number on the center of the grid is {num*3}, you should create a diagonal of {result}"
    
    window.fill(BACKGROUND)
    # Draw the image on the screen
    window.blit(image, (x, y))
    render_and_display_text(window, font, "Press Space Bar to Continue", 200)

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if space_pressed_count == 0:
                        window.fill(BACKGROUND)
                        render_and_display_text(window, font, "CHALLENGE", -150)
                        render_and_display_text(window, font, text, -100)
                        render_and_display_text(window, font, "Press Space Bar to Start", 200)
                        space_pressed_count += 1
                    else:
                        space_pressed_count = 0
                        game_loop()

        pygame.display.update()
        clock.tick(60)

def game_loop():
    global exclude_grid, grid
    preview_grid_text = ""

    for row, col in excluded_cells:
        grid[row][col] = -1
    grid[2][2] = str(central_number)

    player_tiles = generate_random_player_tile()
    latest_player_tiles = copy.deepcopy(player_tiles)
    last_value_on_selected_tile = ""
    reset_button_pressed = False

    # Variable to track the selected grid coordinates
    selected_grid = None
    symbol_selected = False
    number_selected = False

    # Switch between players
    current_player = 1
    # Define player variables
    player1_lives = 20  # Number of lives for player 1
    player2_lives = 20  # Number of lives for player 2
    if debug == True:
        player1_time = 120
        player2_time = 120
    else:
        player1_time = 60  # 60 seconds for player 1
        player2_time = 60  # 60 seconds for player 2
    # Start the timer for the first player's turn
    remaining_time = player1_time

    player1_score = 0
    player2_score = 0

    # Result in grid board
    rounded_result = ""
    # Main game loop
    running = True
    gameover = False
    winner = None

    while running:
        if gameover:
            window.fill(BACKGROUND)
            text_screen("Player 1", CENTRAL, 50, 150)
            text_screen("Player 2", CENTRAL, WINDOW_WIDTH-100, 150)
            text_screen(f"{player1_score}", CENTRAL, 70, 200)
            text_screen(f"{player2_score}", CENTRAL, WINDOW_WIDTH-70, 200)
            text_screen("Game Over!", CENTRAL, (WINDOW_WIDTH//2)-50, 250)
            text_screen(f"{winner}", CENTRAL, (WINDOW_WIDTH//2)-40, 270)
            text_screen("Press Enter to New Game", CENTRAL, WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2-10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome_screen()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if selected_grid is None:  # Check if no grid is currently selected
                            mouse_pos = pygame.mouse.get_pos()
                            # Check if the clicked grid is valid for selection
                            for row in range(GRID_ROWS):
                                for col in range(GRID_COLS):
                                    cell_x = GRID_OFFSET_X + col * GRID_TOTAL_SIZE
                                    cell_y = GRID_OFFSET_Y + row * GRID_TOTAL_SIZE
                                    if (row, col) not in exclude_grid:  # Exclude grid
                                        grid_rect = pygame.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE, border_radius=BORDER_RADIUS)
                                        if grid_rect.collidepoint(mouse_pos):
                                            selected_grid = (row, col)
                                            
                                            # Check if the selected grid falls into the restricted diagonal tiles for the current player
                                            if current_player == 1 and selected_grid in player1_restricted_tiles:
                                                selected_grid = None
                                                break

                                            elif current_player == 2 and selected_grid in player2_restricted_tiles:
                                                selected_grid = None
                                                break
                                            else:
                                                # Grid clicked, update the selected grid
                                                preview_grid_text = grid[row][col]
                                                last_value_on_selected_tile = grid[row][col]

                        elif selected_grid is not None:
                            
                            mouse_pos = pygame.mouse.get_pos()
                            reset_button_rect = pygame.Rect(12, 352, GRID_SIZE - 4, GRID_SIZE - 4)
                            go_button_rect = pygame.Rect(300, 350, GRID_SIZE, GRID_SIZE)
                            

                            # If a grid is already selected, check for Reset (R) button press
                            if reset_button_rect.collidepoint(mouse_pos):
                                row,col = selected_grid
                                player_tiles = latest_player_tiles
                                grid[row][col] = last_value_on_selected_tile
                                preview_grid_text = ""
                                selected_grid = None
                                number_selected = False
                                symbol_selected = False
                                reset_button_pressed = True
                                # player_tiles

                            elif go_button_rect.collidepoint(mouse_pos):
                                selected_row, selected_col = selected_grid
                                if grid[selected_row][selected_col] != "":
                                    preview_grid_text = grid[selected_row][selected_col] 
                                else:
                                    grid[selected_row][selected_col] = rounded_result
                                score_result = check_diagonals(grid)
                                score = score_result[0]
                                if score and current_player == 1:
                                    player1_score = score - player2_score
                                else:
                                    player2_score = score - player1_score
                                
                                if current_player == 1:
                                    player1_lives -= 1  # Decrement the number of lives for player 1
                                    remaining_time = player2_time  # Switch to player 2's turn
                                    current_player = 2
                                else:
                                    player2_lives -= 1  # Decrement the number of lives for player 1
                                    remaining_time = player1_time  # Switch to player 2's turn
                                    current_player = 1
                                selected_grid = None
                                preview_grid_text = ""
                                player_tiles = generate_random_player_tile()
                                latest_player_tiles =  copy.deepcopy(player_tiles)
                                number_selected = False
                                symbol_selected = False
                                reset_button_pressed = False
                                
                            else:
                                
                                for col in range(PLAYER_TILES):
                                    cell_x = GRID_OFFSET_X - (GRID_SIZE + GAP_BETWEEN_GRID) + col * GRID_TOTAL_SIZE
                                    cell_y = GRID_OFFSET_Y + 50 + (GRID_ROWS + 1) * GRID_TOTAL_SIZE
                                    grid_rect = pygame.Rect(cell_x, cell_y, GRID_SIZE, GRID_SIZE)
                                    
                                    if grid_rect.collidepoint(mouse_pos):
                                        if not symbol_selected and not number_selected:
                                            if preview_grid_text != "" and not player_tiles[col].isdigit():
                                                preview_grid_text += str(player_tiles[col])
                                                symbol_selected = True
                                                player_tiles[col] = ""

                                            elif not player_tiles[col].isdigit():
                                                break

                                            else:
                                                if not preview_grid_text.isdigit():
                                                    preview_grid_text += str(player_tiles[col])
                                                    if player_tiles[col].isdigit():
                                                        number_selected = True
                                                        player_tiles[col] = ""
                                        else:
                                            if symbol_selected and player_tiles[col].isdigit():
                                                preview_grid_text += str(player_tiles[col])
                                                symbol_selected = False
                                                number_selected = True
                                                player_tiles[col] = ""
                                            elif number_selected and not player_tiles[col].isdigit():
                                                preview_grid_text += str(player_tiles[col])
                                                number_selected = False
                                                symbol_selected = True
                                                player_tiles[col] = ""

            window.fill(BACKGROUND)
            if reset_button_pressed:
                player_tiles = copy.deepcopy(latest_player_tiles)
                draw_player_tiles(player_tiles)
                selected_grid = None
                reset_button_pressed = False
            else:
                draw_player_tiles(player_tiles)
            draw_power_cards()

            draw_elements(player1_score, current_player, player2_score, preview_grid_text)
            draw_game_board(grid, central_number)

            # Draw a border around the selected grid
            if selected_grid:
                row, col = selected_grid
                cell_x = GRID_OFFSET_X + col * GRID_TOTAL_SIZE
                cell_y = GRID_OFFSET_Y + row * GRID_TOTAL_SIZE

                # Draw a highlight effect on the selected grid
                pygame.draw.rect(window, (200, 25, 0, 100), (cell_x+1, cell_y+1, GRID_SIZE-2, GRID_SIZE-2), 3, border_radius=BORDER_RADIUS)

                # Calculate and draw the result on the selected grid
                rounded_result = calculate_result(preview_grid_text)
                grid[row][col] = rounded_result
                
        # Update the remaining time
            remaining_time -= clock.tick(60) / 1000  # Divide by 1000 to convert milliseconds to seconds

            # Switch to the next player if the time runs out
            if remaining_time <= 0:
                preview_grid_text = ""
                reset_button_pressed = False
                if selected_grid != None:
                    row,col = selected_grid
                    grid[row][col] = last_value_on_selected_tile
                    selected_grid = None
                player_tiles = generate_random_player_tile()
                
                if current_player == 1:
                    player1_lives -= 1  # Decrement the number of lives for player 1
                    remaining_time = player2_time  # Switch to player 2's turn
                    current_player = 2
                else:
                    player2_lives -= 1  # Decrement the number of lives for player 2
                    remaining_time = player1_time  # Switch to player 1's turn
                    current_player = 1

                if player1_lives <= 0 and player2_lives <= 0:
                    # Game over condition, handle it as desired
                    if player1_score > player2_score:
                        winner = "Player 1 Won"
                    elif player1_score == player2_score:
                        winner = "It's a Tie"
                    else:
                        winner = "Player 2 Won"
                    gameover = True

            # Calculate the width of the progress bar based on the remaining time and the current player
            if current_player == 1:
                progress_bar_progress = (remaining_time / player1_time) * WINDOW_WIDTH
                progress_bar_color = DIAGONAL1
            else:
                progress_bar_progress = (remaining_time / player2_time) * WINDOW_WIDTH
                progress_bar_color = DIAGONAL2

            # Draw the progress bar
            pygame.draw.rect(window, progress_bar_color, (progress_bar_x, progress_bar_y, progress_bar_progress, progress_bar_height))

            # Draw the circles/lives for each player
            for i in range(player1_lives):
                circle_x = circle_start_x+15 + (circle_radius + circle_spacing) * i
                pygame.draw.circle(window, DIAGONAL1, (circle_x, circle_y), circle_radius)

            for i in range(player2_lives):
                circle_x = circle_start_x + (circle_radius + circle_spacing) * i
                pygame.draw.circle(window, DIAGONAL2, (WINDOW_WIDTH - 150 + circle_x, circle_y), circle_radius)

        # Update the display
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    welcome_screen()
