import numpy as np
from vector_operations import VectorOperations 

class Ray:
    def __init__(self, origin, pixel) -> None:
        self.pixel = pixel
        self.origin = origin
        self.direction = VectorOperations.normalize(pixel - origin)
        self.min_distance = None
        self.nearest_object = None
        self.shifted_point = None
        self.intersection = None
        
    def reflection(self, illumination, reflection):
        reflection *= self.nearest_object['reflection']
        normal_to_surface = VectorOperations.normalize(self.intersection - self.nearest_object['center'])

        self.origin = self.shifted_point
        self.direction = VectorOperations.reflected(self.direction, normal_to_surface)
        
        return reflection
        
        
        
    def illuminate(self, objects, light, camera):
        self.intersection = self.origin + self.min_distance * self.direction
        normal_to_surface = VectorOperations.normalize(self.intersection - self.nearest_object['center'])
        self.shifted_point = self.intersection + 1e-5 * normal_to_surface
        intersection_to_light = VectorOperations.normalize(light['position'] - self.shifted_point)      
        
        self.nearest_intersected_object_light(objects, intersection_to_light)

        intersection_to_light_distance = np.linalg.norm(light['position'] - self.intersection)
        is_shadowed = self.min_distance < intersection_to_light_distance

        if is_shadowed:
            return np.array([None, None, None])
        
        illumination = np.zeros((3))

        illumination += self.nearest_object['ambient'] * light['ambient']

        illumination += self.nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

        intersection_to_camera = VectorOperations.normalize(camera - self.intersection)
        H = VectorOperations.normalize(intersection_to_light + intersection_to_camera)
        illumination += self.nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (self.nearest_object['shininess'] / 4)
        
        return illumination

        
    def intersect_sphere(self, center, radius):
        b = 2 * np.dot(self.direction, self.origin - center)
        c = np.linalg.norm(self.origin - center) ** 2 - radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None
    
    def nearest_intersected_object(self, objects: list):
        distances: list = []
        for obj in objects:
            print(obj['type'])
            match obj['type']:
                case 'sphere':
                    distances.append(self.intersect_sphere(obj['center'], obj['radius']))
                
                case _:
                    print("This object is not registered")
                
        self.nearest_object = None
        min_distance = np.inf
        for index, distance in enumerate(distances):
            if distance and distance < min_distance:
                min_distance = distance
                self.nearest_object = objects[index]
        
        self.min_distance = min_distance
        
    def intersect_sphere_light (self, center, radius, inter_light):
        b = 2 * np.dot(inter_light, self.shifted_point - center)
        c = np.linalg.norm(self.shifted_point - center) ** 2 - radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None
        
    def nearest_intersected_object_light(self, objects: list, inter_light):
        distances = [self.intersect_sphere_light(obj['center'], obj['radius'], inter_light) for obj in objects]
                
        min_distance = np.inf
        for index, distance in enumerate(distances):
            if distance and distance < min_distance:
                min_distance = distance
                        
        self.min_distance = min_distance
    
    def nearest_intersected_object(self, objects: list):
        distances: list = []
        for obj in objects:
            match obj['type']:
                case 'sphere':
                    distances.append(self.intersect_sphere(obj['center'], obj['radius']))
                
                case _:
                    print("This object is not registered")
                
        self.nearest_object = None
        min_distance = np.inf
        for index, distance in enumerate(distances):
            if distance and distance < min_distance:
                min_distance = distance
                self.nearest_object = objects[index]
        
        self.min_distance = min_distance
    
    def colorize(self, wanted_color: np.array):
        
        unit_direction = VectorOperations.normalize(self.direction)
        
        t = 0.5*(unit_direction[1] + 1.0)
        return np.array([1.0, 1.0, 1.0])*(1.0-t) + wanted_color*t

        