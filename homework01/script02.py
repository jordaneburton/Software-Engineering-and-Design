import names

namelist = []
name = ""
i = 0

while i < 6:
    name = names.get_full_name()
    if (len(name) == 9):
        namelist.append(name)
        i = i + 1

print(namelist)
