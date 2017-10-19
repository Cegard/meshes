from mesh import Mesh

mesh = None


def create_mesh():
    mesh = Mesh()
    
    return mesh


def setup():
    global mesh
    
    mesh = create_mesh()
    size(600, 600, P3D)
    frameRate(1000)


def draw():
    global mesh
    
    stroke(color(255, 255, 255))
    background(0)
    smooth()
    rendering_mode = "retained" if mesh.retained else "immediate"
    text("Mesh mode: " + str(mesh.mode) + ". Rendering mode: " + \
         str(rendering_mode) + ". FPS: " + str(frameRate), 10, 10)
    lights()
    #draw the mesh at the canvas center
    #while performing a little animation
    translate(width/2, height/2, 0)
    rotateX(frameCount*radians(90) / 50)
    rotateY(frameCount*radians(90) / 50)
    mesh.draw()


def keyPressed():
  
    if key == ' ':
        mesh.mode = mesh.mode+1 if mesh.mode < 3 else 0
    
    if key == 'r':
        mesh.retained = not mesh.retained
    
    if key == 'b':
        mesh.bounding_sphere = not mesh.bounding_sphere
    