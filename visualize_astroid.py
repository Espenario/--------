import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGL.GL.shaders import compileProgram, compileShader
import math 
import imgui
from imgui.integrations.glfw import GlfwRenderer
import random
import pygame

deltaz = 0.0
anglez = 0.01
anglex = 0.01
angley = 0.01
posx = 0.0
change = 1
posy = 0.0
posz = 0.0
size = 0.0
deltax = 0.0
deltay = 0.0
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
texCoord = [[]]
tr_x = 0
tr_y = 0
tr_z = 0
random_state = 42
triangles = []
materials = ['gold', 'iron', 'nickel', 'titanium', 'silver']

vertexShaderSource = """
        attribute vec3 position;
        attribute vec2 texcoords;
        //attribute int texid;
          varying vec4 vertex_color;
          varying vec2 texcoords_v;
          varying vec3 v;
          varying vec3 n;

        void main() {
            v = vec3(gl_ModelViewMatrix * gl_Vertex);
            n = normalize(gl_NormalMatrix * gl_Normal);
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            //gl_TexCoord[0] = texcoords;
            //??
            vertex_color = gl_Color;
            texcoords_v = texcoords;

        }""";

fragmentShaderSource = """

            varying vec2 texcoords_v;
            varying vec4 vertex_color;
            varying vec3 v;
            varying vec3 n;

            uniform sampler2D thetexture;//s[2]
            void main() {

                vec4 result = vec4(0.0);
                for (int li = 0; li < gl_MaxLights; ++li)
                {
                    vec3 lightDirection;
                    if (gl_LightSource[li].position.w != 0.0)
                    {
                        // позиционный источник света
                        lightDirection = normalize(gl_LightSource[li].position.xyz - v);
                    }
                    else
                    {
                        // направленный источник света
                        lightDirection = normalize(gl_LightSource[li].position.xyz);
                    }

                    vec4 Iamb = gl_FrontLightProduct[li].ambient;

                    float diffuseAngle = max(dot(n, lightDirection), 0.0);
                    vec4 Idiff = gl_FrontLightProduct[li].diffuse * diffuseAngle;
                    Idiff = clamp(Idiff, 0.0, 1.0);

                    result += Iamb + Idiff;
                }

                //gl_FragColor = vertex_color;
                gl_FragColor = result * texture2D(thetexture, texcoords_v);
                //texture2D(thetexture, texcoords_v)
            }""";


class Window():
    
    def __init__(self):
        if not glfw.init():
            raise SystemExit
        self.window = glfw.create_window(1024, 1024, "Asteroid", None, None)
        if not self.window:
            glfw.terminate()
            raise SystemExit

    def setup_window(self):
        glfw.make_context_current(self.window)
        imgui.create_context()
        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0.0)
        imgui.core.style_colors_dark()
        impl = GlfwRenderer(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_scroll_callback(self.window, scroll_callback)
        while not glfw.window_should_close(self.window):  
            #impl.process_inputs()        
            self.display(impl)
        impl.shutdown()
        glfw.destroy_window(self.window)
        glfw.terminate()
 
    def display(self, impl=None):
        global tr_x, tr_y, tr_z, random_state
        #glfw.poll_events()
        self.create_asteroid_surface()
        #glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()
        imgui.begin("Settings", True)
        #print(tr_x)
        _,values = imgui.slider_float3("Translation x,y,z", tr_x, tr_y, tr_z, -10, 10)
        _,random_state = imgui.slider_int("Forms", random_state, 10, 43)
        tr_x = values[0]
        tr_y = values[1]
        #print(tr_x)
        imgui.end()
        imgui.render()
        impl.render(imgui.get_draw_data())
        #self.imgui_func()

        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def create_asteroid_surface(self):
        global anglez, anglex, angley, texCoord

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 1)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        #create_texture(0)   #

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
       # glEnable(GL_COLOR_MATERIAL)
       # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )

        glRotatef(anglex, 1, 0, 0)
        glRotatef(angley, 0, 1, 0)
        glRotatef(anglez, 0, 0, 1)

        glScalef(change, change, change)

        glTranslatef(tr_x, tr_y, tr_z)

        #glColor3f(233,0, 124)

        vertices = get_asteroid_border()
        parts = get_diff_areas(vertices)
        
        #print(parts)
        #vertices = [-1, -1,0.0,
             #1, -1,0.0,
             #1, 1,0.0]
        #v = np.array(vertices, dtype = np.float32)
        normals = get_surface_normals(vertices)

        buff = []
        for i in range(len(vertices)):
            buff.append([vertices[i][0], vertices[i][1] + 5, vertices[i][2]])
        
        vertex = create_shader(GL_VERTEX_SHADER, vertexShaderSource)
        fragment = create_shader(GL_FRAGMENT_SHADER, fragmentShaderSource)
        program = glCreateProgram()
        # Приcоединяем вершинный шейдер к программе
        glAttachShader(program, vertex)
        # Присоединяем фрагментный шейдер к программе
        glAttachShader(program, fragment)
        # "Собираем" шейдерную программу
        glLinkProgram(program)
        # Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
        glUseProgram(program)

        tex_loc = glGetAttribLocation( program, 'texcoords')
        #print(texCoord)
        #glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 0, texCoord)
        glEnableVertexAttribArray( tex_loc )
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


        buff = []
        for i in range(len(vertices)):
            buff.append([vertices[i][0], vertices[i][1] + 5, vertices[i][2]])


        normals = get_surface_normals(vertices)

        glNormalPointer(GL_FLOAT, 0, normals)

        texCoord = [[]]
        extreme_points = []

        for part in parts:
            extreme_points.append(get_extreme_points(part))

        for i,part in enumerate(parts):
            get_tex_coords(part,extreme_points[i])
        #print(len(parts))
        print(texCoord, '-----------------------')

        #glVertexPointer(3, GL_FLOAT,0,buff)
        #glDrawArrays(GL_TRIANGLE_FAN,0, len(buff))
        #glDeleteTextures(1,texture)    #

        for i in range(len(parts)):
            create_texture(i)  #
            glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 0, texCoord[i])
            glEnableVertexAttribArray( tex_loc )
            glVertexPointer(3, GL_FLOAT,0,parts[i])
            glDrawArrays(GL_POLYGON,0, len(parts[i]))
            glDeleteTextures(1,texture)   #



        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.4, 0.7, 0.2])
        glLightfv(GL_LIGHT0, GL_POSITION, [0,0, 1, 1])
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.4)

        glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
        glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)

        glDeleteTextures(1,texture)
       
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_NORMALIZE)

        anglex += deltax
        angley += deltay
        anglez += deltaz

def create_texture(index):
    random.seed(34)
    material_index = np.random.randint(0,1) + index

    textureSurface = pygame.image.load(f'Текстуры'       
                                        f'\{materials[material_index]}.jpg')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()


    glGenTextures(1, texture)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)

def get_surface_normals(vertex_array):
    normals = []
    for elem in vertex_array:
        normals.append([0,0,1])
    return normals

def create_shader(shader_type, source):
    # Создаем пустой объект шейдера
    shader = glCreateShader(shader_type)
    # Привязываем текст шейдера к пустому объекту шейдера
    glShaderSource(shader, source)
    # Компилируем шейдер
    glCompileShader(shader)
    # Возвращаем созданный шейдер
    return shader

def get_asteroid_border():
    n = 20
    x_center = 100
    y_center = 100
    w = 5
    h = 2
    #glTranslatef (x_center, y_center, 0)
    vertices = []
    angle_increment = 2 * math.pi / n
    i = 0
    random.seed(random_state)
    epsilon = 0.01
    while i < 2 * math.pi:
        random_value_x = random.uniform(-1,1)
        random_value_y = random.uniform(-1,1)
        x = (w + random_value_x)/2 * math.cos(i)
        y = (h + random_value_y)/2 * math.sin(i)
        tx = math.cos(i) * 0.5 + 0.5
        ty = math.sin(i) * 0.5 + 0.5
        #texCoord.append(tx)
        #texCoord.append(ty)
        vertices.append([x,y,0])
        i += angle_increment
    vertices = make_border_smooth(vertices)
    return vertices

def make_border_smooth(vertices):
    new_vertices = []

    firstx = vertices[0][0]
    firsty = vertices[0][1]
    secondx = vertices[1][0]
    secondy = vertices[1][1]
    thirdx = vertices[2][0]
    thirdy = vertices[2][1]
    for j in map(lambda x: x/100.0, range(0,55,5)):
        x = (1.0 - j)**2*firstx + 2*(1.0 - j)*j*secondx + j**2*thirdx
        y = (1.0 - j)**2*firsty + 2*(1.0 - j)*j*secondy + j**2*thirdy
        new_vertices.append([x,y,0])

    for i in range(2, len(vertices) - 1):
        firstx = new_vertices[-1][0]
        firsty = new_vertices[-1][1]
        secondx = vertices[i][0]
        secondy = vertices[i][1]
        thirdx = vertices[i+1][0]
        thirdy = vertices[i+1][1]
        for j in map(lambda x: x/100.0, range(0,55,5)):
            x = (1.0 - j)**2*firstx + 2*(1.0 - j)*j*secondx + j**2*thirdx
            y = (1.0 - j)**2*firsty + 2*(1.0 - j)*j*secondy + j**2*thirdy
            new_vertices.append([x,y,0])

    new_vertices = new_vertices[10:]
    firstx = new_vertices[-1][0]
    firsty = new_vertices[-1][1]
    secondx = vertices[0][0]
    secondy = vertices[0][1]
    thirdx = new_vertices[0][0]
    thirdy = new_vertices[0][1]
    for j in map(lambda x: x/100.0, range(0,105,5)):
        x = (1.0 - j)**2*firstx + 2*(1.0 - j)*j*secondx + j**2*thirdx
        y = (1.0 - j)**2*firsty + 2*(1.0 - j)*j*secondy + j**2*thirdy
        new_vertices.append([x,y,0])

    return new_vertices

def get_tex_coords(vertices, extreme_points):
    global texCoord
    buf = []
    for vertex in vertices:
        buf.append((vertex[0] + abs(extreme_points[0]))/4)
        buf.append((vertex[1] + abs(extreme_points[1]))/4)
    texCoord.append(buf)

def get_extreme_points(vertices):
    min_x = 1024
    min_y = 1024
    for vertex in vertices:
        if vertex[0] < min_x:
            min_x = vertex[0]
        if vertex[1] < min_y:
            min_y = vertex[1]
    return [min_x, min_y]

def get_diff_areas(vertices):
    random.seed(random_state)
    buf_index_list = []
    parts = []
    besie_curves = []
    first_index = random.randint(10,30)
    second_index = random.randint(-30,-10)
    #print(first_index, second_index)
    first_point = vertices[first_index]
    second_point = vertices[second_index]
    midle_point = vertices[0]
    #print(vertices[0])
    parts.append(vertices[:first_index+1])
    #parts.append([])
    random.seed(random_state-5)
    new_index = random.randrange(0,105,5) / 100.0
    new_point = []
    firstx = first_point[0]
    firsty = first_point[1]
    secondx = midle_point[0]
    secondy = midle_point[1]
    thirdx = second_point[0]
    thirdy = second_point[1]
    #print(parts[0], '===============')
    besie_curves.append([])
    for j in map(lambda x: x/100.0, range(0,105,5)):
        x = (1.0 - j)**2*firstx + 2*(1.0 - j)*j*secondx + j**2*thirdx
        y = (1.0 - j)**2*firsty + 2*(1.0 - j)*j*secondy + j**2*thirdy
        if j == new_index:
            new_point = [x,y,0]
            buf_index_list.append(len(besie_curves[0]))
        besie_curves[0].append([x,y,0])
        parts[0].append([x,y,0])

    [parts[0].append(x) for x in vertices[second_index:]]
    
    last_updated_border_index_up = first_index
    last_updated_border_index_down = second_index
    
    i = 1
    while first_index - second_index < len(vertices) - 80:
        #print(first_index - second_index, second_index)
        texCoord.append([])
        first_index += random.randint(10,40)
        second_index += random.randint(-40,-10)
        first_point = vertices[first_index]
        second_point = vertices[second_index]
        midle_point = new_point
        # получили кусочек от прошлой линии + кусочек границы + кусочек от позапрошлой линии (если она есть)
        buf = []
        if i == 1:
            buf = vertices[second_index:last_updated_border_index_down]
            #print(besie_curves[i-1][buf_index_list[i-1]:][::-1])
            parts.append(buf + besie_curves[i-1][buf_index_list[i-1]:][::-1])
            last_updated_border_index_down = second_index
        elif i == 2:
            buf = vertices[last_updated_border_index_up:first_index]
            last_updated_border_index_up = first_index
            buf_past = besie_curves[i-2][:buf_index_list[i-2]]
            parts.append(buf[::-1] + buf_past + besie_curves[i-1][:buf_index_list[i-1]])
        elif i % 2 != 0:
            buf = vertices[second_index:last_updated_border_index_down]
            last_updated_border_index_down = second_index
            buf_past = besie_curves[i-2][buf_index_list[i-2]:][::-1]
            parts.append(buf + buf_past + besie_curves[i-1][buf_index_list[i-1]:])
        else:
            buf = vertices[last_updated_border_index_up:first_index]
            last_updated_border_index_up = first_index
            buf_past = besie_curves[i-2][buf_index_list[i-2]:][::-1]
            parts.append(buf[::-1] + buf_past + besie_curves[i-1][buf_index_list[i-1]:])

        random.seed(random_state)
        new_index = random.randrange(15,85,5) /100.0
        #new_point = []
        firstx = midle_point[0]
        firsty = midle_point[1]
        if i % 2 != 0:
            secondx = first_point[0]
            secondy = first_point[1]
            thirdx = second_point[0]
            thirdy = second_point[1]
        else:
            secondx = second_point[0]
            secondy = second_point[1]
            thirdx = first_point[0]
            thirdy = first_point[1]
        besie_curves.append([])
        for j in map(lambda x: x/100.0, range(0,105,5)):
            x = (1.0 - j)**2*firstx + 2*(1.0 - j)*j*secondx + j**2*thirdx
            y = (1.0 - j)**2*firsty + 2*(1.0 - j)*j*secondy + j**2*thirdy
            if j == new_index:
                new_point = [x,y,0]
                buf_index_list.append(len(besie_curves[i]))
            besie_curves[i].append([x,y,0])
            parts[i].append([x,y,0])
        
        i += 1

    #buf = vertices[first_index:last_updated_border_index_down]
    if i % 2 == 0:
        buf = vertices[first_index:second_index]
        parts.append(buf + besie_curves[i - 1][buf_index_list[i-1]:][::-1] + besie_curves[i-2])
        [parts[i].append(x) for x in vertices[last_updated_border_index_up:first_index]]
    else:
        buf = vertices[first_index:second_index][::-1]
        parts.append(buf + besie_curves[i - 1][::-1] + besie_curves[i - 2][buf_index_list[i-2]:])
        [parts[i].append(x) for x in vertices[second_index:last_updated_border_index_down][::-1]]
        #parts.append(buf + besie_curves[i - 1][buf_index_list[i-1]:][::-1] + besie_curves[i-2])
    return parts

def key_callback(window, key, scancode, action,
    mods):
    global deltaz, deltax, deltay,change1, anglex, angley, anglez
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            deltaz = -0.3  
        if key == 263: # glfw.KEY_LEFT
            deltaz = 0.3
        if key == 264:
            deltax = 0.3
        if key == 265:
            deltax = -0.3
        if key == 266:
            deltay = 0.3
        if key == 267:
            deltay = -0.3
        if key == 257:
            deltay = 0
            deltaz = 0
            deltax = 0
        if key == glfw.KEY_K:
            change1 *= -1

def scroll_callback(window, xoffset, yoffset):
    global size, change
    if (yoffset > 0):
        change *= 1.1
    else:
        change *= 0.9

def main():
    window = Window()
    window.setup_window()

main()
