import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
import pyrr

def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    """
        Compile and link shader modules to make a shader program.

        Parameters:

            vertex_filepath: path to the text file storing the vertex
                            source code
            
            fragment_filepath: path to the text file storing the
                                fragment source code
        
        Returns:

            A handle to the created shader program
    """

    with open(vertex_filepath,'r') as f:
        vertex_src = f.readlines()

    with open(fragment_filepath,'r') as f:
        fragment_src = f.readlines()
    
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    return shader

def loadMesh(filename: str) -> list[float]:
    """
        Load a mesh from an obj file.

        Parameters:

            filename: the filename.
        
        Returns:

            The loaded data, in a flattened format.
    """

    v = []
    vt = []
    vn = []

    vertices = []

    with open(filename, "r") as file:

        line = file.readline()

        while line:

            words = line.split(" ")
            match words[0]:
            
                case "v":
                    v.append(read_vertex_data(words))

                case "vt":
                    vt.append(read_texcoord_data(words))
                
                case "vn":
                    vn.append(read_normal_data(words))
            
                case "f":
                    read_face_data(words, v, vt, vn, vertices)
            
            line = file.readline()

    return vertices
    
def read_vertex_data(words: list[str]) -> list[float]:
    """
        Returns a vertex description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]
    
def read_texcoord_data(words: list[str]) -> list[float]:
    """
        Returns a texture coordinate description.
    """

    return [
        float(words[1]),
        float(words[2])
    ]
    
def read_normal_data(words: list[str]) -> list[float]:
    """
        Returns a normal vector description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]

def read_face_data(
    words: list[str], 
    v: list[list[float]], vt: list[list[float]], 
    vn: list[list[float]], vertices: list[float]) -> None:
    """
        Reads an edgetable and makes a face from it.
    """

    triangleCount = len(words) - 3

    for i in range(triangleCount):

        make_corner(words[1], v, vt, vn, vertices)
        make_corner(words[2 + i], v, vt, vn, vertices)
        make_corner(words[3 + i], v, vt, vn, vertices)
    
def make_corner(corner_description: str, 
    v: list[list[float]], vt: list[list[float]], 
    vn: list[list[float]], vertices: list[float]) -> None:
    """
        Composes a flattened description of a vertex.
    """

    v_vt_vn = corner_description.split("/")
    
    for element in v[int(v_vt_vn[0]) - 1]:
        vertices.append(element)
    for element in vt[int(v_vt_vn[1]) - 1]:
        vertices.append(element)
    for element in vn[int(v_vt_vn[2]) - 1]:
        vertices.append(element)

class Entity:
    """
        A basic object in the world, with a position and rotation.
    """


    def __init__(self, position: list[float], eulers: list[float]):
        """
            Initialize the entity.

            Parameters:

                position: the position of the entity.

                eulers: the rotation of the entity
                        about each axis.
        """

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
    
    def update(self) -> None:
        """
            Update the object, this is hard coded for now.
        """

        self.eulers[1] += 0.25
        
        if self.eulers[1] > 360:
            self.eulers[1] -= 360

    def get_model_transform(self) -> np.ndarray:
        """
            Returns the entity's model to world
            transformation matrix.
        """

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(self.eulers[1]), 
                dtype = np.float32
            )
        )

        return pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.position),dtype=np.float32
            )
        )

class App:
    """
        For now, the app will be handling everything.
        Later on we'll break it into subcomponents.
    """


    def __init__(self):

        self._set_up_pygame()

        self._set_up_timer()

        self._set_up_opengl()

        self._create_assets()

        self._set_onetime_uniforms()

        self._get_uniform_locations()
    
    def _set_up_pygame(self) -> None:
        """
            Initialize and configure pygame.
        """

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)

    def _set_up_timer(self) -> None:
        """
            Set up the app's timer.
        """

        self.clock = pg.time.Clock()
    
    def _set_up_opengl(self) -> None:
        """
            Configure any desired OpenGL options
        """

        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

    def _create_assets(self) -> None:
        """
            Create all of the assets needed for drawing.
        """

        self.cube = Entity(
            position = [0,-2,-28],
            eulers = [0,0,0]
        )
        self.cube_mesh = Mesh("models/house.obj")
        self.wood_texture = Material("gfx/1.png")
        self.shader = create_shader(
            vertex_filepath = "shaders/vertex.txt", 
            fragment_filepath = "shaders/fragment.txt")
    
    def _set_onetime_uniforms(self) -> None:
        """
            Some shader data only needs to be set once.
        """

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 30, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader,"projection"),
            1, GL_FALSE, projection_transform
        )
    
    def _get_uniform_locations(self) -> None:
        """
            Query and store the locations of shader uniforms
        """

        glUseProgram(self.shader)
        self.modelMatrixLocation = glGetUniformLocation(self.shader,"model")
    
    def run(self) -> None:
        """ Run the app """

        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            
            self.cube.update()
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            glUniformMatrix4fv(
                self.modelMatrixLocation,1,GL_FALSE,
                self.cube.get_model_transform())
            self.wood_texture.use()
            self.cube_mesh.arm_for_drawing()
            self.cube_mesh.draw()

            pg.display.flip()

            #timing
            self.clock.tick(60)

    def quit(self) -> None:
        """ cleanup the app, run exit code """

        self.cube_mesh.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Mesh:
    """
        A mesh that can represent an obj model.
    """

    def __init__(self, filename: str):
        """
            Initialize the mesh.
        """

        # x, y, z, s, t, nx, ny, nz
        vertices = loadMesh(filename)
        self.vertex_count = len(vertices)//8
        vertices = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        #Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    
    def arm_for_drawing(self) -> None:
        """
            Arm the triangle for drawing.
        """
        glBindVertexArray(self.vao)
    
    def draw(self) -> None:
        """
            Draw the triangle.
        """

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self) -> None:
        """
            Free any allocated memory.
        """
        
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))
    
    def destroy(self) -> None:
        """
            Free any allocated memory.
        """
        
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))

class Material:
    """
        A basic texture.
    """

    
    def __init__(self, filepath: str):
        """
            Initialize and load the texture.

            Parameters:

                filepath: path to the image file.
        """

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert()
        image_width,image_height = image.get_rect().size
        img_data = pg.image.tostring(image,'RGBA')
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self) -> None:
        """
            Arm the texture for drawing.
        """

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)

    def destroy(self) -> None:
        """
            Free the texture.
        """

        glDeleteTextures(1, (self.texture,))

my_app = App()
my_app.run()
my_app.quit()