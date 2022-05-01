from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=10)
scene.set_floor(-1, (1.0, 1.0, 1.0))
scene.set_directional_light((.2, .2, 1), 0.0, (.1, .1, .1))
scene.set_background_color((0.5, 0.5, 0.4))

@ti.func
def draw_pipe(loc_x):
    green = vec3(0.44, 0.756, 0.172)
    deep_green = vec3(0.40, 0.6, 0.16)
    y = int(ti.random() * 60) - 50
    for i, j, k in ti.ndrange((loc_x, loc_x + 10), (y + 35, 64), 6):
        scene.set_voxel(vec3(i,j,k), 1, green)
    for i, j, k in ti.ndrange((loc_x-1, loc_x + 11), (y + 30, y+35), 6):
        scene.set_voxel(vec3(i,j,k), 1, deep_green + vec3(0.1) * ti.random())    
    for i, j, k in ti.ndrange((loc_x, loc_x + 10), (-63, y-5), 6):
        scene.set_voxel(vec3(i,j,k), 1, green)
    for i, j, k in ti.ndrange((loc_x-1, loc_x + 11), (y - 5, y), 6):
        scene.set_voxel(vec3(i,j,k), 1, deep_green + vec3(0.1) * ti.random())   

@ti.func
def draw_bird(loc):
    yellow = vec3(0.839, 0.753, 0.153)
    orange = vec3(0.882, 0.51, 0.11)
    white = vec3(1, 1, 1)
    for i, j, k in ti.ndrange((loc.x, loc.x + 7), (loc.y, loc.y + 7), (loc.z, loc.z + 7)):
        scene.set_voxel(vec3(i,j,k), 1, yellow)
    for i, j, k in ti.ndrange((loc.x-1, loc.x+3), (loc.y+3, loc.y+4), (loc.z+7, loc.z+9)):
        scene.set_voxel(vec3(i,j,k), 1, white) # bird wing
    for i, j, k in ti.ndrange((loc.x-1, loc.x+3), (loc.y+3, loc.y+4), (loc.z-2, loc.z)):
        scene.set_voxel(vec3(i,j,k), 1, white)    
    for i, j, k in ti.ndrange((loc.x+7, loc.x+10), (loc.y + 4, loc.y + 7), (loc.z, loc.z + 7)):
        scene.set_voxel(vec3(i,j,k), 1, white)
    scene.set_voxel(vec3(loc.x+8, loc.y+5, loc.z+6), 1, vec3(0, 0, 0))
    for i, j, k in ti.ndrange((loc.x+7, loc.x+11), (loc.y, loc.y + 4), (loc.z, loc.z + 7)):
        scene.set_voxel(vec3(i,j,k), 1, orange)

@ti.func
def draw_background():
    for i, j in ti.ndrange((-64, 64), (-64, 64)):
        scene.set_voxel(vec3(i,j,-30), 1, vec3(0.447, 0.772, 0.827))

@ti.func
def draw_cloud(pos, radius, color):
    for I in ti.grouped(
            ti.ndrange((-radius, radius), (-3, 3),
                       (-radius, +radius))):
        f = I / radius
        d = vec2(f[0], f[2]).norm()
        prob = max(0, 1 - d)**2
        if ti.random() < prob:
            scene.set_voxel(pos + I, 1, color + (ti.random() - 0.5) * 0.2)


@ti.kernel
def initialize_voxels():
    draw_background()
    draw_pipe(-40)
    draw_pipe(-10)
    draw_pipe(20)
    draw_pipe(50)

    draw_bird(vec3(-55, 0, 0))

    draw_cloud(vec3(-50, -48, -20), 5, vec3(1))
    draw_cloud(vec3(-40, -51, -20), 10, vec3(1))
    draw_cloud(vec3(-30, -51, -20), 6, vec3(1))
    draw_cloud(vec3(-20, -46, 30), 10, vec3(1))
    draw_cloud(vec3(10, -50, -20), 7, vec3(1))
    draw_cloud(vec3(20, -50, 30), 9, vec3(1))
    draw_cloud(vec3(30, -50, -20), 7, vec3(1))
    draw_cloud(vec3(40, -50, -20), 9, vec3(1))

initialize_voxels()

scene.finish()
