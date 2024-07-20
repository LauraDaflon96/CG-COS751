import numpy as np
import matplotlib.pyplot as plt
from ray_tracying import Ray
from vector_operations import VectorOperations
from dotenv import load_dotenv, dotenv_values
import os
import random

vals = dotenv_values("/Users/lauradaflon/Documents/Faculdade/2024.1/Raytracing/local.env")

num_spheres = int(vals['NUM_SPHERES'])

width = int(vals['HEIGHT'])
height = int(vals['WIDTH'])


objects: list = [
    { 'type': 'sphere', 
     'center': np.array([0, -9000, 0]), 
     'radius': 9000 - 0.7, 
     'ambient': np.array([0.1, 0.1, 0.1]), 
     'diffuse': np.array([0.6, 0.6, 0.6]), 
     'specular': np.array([1, 1, 1]), 
     'shininess': 100, 
     'reflection': 0.5 }
]

for sphere in range(0,num_spheres):
    objects.append(    
        {'type': 'sphere', 
         'center': np.array([random.uniform(-0.3,0.3), random.uniform(-0.5,1.0), random.uniform(-1,0.0)]), 
         'radius': random.uniform(0.0, 0.5), 
         'ambient': np.array([random.uniform(0.0, 0.1), random.uniform(0.0, 0.1), random.uniform(0.0, 0.1)]), 
         'diffuse': np.array([random.uniform(0.0, 0.9), random.uniform(0.0, 0.9), random.uniform(0.0, 0.9)]), 
         'specular': np.array([1, 1, 1]), 
         'shininess': 100, 
         'reflection': 0.5 },
    )

# Camera position 
camera = np.array([0, 0, 1])

# Proportion of the image
ratio = float(width)/height

# Screen is defined by 2 points.
screen = (-1, 1/ratio, 1, -1/ratio)

image = np.zeros((height, width, 3))

max_depth = 3

light = { 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }


# We can see the image as a matrix of pixels so we look pixel by pixel
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        pixel = np.array([x, y, 0])
        ray = Ray(origin=camera, pixel=pixel)
        
        col = ray.colorize(np.array([0.2, 0.1, 0.7]))
        
        image[i][j] = col
        
        color = np.zeros((3))
        reflection = 1

        ray.nearest_intersected_object(objects)
        
        if ray.nearest_object is None:
            continue
        
        illumination = ray.illuminate(objects, light, camera)
        
        if np.any(illumination == None):
            image[i, j] = np.clip(0, 0, 0)
            continue
        
        color += reflection * illumination
        
        reflection = ray.reflection(illumination=illumination, reflection=reflection)

        image[i, j] = np.clip(color, 0, 1)
        
plt.imsave('image.png', image)
