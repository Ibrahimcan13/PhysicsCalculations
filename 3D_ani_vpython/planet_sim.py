import vpython as vp

vp.canvas(title='Solar System', width=900, height=600, background=vp.color.black)

sun = vp.sphere(pos=vp.vector(0,0,0), radius= 2 , color = vp.color.yellow)
sun.mass = 1000

mercury = vp.sphere(pos=vp.vector(5,0,0), radius= 0.3 , color = vp.color.white)
mercury.velocity = vp.vector(0,0,14)
mercury.mass = 0.6

venus = vp.sphere(pos=vp.vector(9,0,0), radius= 0.5 , color = vp.color.red)
venus.velocity = vp.vector(0,0,10.5)
venus.mass = 0.8

earth = vp.sphere(pos=vp.vector(14,0,0), radius= 0.6 , color = vp.color.blue)
earth.velocity = vp.vector(0,0,8.5)
earth.mass = 1

G = 1
dt = 0.001


while True:
    vp.rate(200)

    r_vector_mercury = sun.pos - mercury.pos
    r_mag_vec_mercury = r_vector_mercury.mag
    r_hat_mercury = r_vector_mercury.hat
    F1 = G * sun.mass * mercury.mass/(r_mag_vec_mercury**2) * r_hat_mercury
    mercury.velocity  += (F1 / mercury.mass) * dt
    mercury.pos += mercury.velocity * dt

    r_vector_venus = sun.pos - venus.pos
    r_mag_vec_venus = r_vector_venus.mag
    r_hat_venus = r_vector_venus.hat
    F2 = G * sun.mass * venus.mass / (r_mag_vec_venus ** 2) * r_hat_venus
    venus.velocity += (F2 / venus.mass) * dt
    venus.pos += venus.velocity * dt

    r_earth = sun.pos - earth.pos
    r_mag_vec_earth = r_earth.mag
    r_hat_earth = r_earth.hat
    F3 = G * sun.mass * earth.mass / (r_mag_vec_earth ** 2) * r_hat_earth
    earth.velocity += (F3 / earth.mass) * dt
    earth.pos += earth.velocity * dt