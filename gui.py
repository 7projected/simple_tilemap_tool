import pygame

class Text:
    pygame.font.init()
    font = pygame.font.Font('assets/Hack-Regular.ttf', 32)
    text_list = []
    
    def __init__(self, x, y, text):
        self.pos = [x, y]
        self.text = text
        self.surf = Text.font.render(text, True, [255,255,255], None)
        Text.text_list.append(self)
    
    def draw(self, surf):
        surf.blit(self.surf, self.pos)
        
    def clear_list():
        Text.text_list = []
    
class NumberField:
    pygame.font.init()
    font = pygame.font.Font('assets/Hack-Regular.ttf', 32)
    field_list = []
    
    def __init__(self, x, y, max_char):
        self.pos = [x, y]
        self.text = '5'
        self.focused = False
        self.max_char = max_char
        NumberField.field_list.append(self)
    
    def poll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + self.max_char * 24:
                    if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 32:
                        self.focused = True
                        return
                self.focused = False
                
        if self.focused:
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_BACKSPACE:
                   self.text = self.text[:-1]
               else:
                   if len(self.text) < self.max_char:
                    if event.key - 48 >= 0 and event.key - 48 <= 9:
                        self.text += str(event.key - 48)
    
    def draw(self, surf):
        if self.focused:
            pygame.draw.rect(surf, [120, 120, 120], [self.pos[0], self.pos[1], self.max_char * 24, 32])
        else:
            pygame.draw.rect(surf, [100, 100, 100], [self.pos[0], self.pos[1], self.max_char * 24, 32])
            
        s = NumberField.font.render(self.text, True, [255,255,255], None)
        surf.blit(s, self.pos)
    
    def clear_list():
        NumberField.field_list = []

class Button:
    pygame.font.init()
    font = pygame.font.Font('assets/Hack-Regular.ttf', 32)
    button_list = []
    
    def __init__(self, x, y, text, callback:callable):
        self.pos = [x, y]
        self.surf = Button.font.render(text, True, [255,255,255], [150, 150, 150])
        self.callback = callback
        Button.button_list.append(self)
    
    def draw(self, surf):
        surf.blit(self.surf, self.pos)
    
    def poll(self, x, y):
        if x > self.pos[0] and x < self.pos[0] + self.surf.get_width():
            if y > self.pos[1] and y < self.pos[1] + self.surf.get_height():
                self.callback()
    
    def kill(self):
        for button in Button.button_list:
            if button == self:
                Button.button_list.remove(button)
                self = None
    
    def clear_list():
        Button.button_list = []