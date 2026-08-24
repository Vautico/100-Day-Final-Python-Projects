import random
import time
from turtle import Screen, Turtle


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_Y = -250
BALL_START_Y = -210
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BRICK_WIDTH = 78
BRICK_HEIGHT = 28
BRICK_ROWS = 5
BRICK_COLUMNS = 9
BRICK_START_Y = 220
BRICK_GAP = 8
BALL_SIZE = 12
MOVE_STEP = 35

COLORS = [
    "tomato",
    "orange",
    "gold",
    "lime green",
    "deep sky blue",
    "medium purple",
    "hot pink",
    "turquoise",
]


def make_rectangle(width, height, color):
    turtle = Turtle()
    turtle.shape("square")
    turtle.penup()
    turtle.color(color)
    turtle.shapesize(stretch_wid=height / 20, stretch_len=width / 20)
    return turtle


class Paddle:
    def __init__(self):
        self.turtle = make_rectangle(PADDLE_WIDTH, PADDLE_HEIGHT, "white")
        self.turtle.goto(0, PADDLE_Y)

    def move_left(self):
        new_x = max(self.turtle.xcor() - MOVE_STEP, -SCREEN_WIDTH / 2 + PADDLE_WIDTH / 2)
        self.turtle.setx(new_x)

    def move_right(self):
        new_x = min(self.turtle.xcor() + MOVE_STEP, SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2)
        self.turtle.setx(new_x)


class Ball:
    def __init__(self):
        self.turtle = Turtle()
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.color("white")
        self.turtle.shapesize(BALL_SIZE / 20)
        self.dx = 4
        self.dy = 4
        self.reset()

    def reset(self):
        self.turtle.goto(0, BALL_START_Y)
        self.dx = random.choice([-4, 4])
        self.dy = 4

    def move(self):
        self.turtle.goto(self.turtle.xcor() + self.dx, self.turtle.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.writer = Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.color("white")
        self.writer.goto(0, 265)
        self.update()

    def update(self):
        self.writer.clear()
        self.writer.write(
            f"Score: {self.score}    Lives: {self.lives}",
            align="center",
            font=("Arial", 18, "bold"),
        )

    def add_point(self):
        self.score += 10
        self.update()

    def lose_life(self):
        self.lives -= 1
        self.update()

    def show_message(self, text):
        self.writer.goto(0, 0)
        self.writer.write(text, align="center", font=("Arial", 28, "bold"))


class BrickWall:
    def __init__(self):
        self.bricks = []
        self.build()

    def build(self):
        total_width = BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP
        start_x = -total_width / 2 + BRICK_WIDTH / 2

        for row in range(BRICK_ROWS):
            for column in range(BRICK_COLUMNS):
                brick = make_rectangle(BRICK_WIDTH, BRICK_HEIGHT, random.choice(COLORS))
                x = start_x + column * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_START_Y - row * (BRICK_HEIGHT + BRICK_GAP)
                brick.goto(x, y)
                self.bricks.append(brick)

    def randomize_colors(self):
        for brick in self.bricks:
            brick.color(random.choice(COLORS))

    def remove(self, brick):
        brick.hideturtle()
        self.bricks.remove(brick)


def hit_rectangle(ball, rectangle, width, height):
    return (
        abs(ball.turtle.xcor() - rectangle.xcor()) < width / 2 + BALL_SIZE / 2
        and abs(ball.turtle.ycor() - rectangle.ycor()) < height / 2 + BALL_SIZE / 2
    )


def main():
    screen = Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.bgcolor("black")
    screen.title("Breakout")
    screen.tracer(0)

    paddle = Paddle()
    ball = Ball()
    wall = BrickWall()
    scoreboard = Scoreboard()
    paddle_hits = 0

    screen.listen()
    screen.onkeypress(paddle.move_left, "Left")
    screen.onkeypress(paddle.move_right, "Right")
    screen.onkeypress(paddle.move_left, "a")
    screen.onkeypress(paddle.move_right, "d")

    game_running = True
    while game_running:
        screen.update()
        time.sleep(0.01)
        ball.move()

        if ball.turtle.xcor() > SCREEN_WIDTH / 2 - BALL_SIZE or ball.turtle.xcor() < -SCREEN_WIDTH / 2 + BALL_SIZE:
            ball.bounce_x()

        if ball.turtle.ycor() > SCREEN_HEIGHT / 2 - BALL_SIZE:
            ball.bounce_y()

        if ball.dy < 0 and hit_rectangle(ball, paddle.turtle, PADDLE_WIDTH, PADDLE_HEIGHT):
            ball.turtle.sety(PADDLE_Y + PADDLE_HEIGHT)
            ball.bounce_y()
            paddle_hits += 1

            if paddle_hits % 2 == 0:
                wall.randomize_colors()

        for brick in wall.bricks[:]:
            if hit_rectangle(ball, brick, BRICK_WIDTH, BRICK_HEIGHT):
                wall.remove(brick)
                scoreboard.add_point()
                ball.bounce_y()
                break

        if ball.turtle.ycor() < -SCREEN_HEIGHT / 2:
            scoreboard.lose_life()
            if scoreboard.lives == 0:
                scoreboard.show_message("Loser :)")
                game_running = False
            else:
                ball.reset()
                screen.update()
                time.sleep(0.8)

        if not wall.bricks:
            scoreboard.show_message("Winner :(")
            game_running = False

    screen.exitonclick()


if __name__ == "__main__":
    main()
