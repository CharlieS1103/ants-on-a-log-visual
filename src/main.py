"""
This module simulates ants moving on a log.
"""

import random
import sys
import pygame as pg

# Define global variables & constants (some of these aren't exactly "constants"
# but close enoguh)
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
NUMBER_OF_ANTS = 100
TIME = 0  # To be incremented in seconds
ANT_SPEED = 20  # Meter per Minute
LOG_DISTANCE = WIDTH - 20  # Fixed log distance
COLLIDE = False  # Collision toggle


class Ant(pg.sprite.Sprite):
    """
    Class representing an ant.
    """
    def __init__(self, pos, direction, color=BLACK):
        super().__init__()
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.direction = pg.math.Vector2(direction).normalize()
        self.vel = self.direction * ANT_SPEED / 60
        # Convert speed to pixels per frame
        self.font = pg.font.Font(None, 24)
        self.color = color

    def update(self):
        """
        Update the ant's position and draw the arrow
        """
        self.vel = self.direction * ANT_SPEED / 60
        self.pos += self.vel
        self.rect.center = self.pos
        self.image.fill((0, 0, 0, 0))  # Clear the image
        pg.draw.circle(self.image, self.color, (10, 10), 10)
        self.draw_arrow()

    def draw_arrow(self):
        """
        Draw an arrow indicating the direction of the ant.
        """
        arrow_length = 10
        arrow_width = 5
        end_pos = (10 + self.direction.x * arrow_length,
                   10 + self.direction.y * arrow_length)
        pg.draw.line(self.image, WHITE, (10, 10), end_pos, 2)
        left_wing = self.direction.rotate(135) * arrow_width
        right_wing = self.direction.rotate(-135) * arrow_width
        pg.draw.line(self.image, WHITE, end_pos,
                     (end_pos[0] + left_wing.x, end_pos[1] + left_wing.y), 2)
        pg.draw.line(self.image, WHITE, end_pos,
                     (end_pos[0] + right_wing.x, end_pos[1] + right_wing.y), 2)

    def set_direction(self, direction):
        """
        Set the direction of the ant.
        """
        self.direction = pg.math.Vector2(direction).normalize()
        self.vel = self.direction * ANT_SPEED / 60


class Log(pg.sprite.Sprite):
    """
    Class representing the log.
    """
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((LOG_DISTANCE, 10))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=pos)


def generate_ants(number_of_ants):
    """
    Generate a group of ants.
    """
    ants = pg.sprite.Group()
    colors = [BLACK, (150, 150, 150), (200, 200, 200),
              (100, 100, 100)]
    for i in range(number_of_ants):
        pos = (random.randint(0, LOG_DISTANCE), (HEIGHT // 2 - 10))
        direction = (random.choice([-1, 1]), 0)
        ant = Ant(pos, direction, random.choice(colors))
        ants.add(ant)
    return ants


def generate_log():
    """
    Generate the log.
    """
    logs = pg.sprite.Group()
    log = Log((WIDTH // 2, HEIGHT // 2))
    logs.add(log)
    return logs


def draw_textboxes(number_of_ants_textbox, ant_speed_textbox, collide_button):
    """
    Draw the textboxes and buttons on the screen.
    """
    start_button_text = pg.font.Font(None, 36).render("Start", True, BLACK,
                                                      WHITE)
    collide_button_text = pg.font.Font(None, 36).render(
        "Collide: On" if COLLIDE else "Collide: Off", True, WHITE)
    pg.draw.rect(screen, WHITE, number_of_ants_textbox)
    font.render("Number of Ants", True, BLACK)
    pg.draw.rect(screen, WHITE, ant_speed_textbox)
    font.render("Ant Speed", True, BLACK)
    pg.draw.rect(screen, WHITE, collide_button)
    screen.blit(start_button_text, (100, 10))
    screen.blit(collide_button_text,
                (collide_button.x + 5, collide_button.y + 5))


def draw_timer(time):
    """
    Draw the timer on the screen
    """
    time_surface = font.render(f"Time: {time:.2f} seconds", True, BLACK)
    screen.blit(time_surface,
                (WIDTH // 2 - time_surface.get_width() // 2,
                 (HEIGHT // 2 - time_surface.get_height() // 2) - 100))


def on_start_button_click(number_of_ants_text, ant_speed_text):
    """
    Handle the start button click event.
    """
    global NUMBER_OF_ANTS
    global ANT_SPEED
    # Limit the amount of ants to x
    # (using x because I change this variable so often)
    x = 100
    if (number_of_ants_text == 'Number of ants' or
            int(number_of_ants_text) > x):
        number_of_ants_text = 'f{x}'
    if ant_speed_text == 'Ant Speed':
        ant_speed_text = '1'

    NUMBER_OF_ANTS = int(number_of_ants_text)
    ANT_SPEED = int(ant_speed_text) * 13
    # 13 as WIDTH - 20 = 780, 780 / 60 = 13
    # im not going to bother with trying to allow flexible windows rn
    # Reset time
    global TIME
    TIME = 0
    # Generate ants
    ants = generate_ants(NUMBER_OF_ANTS)
    logs = generate_log()
    return ants, logs


def handle_collisions(ants):

    for ant1 in ants:
        for ant2 in ants:
            # Will this be fast enough, idk how to do this
            toggled_once = False
            if (ant1 != ant2 and ant1.rect.colliderect(ant2.rect) and
               toggled_once is False):
                ant1.set_direction((-ant1.direction.x, 0))
                ant2.set_direction((-ant2.direction.x, 0))
                ant1.update()
                ant2.update()
                toggled_once = True
                print("Collision")


if __name__ == "__main__":
    """
    Runtime Logic
    """
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    font = pg.font.Font(None, 36)
    number_of_ants_textbox = pg.Rect(300, 10, 140, 32)
    ant_speed_textbox = pg.Rect(300, 50, 140, 32)
    collide_button = pg.Rect(300, 90, 140, 32)
    number_of_ants_text = 'Number of ants'
    ant_speed_text = 'Ant Speed'
    active_textbox = None
    # Game loop
    start = False
    while not start:
        screen.fill(BLACK)
        draw_textboxes(number_of_ants_textbox, ant_speed_textbox,
                       collide_button)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if number_of_ants_textbox.collidepoint(event.pos):
                    active_textbox = 'number_of_ants'
                elif ant_speed_textbox.collidepoint(event.pos):
                    active_textbox = 'ant_speed'
                elif collide_button.collidepoint(event.pos):
                    COLLIDE = not COLLIDE
                else:
                    active_textbox = None
                # Coordinates of start button are 100, 10, 100, 50
                if 100 <= event.pos[0] <= 200 and 10 <= event.pos[1] <= 60:
                    start = True
            if event.type == pg.KEYDOWN and active_textbox:
                if event.key == pg.K_BACKSPACE:
                    if active_textbox == 'number_of_ants':
                        if number_of_ants_text != 'Number of ants':
                            number_of_ants_text = number_of_ants_text[:-1]
                        else:
                            number_of_ants_text = ''
                    elif active_textbox == 'ant_speed':
                        if ant_speed_text != 'Ant Speed':
                            ant_speed_text = ant_speed_text[:-1]
                        else:
                            ant_speed_text = ''
                else:
                    if active_textbox == 'number_of_ants':
                        if number_of_ants_text == 'Number of ants':
                            number_of_ants_text = ''
                        number_of_ants_text += event.unicode
                    elif active_textbox == 'ant_speed':
                        if ant_speed_text == 'Ant Speed':
                            ant_speed_text = ''
                        ant_speed_text += event.unicode

        # Render the text
        number_of_ants_surface = font.render(number_of_ants_text, True, BLACK)
        ant_speed_surface = font.render(ant_speed_text, True, BLACK)
        collide_button_text = font.render(
            "Collide: On" if COLLIDE else "Collide: Off", True, BLACK)

        screen.blit(number_of_ants_surface,
                    (number_of_ants_textbox.x + 5,
                     number_of_ants_textbox.y + 5))
        screen.blit(
            ant_speed_surface,
            (ant_speed_textbox.x + 5, ant_speed_textbox.y + 5)
        )
        screen.blit(collide_button_text,
                    (collide_button.x + 5, collide_button.y + 5))

        pg.display.flip()
        clock.tick(30)

    # Start
    ants, logs = on_start_button_click(
        number_of_ants_text, ant_speed_text
    )
    running = True
    start_ticks = pg.time.get_ticks()  # Start timer
    while running:
        screen.fill(WHITE)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        ants.update()
        draw_timer((pg.time.get_ticks() - start_ticks)/1000)
        # Handle collisions if collide is enabled
        if COLLIDE:
            handle_collisions(ants)

        # Remove ants that have moved off the log
        for ant in ants:
            if ant.pos.x < 20 or ant.pos.x > LOG_DISTANCE:
                ant.kill()

        # Stop the timer and display the time when all ants are gone
        if len(ants) == 0:
            running = False
            end_ticks = pg.time.get_ticks()
            elapsed_time = (end_ticks - start_ticks) / 1000
            # Convert to seconds
            print(f"All ants have fallen. Time: {elapsed_time:.2f} seconds")
            time_surface = font.render(f"Time: {elapsed_time:.2f} seconds",
                                       True, BLACK)
            screen.blit(time_surface,
                        (WIDTH // 2 - time_surface.get_width() // 2,
                         HEIGHT // 2 - time_surface.get_height() // 2))
            pg.display.flip()
            # Probably a better way to handle this logic
            # but for a project like this one, its fine.
            quit_button = pg.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
            quit_text = font.render("Quit", True, BLACK)
            restart_button = pg.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 50, )
            pg.draw.rect(screen, WHITE, quit_button)
            screen.blit(quit_text, (WIDTH // 2 - 25, HEIGHT // 2 + 60))
            pg.display.flip()
            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if quit_button.collidepoint(event.pos):
                            pg.quit()
                            quit()
        ants.draw(screen)
        logs.draw(screen)
        pg.display.flip()
        clock.tick(60)
    pg.quit()
    sys.exit()

"""
TODO:
- Fix collision detection
- Make UI a tad prettier
"""
