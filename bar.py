import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Progress Bar Animation")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)

# Progress bar dimensions
progress_bar_width = 600
progress_bar_height = 50
progress_bar_x = (screen_width - progress_bar_width) // 2
progress_bar_y = screen_height // 2 - 50

# Button dimensions
button_width = 150
button_height = 40
button_x = (screen_width - button_width) // 2
button_y = progress_bar_y + progress_bar_height + 50

# Color button dimensions
color_button_radius = 50
color_button_y = progress_bar_y - color_button_radius - 30
color_button_x_offsets = [-200, 0, 200]

# Progress states
progress = 0
progress_speed = 7  # Slowed down speed of progress

# Initialize percentages and toggle values
toggle_values = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
red_percentage = 30
yellow_percentage = 20
green_percentage = 50

# Set up the clock for frame rate control
clock = pygame.time.Clock()
fps = 60  # Frame rate

def adjust_percentages():
    """Ensure the total percentage is always 100."""
    global red_percentage, yellow_percentage, green_percentage
    total = red_percentage + yellow_percentage + green_percentage
    
    if total > 100:
        if red_percentage != max(toggle_values):
            red_percentage = max(toggle_values)
        elif yellow_percentage != max(toggle_values):
            yellow_percentage = max(toggle_values)
        elif green_percentage != max(toggle_values):
            green_percentage = max(toggle_values)
    else:
        if red_percentage == 100:
            yellow_percentage, green_percentage = 0, 0
        elif yellow_percentage == 100:
            red_percentage, green_percentage = 0, 0
        elif green_percentage == 100:
            red_percentage, yellow_percentage = 0, 0
    
    total = red_percentage + yellow_percentage + green_percentage
    
    if total != 100:
        if red_percentage != max(toggle_values):
            yellow_percentage = 100 - red_percentage - green_percentage

def draw_round_button(x, y, radius, color, text):
    pygame.draw.circle(screen, color, (x, y), radius)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_status_text(x, y, text, color):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_heading():
    font = pygame.font.Font(None, 48)
    heading_surface = font.render("CRITICAL PERCENTAGE VIEW", True, white)
    heading_rect = heading_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(heading_surface, heading_rect)

# Main loop
running = True
progressing = False
show_text = False

while running:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check for clicks on color buttons
            if color_button_y - color_button_radius <= mouse_y <= color_button_y + color_button_radius:
                if color_button_x_offsets[0] + screen_width // 2 - color_button_radius <= mouse_x <= color_button_x_offsets[0] + screen_width // 2 + color_button_radius:
                    # Toggle red and adjust yellow
                    red_percentage = toggle_values[(toggle_values.index(red_percentage) + 1) % len(toggle_values)]
                    yellow_percentage = 100 - red_percentage - green_percentage
                elif color_button_x_offsets[1] + screen_width // 2 - color_button_radius <= mouse_x <= color_button_x_offsets[1] + screen_width // 2 + color_button_radius:
                    # Toggle yellow and adjust green
                    yellow_percentage = toggle_values[(toggle_values.index(yellow_percentage) + 1) % len(toggle_values)]
                    green_percentage = 100 - red_percentage - yellow_percentage
                elif color_button_x_offsets[2] + screen_width // 2 - color_button_radius <= mouse_x <= color_button_x_offsets[2] + screen_width // 2 + color_button_radius:
                    # Toggle green and adjust red
                    green_percentage = toggle_values[(toggle_values.index(green_percentage) + 1) % len(toggle_values)]
                    red_percentage = 100 - yellow_percentage - green_percentage
            
            adjust_percentages()

            # Check for click on start button
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                if red_percentage + yellow_percentage + green_percentage == 100:
                    progressing = True
                    progress = 0
                    show_text = False

    # Update progress
    if progressing:
        progress += progress_speed
        if progress >= progress_bar_width:
            progress = progress_bar_width
            progressing = False
            show_text = True  # Show text lines when progress completes

    # Draw heading
    draw_heading()

    # Draw progress bar
    pygame.draw.rect(screen, white, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)

    # Draw red part
    if progress > 0:
        red_width = min(progress, progress_bar_width * (red_percentage / 100))
        pygame.draw.rect(screen, red, (progress_bar_x, progress_bar_y, red_width, progress_bar_height))
    
    # Draw yellow part
    if progress > progress_bar_width * (red_percentage / 100):
        yellow_width = min(progress - progress_bar_width * (red_percentage / 100), progress_bar_width * (yellow_percentage / 100))
        pygame.draw.rect(screen, yellow, (progress_bar_x + progress_bar_width * (red_percentage / 100), progress_bar_y, yellow_width, progress_bar_height))
    
    # Draw green part
    if progress > progress_bar_width * ((red_percentage + yellow_percentage) / 100):
        green_width = min(progress - progress_bar_width * ((red_percentage + yellow_percentage) / 100), progress_bar_width * (green_percentage / 100))
        pygame.draw.rect(screen, green, (progress_bar_x + progress_bar_width * ((red_percentage + yellow_percentage) / 100), progress_bar_y, green_width, progress_bar_height))

    # Draw start button
    pygame.draw.rect(screen, white, (button_x, button_y, button_width, button_height), 2)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Start", True, white)
    text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text_surface, text_rect)

    # Draw color buttons
    draw_round_button(screen_width // 2 + color_button_x_offsets[0], color_button_y, color_button_radius, red, str(red_percentage))
    draw_round_button(screen_width // 2 + color_button_x_offsets[1], color_button_y, color_button_radius, yellow, str(yellow_percentage))
    draw_round_button(screen_width // 2 + color_button_x_offsets[2], color_button_y, color_button_radius, green, str(green_percentage))

    # Draw the status text lines only after the progress completes
    if show_text:
        text_x = progress_bar_x
        text_y = button_y + button_height + 50
        draw_status_text(text_x, text_y, f"Current situation overview:", white)
        draw_status_text(text_x, text_y + 40, f"{red_percentage}% very critical.", red)
        draw_status_text(text_x, text_y + 80, f"{yellow_percentage}% critical.", yellow)
        draw_status_text(text_x, text_y + 120, f"{green_percentage}% safe.", green)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
