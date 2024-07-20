import numpy as np

class VectorOperations:
    def __init__(self) -> None:
        pass
    
    def reflected(vector, axis):
        return vector - 2 * np.dot(vector, axis) * axis

    def normalize(vector):
        return vector / np.linalg.norm(vector)