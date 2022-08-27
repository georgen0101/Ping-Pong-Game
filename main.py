"""
This is the Ping-Pong game not completed yet only the variables and classes.
For the program to do something instead of just a black screen.
I add a temporary code from the Turtle graphics library.
"""

# Libraries
# from turtle import Screen
from scoreboard import Scoreboard
from ball import Ball
from paddle import Paddle
# Temporary import, * imports all.
from turtle import *


screen = Screen()
screen.title("Ping Pong")
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.tracer(0)
screen.listen()

# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))

ball = Ball()
scoreboard = Scoreboard()

# screen.onkeypress(r_paddle.move_up, "Up")
# screen.onkeypress(r_paddle.move_down, "Down")
# screen.onkeypress(l_paddle.move_up, "w")
# screen.onkeypress(l_paddle.move_down, "s")

# --------- Temporary code ---------
color('red', 'yellow')
begin_fill()
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()
done()


screen.exitonclick()
