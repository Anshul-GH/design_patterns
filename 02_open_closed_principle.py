from enum import Enum
from typing import SupportsIndex

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Product:
    def __init__(self, name, color, size) -> None:
        self.name = name
        self.color = color
        self.size = size

# voilation of the Open Closed Principle
# if we want to add new functionality, 
# we have to add it via extension
# open for extension but closed for
# modification
class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p

    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p

    def filter_by_size_and_color(self, products, size, color):
        for p in products:
            if p.size == size and p.color == color:
                yield p

# correct approach

#############################
# base classes:
class Specification:
    def is_satisfied(self, item):
        pass

class Filter:
    def filter(self, items, spec):
        pass

#############################
# derived classes
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size

class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args
        ))

class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item

#############################
if __name__ == "__main__":
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    pear = Product('Pear', Color.GREEN, Size.MEDIUM)
    jackfruit = Product('Jackfruit', Color.BLUE, Size.LARGE)
    tree = Product('Tree', Color.BLUE, Size.MEDIUM)
    house = Product('House', Color.RED, Size.LARGE)
    car = Product('Car', Color.RED, Size.LARGE)

products = [apple, pear, jackfruit, tree, house, car]

# wrong/old approach
pf = ProductFilter()
color = Color.GREEN
print("Green Products (old):")
for p in pf.filter_by_color(products, color):
    print(f"{p.name} is {p.color.name}")

# correct approach
bf = BetterFilter()

color = Color.BLUE
spec = ColorSpecification(color)
print("\nBlue Products (new):")
for p in bf.filter(products, spec):
    print(f"{p.name} is {spec.color.name}")

size = Size.LARGE
spec = SizeSpecification(size)
print("\nLarge Products (new):")
for p in bf.filter(products, spec):
    print(f"{p.name} is {spec.size.name}")

large_spec = SizeSpecification(Size.LARGE)
blue_spec = ColorSpecification(Color.BLUE)
large_blue_spec = AndSpecification(large_spec, blue_spec)
print("\nLarge Blue Products:")
for p in bf.filter(products, large_blue_spec):
    print(f"{p.name} is large and blue")
