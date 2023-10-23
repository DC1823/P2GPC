import pygame
from pygame.locals import *
from figu import *
from luces import *
from RayTracer import RayTracer
from mats import *
import random

Width = 550
Height = 550
pygame.init()
pantalla = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
pantalla.set_alpha(None)
rayTracer = RayTracer(pantalla)
rayTracer.emap = pygame.image.load("Texturas/espa.bmp")
estrella = Material(txtu=pygame.image.load("Texturas/esta.jpg"))
satu= Material(txtu=pygame.image.load("Texturas/satu.jpg"))
sol= Material(txtu=pygame.image.load("Texturas/sol.jpg"))
metal= Material(txtu=pygame.image.load("Texturas/metal.jpg"))
for i in range(100):
    x = random.randint(-13,13)
    y = random.randint(-13,13)
    z = -25
    rayTracer.escena.append(Sphere(pos=(x,y,z),radi=0.1,mat=estrella))
rayTracer.escena.append(Sphere(pos=(-5,5,-15),radi=3,mat=sol))
rayTracer.escena.append(Sphere(pos=(0,-11,-25),radi=2.5,mat=satu))
rayTracer.escena.append(Disk(pos=(0,-11,-25),norm=(0,1,0),mat=estrella,radi=4))
rayTracer.escena.append(Sphere(pos=(10,5,-25),radi=3.5,mat=mirror()))
rayTracer.escena.append(Sphere(pos=(10,12,-25),radi=3,mat=blackhole()))
rayTracer.escena.append(Disk(pos=(10,12,-25),norm=(0,1,0),mat=bhhalo(),radi=4))
rayTracer.escena.append(AABB(pos=(-13,0,-25),tama=(2,3,3),mat=satelite()))
rayTracer.escena.append(AABB(pos=(-9,0,-25),tama=(2,3,3),mat=satelite()))
rayTracer.escena.append(Sphere(pos=(-11,0,-24),radi=1,mat=metal))
rayTracer.luces.append(AmbientLight(intens=1))
rayTracer.luces.append(DirectionalLight(dir=(1,1,1),intens=3,col=(1,1,1)))
rayTracer.luces.append(PointLight(puntop=(5,-5,-15), intens=6,col=(1,1,0)))
rayTracer.luces.append(PointLight(puntop=(10,12,-25), intens=-5,col=(1,1,0)))

corriendo = True
rayTracer.rayclear()
rayTracer.raytRend()

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                corriendo = False
    pygame.display.flip()
pan = pygame.Rect(0, 0, Width, Height)
sb = pantalla.subsurface(pan)
pygame.image.save(sb, "output.png")
pygame.quit()