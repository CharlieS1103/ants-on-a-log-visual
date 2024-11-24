"""
This module simulates ants moving on a log.
"""

import random
import sys
import pygame as pg
import matplotlib.pyplot as plt
# Define global variables & constants (some of these aren't exactly "constants"
# but close enoguh)
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
NUMBER_OF_ANTS = 100
TIME = 0  # To be incremented in seconds
LOG_DISTANCE = WIDTH - 20  # Fixed log distance
COLLIDE = False  # Collision toggle
SIMULATE = False
sims = []


class Ant(pg.sprite.Sprite):
    """
    Class representing an ant.
    """
    def __init__(self, pos, direction, color=BLACK):
        super().__init__()
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect
        self.collision_rect.center = self.rect.center
        self.pos = pg.math.Vector2(pos)
        self.direction = pg.math.Vector2(direction).normalize()
        self.vel = self.direction * ANT_SPEED / 60
        self.font = pg.font.Font(None, 24)
        self.color = color

    def update(self, move_position=True):
        """
        Update the ant's position and draw the arrow
        """
        self.vel = self.direction * ANT_SPEED / 60
        if move_position:
            self.pos += self.vel
        self.rect.center = self.pos
        self.collision_rect.center = self.rect.center
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


class SimIteration():
    def __init__(self, ant_speed, elapsed_time):
        self.ant_speed = ant_speed
        self.elapsed_time = elapsed_time
        self.expected_time = 780 / ant_speed
        self.actual_time = elapsed_time
        self.diff = self.expected_time - self.actual_time

    def __str__(self):
        return (f"Ant Speed: {self.ant_speed},",
                f"Expected Time: {self.expected_time},",
                f"Actual Time: {self.actual_time}, Difference: {self.diff}")


def generate_ants(number_of_ants):
    """
    Generate a group of ants.
    """
    ants = pg.sprite.Group()
    colors = [BLACK, (150, 150, 150), (200, 200, 200), (100, 100, 100)]
    positions = [(20, HEIGHT // 2 - 10), (LOG_DISTANCE, HEIGHT // 2 - 10)]
    directions = [(1, 0), (-1, 0)]
    for i in range(2):
        ant = Ant(positions[i], directions[i], random.choice(colors))
        ants.add(ant)
    for i in range(number_of_ants - 2):
        while True:
            pos = (random.randint(0, LOG_DISTANCE), (HEIGHT // 2 - 10))
            direction = (random.choice([-1, 1]), 0)
            ant = Ant(pos, direction, random.choice(colors))
            if not any(
                ant.rect.colliderect(existing_ant.rect)
                for existing_ant in ants
            ):
                ants.add(ant)
                break

    ants_list = list(ants)
    n = len(ants_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if ants_list[j].rect.x > ants_list[j+1].rect.x:
                ants_list[j], ants_list[j+1] = ants_list[j+1], ants_list[j]

    sorted_ants_group = pg.sprite.Group(ants_list)

    return sorted_ants_group


def generate_log():
    """
    Generate the log.
    """
    logs = pg.sprite.Group()
    log = Log((WIDTH // 2, HEIGHT // 2))
    logs.add(log)
    return logs


def draw_textboxes(number_of_ants_textbox, ant_speed_textbox, collide_button,
                   sim_button):
    """
    Draw the textboxes and buttons on the screen.
    """
    start_button_text = pg.font.Font(None, 36).render("Start", True, BLACK,
                                                      WHITE)
    collide_button_text = pg.font.Font(None, 36).render(
        "Collide: On" if COLLIDE else "Collide: Off", True, WHITE)
    sim_button_text = pg.font.Font(None, 36).render(
        "Sim: On" if SIMULATE else "Sim: Off", True, WHITE
    )
    pg.draw.rect(screen, WHITE, number_of_ants_textbox)
    font.render("Number of Ants", True, BLACK)
    pg.draw.rect(screen, WHITE, ant_speed_textbox)
    font.render("Ant Speed", True, BLACK)
    pg.draw.rect(screen, WHITE, collide_button)
    pg.draw.rect(screen, WHITE, sim_button)
    screen.blit(start_button_text, (100, 10))
    screen.blit(collide_button_text,
                (collide_button.x + 5, collide_button.y + 5))
    screen.blit(sim_button_text, (sim_button.x + 5, sim_button.y + 5))


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
    x = 20
    if (number_of_ants_text == 'Number of ants' or
            int(number_of_ants_text) > x):
        number_of_ants_text = x
    if ant_speed_text == 'Ant Speed':
        ant_speed_text = '1'

    NUMBER_OF_ANTS = int(number_of_ants_text)
    ANT_SPEED = (float(ant_speed_text) * 13) / 2
    # 13 as WIDTH - 20 = 780, 780 / 60 = 13
    # Divide by 2 as we update the position twice per frame
    # im not going to bother with trying to allow flexible windows rn
    # Reset time
    global TIME
    TIME = 0
    # Generate ants
    ants = generate_ants(NUMBER_OF_ANTS)
    logs = generate_log()
    return ants, logs


def handle_collisions(ants):
    ants_list = sorted(ants, key=lambda ant: ant.rect.x)
    for i in range(len(ants_list) - 1):
        ant1 = ants_list[i]
        ant2 = ants_list[i + 1]
        if ant1.rect.colliderect(ant2.rect):
            ant1.set_direction((-ant1.direction.x, 0))
            ant2.set_direction((-ant2.direction.x, 0))
            # Need to not move position so collisions don't speed up
            ant1.update()
            ant2.update()


def generate_sim_graph(sim_iterations):
    ant_speeds = [sim_iteration.ant_speed for sim_iteration in sim_iterations]
    elapsed_times = [
        sim_iteration.elapsed_time for sim_iteration in sim_iterations
    ]
    expected_times = [
        sim_iteration.expected_time for sim_iteration in sim_iterations
    ]
    differences = [sim_iteration.diff for sim_iteration in sim_iterations]
    plt.plot(ant_speeds, elapsed_times, label="Actual Time")
    plt.plot(ant_speeds, expected_times, label="Expected Time")
    plt.plot(ant_speeds, differences, label="Difference")
    plt.xlabel("Ant Speed")
    plt.ylabel("Time (s)")
    plt.title("Ant Speed vs Time")
    plt.legend()
    plt.show()


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
    sim_button = pg.Rect(300, 130, 140, 32)
    number_of_ants_text = 'Number of ants'
    ant_speed_text = 'Ant Speed'
    active_textbox = None
    sim_iterations = []

    # Game loop
    start = False
    while not start:
        screen.fill(BLACK)
        draw_textboxes(number_of_ants_textbox, ant_speed_textbox,
                       collide_button, sim_button)
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
                elif sim_button.collidepoint(event.pos):
                    SIMULATE = not SIMULATE
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
        sim_button_text = font.render(
            "Sim: On" if SIMULATE else "Sim: Off", True, BLACK
        )

        screen.blit(number_of_ants_surface,
                    (number_of_ants_textbox.x + 5,
                     number_of_ants_textbox.y + 5))
        screen.blit(
            ant_speed_surface,
            (ant_speed_textbox.x + 5, ant_speed_textbox.y + 5)
        )
        screen.blit(collide_button_text,
                    (collide_button.x + 5, collide_button.y + 5))
        screen.blit(sim_button_text, (sim_button.x + 5, sim_button.y + 5))

        pg.display.flip()

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
        elapsed_time = (pg.time.get_ticks() - start_ticks) / 1000
        draw_timer(elapsed_time)
        # Handle collisions if collide is enabled
        if COLLIDE:
            handle_collisions(ants)
        for ant in ants:
            ant.update()
        clock.tick(60)
        # Remove ants that have moved off the log
        for ant in ants:
            if ant.pos.x < 20 or ant.pos.x > LOG_DISTANCE:
                ant.kill()

        # Stop the timer and display the time when all ants are gone
        if len(ants) == 0:
            running = False
            end_ticks = pg.time.get_ticks()
            elapsed_time = (end_ticks - start_ticks) / 1000
            print(f"All ants have fallen. Time: {elapsed_time:.2f} seconds")

    # Run the simulation for different speeds if SIMULATE is enabled
    if SIMULATE:
        speed_values = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1,
                        0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        for speed in speed_values:
            ant_speed_text = str(speed)
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
                elapsed_time = (pg.time.get_ticks() - start_ticks) / 1000
                draw_timer(elapsed_time)
                # Handle collisions if collide is enabled
                if COLLIDE:
                    handle_collisions(ants)
                for ant in ants:
                    ant.update()
                clock.tick(60)
                # Remove ants that have moved off the log
                for ant in ants:
                    if ant.pos.x < 20 or ant.pos.x > LOG_DISTANCE:
                        ant.kill()

                # Stop the timer and display the time when all ants are gone
                if len(ants) == 0:
                    running = False
                    end_ticks = pg.time.get_ticks()
                    elapsed_time = (end_ticks - start_ticks) / 1000
                    sim_iterations.append(SimIteration(speed, elapsed_time))
                    print(SimIteration(speed, elapsed_time))

                ants.draw(screen)
                logs.draw(screen)
                pg.display.flip()

        # Generate the simulation graph
        generate_sim_graph(sim_iterations)

    pg.quit()
    sys.exit()

"""
TODO:
- Fix collision detection
- Make UI a tad prettier
"""
