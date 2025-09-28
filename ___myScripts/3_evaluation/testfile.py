a = {2: 5, 3: 3}
b = 4
if b in a:
    print("found")
    a[b] += 1
else:
    print("not found")
    a[b] = 1

for key in a:
    print(key)
    print(key[0])
print(a)