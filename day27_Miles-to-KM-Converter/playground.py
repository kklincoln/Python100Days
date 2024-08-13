def add(n1,n2):
    print(n1+n2)

def addmany(*args):
    total=0
    for n in args:
        total +=n
    print(total)

addmany(1,2,3,4,5)

def calculate (n, **kwargs):
    print(kwargs)   #shows the key:value pairs from line 17::  {'add':2, 'multiply':2}
    n += kwargs["add"] #searches the kwargs for one called add and it takes the n value and += to the argument
    n *= kwargs["multiply"] #searches the kwargs for one called multiply and it takes the n value and *= to the argument
    print(n)
calculate(2, add=2, multiply=2)

#creating a class similar to the tk Label class, with the optional arguments passed as default
class Car:
    def __init__(self, **kw):
        #setting the kw with the .get() method allows these to become optional kwargs
        self.make = kw.get("make")
        self.model = kw.get("model")

my_car = Car(make="Nissan", model="GTR")
print(my_car.model)