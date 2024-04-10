
from Base3DObjects import *
import random

class Particle:
    def __init__(self, position, motion) -> None:
        self.pos = position
        self.dir = motion
        self.time_lived = 0


class ParticleEffect:
    def __init__(self, position, texture, opacity, rate = 10, time_to_live = 2.0, fade_time = 0.5) -> None:
        self.texture = texture
        self.position = position
        self.sprite = Sprite()
        self.particles = []
        self.time_since_particle = 0.0
        self.rate = rate
        self.ttl = time_to_live
        self.opacity = opacity
        self.fade_time = fade_time

    def update(self, delta_time):
        particles_to_kill = []
        for particle in self.particles:
            particle.time_lived += delta_time
            if particle.time_lived > self.ttl:
                particles_to_kill.append(particle)
            particle.pos += particle.dir * delta_time

        for particle in particles_to_kill:
            self.particles.remove(particle)

        self.time_since_particle += delta_time
        time_per_particle = 1.0 / self.rate
        while self.time_since_particle > time_per_particle:
                self.time_since_particle -= time_per_particle # emission area rnadom * 0.2
                self.particles.append(Particle(Point(random.random() * 0.2, random.random()* 0.2, random.random()* 0.2),
                                       Vector(random.random() - 0.5, random.random() + 1.0, random.random() - 0.5) * 0.1))

    def draw(self, sprite_shader, model_matrix):
        glDisable(GL_DEPTH_TEST)


        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)    

        # glActiveTexture(GL_TEXTURE3)
        # glBindTexture(GL_TEXTURE_2D, self.texture)
        sprite_shader.set_diffuse_texture(3)
        sprite_shader.set_alpha_texture(None)

        model_matrix.push_matrix()
        model_matrix.add_translation(self.position.x, self.position.y, self.position.z)
        model_matrix.add_scale(8,8,8)
        # self.model_matrix.add_rotation_x(pi / 2.0)


        for particle in self.particles:
            if particle.time_lived < self.fade_time:
                opacity = (particle.time_lived / self.fade_time) * self.opacity
            elif particle.time_lived > (self.ttl - self.fade_time):
                opacity = ((1.0 - (particle.time_lived - (self.ttl - self.fade_time)) 
                            / self.fade_time) * self.opacity)
            else:
                opacity = self.opacity

            sprite_shader.set_opacity(opacity)
            model_matrix.push_matrix()
            model_matrix.add_translation(particle.pos.x, particle.pos.y, particle.pos.z)
            model_matrix.add_scale(0.6, 0.6, 1.0)
            sprite_shader.set_model_matrix(model_matrix.matrix)
            self.sprite.draw(sprite_shader)
            model_matrix.pop_matrix()    
       
        model_matrix.pop_matrix()
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)