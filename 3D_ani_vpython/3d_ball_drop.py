import vpython as vp

vp.canvas(title='3D Ball Drop' , width=900, height=650, background=vp.color.white)

floor = vp.box(pos = vp.vector(1,1,1), size = vp.vector(1000,10,1000), color = vp.color.blue)

ball = vp.sphere(pos = vp.vector(0,200,0), radius = 2, color = vp.color.green, make_trail = True)

ball_velocity_y = float(input("Enter ball velocity in y axes: "))
ball_velocity_x = float(input("Enter ball velocity in x axes: "))
dt = 0.01
g = -9.81

while True:
    vp.rate(120)

    ball_velocity_y += g * dt

    ball.pos.x += ball_velocity_x * dt
    ball.pos.y += ball_velocity_y * dt

    if ball.pos.y <= 2.2:
        ball.pos.y = 2.2

        ball_velocity_y = -ball_velocity_y * 0.85
        ball_velocity_x = ball_velocity_x * 0.95