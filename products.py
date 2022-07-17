from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float

    def prepare(self):
        pass

    def __repr__(self):  # магический метод (дандер метод)
        return f'{self.name}={self.price}'

    def __str__(self):  # магический метод (дандер метод)
        return f'{self.name}={self.price}'


@dataclass(repr=False)
class CookableProduct(Product):
    def prepare(self):
        self.cook()
        self.put_on_desk()

    def cook(self):
        pass


@dataclass(repr=False)
class AssemblingProduct(Product):
    def prepare(self):
        self.assemble()

    def assemble(self):
        pass
