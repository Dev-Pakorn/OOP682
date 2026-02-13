#Open-Closed Principle - Bad Idea

# Bad Idea
class Circle:
    def __init__(self, radius):
        self.radius = radius


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height



def calculate_area(shape):
    if isinstance(shape, Circle):
        return 3.14 * shape.radius * shape.radius
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    else:
        raise TypeError("Unknown shape")