import pygame, sys , utilities

pygame.init()

world_size_x = 0
world_size_y = 0
start_tile = 4 # Empty grass

world_list = []

def get_surf_from_world():
    surf = pygame.Surface((world_size_x * 16, world_size_y * 16))
    
    for y_i, y in enumerate(world_list):
        for x_i, x in enumerate(y):
            if x != -1:
                surf.blit(tiles[x], [x_i * 16, y_i * 16])
    
    return surf

def load_tileset(path, x_tiles, y_tiles):
    img = pygame.image.load(path).convert_alpha()
    
    tile_size_x = img.get_width() / x_tiles
    tile_size_y = img.get_height() / y_tiles
    
    for y in range(y_tiles):
        for x in range(x_tiles):
            tile = pygame.Surface((16, 16))
            tile.blit(img, (-x * tile_size_x, -y * tile_size_y))
            tiles.append(tile)


def movement():
    if up_pressed:
        camera_pos[1] -= camera_speed
    if down_pressed:
        camera_pos[1] += camera_speed
    
    if left_pressed:
        camera_pos[0] -= camera_speed
    if right_pressed:
        camera_pos[0] += camera_speed

def draw(mouse_pos, mode):
    global_mouse_pos = (mouse_pos[0] + camera_pos[0],mouse_pos[1] + camera_pos[1])
    mouse_coords = (int(global_mouse_pos[0] / 16), int(global_mouse_pos[1] / 16))
    
    if mouse_coords[0] >= world_size_x:
        return
    if mouse_coords[1] >= world_size_y:
        return
    
    if mode == 1:
        world_list[mouse_coords[1]][mouse_coords[0]] = tile_index
    if mode == 0:
        world_list[mouse_coords[1]][mouse_coords[0]] = -1

print("1. Load  2. Create")
start_value = int(input("Enter Option: "))

if start_value == 1:
    dimensions, world_list = utilities.load_map_file(input("Enter map file name without file extension: "))
    world_size_x = int(dimensions[0])
    world_size_y = int(dimensions[1])

if start_value == 2:
    world_size_x = int(input("World width: "))
    world_size_y = int(input("World height: "))
    world_list = utilities.get_list(start_tile, world_size_x, world_size_y)

screen = pygame.display.set_mode([1280, 720])
clock = pygame.time.Clock()
camera_pos = [0, -72]
camera_speed = 2
scroll_strength = 2
scroll = 0

up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False 

drawing = False
erasing = False

tiles = []
tile_index = 0

load_tileset("assets/grass_tileset.png", 3, 4)
while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    up_pressed = True
                    break
                case pygame.K_a:
                    left_pressed = True
                    break
                case pygame.K_d:
                    right_pressed = True
                    break
                case pygame.K_s:
                    down_pressed = True
                    break
                case pygame.K_F1:
                    utilities.save_to_file(input("Save file with the name of: "), world_size_x, world_size_y, world_list)
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w:
                    up_pressed = False
                    break
                case pygame.K_a:
                    left_pressed = False
                    break
                case pygame.K_d:
                    right_pressed = False
                    break
                case pygame.K_s:
                    down_pressed = False
                    break
        if event.type == pygame.MOUSEWHEEL:
            if mouse_pos[1] < 720/7:
                scroll += event.y * scroll_strength
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if mouse_pos[1] < 64:
                    drawing = False
                    tile_index = int((mouse_pos[0] + scroll) / 64)
                    if tile_index > len(tiles)-1: tile_index = len(tiles)-1
                else:
                    drawing = True
            
            if event.button == pygame.BUTTON_RIGHT:
                if mouse_pos[1] > 64:
                    erasing = True
                else:
                    erasing = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                drawing = False
            if event.button == pygame.BUTTON_RIGHT:
                erasing = False
                        
    if scroll < 0: scroll = 0
    if scroll > 100: scroll = 100
    
    if drawing: draw(mouse_pos, 1)
    if erasing: draw(mouse_pos, 0)
    
    movement()
    
    screen.fill([0, 0, 0])
    
    screen.blit(get_surf_from_world(), (-camera_pos[0], -camera_pos[1]))
    
    # Background for tile selector
    pygame.draw.rect(screen, [255,255,255], [0, 0, 1280, 72])
    
    for i, tile in enumerate(tiles):
        t = pygame.transform.scale(tile, (64, 64))
        screen.blit(t, [i*64 - scroll, 4])
    
    pygame.display.update()
    clock.tick(60)