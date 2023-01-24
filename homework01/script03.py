import names

def length_of_name(n):
    length = len(n) - 1
    return length

namelist = []
name = ""
duplicates = False
i = 0

while (i < 6):
    name = names.get_full_name()
    for x in namelist:
        if (x == name):
            duplicates = True
    if (duplicates):
        duplicates = False
    else:
        namelist.append(name)
        i = i + 1

print(namelist)
for x in namelist:
    print(x, length_of_name(x))
