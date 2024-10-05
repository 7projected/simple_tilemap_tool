import pygame, sys, utilities, gui

pygame.init()

class App:
    def __init__(self):
        self.world_size_x = 0
        self.world_size_y = 0
        self.start_tile = 0

        self.world_list = []

        self.WORLD = 0
        self.MAIN_MENU = 1
        self.CREATE = 2
        self.LOAD = 3

        self.tile_size = 32
        self.zoom_amount = 0

        # ADD SUPPORT FOR OTHER TILESETS

        self.scene = self.MAIN_MENU
    
        self.screen = pygame.display.set_mode([1280, 720])
        self.clock = pygame.time.Clock()
        self.camera_pos = [0, -72]
        self.camera_speed = 2
        self.scroll_strength = 10
        self.scroll = 0

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False 

        self.drawing = False
        self.erasing = False

        self.tiles = []
        self.scaled_tiles = []
        self.tile_index = 0

        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Simple Tilemap Tool")

        self.set_scene_to_menu()

    def scroll_to_zoom(self, event_y):
        self.zoom_amount += event_y

        if self.zoom_amount < 0:
            self.zoom_amount = 0
        
        self.resize_tileset(self.tile_size + self.zoom_amount, self.tile_size + self.zoom_amount)
        

    def get_surf_from_world(self):
        surf = pygame.Surface((self.world_size_x * (self.tile_size + self.zoom_amount), self.world_size_y * (self.tile_size + self.zoom_amount)))
        self.resize_tileset(self.tile_size + self.zoom_amount, self.tile_size + self.zoom_amount)
        
        for y_i, y in enumerate(self.world_list):
            for x_i, x in enumerate(y):
                if x != -1:
                    surf.blit(self.scaled_tiles[x], [x_i * (self.tile_size + self.zoom_amount), y_i * (self.tile_size + self.zoom_amount)])
        
        return surf

    def load_tileset(self, path):
        img = pygame.image.load(path).convert_alpha()
        
        x_tiles = int(gui.run_popup("How many rows of tiles on tileset? (X)"))
        y_tiles = int(gui.run_popup("How many columns of tiles on tileset? (Y)"))
        
        tile_size_x = img.get_width() / x_tiles
        tile_size_y = img.get_height() / y_tiles
        
        for y in range(y_tiles):
            for x in range(x_tiles):
                tile = pygame.Surface((tile_size_x, tile_size_y))
                tile.blit(img, (-x * tile_size_x, -y * tile_size_y))
                
                tile = pygame.transform.scale(tile, [self.tile_size, self.tile_size])
                self.tiles.append(tile)

    def resize_tileset(self, size_x, size_y):
        self.scaled_tiles = self.tiles.copy()
        
        for i, tile in enumerate(self.tiles):
            self.scaled_tiles[i] = pygame.transform.scale(tile, [size_x, size_y])
        

    def movement(self):
        if self.up_pressed:
            self.camera_pos[1] -= self.camera_speed
        if self.down_pressed:
            self.camera_pos[1] += self.camera_speed
        
        if self.left_pressed:
            self.camera_pos[0] -= self.camera_speed
        if self.right_pressed:
            self.camera_pos[0] += self.camera_speed

    def draw(self, mouse_pos, mode):
        global_mouse_pos = (mouse_pos[0] + self.camera_pos[0], mouse_pos[1] + self.camera_pos[1])
        mouse_coords = (int(global_mouse_pos[0] / (self.tile_size + self.zoom_amount)), int(global_mouse_pos[1] / (self.tile_size + self.zoom_amount)))

        if mouse_coords[0] < 0:
            return
        if mouse_coords[0] >= self.world_size_x:
            return
        if mouse_coords[1] < 0:
            return
        if mouse_coords[1] >= self.world_size_y:
            return
        
        if mode == 1:
            self.world_list[mouse_coords[1]][mouse_coords[0]] = self.tile_index
        if mode == 0:
            self.world_list[mouse_coords[1]][mouse_coords[0]] = -1


    def clear_lists(self):
        gui.Button.clear_list()
        gui.NumberField.clear_list()
        gui.Text.clear_list()

    def press_create_world(self):
        self.load_tileset(f'assets/{gui.run_popup("Enter tileset file name without file extension: ")}.png')
        for i, field in enumerate(gui.NumberField.field_list):
            
            if i == 0:
                self.world_size_x = int(field.text)
            if i == 1:
                self.world_size_y = int(field.text)
            self.world_list = utilities.get_list(self.start_tile, self.world_size_y, self.world_size_x)
            
            self.set_scene_to_world()


    def set_scene_to_load(self):
        popup_output = gui.run_popup("Enter map file name without file extension: ")
        self.load_tileset(f'assets/{gui.run_popup("Enter tileset file name without file extension: ")}.png')
        
        if popup_output != None:
            self.scene = self.LOAD
            self.clear_lists()
            
            dimensions, self.world_list = utilities.load_map_file(popup_output)
            self.world_size_x = int(dimensions[0])
            self.world_size_y = int(dimensions[1])
            
            self.set_scene_to_world()

    def set_scene_to_create(self):
        self.scene = self.CREATE
        self.clear_lists()
        
        back_button = gui.Button(10, 10, "Back", self.set_scene_to_menu)
        width_field = gui.NumberField(10, 62, 3)
        height_field = gui.NumberField(10, 62 + 10 + 32, 3)
        width_text = gui.Text(3 * 24 + 10 + 32, 62, "Width")
        height_text = gui.Text(3 * 24 + 10 + 32, 62 + 10 + 32, "Height")
        create_world_button = gui.Button(10, 62 + 10 + 32 + 10 + 32 + 10, "Create World", self.press_create_world)

    def set_scene_to_menu(self):
        self.scene = self.MAIN_MENU
        self.clear_lists()
        
        load_button = gui.Button(10, 10, "Load Map  ", self.set_scene_to_load)
        create_button = gui.Button(10, 10 + 32 + 10, "Create Map", self.set_scene_to_create)
        quit_button = gui.Button(10, 10 + 32 + 10 + 32 + 10, "Quit App  ", quit)

    def set_scene_to_world(self):
        self.scene = self.WORLD
        self.clear_lists()
        
        back_button = gui.Button(10, 720 - 32 - 10, "Back", self.set_scene_to_menu)

    def quit(self):
        pygame.quit()
        sys.exit()

    # Load Map
    #  dimensions, world_list = utilities.load_map_file(input("Enter map file name without file extension: "))
    #  world_size_x = int(dimensions[0])
    #  world_size_y = int(dimensions[1])

    # Create Map
    # world_size_x = int(input("World width: "))
    # world_size_y = int(input("World height: "))
    # world_list = utilities.get_list(start_tile, world_size_x, world_size_y)

    def loop(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                for f in gui.NumberField.field_list:
                    f.poll(event)
                
                if event.type == pygame.QUIT:
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_w:
                            self.up_pressed = True
                            break
                        case pygame.K_a:
                            self.left_pressed = True
                            break
                        case pygame.K_d:
                            self.right_pressed = True
                            break
                        case pygame.K_s:
                            self.down_pressed = True
                            break
                        case pygame.K_F1:
                            utilities.save_to_file(self.world_size_x, self.world_size_y, self.world_list)
                
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_w:
                            self.up_pressed = False
                            break
                        case pygame.K_a:
                            self.left_pressed = False
                            break
                        case pygame.K_d:
                            self.right_pressed = False
                            break
                        case pygame.K_s:
                            self.down_pressed = False
                            break
                
                if event.type == pygame.MOUSEWHEEL:
                    if mouse_pos[1] < 720/7:
                        self.scroll += event.y * self.scroll_strength
                    else:
                        self.scroll_to_zoom(event.y)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for b in gui.Button.button_list:
                            b.poll(mouse_pos[0], mouse_pos[1])
                            
                        if mouse_pos[1] < 64:
                            self.drawing = False
                            self.tile_index = int((mouse_pos[0] + self.scroll) / 64)
                            if self.tile_index > len(self.tiles)-1:
                                self.tile_index = len(self.tiles) - 1
                        else:
                            self.drawing = True
                    
                    if event.button == pygame.BUTTON_RIGHT:
                        if mouse_pos[1] > 64:
                            self.erasing = True
                        else:
                            self.erasing = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        self.drawing = False
                    if event.button == pygame.BUTTON_RIGHT:
                        self.erasing = False
                                
            if self.scroll < 0:
                self.scroll = 0
            
            if self.drawing: self.draw(mouse_pos, 1)
            if self.erasing: self.draw(mouse_pos, 0)
            
            self.movement()
            
            self.screen.fill([0, 0, 0])
            
            if self.scene == self.WORLD:
                self.screen.blit(self.get_surf_from_world(), (-self.camera_pos[0], -self.camera_pos[1]))
                pygame.draw.rect(self.screen, [255,255,255], [0, 0, 1280, 72])
                
                for i, tile in enumerate(self.tiles):
                    t = pygame.transform.scale(tile, (64, 64))
                    self.screen.blit(t, [i*64 - self.scroll, 4])
            
            for b in gui.Button.button_list:
                b.draw(self.screen)
            
            for f in gui.NumberField.field_list:
                f.draw(self.screen)
            
            for t in gui.Text.text_list:
                t.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    app = App()
    app.loop()