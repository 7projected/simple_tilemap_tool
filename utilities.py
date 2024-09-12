def get_list(default_value, lines, letters):
    r = []
    for y in range(lines):
        app = []
        for x in range(letters):
            app.append(default_value)
        r.append(app)
    return r

def load_map_file(file_name:str):
    ret_dimensions = [0, 0]
    hex_world = []
    num_world = []
    width = 0
    height = 0
    try:
        with open(f'maps/{file_name}.map', 'r') as file:
            for line_num, line in enumerate(file):
                if line_num == 0:
                    ret_dimensions[0] = int(line)
                    width = int(line)
                elif line_num == 1:
                    ret_dimensions[1] = int(line)
                    height = int(line)
                else:
                    # Load hex values into hex_world  with int(letter + letter[y][x+1], 16)
                    app = ""
                    letter_holder = []
                    for letter in line:
                        app += letter
                        if len(app) == 2:
                            letter_holder.append(app)
                            app = ''
                    
                    hex_world.append(letter_holder)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}.map' does not exist.")
    except IOError:
        print(f"Error: Could not read the file '{file_name}.map '.")
    
    num_world = get_list(-1, height, width)
    
    for y, str_list in enumerate(hex_world):
        for x, str in enumerate(str_list):
            if str == "X1":
                num_world[y][x] = -1
            else:
                num_world[y][x] = int(str, 16)
    
    return ret_dimensions, num_world

#file_name.map
def save_to_file(file_name, world_size_x, world_size_y, list, space_tiles_in_save_file=False):
    f = open(f'maps/{file_name}.map', "w")
    f.write(str(world_size_x) + "\n")
    f.write(str(world_size_y) + "\n")
    for y in list:
        s = ''
        for x in y:
            # stores it in hex
            num = str(hex(x)[2:].upper())
            
            if len(num) == 1:
                num = f'0{num}'
            
            if space_tiles_in_save_file:
                num += " "
            
            s += num
        f.write(s + "\n")