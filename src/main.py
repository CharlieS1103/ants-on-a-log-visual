import pygame as pg
import random


# Define global variables & constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
global number_of_ants
number_of_ants = 100
global time
time = 0  # To be incremented in seconds
global ant_speed
ant_speed = 1  # Meter per Minute
global collide
collide = True  # enable collision between ants

# Making it the same as the classic 1 meter per minute problem
LOG_DISTANCE = WIDTH - 20  # Fixed log distance


class Ant(pg.sprite.Sprite):
    def __init__(self, pos, direction, identifier):
        super().__init__()
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)
        self.direction = pg.math.Vector2(direction).normalize()
        self.identifier = identifier
        self.vel = self.direction * ant_speed / 60
        # Note the 60 is for frame rate not for units
        self.font = pg.font.Font(None, 24)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        self.image.fill((0, 0, 0, 0))  # Clear the image
        pg.draw.circle(self.image, BLACK, (10, 10), 10)
        self.draw_arrow()
        self.draw_identifier()

    def draw_arrow(self):
        arrow_length = 10
        arrow_width = 5
        end_pos = (10 + self.direction.x * arrow_length,
                   10 + self.direction.y * arrow_length)
        pg.draw.line(self.image, WHITE, (10, 10), end_pos, 2)
        # Draw arrowhead
        left_wing = self.direction.rotate(135) * arrow_width
        right_wing = self.direction.rotate(-135) * arrow_width
        pg.draw.line(self.image, WHITE, end_pos,
                     (end_pos[0] + left_wing.x, end_pos[1] + left_wing.y), 
                     2)
        pg.draw.line(
            self.image, WHITE, end_pos,
            (end_pos[0] + right_wing.x, end_pos[1] + right_wing.y), 2)
        
    def draw_identifier(self):
        identifier_surface = self.font.render(str(self.identifier), True,
                                              BLACK)
        identifier_rect = identifier_surface.get_rect(center=(10, -10))
        self.image.blit(identifier_surface, identifier_rect)


class Log(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((LOG_DISTANCE, 10))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pg.math.Vector2(0, 0)
        self.pos = pg.math.Vector2(pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos


def generate_ants(number_of_ants):
    ants = pg.sprite.Group()
    for i in range(number_of_ants):
        pos = (random.randint(0, LOG_DISTANCE), (HEIGHT // 2 - 10))
        direction = (random.choice([-1, 1]), 0)
        ant = Ant(pos, direction, i + 1)
        ants.add(ant)
    return ants


# Func is a tad redundant, but it's here for the sake of clarity
def generate_log():
    logs = pg.sprite.Group()
    log = Log((WIDTH // 2, HEIGHT // 2))
    logs.add(log)
    return logs


def draw_textboxes(number_of_ants_textbox, ant_speed_textbox):
    # , collide_button):
    start_button_text = pg.font.Font(None, 36).render("Start", True, WHITE)
    pg.draw.rect(screen, WHITE, number_of_ants_textbox)
    font.render("Number of Ants", True, BLACK)
    pg.draw.rect(screen, WHITE, ant_speed_textbox)
    font.render("Ant Speed", True, BLACK)
    # pg.draw.rect(screen, WHITE, collide_button)
    screen.blit(start_button_text, (100, 10))


def on_start_button_click(number_of_ants_text, ant_speed_text):
    # Update global variables
    global number_of_ants
    global ant_speed
    if number_of_ants_text == 'Number of ants':
        number_of_ants_text = '100'
    if ant_speed_text == 'Ant Speed':
        ant_speed_text = '1'

    number_of_ants = int(number_of_ants_text)
    ant_speed = int(ant_speed_text) * 13
    # 13 as WIDTH - 20 = 780, 780 / 60 = 13
    # im not going to bother with trying to allow flexible windows rn
    # Reset time
    global time
    time = 0
    # Generate ants
    ants = generate_ants(number_of_ants)
    logs = generate_log()
    return ants, logs


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    font = pg.font.Font(None, 36)
    number_of_ants_textbox = pg.Rect(300, 10, 140, 32)
    ant_speed_textbox = pg.Rect(300, 50, 140, 32)
    number_of_ants_text = 'Number of ants'
    ant_speed_text = 'Ant Speed'
    # collide_button = pg.Rect(300, 90, 140, 32)
    active_textbox = None
    # Game loop
    start = False
    while not start:
        screen.fill(BLACK)
        draw_textboxes(number_of_ants_textbox, 
                       ant_speed_textbox)  
        # add this back later collide_button)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if number_of_ants_textbox.collidepoint(event.pos):
                    active_textbox = 'number_of_ants'
                elif ant_speed_textbox.collidepoint(event.pos):
                    active_textbox = 'ant_speed'
                # elif collide_button.collidepoint(event.pos):
                # collide = not collide
                else:
                    active_textbox = None
                # Coordinates of start button are 100, 10, 100, 50
                if 100 <= event.pos[0] <= 200 and 10 <= event.pos[1] <= 60:
                    start = True
            if event.type == pg.KEYDOWN and active_textbox:
                if event.key == pg.K_BACKSPACE:
                    if active_textbox == 'number_of_ants':
                        number_of_ants_text = number_of_ants_text[:-1]
                    elif active_textbox == 'ant_speed':
                        ant_speed_text = ant_speed_text[:-1]
                else:
                    if active_textbox == 'number_of_ants':
                        number_of_ants_text += event.unicode
                    elif active_textbox == 'ant_speed':
                        ant_speed_text += event.unicode
        
        # Render the text
        number_of_ants_surface = font.render(number_of_ants_text, True, BLACK)
        ant_speed_surface = font.render(ant_speed_text, True, BLACK)
        
        screen.blit(number_of_ants_surface, 
                    (number_of_ants_textbox.x + 5, 
                     number_of_ants_textbox.y + 5))
        screen.blit(
            ant_speed_surface,
            (ant_speed_textbox.x + 5, ant_speed_textbox.y + 5)
        )
        
        pg.display.flip()
        clock.tick(60)

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
        logs.update()
        # Change to if collide after I implement the collision button
        if True:
            for ant1 in ants:
                for ant2 in ants:
                    if ant1 != ant2 and ant1.rect.colliderect(ant2.rect):
                        ant1.direction *= -1
                        ant1.vel = ant1.direction * ant_speed / 60
                        ant2.direction *= -1
                        ant2.vel = ant2.direction * ant_speed / 60
        # Remove ants that have moved off the log
        for ant in ants:
            if ant.pos.x < 20 or ant.pos.x > LOG_DISTANCE:
                ant.kill()

        # Stop the timer and display the time when all ants are gone
        if len(ants) == 0:
            running = False
            end_ticks = pg.time.get_ticks()
            elapsed_time = (end_ticks - start_ticks) / 1000
            print(f"All ants have fallen. Time: {elapsed_time:.2f}")
            time_surface = font.render(
                f"Time: {elapsed_time:.2f} seconds", True, BLACK)
            screen.blit(time_surface,
                        (WIDTH // 2 - time_surface.get_width() // 2,
                         HEIGHT // 2 - time_surface.get_height() // 2))
            pg.display.flip()
            # Probably a better way to handle this logic
            # but for a project like this one, its fine.
            quit_button = pg.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
            quit_text = font.render("Quit", True, BLACK)
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
