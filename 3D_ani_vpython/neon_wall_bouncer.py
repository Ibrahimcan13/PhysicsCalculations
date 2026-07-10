import  vpython as vp
import random
vp.canvas(title='Neon Wall Bouncer', width=900, height=600, background=vp.color.black)

left_wall = vp.box(pos=vp.vector(-10,0,0), size=vp.vector(0.5,20,5), color = vp.color.blue)
right_wall = vp.box(pos=vp.vector(10,0,0), size=vp.vector(0.5,20,5), color = vp.color.blue)
top_wall = vp.box(pos=vp.vector(0,10,0), size=vp.vector(20,0.5,5), color = vp.color.blue)
bottom_wall = vp.box(pos=vp.vector(0,-10,0), size=vp.vector(20,0.5,5), color = vp.color.blue)

ball = vp.sphere(pos= vp.vector(0,0,0), radius = 1 , make_trail= True)

ball_velocity_x = float(input('Enter ball velocity x : '))
ball_velocity_y = float(input('Enter ball velocity y : '))

dt = 0.01
neon_colors = [
    vp.color.blue,
    vp.color.green,
    vp.color.yellow,
    vp.color.orange,
    vp.color.magenta,
    vp.color.cyan,
    vp.color.red
]

while True:
    vp.rate(120)

    ball.pos.x += ball_velocity_x * dt
    ball.pos.y += ball_velocity_y * dt

    if ball.pos.x >= 9:
        ball.pos.x = 9
        ball_velocity_x = -ball_velocity_x

        new_color = random.choice(neon_colors)
        ball.color = new_color
        ball.trail_color = new_color

    elif ball.pos.x <= -9:
        ball.pos.x = -9
        ball_velocity_x = -ball_velocity_x

        new_color = random.choice(neon_colors)
        ball.color = new_color
        ball.trail_color = new_color


    if ball.pos.y >= 9:
            ball.pos.y = 9
            ball_velocity_y = -ball_velocity_y

            new_color = random.choice(neon_colors)
            ball.color = new_color
            ball.trail_color = new_color

    elif ball.pos.y <= -9:
        ball.pos.y = -9
        ball_velocity_y = -ball_velocity_y

        new_color = random.choice(neon_colors)
        ball.color = new_color
        ball.trail_color = new_color


