import pygame

# Initialize the game
pygame.init()
# Screen size
WIDTH, HEIGHT = 700, 500
# Display the window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# Coordinates of the text
WON = pygame.display.set_mode((WIDTH, HEIGHT))
# Title of the window
pygame.display.set_caption("Pong Game")
# Refresh rate but depends on the computer.
FPS = 60
# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("arial", 50)
WINNING_SCORE = 10


class Paddle:
    COLOR = WHITE  # Color of the ball
    speed = 4  # Normal speed of the ball

    def __init__(self, x, y, width, height):
        # Original_axis is to return the paddle to the starting position
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        # Model to draw the paddle
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        # Move the paddles up or down
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

    def reset(self):
        # Reset the coordinates of the paddle
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5  # MAX velocity the ball will get
    COLOR = WHITE  # Color of the ball

    def __init__(self, x, y, radius):
        # Original_axis is to return the paddle to the starting position
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    # Model for the ball
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    # Change the direction of the ball
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Reset the ball attributes to the starting attributes and the ball direction changes.
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1  # Ball x vel changed


def draw(win, paddles, ball, left_score, right_score):
    # Fill the background with the RGB color
    win.fill(BLACK)
    # Draw the scoreboard for the left and right side
    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)
    # Coordinates of the scoreboard of each side
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    # Draw all the paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw the middle dash line, with rectangles function.
    for i in range(10, HEIGHT, HEIGHT // 20):  # (starting, end, increment)
        if i % 2 == 1:
            # Case e.g.
            # 10 % 2 = 0
            # (10 + 25) % 2 = 1 --> 35 % 2 = 34, 1 "Reminder"
            continue
        # Use rectangle function (window, color, (x, y, width, height))
        # The x is the center of the screen minus the half of the rectangle width
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
    # Draw the ball
    ball.draw(win)
    # Update the display to show the changes.
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    # Make the ball bounce off the top and bottom walls
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    # make the ball bounce on the left or right paddle depending on the distance from the center of the paddle to the
    # radius (depends on the direction, left or right) make the ball bounce faster or slower.
    if ball.x_vel < 0:
        # Original l chain ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height
        # Original r chain ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Move the left paddle with W and S keys and prevent the paddle to go off the screen
    if keys[pygame.K_w] and left_paddle.y - left_paddle.speed >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.speed + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # Move the right paddle with UP and Down keys and prevent the paddle to go off the screen
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.speed >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.speed + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock()
    # Create the objects
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    # Score var
    left_score = 0
    right_score = 0

    # Main loop of the program
    while run:
        # Prevent the program from going to fast
        clock.tick(FPS)
        # Call the draw function
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)
        # Loop through all the events
        for event in pygame.event.get():
            # If the user click the exit (close, upper right corner) the program end
            if event.type == pygame.QUIT:
                run = False
                break
        # List or map of all keys pressed
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Detect if the ball score
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Condition for winning
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        # Winning text and reset
        if won:
            text = SCORE_FONT.render(win_text, True, WHITE)
            WON.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


# Check if the file that runs it is this.
if __name__ == "__main__":
    main()
