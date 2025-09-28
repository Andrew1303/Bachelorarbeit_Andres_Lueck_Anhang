import random
Tabledata = {}

names = ["Herbert", "Franz", "Peter", "Gustav"]

for n, name in enumerate(names):
    Tabledata[name] = {"name": name, "age": n+random.randint(20,40)}

print(Tabledata)