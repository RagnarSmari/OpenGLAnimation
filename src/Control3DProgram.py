
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *
from Particles import *
from bezier import *
from Base3DObjects import *

import ojb_3D_loading

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_caption('Sein skil :("')

        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.sprite_shader = SpriteShader()
        self.sprite_shader.use()
    
        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(120.0, 13.0, 94.0), Point(10, 20, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 50)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800/600, 0.1, 300)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        
        self.cube = Cube()
        self.sphere = OptimizedSphere(128, 256)
        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "smooth_sphere.obj")
        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "stytta.obj")
        # self.statue_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "untitled.obj")
        self.ground_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "ground.obj")
        self.scene_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "mountain_range.obj")
        self.boat_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "boat.obj")
        self.dock_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "dock.obj")
        self.log_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "logs.obj")
        self.statue_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models", "stytta.obj")
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.sprite = Sprite()
        self.sky_sphere = SkySphere(128, 256)


        self.fr_ticker = 0
        self.fr_sum = 0

        self.boat_location = Point(63.0, 8, 113.0)
        self.bezier_points = [
        [Point(120.0, 13.0, 94.0),Point(85, 20.0, 105.0),Point(75, 20.0, 110.0),Point(63.0, 13.0, 113.0)],
        [Point(63.0, 13.0, 113.0),Point(63.0, 13.0, 130.0),Point(63.0, 13.0, 160.0),Point(63.0, 13.0, 180.0)],
        [Point(63.0, 13.0, 180.0),Point(0.0, 20.0, 160.0),Point(-30.0, 20.0, 130.0),Point(42.0, 22.0, 120.0)],  
        ]
        self.bezier = Bezier()
        self.startTime = time.time()

        ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.UP_key_down = False
        self.W_key_down = False 
        self.S_key_down = False 
        self.A_key_down = False 
        self.D_key_down = False
        self.SPACE_key_down = False
        self.CTRL_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.DOWN_key_down = False

        self.white_background = False

        ### TEXTURES ###
        self.texture_id_sky_sphere = self.load_texture(sys.path[0] + "/textures/sky_sphere_01.jpg")
        # self.texture_id_statue     = self.load_texture(sys.path[0] + "/textures/stytta.jpg")
        self.texture_id_ground     = self.load_texture(sys.path[0] + "/textures/ground.jpg")
        self.texture_id_water       = self.load_texture(sys.path[0] + "/textures/water.jpg")        
        
        ## PARTICLES
        self.texture_id_fire_particle = self.load_texture(sys.path[0] + "/textures/fire_particle.png")
        self.particle_effect = ParticleEffect(Point(98.0, 18.0, 60.0), self.texture_id_fire_particle, 1.0, rate=100)
        self.bind_textures()

        # STarting pos
        self.view_matrix.yaw(-pi/2)

        self.counter = 0

        # self.bezier_points = [
        #     [Point(2, 3, 6),
        #     Point(0, 3.0, 1 - 1.0),
        #     Point(0 + 1, 1.0, 1),
        #     Point(0, 3.0, 1 + 1.0)]]

    def load_texture(self, path_string):
        # Texturing
        surface = pygame.image.load(path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id
    
    def bind_textures(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id_sky_sphere)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id_ground)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.texture_id_water)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.texture_id_fire_particle)



    def getCurrentTime(self):
        '''Get Current time'''
        return time.time() - self.startTime


    
    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            # print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0
        if self.getCurrentTime() > 5:
            self.boat_location.z += 5*delta_time
        
        if round(self.getCurrentTime()) == 5:
            self.view_matrix.yaw((pi / 10) * delta_time)
            self.counter += 1

        if round(self.getCurrentTime()) >= 18 and round(self.getCurrentTime()) < 24:
            self.view_matrix.yaw((pi / 18) * delta_time)
        
        if round(self.getCurrentTime()) >= 24 and round(self.getCurrentTime()) < 26:
            self.view_matrix.yaw((-pi / 18) * delta_time)
        
        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)
        # print(self.getCurrentTime())
        self.particle_effect.update(delta_time)
        # print(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        if self.W_key_down:
            self.view_matrix.slide(0, 0, -50 * delta_time)
        if self.S_key_down:
            self.view_matrix.slide(0, 0, 50 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-50 * delta_time, 0, 0)
        if self.D_key_down:
            self.view_matrix.slide(50 * delta_time, 0, 0)
        if self.SPACE_key_down:
            self.view_matrix.slide(0, 50 * delta_time, 0)
        if self.CTRL_key_down:
            self.view_matrix.slide(0, -50 * delta_time, 0)
        
        
        if self.LEFT_key_down:
            self.view_matrix.yaw(pi * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.yaw(-pi * delta_time)

        if self. DOWN_key_down: # TODO
            self.fov += 0.25 * delta_time

        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False
    


    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)
        
        self.model_matrix.load_identity()
         
        glDisable(GL_DEPTH_TEST)

        self.sprite_shader.use() # Switch to the spride shader
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())


        ### SKY SPHERE ###

        glActiveTexture(GL_TEXTURE0)
        self.sprite_shader.set_diffuse_texture(0)
        self.sprite_shader.set_alpha_texture(None)
        self.sprite_shader.set_opacity(1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x,
                                          self.view_matrix.eye.y, 
                                          self.view_matrix.eye.z)
        self.sprite_shader.set_model_matrix(self.model_matrix.matrix) 
        self.sky_sphere.draw(self.sprite_shader)
        self.model_matrix.pop_matrix()       
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
       
        ### END ###





        self.shader.use() # Switching shader
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.1, 300)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        box_pos = self.bezier.get_bezier_position(self.getCurrentTime(), self.bezier_points[0], 0.0, 5.0)
        if self.getCurrentTime() > 5:
            box_pos = self.bezier.get_bezier_position(self.getCurrentTime(), self.bezier_points[1], 5.0, 18.0)
        if self.getCurrentTime() > 18:
            box_pos = self.bezier.get_bezier_position(self.getCurrentTime(), self.bezier_points[2], 18.0, 28.0)
        self.view_matrix.eye = Point(box_pos.x, box_pos.y, box_pos.z)
        # self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(10 * cos(self.angle), 0.0, 10 *sin(self.angle)))
        self.shader.set_light_position(Point(10.0, 100.0, 10.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(1)

        ### Mountain Range ###
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.0, 1.0, 0.0)
        self.model_matrix.add_scale(80, 80, 80)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.scene_model.draw(self.shader)
        self.model_matrix.pop_matrix()


        # Switch Shader
        # self.sprite_shader.use()
        # self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        # self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())
        self.sprite_shader.use() # Switching shader
        # self.sprite_shader.set_perspective(self.fov, 800 / 600, 0.1, 100)
        # self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        # self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())


        self.sprite_shader.use() # Switch to the spride shader
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())
        ### Water ###
        # glActiveTexture(GL_TEXTURE2)
        self.sprite_shader.set_diffuse_texture(2)
        self.sprite_shader.set_alpha_texture(None)
        self.sprite_shader.set_opacity(1.0)

        for x in range(4):
            for i in range(4):
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(-70.0 + i*(50), 10, 100 + x*(50))
                self.model_matrix.add_scale(50, 50, 50)
                # self.model_matrix.add_scale(2, 2, 2)
                self.model_matrix.add_rotation_x(pi/2)
                self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
                self.sprite.draw(self.sprite_shader)
                self.model_matrix.pop_matrix()

        # self.particle_effect.draw(self.sprite_shader, self.model_matrix.matrix)

        self.shader.use() # Switching shader
        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.1, 300)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        # box_pos = self.bezier.get_bezier_position(self.getCurrentTime(), self.bezier_points[0], 0.0, 10.0)
        # self.view_matrix.eye = Point(box_pos.x, box_pos.y, box_pos.z)
        # self.shader.set_light_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(10 * cos(self.angle), 0.0, 10 *sin(self.angle)))
        self.shader.set_light_position(Point(10.0, 100.0, 10.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(25)

        ### BOAT ###
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.boat_location.x, self.boat_location.y, self.boat_location.z)
        self.model_matrix.add_scale(2, 2, 2)
        self.model_matrix.add_rotation_y(pi)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.boat_model.draw(self.shader)
        self.model_matrix.pop_matrix()


        ### DOCK ###
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(100.0, 5.0, 60.0)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.dock_model.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        


        ### LOGS ###
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(100.0, 15.0, 60.0)
        self.model_matrix.add_scale(0.05, 0.05, 0.05)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.log_model.draw(self.shader)
        self.model_matrix.pop_matrix()


        ### STATUES ###
        # self.boat_location = Point(63.0, 8, 113.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(15.0 , -8.0, 143.0)
        self.model_matrix.add_scale(5, 5, 5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.statue_model.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-29.0, -8.0, 143.0)
        self.model_matrix.add_scale(5, 5, 5)    
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.statue_model.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.sprite_shader.use() # Switch to the spride shader
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())
        # Drawing particle effect fire
        self.particle_effect.draw(self.sprite_shader, self.model_matrix)




        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_UP:
                        self.UP_key_down = True
                    # W A S D keys movement
                    if event.key == K_w:
                        self.W_key_down = True
                    if event.key == K_s:
                        self.S_key_down = True
                    if event.key == K_a:
                        self.A_key_down = True
                    if event.key == K_d:
                        self.D_key_down = True
                    if event.key == K_SPACE:
                        self.SPACE_key_down = True
                    if event.key == K_LCTRL or event.key == K_RCTRL:
                        self.CTRL_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_DOWN:
                        self.DOWN_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_w:
                        self.W_key_down = False
                    if event.key == K_s:
                        self.S_key_down = False
                    if event.key == K_a:
                        self.A_key_down = False
                    if event.key == K_d:
                        self.D_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_SPACE:
                        self.SPACE_key_down = False
                    if event.key == K_LCTRL or event.key == K_RCTRL:
                        self.CTRL_key_down = False
                    if event.key == K_DOWN:
                        self.DOWN_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()