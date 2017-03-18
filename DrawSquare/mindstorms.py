import turtle

def draw_lines(turtle_instance, distance, angle, corners):
    for index in range(0, corners):
        turtle_instance .forward(distance)
        turtle_instance.right(angle)

def draw_j(j):
    j.forward(25)
    j.right(90)
    j.forward(150)
    j.right(90)
    j.forward(75)
    j.right(90)
    j.forward(25)

def draw_c(c):
    c.forward(75)
    c.right(90)
    c.forward(25)
    c.backward(25)
    c.left(90)
    c.backward(75)
    c.right(90)
    c.forward(150)
    c.left(90)
    c.forward(75)
    c.left(90)
    c.forward(25)


def draw_square(square):
    draw_lines(square, 100, 90, 4) 

def draw_circle(circle):
    circle.circle(100)

def draw_triangle(triangle):
    draw_lines(triangle, -150, 120, 3)

def draw_shapes():    
    window = turtle.Screen()    
    window.bgcolor("red")
    
    # circle = turtle.Turtle()
    # circle.shape("arrow")
    # circle.color("green")
    # circle.speed(3)

    # draw_circle(circle)

    # triangle = turtle.Turtle()
    # triangle.shape("turtle")
    # triangle.color("yellow")
    # triangle.speed(2)
    
    # draw_triangle(triangle)

    j = turtle.Turtle()
    j.shape("circle")
    j.color("blue")
    j.speed(5)
    j.width(2)
    j.setx(-25)

    c = turtle.Turtle()
    c.shape("circle")
    c.color("blue")
    c.speed(5)
    c.width(2)
    c.setx(25)

    draw_j(j)
    draw_c(c)

    window.exitonclick()
    exit

draw_shapes()