class Mesh:

  
    def __init__(self, radius = 150):
        self.radius = radius
        self.top_pent = [] # [PVector() for _ in range(5)]
        self.bottom_pent = [] # [PVector() for _ in range(5)]
        self.vertices = {}
        self.faces = {}
        self.retained = False
        self.bounding_sphere = False
        self.mode = 0
        self.figure = createShape()
        self.figure.disableStyle()
        self.make_vertices()
        self.build()
    
    
    def make_vertices(self):
        self.figure.beginShape()
        angle = 0
        c = dist(cos(0) * self.radius,
                 sin(0) * self.radius,
                 cos(radians(72)) * self.radius,
                 sin(radians(72)) * self.radius)
        b = self.radius
        a = sqrt((c**2) - (b**2))
        self.triHeight = sqrt((c**2) - (c / 2)**2)
        self.top_point = PVector(0, 0, self.triHeight / 2.0 + a)
        self.figure.vertex(self.top_point.x, self.top_point.y, self.top_point.z)
        self.vertices[self.top_point] = []
        
        for i in range(5):
            v_point = PVector(cos(angle) * self.radius,
                              sin(angle) * self.radius,
                              self.triHeight / 2.0)
            self.top_pent.append(v_point)
            self.figure.vertex(v_point.x, v_point.y, v_point.z)
            self.vertices[v_point] = []
            angle += radians(72)
        
        angle = 72.0 / 2.0
        
        for i in range(5):
            v_point = PVector(cos(angle) * self.radius,
                              sin(angle) * self.radius,
                              -self.triHeight / 2.0)
            self.bottom_pent.append(v_point)
            self.figure.vertex(v_point.x, v_point.y, v_point.z)
            self.vertices[v_point] = []
            angle += radians(72)
        
        self.bottom_point = PVector(0, 0, -(self.triHeight / 2.0 + a))
        self.figure.vertex(self.bottom_point.x, self.bottom_point.y, self.bottom_point.z)
        self.vertices[self.bottom_point] = []
        self.figure.endShape()
    
    
    def make_face(self, vertex_1, vertex_2, vertex_3):
        face = createShape()
        face.beginShape(TRIANGLE)
        face.vertex(vertex_1.x, vertex_1.y, vertex_1.z)
        face.vertex(vertex_2.x, vertex_2.y, vertex_2.z)
        face.vertex(vertex_3.x, vertex_3.y, vertex_3.z)
        face.endShape(CLOSE)
        self.faces[face] = [vertex_1, vertex_2, vertex_3]
        self.vertices[vertex_1] = self.vertices[vertex_1] + [face]
        self.vertices[vertex_2] = self.vertices[vertex_2] + [face]
        self.vertices[vertex_3] = self.vertices[vertex_3] + [face]
        
        return face
            
            
    def build(self):
        
        for i in xrange(4, -1, -1):
            self.make_face(self.bottom_point, self.bottom_pent[i], self.bottom_pent[i-1])
            self.make_face(self.top_point, self.top_pent[i], self.top_pent[i-1])
        
        ####### sorry :_(  ######## 
        self.make_face(self.top_pent[0], self.bottom_pent[2], self.top_pent[1])
        self.make_face(self.bottom_pent[0], self.top_pent[4], self.bottom_pent[1])
        
        self.make_face(self.top_pent[1], self.bottom_pent[3], self.top_pent[2])
        self.make_face(self.bottom_pent[1], self.top_pent[0], self.bottom_pent[2])
        
        self.make_face(self.top_pent[2], self.bottom_pent[4], self.top_pent[3])
        self.make_face(self.bottom_pent[2], self.top_pent[1], self.bottom_pent[3])
        
        self.make_face(self.top_pent[3], self.bottom_pent[0], self.top_pent[4])
        self.make_face(self.bottom_pent[3], self.top_pent[2], self.bottom_pent[4])
        
        self.make_face(self.top_pent[4], self.bottom_pent[1], self.top_pent[0])
        self.make_face(self.bottom_pent[4], self.top_pent[3], self.bottom_pent[0])
        #######################################
    
    
    def draw_immediate(self):
        
        for face in self.faces: 
            beginShape(TRIANGLE)
            
            for figure_vertex in self.faces[face]:
                vertex(figure_vertex.x, figure_vertex.y, figure_vertex.z)
            
            endShape()
    
    
    def draw(self):
        pushMatrix()
        
        # mesh visual attributes
        stroke_weight = 3
        middle_color = 0 if self.retained else 255
        line_color = color(255, middle_color, 0)
        face_color = color(0, middle_color, 255, 100)
        
        strokeWeight(stroke_weight)
        stroke(line_color)
        fill(face_color)
        
        if self.mode == 1:
            noFill()
        
        elif self.mode == 2:
            noStroke()
        
        elif self.mode == 3:
            line_color = color(0, 0, 0)
            stroke_weight = 1
            strokeWeight(stroke_weight)
            stroke(line_color)
        
        #rendering modes
        if self.retained:
            #shape(self.figure)
            for face in self.faces:
                shape(face)
        
        else:
            self.draw_immediate()
        
        popMatrix()
    
        # visual hint
        if self.bounding_sphere:
            pushMatrix()
            noStroke()
            fill(0, 255, 255, 125)
            sphere(self.radius)
            popMatrix()