import pygame
import sys
import math

class Col:
    """Defines all used colours"""
    def __init__(self):
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.red=(255,0,0)
        
        self.yellow=(255,255,0)
        self.green=(0,200,0)
        self.blue=(0,0,255)
        self.purple=(155,0,255)
        self.cyan=(0,255,255)
        self.grey=(120,120,120)
        self.pink=(255,120,120)
        self.darkgreen=(0,50,0)
        self.brown=(140,42,42)
c=Col()


bg_color=(50,50,50) #tuple

screen = pygame.display.set_mode([1366,768])
        
pygame.init()
pygame.display.set_caption("Drag and drop")
#clock=pygame.time.Clock()
screen.fill(bg_color)
#gameIcon = pygame.image.load('icon.jpg')
#pygame.display.set_icon(gameIcon)

color=(200,200,200)

class Label:
    def __init__(self,text,color,position=[0,0]):
        myfont = pygame.font.SysFont("Cambria", 20)
        lbl = myfont.render(text, 20, color)
        self.lbl=lbl
        self.position=position
        screen.blit(lbl, (position[0],position[1]))        
        
def refresh():
    screen.fill(bg_color)
    for i,rect in enumerate(rects):
        rect.draw()
   
    for i,label in enumerate(labels):
        screen.blit(label.lbl, (label.position[0], label.position[1]))
        
class DraggableRect:
    def __init__(self,pos,size):
        self.x=pos[0]
        self.y=pos[1]
        self.dx=size[0]
        self.dy=size[1]
        
    def draw(self): 
        pygame.draw.rect(screen,color,[self.x,self.y,self.dx,self.dy])    
    
    def is_point_in_rectangle(self,pos):
        if self.x<pos[0] and pos[0]<self.x+self.dx and self.y<pos[1] and pos[1]<self.y+self.dy:
            return(True)
        else:
            return(False)
    
    def is_collided(self):
        for i in range(len(rects)):
            if rects[i]!=self:
                collision=False
                if self.is_point_in_rectangle([rects[i].x,rects[i].y]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].x+rects[i].dx,rects[i].y]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].x,rects[i].y+rects[i].dy]):
                    collision=True
                if self.is_point_in_rectangle([rects[i].x+rects[i].dx,rects[i].y+rects[i].dy]):
                    collision=True
                if collision:
                    self.collision_function()
    
    def collision_function(self):
        self.dx+=0.1
        self.dy+=0.1
  


class Position:
    def __init__(self,position):
        self.position=position
        self.x=position[0]
        self.y=position[1]
    def distance(self,diff_position):
        return(math.hypot(self.x-diff_position.x,self.y-diff_position.y))
    
class Rectangle(Position):
    def __init__(self,position,size):
        super().__init__(position)
        self.size = size #list of two values
    def width(self):
        return(self.size[0]) 
    def height(self):
        return(self.size[1])
    
class Window(Rectangle):
    def __init__(self,size,position=[0,0],bg_color=c.black):
        super().__init__(position,size)
        self.bg_color=bg_color
        self.screen = pygame.display.set_mode(self.size)
        
    def initialize_game(self):    
        pygame.init()
        pygame.display.set_caption("Drag and drop")
        clock=pygame.time.Clock()
        self.screen.fill(self.bg_color)
        #gameIcon = pygame.image.load('icon.png')
        #pygame.display.set_icon(gameIcon)
        return(clock)  
      
    def draw_grid(self,grid):
        for row in range(grid.rows):
            for column in range(grid.columns):
                value=grid.grid[row][column]
                color = grid.colors[value]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0],
                                  (grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1],
                                  grid.cell_size[0],
                                  grid.cell_size[1]])      
    
    def draw_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, label.color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
        
    def remove_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, self.bg_color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
              
        
selected_offset_x=0
selected_offset_y=0
selected=None


labels=[]#[Label("ahoj",(100,100,100),[200,200])]
rects=[DraggableRect([50,50],[30,30]),DraggableRect([150,100],[30,30])]



def main_program_loop(window,clock):
    selected=None
    done = False
    grids=[]
    labels=[]
    time_fr=0 #1/60 sec
    time=0 #1 sec
    #gameIcon = pygame.image.load('icon.png')
    #window.screen.blit(gameIcon,(10,10))
    while not done:  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #game_mechanics.evaluate_click(grids,pos)   
                for i,rect in enumerate(rects):
                    if pos[0]>rect.x and pos[0]<rect.x+rect.dx and pos[1]>rect.y and pos[1]<rect.y+rect.dy:
                        selected=i
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                selected = None
            elif event.type == pygame.MOUSEMOTION:
                for i,rect in enumerate(rects):
                    if selected==i:
                        rect.x = event.pos[0] + offset_x
                        rect.y = event.pos[1] + offset_y
                
            pygame.event.pump()
            keys = pygame.key.get_pressed()
                                 

        pygame.display.flip()   
        

        
        for grid in grids:
            window.draw_grid(grid)
        for label in labels:
            window.draw_label(label)                   
        
        clock.tick(60)
        
        time_fr+=1
        
        if time_fr%1==0:
            refresh()
            for i,rect in enumerate(rects):
                rect.is_collided()
        
        if time_fr%5==0:
            pass
            #game_mechanics.update_labels(labels)
            #game_mechanics.time_event(grids,time_fr)
        if time_fr%60==0:
            time+=1
            print("time:",time)
            
            
        pygame.display.flip()   
        

def run():
    window=Window([1600,900])
    clock = window.initialize_game()
    main_program_loop(window, clock)
    pygame.quit()
    

run()