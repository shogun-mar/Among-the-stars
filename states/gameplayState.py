import pygame
from math import pi
from states.gameState import GameState
from settings import *
from logic.powerup import PowerUp
from logic.enemy import Enemy

heart_sprite = pygame.image.load("graphics/heart_icon.png")
heart_rects = [heart_sprite.get_rect(topleft = ((SCREEN_WIDTH // 2) - i * 30, 70)) for i in range(3)]

circle_progress = 0 # Progress of the attack cooldown circle

def handle_gameplay_events(game, key):
    if key == PAUSE_KEY:
        game.game_state = GameState.PAUSE
    elif key == HYPERSPACE_KEY:
        current_time = pygame.time.get_ticks()
        temp_hyperspace_travel_time = current_time - game.last_hyperspace_travel_time
        if temp_hyperspace_travel_time > 0:
            game.game_state = GameState.HYPERSPACE
            game.last_hyperspace_travel_time = current_time
            game.hyperspace_travel_duration = temp_hyperspace_travel_time if temp_hyperspace_travel_time < game.hyperspace_travel_maximum_duration else game.hyperspace_travel_maximum_duration
            game.alpha_surface.set_alpha(HYPERSPACE_ALPHA_VALUE)
            print(f"Entering hyperspace for {game.hyperspace_travel_duration} ms")

def handle_gameplay_events_mouse(game, button, mouse_pos):
    if button == 1: #Left mouse button
        check_collisions(game, mouse_pos)

def render_gameplay(game):
    game.fake_screen.blit(game.alpha_surface, (0,0)) 
    game.game_starfield.draw()
    render_hyperspace_cooldown_bar(game)
    game.fake_screen.blit(game.rendered_score, game.rendered_score_rect)
    for i in range(game.life_points): game.fake_screen.blit(heart_sprite, heart_rects[i])
    if circle_progress != 1:draw_attack_cooldown_circle(game) # Draw attack cooldown circle if not fully charged
    
def check_collisions(game, mouse_pos):
    global circle_progress

    if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
        current_time = pygame.time.get_ticks()
        if current_time - game.last_attack_time > game.attack_cooldown:  # Check if the attack cooldown has passed
            game.last_attack_time = current_time  # Update last attack time immediately after cooldown check
            circle_progress = 0  # Reset the attack cooldown circle progress

            if not is_mouse_over_star(game, mouse_pos):  # Check if the mouse is not over a star
                elements_to_check = game.game_starfield.enemies + game.game_starfield.powerups # Combine enemies and powerups into a single list
                elements_to_check.sort(key=lambda element: element.pos3d.z, reverse=True)  # Sort the list by z distance in descending order
                for element in elements_to_check:  # Iterate over the combined list
                    if element.rect.collidepoint(mouse_pos):  # Check for collision with the mouse position
                        game.game_starfield.objects_to_remove.append(element)  # Add the element to the list of objects to remove
                        return  # Exit the method after finding and removing the element
                        
def is_mouse_over_star(game, mouse_pos):
        for star in game.game_starfield.stars:
            if star.rect.collidepoint(mouse_pos):
                return True
        return False

def activate_powerup(powerup):
    if powerup.type == 'life':
        print("Life powerup activated")
    elif powerup.type == 'cooldown':
        print("Cooldown powerup activated")
    elif powerup.type == 'score':
        print("Score powerup activated")
        #game.update_score(5)

def render_hyperspace_cooldown_bar(game):
    cooldown_percentage = (pygame.time.get_ticks() - game.last_hyperspace_travel_time) / game.hyperspace_travel_maximum_duration
    cooldown_width = int(SCREEN_WIDTH * cooldown_percentage)
    pygame.draw.rect(game.fake_screen, 'crimson', (0, 0, cooldown_width, 10))

def draw_attack_cooldown_circle(game):
    global circle_progress

    # Constants
    FULL_CIRCLE = 2 * pi  # Full circle in radians

    # Calculate progress based on time since last attack
    current_time = pygame.time.get_ticks()
    time_since_last_attack = current_time - game.last_attack_time
    circle_progress = time_since_last_attack / ATTACK_COOLDOWN
    circle_progress = min(max(circle_progress, 0), 1)  # Clamp between 0 and 1

    # Background circle
    thickness = 2
    radius = 20
    position = (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40)  # Bottom right corner
    pygame.draw.circle(game.fake_screen, (100, 100, 100), position, radius, thickness)  # Dark gray background

    # Cooldown circle
    end_angle = FULL_CIRCLE * circle_progress
    rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(game.fake_screen, (255, 255, 255), rect, -pi / 2, end_angle - pi / 2, radius) # White cooldown arc