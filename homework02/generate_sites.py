import random
import json

def generate_site(id_num): # generates a dictionary of properties for site
    lat = 16 + 2*random.random()
    lon = 82 + 2*random.random()
    comp = random.choice(["stony", "iron", "stony-iron"])
    return {
            "site_id": id_num,
            "latitude": lat,
            "longitude": lon,
            "composition": comp
            }

site_list = []
for x in range(5): # generate 5 sites with random properties
    site_list.append(generate_site(x+1))

site_dict = {"sites": site_list} 

with open('sites.json', 'w') as out:
    json.dump(site_dict, out, indent=2)
