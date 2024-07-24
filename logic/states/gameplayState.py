import pygame
from math import pi
from logic.states.gameState import GameState
from settings import *
from logic.powerup import PowerUp
from logic.enemy import Enemy
from logic.projectile import Projectile

# Constants
FULL_CIRCLE = 2 * pi  # Full circle in radians

def handle_gameplay_events(game, key):
    if key == PAUSE_KEY:
        game.game_state = GameState.PAUSE
        game.alpha_surface.set_alpha(HYPERSPACE_ALPHA_VALUE)
    elif key == SHIELD_KEY and game.shield_circle_progress == 1:
        game.is_shield_active = True
        game.last_shield_activation_time = pygame.time.get_ticks()
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
    game.fake_screen.blit(game.player.sprite, game.player.rect)
    if game.is_shield_active: game.fake_screen.blit(game.shield_sprite, game.shield_rect)
    game.fake_screen.blit(game.rendered_score, game.rendered_score_rect)
    for i in range(game.current_life_points): game.fake_screen.blit(game.heart_sprite, game.heart_rects[i])
    render_hyperspace_cooldown_bar(game) # Draw hyperspace cooldown bar
    if game.attack_circle_progress != 1: render_attack_cooldown_circle(game) # Draw attack cooldown circle if not fully charged
    if game.shield_circle_progress != 1: render_shield_cooldown_circle(game) # Draw shield cooldown circle if not fully charged
    
def check_collisions(game, mouse_pos):

    if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
        current_time = pygame.time.get_ticks()
        if current_time - game.last_attack_time > game.attack_cooldown:  # Check if the attack cooldown has passed
            game.last_attack_time = current_time  # Update last attack time immediately after cooldown check
            game.attack_circle_progress = 0  # Reset the attack cooldown circle progress

            if not is_mouse_over_star(game, mouse_pos):  # Check if the mouse is not over a star
                elements_to_check = game.game_starfield.enemies + game.game_starfield.powerups # Combine enemies and powerups into a single list
                elements_to_check.sort(key=lambda element: element.pos3d.z, reverse=True)  # Sort the list by z distance in descending order
                for element in elements_to_check:  # Iterate over the combined list
                    if element.rect.collidepoint(mouse_pos):  # Check for collision with the mouse position
                        if isinstance(element, PowerUp): activate_powerup(game, element)  # Activate the powerup if it is a powerup
                        if isinstance(element, Enemy): game.update_score(1)
                        shoot_at_target(game, element.rect.midbottom)  # Shoot at the element
                        game.game_starfield.objects_to_remove.append(element)  # Add the element to the list of objects to remove
                        return  # Exit the method after finding and removing the element
                        
def is_mouse_over_star(game, mouse_pos):
        for star in game.game_starfield.stars:
            if star.rect.collidepoint(mouse_pos):
                return True
        return False

def activate_powerup(game, powerup):
    if powerup.type == 'life' and game.current_life_points < PLAYER_LIFE_POINTS:
        game.current_life_points += 1
    elif powerup.type == 'cooldown':
        print("Cooldown powerup activated")
    elif powerup.type == 'score':
        game.update_score(2)

def shoot_at_target(game, target_pos):
    projectile = Projectile(original_entity=game.player, target_pos=target_pos, game=game) # Create a projectile aimed at the player's position
    game.game_starfield.projectiles.append(projectile) # Add the projectile to the projectiles list in game_starfield

def render_hyperspace_cooldown_bar(game):
    cooldown_percentage = (pygame.time.get_ticks() - game.last_hyperspace_travel_time) / game.hyperspace_travel_maximum_duration
    cooldown_width = int(SCREEN_WIDTH * cooldown_percentage)
    pygame.draw.rect(game.fake_screen, 'crimson', (0, 0, cooldown_width, 10))

def render_shield_cooldown_circle(game):

    # Calculate progress based on time since last attack
    current_time = pygame.time.get_ticks()
    time_since_last_shield = current_time - game.last_shield_activation_time
    game.shield_circle_progress = time_since_last_shield / SHIELD_COOLDOWN
    game.shield_circle_progress = min(max(game.shield_circle_progress, 0), 1)  # Clamp between 0 and 1

    # Background circle
    thickness = 2
    radius = 20
    position = (40, SCREEN_HEIGHT - 40)  # Bottom left corner
    pygame.draw.circle(game.fake_screen, (100, 100, 100), position, radius, thickness)  # Dark gray background

    # Cooldown circle
    end_angle = FULL_CIRCLE * game.shield_circle_progress
    rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(game.fake_screen, (0, 0, 255), rect, -pi / 2, end_angle - pi / 2, radius) # Cooldown arc

def render_attack_cooldown_circle(game):

    # Calculate progress based on time since last attack
    current_time = pygame.time.get_ticks()
    time_since_last_attack = current_time - game.last_attack_time
    game.attack_circle_progress = time_since_last_attack / ATTACK_COOLDOWN
    game.attack_circle_progress = min(max(game.attack_circle_progress, 0), 1)  # Clamp between 0 and 1

    # Background circle
    thickness = 2
    radius = 20
    position = (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40)  # Bottom right corner
    pygame.draw.circle(game.fake_screen, (100, 100, 100), position, radius, thickness)  # Dark gray background

    # Cooldown circle
    end_angle = FULL_CIRCLE * game.attack_circle_progress
    rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)
    pygame.draw.arc(game.fake_screen, (255, 0, 0), rect, -pi / 2, end_angle - pi / 2, radius) # Cooldown arc