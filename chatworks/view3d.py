import sys
import os
import pyglet
from pyglet.gl import *

# Set the X11 backend for Pyglet on Xubuntu
pyglet.options['shadow_window'] = False
pyglet.options['x11_mouse_cursor'] = True
pyglet.options['vsync'] = False
pyglet.options['debug_gl'] = False
pyglet.options['audio'] = ('alsa', 'openal', 'silent')

# Initialize the window
window = pyglet.window.Window(width=800, height=600, resizable=True)

# Set up OpenGL
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# Load the GLTF/GLB file
if len(sys.argv) < 2:
    print("Please specify a GLTF/GLB file to load.")
    sys.exit()

file_path = sys.argv[1]
if not os.path.isfile(file_path):
    print("File not found: " + file_path)
    sys.exit()

model = pyglet.resource.image(file_path).texture
model_width = model.width
model_height = model.height

# Set up the camera
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60.0, float(model_width) / float(model_height), 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

@window.event
def on_draw():
    # Clear the window
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the model
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, model.id)
    glBegin(GL_TRIANGLES)
    for vertex in model.vertices:
        glTexCoord2f(vertex.tex_coord[0], vertex.tex_coord[1])
        glNormal3f(vertex.normal[0], vertex.normal[1], vertex.normal[2])
        glVertex3f(vertex.position[0], vertex.position[1], vertex.position[2])
    glEnd()
    glDisable(GL_TEXTURE_2D)

pyglet.app.run()