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
progress_speed = 7

# Initialize percentages
red_percentage = 0
yellow_percentage = 0
green_percentage = 0

# Toggle values and initial percentages
toggle_colors = [red, yellow, green]
labels = ["Rain", "Fog", "Snow"]
statuses = ["Heavy", "Light", "Clear"]
color_selections = [red, yellow, green]

# Set up the clock for frame rate control
clock = pygame.time.Clock()
fps = 60

def draw_round_button(x, y, radius, color, label, status):
    pygame.draw.circle(screen, color, (x, y), radius)
    font = pygame.font.Font(None, 36)
    label_surface = font.render(label, True, black)
    label_rect = label_surface.get_rect(center=(x, y))
    screen.blit(label_surface, label_rect)

    status_surface = font.render(status, True, white)
    status_rect = status_surface.get_rect(center=(x, y + 60))
    screen.blit(status_surface, status_rect)

def draw_status_text(x, y, text, color):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_heading():
    font = pygame.font.Font(None, 48)
    heading_surface = font.render("ROAD CONDITION ANALYSIS", True, white)
    heading_rect = heading_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(heading_surface, heading_rect)

def calculate_percentages():
    """Calculate the percentage of each selected color."""
    total_buttons = len(color_selections)
    red_percentage = color_selections.count(red) * 100 / total_buttons
    yellow_percentage = color_selections.count(yellow) * 100 / total_buttons
    green_percentage = color_selections.count(green) * 100 / total_buttons
    return red_percentage, yellow_percentage, green_percentage

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
            for i, offset in enumerate(color_button_x_offsets):
                if color_button_y - color_button_radius <= mouse_y <= color_button_y + color_button_radius:
                    if offset + screen_width // 2 - color_button_radius <= mouse_x <= offset + screen_width // 2 + color_button_radius:
                        current_color_index = toggle_colors.index(color_selections[i])
                        next_color_index = (current_color_index + 1) % len(toggle_colors)
                        color_selections[i] = toggle_colors[next_color_index]

            # Check for click on start button
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                progressing = True
                progress = 0
                show_text = False
                red_percentage, yellow_percentage, green_percentage = calculate_percentages()

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
    for i, offset in enumerate(color_button_x_offsets):
        status_text = statuses[toggle_colors.index(color_selections[i])]
        draw_round_button(screen_width // 2 + offset, color_button_y, color_button_radius, color_selections[i], labels[i], status_text)

    # Draw the status text lines only after the progress completes
    if show_text:
        text_x = progress_bar_x
        text_y = button_y + button_height + 50
        draw_status_text(text_x, text_y, f"Current road condition for driving:", white)
        draw_status_text(text_x, text_y + 40, f"{int(red_percentage)}% very critical", red)
        draw_status_text(text_x, text_y + 80, f"{int(yellow_percentage)}% critical", yellow)
        draw_status_text(text_x, text_y + 120, f"{int(green_percentage)}% safe", green)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
