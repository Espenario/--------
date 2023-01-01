import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

delta = 0.0
angle = 0.01
anglex = 0.01
angley = 0.01
posx = 0.0
change = 0.1
posy = 0.0
posz = 0.0
size = 0.0
deltax = 0.0
deltay = 0.0
window = None
change1 = 1
test = 1
m = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
R = 2
z = 0
bublik1 = []
y = 0
dx = 0
dy = 0
dz = 0
d1 = 0.0
d2 = 0.00
d3 = 0.0
texture = 0
texCoord = [0,0, 2,0, 2,2, 0,2]
triangles = []

def main():
    global window

    if not glfw.init():
        return
    window = glfw.create_window(1024, 1024, "Lab1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    #create_texture()
    #initshaders()
    while not glfw.window_should_close(window):
        display()
    glfw.destroy_window(window)
    glfw.terminate()

def key_callback(window, key, scancode, action,
mods):
    global delta, deltax, deltay, index,change1
    global angle
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            delta = -0.3
        if key == 263: # glfw.KEY_LEFT
            delta = 0.3
        if key == 264:
            deltax = 0.3
        if key == 265:
            deltax = -0.3
        if key == 266:
            deltay = 0.3
        if key == 267:
            deltay = -0.3
        if key == 257:
            #index = index+1
            #angle = 0
            #anglex = 0
            #angley = 0
            deltay = 0
            delta = 0
            deltax = 0
        if key == glfw.KEY_K:
            change1 *= -1

def scroll_callback(window, xoffset, yoffset):
    global size, change
    if (xoffset > 0):
        change *= 1.1
    else:
        change *= 0.9


def test():
    bublik1 = []
    phi = 0.0
    a = 1
    b = 4
    theta = 0.0
    while theta < 1:
        phi = 0
        glBegin(GL_TRIANGLE_STRIP)
        while phi <= 2*pi+0.1:
            z = 0
            x = 4 + a*cos(phi)
            y = b*sin(phi)
            phi += 0.1
            #bublik1.append(x)
            #bublik1.append(y)
            #bublik1.append(z)
            glVertex3f(x,y,z)
            glVertex3f(x,y,z+ 0.1)
        glEnd()
        glRotatef(theta/pi*180, 0,1,0)
        theta += 0.01

def movement():
    global dx,d1, dy, d2, d3,dz
    dx += d1
    dy += d2
    dz += d3
    if R + dx >= 9 or -R + dx <= -9:
        d1 *= -1
    if R + dy >= 9 or -R + dy <= -9:
        d2 *= -1
    if R + dz >= 9 or -R + dz <= -9:
        d3 *= -1

def create_texture():
    data = [0,255,0, 0,255,255, 0,0,0, 0,255,0]

    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_UNSIGNED_BYTE, data)

    glBindTexture(GL_TEXTURE_2D, 0)



def bublik():
    global dx, triangles
    bublik1 = []
    phi = 0.0
    R = 2
    r = 1
    theta = 0.0
    a = 1
    b = 4
    triangles = []

    #glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    #glEnable(GL_COLOR_MATERIAL)


    #glBegin(GL_TRIANGLE_STRIP)
    while theta < 2*pi:
        phi = 0
        while phi <= 2*pi:
            z = r*sin(phi) + dz
            x = R*cos(theta) + r*cos(phi)*cos(theta) + dx
            y = R*sin(theta) + r*cos(phi)*sin(theta) + dy
            triangles.append([x,y,z])
            #print(x, y, z)
            z = r*sin(phi) + dz
            x = R*cos(theta+2*pi/10) + r*cos(phi)*cos(theta+2*pi/10) + dx
            y = R*sin(theta+2*pi/10) + r*cos(phi)*sin(theta+2*pi/10) + dy
            triangles.append([x,y,z])
            phi += 2*pi/100
        #glRotatef(theta/pi*180, 0,1,0)
        theta += 2*pi/10

    i = 0
    normals = []
    '''while i < len(triangles) - 2:
        ax = triangles[i+1][0] - triangles[i][0]
        bx = triangles[i+1][1] - triangles[i][1]
        cx = triangles[i+1][2] - triangles[i][2]
        ox = triangles[i+2][0] - triangles[i][0]
        oy = triangles[i+2][1] - triangles[i][1]
        oz = triangles[i+2][2] - triangles[i][2]
        AB = [ax, bx, cx]
        AO = [ox, oy, oz]
        norm = [(AB[1]*AO[2] - AO[1]*AB[2]), (-1*AB[0]*AO[2] + AO[0]*AB[2]),(AB[0]*AO[1] - AO[0]*AB[1])]
        normals.append(norm)
        i += 1'''

    theta = 0
    while i < len(triangles) - 2:
        cx = (triangles[i][0] + triangles[i+1][0] + triangles[i+2][0]) / 3
        cy = (triangles[i][1] + triangles[i+1][1] + triangles[i+2][1]) / 3
        cz = (triangles[i][2] + triangles[i+1][2] + triangles[i+2][2]) / 3
        norm = [(R*cos(theta%(98*2*pi/10)) - cx, R*sin(theta%(98*2*pi/10)) - cy, -cz)]
        normals.append(norm)
        theta += 2*pi/10
        i += 1




    test = [-2,-2,0, 2,-2,0 ,2,2,0, -2,2,0]

    glColor3f(1,1,1)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3,GL_FLOAT, 0, triangles)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, triangles)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, len(triangles))


    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)


    '''glBegin(GL_TRIANGLE_STRIP)

    for i in    range(len(triangles)):
        if i % 2 == 0:
            normx = normals[i][0] + normals[i-1][0] + normals[i-2][0] + normals[(i + 100 - 1)%len(normals)][0] + normals[(i + 100 - 2)%len(normals)][0] + normals[(i + 100 - 3)%len(normals)][0]
            normy = normals[i][1] + normals[i-1][1] + normals[i-2][1] + normals[(i + 100 - 1)%len(normals)][1] + normals[(i + 100 - 2)%len(normals)][1] + normals[(i + 100 - 3)%len(normals)][1]
            normz = normals[i][2] + normals[i-1][2] + normals[i-2][2] + normals[(i + 100 - 1)%len(normals)][2] + normals[(i + 100 - 2)%len(normals)][2] + normals[(i + 100 - 3)%len(normals)][2]
            glNormal3f(normx, normy, normz)
        else:
            normx = normals[i][0] + normals[i-1][0] + normals[i-2][0] + normals[i - 100 - 1][0] + normals[i - 100 + 1][0] + normals[i - 100][0]
            normy = normals[i][1] + normals[i-1][1] + normals[i-2][1] + normals[i - 100 - 1][1] + normals[i - 100 + 1][1] + normals[i - 100][1]
            normz = normals[i][2] + normals[i-1][2] + normals[i-2][2] + normals[i - 100 - 1][2] + normals[i - 100 + 1][2] + normals[i - 100][2]
            glNormal3f(normx, normy, normz)
        print(dx)
        glVertex3f(triangles[i][0], triangles[i][1], triangles[i][2])


    glEnd()'''
    #glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    movement()

    #glEnableClientState(GL_VERTEX_ARRAY)
    #glVertexPointer(3,GL_FLOAT, 0, bublik1)
    #glDrawArrays(GL_TRIANGLES, 0, len(bublik1) / 3)
    #glDisableClientState(GL_VERTEX_ARRAY)



#    glRotatef(angle, 0, 0, 1)
#    glRotatef(anglex, 1, 0, 0)
#    glRotatef(angley, 0, 1, 0)

    '''glBegin(GL_QUADS)

    delt = 0

    glColor4f(1.0,1.0,1.0,0.5)
    glVertex3f( 1.0 + delt, 1.0,-1.0)
    glVertex3f(-1.0 + delt , 1.0,-1.0)
    glVertex3f(-1.0 + delt , 1.0, 1.0)
    glVertex3f( 1.0 + delt , 1.0, 1.0)

    glColor4f(0.0,1.0,0.0,0.5)
    glVertex3f( 1.0+ delt ,-1.0, 1.0)
    glVertex3f(-1.0 + delt ,-1.0, 1.0)
    glVertex3f(-1.0 + delt ,-1.0,-1.0)
    glVertex3f( 1.0 + delt ,-1.0,-1.0)

    glColor4f(1.0,1.0,1.0,0.5)
    glVertex3f( 1.0 + delt , 1.0, 1.0)
    glVertex3f(-1.0 + delt , 1.0, 1.0)
    glVertex3f(-1.0 + delt ,-1.0, 1.0)
    glVertex3f( 1.0 + delt ,-1.0, 1.0)

    glColor4f(0.0,0.0,0.0,0.5)
    glVertex3f( 1.0 + delt ,-1.0,-1.0)
    glVertex3f(-1.0 + delt ,-1.0,-1.0)
    glVertex3f(-1.0 + delt , 1.0,-1.0)
    glVertex3f( 1.0 + delt , 1.0,-1.0)

    glColor4f(0.0,0.0,1.0,0.5)
    glVertex3f(-1.0 + delt , 1.0, 1.0)
    glVertex3f(-1.0 + delt , 1.0,-1.0)
    glVertex3f(-1.0 + delt ,-1.0,-1.0)
    glVertex3f(-1.0 + delt ,-1.0, 1.0)

    glColor4f(1.0,0.0,0.0,0.5)
    glVertex3f( 1.0 + delt , 1.0,-1.0)
    glVertex3f( 1.0 + delt , 1.0, 1.0)
    glVertex3f( 1.0 + delt ,-1.0, 1.0)
    glVertex3f( 1.0 + delt ,-1.0,-1.0)

    glEnd()'''

def lox():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #glRotatef(angle,1,1,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(anglex,1,0,0)
    glRotatef(angley,0,1,0)
    glRotatef(angle,0,0,1)
    glScalef(change, change, change)

    bublik()
    #test()

def display():

    global angle, anglex, angley, change, delta, deltax, deltay, test, m, ly, lz, index,change1

    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    lox()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, [0,0, 5, 1])
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0,0,0,1])
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 120)
    glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)



    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #glFrontFace(GL_CW)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #glPushMatrix()
    #glRotatef(23, 1, 1, 1)




    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    #glPopMatrix()



    #glTranslatef(1,0,0)
    #glPushMatrix()
    #glTranslatef(5,0,0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)
    glDisable(GL_NORMALIZE)



    #glFlush()
    #glPushMatrix()
    #change = 1.0
    angle += delta
    anglex += deltax
    angley += deltay
    #delta = 0
    #deltax = 0
    #deltay = 0
    glfw.swap_buffers(window)
    glfw.poll_events()


main()
