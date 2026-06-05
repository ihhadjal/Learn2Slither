import turtle as t
import random
import time

d = 0.1
s = 0
hs = 0
run = True

# SCREEN SPECIFICATIONS
sc = t.Screen()
sc.title("Learn2Slither")
sc.bgcolor("White")
sc.setup(width=600, height=600)
sc.tracer(0)


def draw_grid(size=600, cells=10):
    step = size // cells

    grid = t.Turtle()
    grid.speed(0)
    grid.color("lightgray")
    grid.penup()
    grid.hideturtle()

    for x in range(-size//2, size//2 + 1, step):
        grid.penup()
        grid.goto(x, -size//2)
        grid.pendown()
        grid.goto(x, size//2)

    for y in range(-size//2, size//2 + 1, step):
        grid.penup()
        grid.goto(-size//2, y)
        grid.pendown()
        grid.goto(size//2, y)


# SNAKE HEAD SPECIFICATIONS
h = t.Turtle()
h.shape("square")
h.color("blue")
h.shapesize(stretch_wid=3, stretch_len=3)
h.penup()
h.goto(0, 0)
h.direction = "Stop"

# FOOD SPECIFICATIONS
f = t.Turtle()
f.shape("square")
f.color("green")
f.shapesize(stretch_wid=3, stretch_len=3)
f.penup()
f.goto(0, 0)


def up():
    if h.direction != "down":
        h.direction = "up"


def down():
    if h.direction != "up":
        h.direction = "down"


def left():
    if h.direction != "right":
        h.direction = "left"


def right():
    if h.direction != "left":
        h.direction = "right"


def move():

    if h.direction == "up":
        h.sety(h.ycor() + 20)

    elif h.direction == "down":
        h.sety(h.ycor() - 20)

    elif h.direction == "left":
        h.setx(h.xcor() - 20)

    elif h.direction == "right":
        h.setx(h.xcor() + 20)


sc.listen()


sc.onkeypress(up, "Up")
sc.onkeypress(down, "Down")
sc.onkeypress(left, "Left")
sc.onkeypress(right, "Right")


seg = []

while run:
    draw_grid(600, 10)
    try:
        sc.update()

        # wall collision
        if abs(h.xcor()) > 290 or abs(h.ycor()) > 290:
            time.sleep(1)
            h.goto(0, 0)
            h.direction = "Stop"

            for segment in seg:
                segment.goto(1000, 1000)
            seg.clear()

            s = 0
            d = 0.1

        # food collision
        if h.distance(f) < 20:
            f.goto(random.randint(-270, 270), random.randint(-270, 270))
            new_seg = t.Turtle()
            new_seg.shape("square")
            new_seg.shapesize(stretch_len=3, stretch_wid=3)
            new_seg.color("blue")
            new_seg.penup()
            seg.append(new_seg)
            d -= 0.001
            s += 10

            if s > hs:
                hs = s

        # move body
        for i in range(len(seg) - 1, 0, -1):
            x = seg[i - 1].xcor()
            y = seg[i - 1].ycor()
            seg[i].goto(x, y)

        if seg:
            seg[0].goto(h.xcor(), h.ycor())
        move()

        # self collision
        for segment in seg:
            if segment.distance(h) < 20:
                time.sleep(1)
                h.goto(0, 0)
                h.direction = "Stop"

                for segment in seg:
                    segment.goto(1000, 1000)
                seg.clear()

                s = 0
                d = 0.1

        time.sleep(d)

    except t.Terminator:
        run = False
