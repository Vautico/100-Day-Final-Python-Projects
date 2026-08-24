import random
import turtle


WIDTH = 700
HEIGHT = 650
PLAYER_Y = -270
PLAYER_SPEED = 28
BULLET_SPEED = 15
ALIEN_SPEED = 1
ALIEN_DROP = 28
COLLISION_DISTANCE = 24


screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Simple Space Invaders")
screen.bgcolor("black")
screen.tracer(0)


player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.setheading(90)
player.goto(0, PLAYER_Y)


bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.shapesize(stretch_wid=0.35, stretch_len=0.8)
bullet.setheading(90)
bullet.hideturtle()


hud = turtle.Turtle()
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 45)


message = turtle.Turtle()
message.color("white")
message.penup()
message.hideturtle()


aliens = []
score = 0
lives = 10
alien_direction = 1
bullet_active = False
game_running = True


def create_alien(x, y):
    alien = turtle.Turtle()
    alien.shape("turtle")
    alien.color(random.choice(["lime", "orange", "magenta", "red"]))
    alien.penup()
    alien.setheading(270)
    alien.goto(x, y)
    return alien


def reset_aliens():
    global aliens, alien_direction

    for alien in aliens:
        alien.hideturtle()

    aliens = []
    alien_direction = 1

    start_x = -240
    start_y = 220
    for row in range(3):
        for column in range(8):
            aliens.append(create_alien(start_x + column * 70, start_y - row * 55))


def update_hud():
    hud.clear()
    hud.write(f"Score: {score}   Lives: {lives}", font=("Arial", 18, "normal"))


def show_message(text):
    message.clear()
    message.goto(0, 0)
    message.write(text, align="center", font=("Arial", 24, "bold"))


def move_left():
    if not game_running:
        return
    next_x = max(player.xcor() - PLAYER_SPEED, -WIDTH // 2 + 35)
    player.setx(next_x)


def move_right():
    if not game_running:
        return
    next_x = min(player.xcor() + PLAYER_SPEED, WIDTH // 2 - 35)
    player.setx(next_x)


def fire_bullet():
    global bullet_active

    if bullet_active or not game_running:
        return

    bullet_active = True
    bullet.goto(player.xcor(), player.ycor() + 20)
    bullet.showturtle()


def hide_bullet():
    global bullet_active

    bullet_active = False
    bullet.hideturtle()
    bullet.goto(0, PLAYER_Y + 20)


def collision(first, second):
    return first.distance(second) < COLLISION_DISTANCE


def lose_life():
    global lives, game_running

    lives -= 1
    update_hud()

    if lives <= 0:
        game_running = False
        show_message("Game Over\nPress R to restart")
        return

    player.goto(0, PLAYER_Y)
    reset_aliens()
    hide_bullet()


def move_bullet():
    global score

    if not bullet_active:
        return

    bullet.sety(bullet.ycor() + BULLET_SPEED)

    if bullet.ycor() > HEIGHT // 2:
        hide_bullet()
        return

    for alien in aliens[:]:
        if collision(bullet, alien):
            alien.hideturtle()
            aliens.remove(alien)
            score += 10
            update_hud()
            hide_bullet()
            break


def move_aliens():
    global alien_direction, game_running

    if not aliens:
        game_running = False
        show_message("You Win!\nPress R to restart")
        return

    should_drop = any(
        alien.xcor() > WIDTH // 2 - 45 if alien_direction == 1 else alien.xcor() < -WIDTH // 2 + 45
        for alien in aliens
    )

    if should_drop:
        alien_direction *= -1
        for alien in aliens:
            alien.sety(alien.ycor() - ALIEN_DROP)
    else:
        for alien in aliens:
            alien.setx(alien.xcor() + ALIEN_SPEED * alien_direction)

    for alien in aliens:
        if alien.ycor() <= PLAYER_Y + 35 or collision(alien, player):
            lose_life()
            break


def restart():
    global score, lives, game_running

    if game_running:
        return

    score = 0
    lives = 10
    game_running = True
    message.clear()
    player.goto(0, PLAYER_Y)
    hide_bullet()
    reset_aliens()
    update_hud()
    game_loop()


def game_loop():
    if game_running:
        move_bullet()
        move_aliens()
        screen.update()
        screen.ontimer(game_loop, 45)
    else:
        screen.update()


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")
screen.onkeypress(restart, "r")
screen.onkeypress(restart, "R")

reset_aliens()
update_hud()
game_loop()

turtle.done()
