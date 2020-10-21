import pygame
import sys

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
    def __init__(self,text,color):
        myfont = pygame.font.SysFont("Cambria", 20)
        lbl = myfont.render(text, 20, color)
        screen.blit(lbl, (120, 320))        
        
def refresh():
    screen.fill(bg_color)
    for i,rect in enumerate(rects):
        rect.draw()
    
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
                
        
done=False
t=0

selected_offset_x=0
selected_offset_y=0
selected=None

rects=[DraggableRect([50,50],[30,30]),DraggableRect([150,100],[30,30])]


while not done:  
    try:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
            if (keys[pygame.K_RIGHT]):
                print("right")                
            if (keys[pygame.K_LEFT]):
                print("left")                
            if (keys[pygame.K_UP]):
                print("up")                 
            if (keys[pygame.K_DOWN]):
                print("down")               
            if (keys[pygame.K_ESCAPE]):
                print("quit")
                done=True
            if (keys[pygame.K_RETURN]):
                print("enter")                

        pygame.display.flip()   

    except KeyboardInterrupt:
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)

    t=t+10
    if t%10==0:
        refresh()
        for i,rect in enumerate(rects):
            rect.is_collided()
        try:
            print(rects[0].x,rects[0].y)
            print(selected)
        except IndexError:
            pass
        print(t)
    pygame.time.wait(10)
    
  
pygame.display.quit()
pygame.quit()
sys.exit(0)

