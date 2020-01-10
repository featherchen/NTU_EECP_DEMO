import pygame
import sys,os
import random
import copy
from pygame.locals import* 

pygame.init()
#大小
size = (800, 800)
#定義顏色 
white = "white"
blue = "blue"
red = "red"
green = "green"
yellow = "yellow"
black=(0,0,0)
purple= "purple"
orange = "orange"
rainbow="rainbow"

normal="normal"
stripe_col="stripe_col"
stripe_row="stripe_row"
wrap="wrap"
ball="ball"

#分數
score=0
#視窗
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Candy Crash")
width =50 #寬
height = 50 #高
color=[blue,red,yellow,green,purple,orange] 
N=9#數量

space=5 #空隙

pygame.mixer.init()
pygame.mixer.music.load(f"music/background_music.OGG")
pygame.mixer.music.play(-1)
sound_switch = pygame.mixer.Sound("music/switch.OGG")
sound_elimiante =pygame.mixer.Sound("music/eliminate.OGG")
sound_square1 =pygame.mixer.Sound("music/Square_Removed1.OGG")
sound_square2 =pygame.mixer.Sound("music/Square_Removed2.OGG")
sound_land =pygame.mixer.Sound("music/candy_land1.OGG")
sound_elimiante_stripe =pygame.mixer.Sound("music/eliminate_stripe.OGG")
Run=1

class Candy(pygame.sprite.Sprite):
    def __init__(self,x,y,color,type="normal"):  #type代表不同功能的糖果

        super().__init__()
        self.x=x
        self.y=y
        self.color=color
        self.type=type  
        self.need_eli=False
        self.caneli= True

    def display_image(self):
        way=f"Candy_Crush素材\{self.color}_{self.type}.jpg"
        self.preimage= pygame.image.load(way).convert_alpha()
        self.image = pygame.transform.scale(self.preimage, (width, height))

font = pygame.font.Font("C:\WINDOWS\Fonts\msjh.ttc", 24)
def show_text(context,score, x, y):#專門顯示文字的方法，除了顯示文字還能指定顯示的位置
    x = x
    y = y
    word = font.render(f"{context} : {score}", True, (255, 255, 255))
    window_surface.blit(word, (x, y))
    pygame.display.update()

def show(L,delay=50):
    for i in range(N):
        for j in range(N):
            L[i][j].display_image()

            window_surface.blit(L[i][j].image, pygame.Rect(j*(width+space),i*(height+space), width, height))
    pygame.display.update()
    pygame.time.delay(delay)    
def count_score(type):
    if type==normal:
        return 60
    if type==stripe_col or stripe_row :
        return 60*60
    if type==wrap:
        return 60*100
    if type==ball:
        return 100*100
def renew(L):

    for i in range(N):
        for j in range(N):
            if L[i][j].type==ball or L[i][j].color==white:
                return True
            #橫 連
            if j<=N-2 and L[i][j].color==L[i][j+1].color:
                if j>=2 and L[i][j].color==L[i][j-2].color:
                    return True
                if j>=1 and i>=1 and L[i][j].color==L[i-1][j-1].color:
                    return True
                if j>=1 and i<=N-2 and L[i][j].color==L[i+1][j-1].color:
                    return True
                if j<=N-4 and L[i][j].color==L[i][j+3].color:
                    return True
                if j<=N-3 and i>=1 and L[i][j].color==L[i-1][j+2].color:
                    return True
                if j<=N-3 and i<=N-2 and L[i][j].color==L[i+1][j+2].color:
                    return True
            #橫 
            if j<=N-3 and L[i][j].color==L[i][j+2].color:
                if i>=1 and L[i][j].color==L[i-1][j+1].color:
                    return True
                if i<=N-2 and L[i][j].color==L[i+1][j+1].color:
                    return True
            #直 連
            if i<=N-2 and L[i][j].color==L[i+1][j].color:
                if i>=2 and L[i][j].color==L[i-2][j].color:
                    return True
                if i>=1 and j>=1 and L[i][j].color==L[i-1][j-1].color:
                    return True
                if i>=1 and j<=N-2 and L[i][j].color==L[i-1][j+1].color:
                    return True
                if i<=N-4 and L[i][j].color==L[i+3][j].color:
                    return True
                if i<=N-3 and j>=1 and L[i][j].color==L[i+2][j-1].color:
                    return True
                if i<=N-3 and j<=N-2 and L[i][j].color==L[i+2][j+1].color:
                    return True
            #直
            if i<=N-3 and L[i][j].color==L[i+2][j].color:
                if j>=1 and L[i][j].color==L[i+1][j-1].color:
                    return True
                if j<=N-2 and L[i][j].color==L[i+1][j+1].color:
                    return True
    return False

def eliminate_three(L,CANDY):
    if CANDY.color==white:
        return False
    j=CANDY.x
    i=CANDY.y
    #左
    if j>=2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i][j].color=white
            return True
    #右
    if j<=N-3:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i][j].color=white
            return True
    #上
    if i>=2:
        if L[i-1][j].color==L[i-2][j].color==L[i][j].color:
            L[i-1][j].color=L[i-2][j].color=L[i][j].color=white
            return True
    if i<=N-3:
        if L[i+1][j].color==L[i+2][j].color==L[i][j].color:
            L[i+1][j].color=L[i+2][j].color=L[i][j].color=white   
            return True
    #上下
    if i>=1 and i<=N-2:
        if L[i+1][j].color==L[i-1][j].color==L[i][j].color:
            L[i+1][j].color=L[i-1][j].color=L[i][j].color=white
            return True
    #左右
    if j>=1 and j<=N-2:
        if L[i][j+1].color==L[i][j-1].color==L[i][j].color:
            L[i][j+1].color=L[i][j-1].color=L[i][j].color=white
            return True
    
    return False

def eliminate_four(L,CANDY):
    if CANDY.color==white:
        return False
    j=CANDY.x
    i=CANDY.y
    #橫左
    if j>=1 and j<=N-3:
        if L[i][j-1].color==L[i][j].color==L[i][j+1].color==L[i][j+2].color:
            L[i][j-1].color=L[i][j+1].color=L[i][j+2].color=white
            L[i][j].type=stripe_col
            return True
    #橫右
    if j>=2 and j<=N-2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i][j+1].color:
            L[i][j-1].color=L[i][j-2].color=L[i][j+1].color=white
            L[i][j].type=stripe_col
            return True
    #直上
    if i>=1 and i<=N-3:
        if L[i-1][j].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color:
            L[i-1][j].color=L[i+1][j].color=L[i+2][j].color=white
            L[i][j].type=stripe_row
            return True
    #直下
    if i>=2 and i<=N-2:
        if L[i-1][j].color==L[i-2][j].color==L[i][j].color==L[i+1][j].color:
            L[i-1][j].color=L[i-2][j].color=L[i+1][j].color=white   
            L[i][j].type=stripe_row
            return True


    return False

def eliminate_five(L,CANDY):
    if CANDY.color==white:
        return False
    j=CANDY.x
    i=CANDY.y
    #橫
    if j>=2 and j<=N-3:
        if L[i][j-2].color==L[i][j-1].color==L[i][j].color==L[i][j+1].color==L[i][j+2].color:
            L[i][j-2].color=L[i][j-1].color=L[i][j+1].color=L[i][j+2].color=white
            L[i][j].color=rainbow
            L[i][j].type=ball
            return True
    #直
    if i>=2 and i<=N-3:
        if L[i-2][j].color==L[i-1][j].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color:
            L[i-2][j].color=L[i-1][j].color=L[i+1][j].color=L[i+2][j].color=white
            L[i][j].color=rainbow
            L[i][j].type=ball
            return True
    ##L
    #左上
    if j>=2 and i>=2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i-1][j].color=L[i-2][j].color=white
            L[i][j].type=wrap
            
            return True
    #左下
    if j>=2 and i<=N-3:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i+1][j].color=L[i+2][j].color=white
            L[i][j].type=wrap
            
            return True    
    #右上
    if j<=N-3 and i>=2:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i-1][j].color=L[i-2][j].color=white
            L[i][j].type=wrap
            return True
    #右下
    if j<=N-3 and i<=N-3:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i+1][j].color=L[i+2][j].color=white
            L[i][j].type=wrap
            
            return True
    ##T
    #左
    if j>=2 and i>=1 and i<=N-2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i-1][j].color==L[i+1][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i-1][j].color=L[i+1][j].color=white
            L[i][j].type=wrap
         
            return True
    #下
    if j>=1 and j<=N-2 and i<=N-3:
        if L[i][j-1].color==L[i][j+1].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color:
            L[i][j-1].color=L[i][j+1].color=L[i+1][j].color=L[i+2][j].color=white
            L[i][j].type=wrap

            return True    
    #上
    if j>=1 and j<=N-2 and i>=2:
        if L[i][j+1].color==L[i][j-1].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color:
            L[i][j+1].color=L[i][j-1].color=L[i-1][j].color=L[i-2][j].color=white
            L[i][j].type=wrap
            return True
    #右
    if j<=N-3 and i>=1 and i<=N-2:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i+1][j].color==L[i-1][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i+1][j].color=L[i-1][j].color=white
            L[i][j].type=wrap
 
            return True
    return False
def eliminate_six(L,CANDY):
    if CANDY.color==white:
        return False
    j=CANDY.x
    i=CANDY.y
    #左上 右
    if j>=2 and i>=2 and j<=N-2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color==L[i][j+1].color:
            L[i][j-1].color=L[i][j-2].color=L[i-1][j].color=L[i-2][j].color=L[i][j+1].color=white
            L[i][j].type=wrap
            
            return True
    #左上 下
    if j>=2 and i>=2 and i<=N-2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color==L[i+1][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i-1][j].color=L[i-2][j].color=L[i+1][j].color=white
            L[i][j].type=wrap
            
            return True
    #左下 右
    if j>=2 and i<=N-3 and j<=N-2:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color==L[i][j+1].color:
            L[i][j-1].color=L[i][j-2].color=L[i+1][j].color=L[i+2][j].color=L[i][j+1].color=white
            L[i][j].type=wrap
            
            return True
    #左下 上
    if j>=2 and i<=N-3 and i>=1:
        if L[i][j-1].color==L[i][j-2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color==L[i-1][j].color:
            L[i][j-1].color=L[i][j-2].color=L[i+1][j].color=L[i+2][j].color=L[i-1][j].color=white
            L[i][j].type=wrap
            
            return True
    #右上 左
    if j<=N-3 and i>=2 and j>=1:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color==L[i][j-1].color:
            L[i][j+1].color=L[i][j+2].color=L[i-1][j].color=L[i-2][j].color=L[i][j-1].color=white
            L[i][j].type=wrap
            
            return True
    #右上 下
    if j<=N-3 and i>=2 and i<=N-2:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i-1][j].color==L[i-2][j].color==L[i+1][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i-1][j].color=L[i-2][j].color=L[i+1][j].color=white
            L[i][j].type=wrap
            
            return True      
    #右下 左
    if j<=N-3 and i<=N-3 and j>=1:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color==L[i][j-1].color:
            L[i][j+1].color=L[i][j+2].color=L[i+1][j].color=L[i+2][j].color=L[i][j-1].color=white
            L[i][j].type=wrap
            
            return True
    #右下 上
    if j<=N-3 and i<=N-3 and i>=1:
        if L[i][j+1].color==L[i][j+2].color==L[i][j].color==L[i+1][j].color==L[i+2][j].color==L[i-1][j].color:
            L[i][j+1].color=L[i][j+2].color=L[i+1][j].color=L[i+2][j].color=L[i-1][j].color=white
            L[i][j].type=wrap
            
            return True
    return False

def check_all(L):
    for i in range(N):
        for j in range(N):
            if eliminate_six(L,L[i][j]):
                sound_elimiante.play()

    for i in range(N):
        for j in range(N):    
             if eliminate_five(L,L[i][j]):
                sound_elimiante.play()
    for i in range(N):
        for j in range(N):
            if eliminate_four(L,L[i][j]):
                sound_elimiante.play()

    for i in range(N):
        for j in range(N):
            if eliminate_three(L,L[i][j]):
                sound_elimiante.play()

def eliminate_nine(CANDY,L):
    global score
    i=CANDY.y
    j=CANDY.x
    for col in range(max(0,i-1),min(N,i+2)):
        for row in range(max(0,j-1),min(N,j+2)):
            L[col][row].color=white
            
            score+=count_score(L[col][row].type)
def eliminate_twentyfive(CANDY,L):
    global score
    i=CANDY.y
    j=CANDY.x
    for col in range(max(0,i-2),min(N,i+3)):
        for row in range(max(0,j-2),min(N,j+3)):
            L[col][row].color=white

            score+=count_score(L[col][row].type)


def eliminate_special(L):
    global score
    while True:
        been_eliminate=0
        for i in range(N):
            for j in range(N):
                if L[i][j].color==white and L[i][j].type==stripe_col:  #縱
                    been_eliminate+=1
                    L[i][j].type = normal
                    for col in range(N):
                        L[col][j].color=white
                        score+=count_score(L[col][j].type)
                    sound_elimiante_stripe.play()
                if L[i][j].color==white and L[i][j].type==stripe_row: #橫
                    been_eliminate+=1
                    L[i][j].type = normal
                    for row in range(N):
                        L[i][row].color=white
                        score+=count_score(L[i][row].type)
                    sound_elimiante_stripe.play()
                if L[i][j].color==white and L[i][j].type==wrap:  #九宮格
 
                    been_eliminate+=1
                    CANDY_wrap=Candy(j,i,L[i][j].color,L[i][j].type)
                    show(L,10)
                    eliminate_nine(CANDY_wrap,L)
                    show(L)
                    sound_square1.play()
                    factor=i

                    while  factor<N:
                        if L[factor][j].color==white : 
                            factor+=1
                        
                        else :
                            break
                    fall(L)
                    show(L)

                    if factor==N-1:
                        CANDY_wrap2=Candy(j,factor,L[factor][j].color,L[factor][j].type)
                        eliminate_nine(CANDY_wrap2,L)

                    else:
                        CANDY_wrap3=Candy(j,factor-1,L[factor-1][j].color,L[factor-1][j].type)
                        eliminate_nine(CANDY_wrap3,L)
          
                    L[i][j].type=normal
                    L[i][j].caneli=True
                    sound_square2.play()

                if L[i][j].color==white and L[i][j].type==ball:
                    been_eliminate+=1
                    L[i][j].type=normal
                    COLOR=random.choice(color)
                    for col in range(N):
                        for row in range(N):
                            if L[col][row].color==COLOR:
                                L[col][row].color=white
                                score+=count_score(L[col][row].type)
                    
        show(L)            
        if been_eliminate==0:
            break
                
def eliminate_speswitch(CANDY1,CANDY2):
    global score
    if CANDY1.type==normal and CANDY2.type==normal:
        return False
    else:
        if CANDY1.type==stripe_col:
            if CANDY2.type==stripe_col:
                return False
            elif CANDY2.type==stripe_row:
                i=CANDY1.y
                j=CANDY1.x
                for col in range(N):
                    L[i][col].color=white
                for row in range(N):
                    L[row][j].color=white
                L[CANDY2.y][CANDY2.x].type=normal
                L[CANDY1.y][CANDY1.x].type=normal
                return True


        if CANDY1.type==stripe_row:
            if CANDY2.type==stripe_row:
                return False
            elif CANDY2.type==stripe_col:
                i=CANDY1.y
                j=CANDY1.x
                for col in range(N):
                    L[i][col].color=white
                for row in range(N):
                    L[row][j].color=white
                L[CANDY2.y][CANDY2.x].type=normal
                L[CANDY1.y][CANDY1.x].type=normal
                return True

        if CANDY1.type==ball:
            if CANDY2.type==normal:
                for col in range(N):
                    for row in range(N):
                        if  L[col][row].color==CANDY2.color:
                            L[col][row].color=white
                            score+=count_score(L[col][row].type)
                L[CANDY2.y][CANDY2.x].type=normal
                L[CANDY2.y][CANDY2.x].color=white

                return True

        if CANDY2.type==ball:
            if CANDY1.type==normal:

                for col in range(N):
                    for row in range(N):
                        if  L[col][row].color==CANDY1.color:
                            L[col][row].color=white

                            score+=count_score(L[col][row].type)
                L[CANDY1.y][CANDY1.x].color=white
                L[CANDY1.y][CANDY1.x].type=normal
                return True
        if CANDY1.type==ball and CANDY2.type==ball:

            for col in range(N):
                for row in range(N):
                    score+=count_score(L[col][row].type)
                    C=random.choice(color)
                    L[col][row].color=C
                    L[col][row].type=normal

            return True
        if CANDY1.type==wrap and (CANDY2.type==stripe_col or CANDY2.type==stripe_row):
            
            for i in range(max(0,CANDY2.y-1),min(N,CANDY2.y+2)):
                for j in range(N):
                    L[i][j].color=white
                    score+=count_score(L[i][j].type)
            show(L,10)
            for j in range(max(0,CANDY2.x-1),min(N,CANDY2.x+2)):
                for i in range(N):
                    L[i][j].color=white
                    score+=count_score(L[i][j].type)
            show(L,10)
            return True
        if CANDY2.type==wrap and (CANDY1.type==stripe_col or CANDY1.type==stripe_row):
 
            for i in range(max(0,CANDY1.y-1),min(N,CANDY1.y+2)):
                for j in range(N):
                    L[i][j].color=white
                    score+=count_score(L[i][j].type)
            show(L,10)
            for j in range(max(0,CANDY1.x-1),min(N,CANDY1.x+2)):
                for i in range(N):
                    L[i][j].color=white
                    score+=count_score(L[i][j].type)
            show(L,10)
            return True
        if CANDY1.type==ball and (CANDY2.type==stripe_col or CANDY2.type==stripe_row):
      
            L[CANDY2.y][CANDY2.x].type=normal
            L[CANDY2.y][CANDY2.x].color=white
            for i in range(N):
                for j in range(N):
                    if L[i][j].color==CANDY2.color:
                        L[i][j].type=random.choice([stripe_col,stripe_row])
                        
                        L[i][j].need_eli=True
            show(L,10)
            for i in range(N):
                for j in range(N):
                    if L[i][j].need_eli:
                   
                        L[i][j].color=white

                        L[i][j].need_eli=False
                        
            return True
        if CANDY2.type==ball and (CANDY1.type==stripe_col or CANDY1.type==stripe_row):
         
            L[CANDY1.y][CANDY1.x].type=normal
            L[CANDY1.y][CANDY1.x].color=white
            for i in range(N):
                for j in range(N):
                    if L[i][j].color==CANDY1.color:
                        L[i][j].type=random.choice([stripe_col,stripe_row])
                        
                        L[i][j].need_eli=True
            show(L,10)
            for i in range(N):
                for j in range(N):
                    if L[i][j].need_eli:
                        
                        L[i][j].color=white
                        L[i][j].need_eli=False
            return True
        if CANDY1.type==ball and CANDY2.type==wrap:

            L[CANDY2.y][CANDY2.x].type=normal
            L[CANDY2.y][CANDY2.x].color=white
            for i in range(N):
                for j in range(N):
                    if L[i][j].color==CANDY2.color:
                        L[i][j].type=wrap
                        
                        L[i][j].need_eli=True
            show(L,10)
            for i in range(N):
                for j in range(N):
                    if L[i][j].need_eli:

                        L[i][j].color=white

                        L[i][j].need_eli=False
                        L[i][j].caneli=False
            return True
        if CANDY1.type==wrap and CANDY2.type==wrap:

            eliminate_twentyfive(CANDY1,L)
            show(L)
            i=CANDY1.y
            j=CANDY1.x
            factor=i

            print(L[factor][j].color)
            while  factor<N:
                if L[factor][j].color==white : 
                    factor+=1
                    print(factor)
                else :
                    break
            fall(L)
            show(L)
        
            if factor==N-1:
                CANDY_wrap2=Candy(j,factor,L[factor][j].color,L[factor][j].type)
                eliminate_twentyfive(CANDY_wrap2,L)
            else:
                CANDY_wrap3=Candy(j,factor-1,L[factor-1][j].color,L[factor-1][j].type)
                eliminate_twentyfive(CANDY_wrap3,L)

            L[i][j].type=normal
            L[CANDY2.y][CANDY2.x].type=normal
            return True
        return False
        

                




def fall(L):
    candy_fall=0
    for i in range(N):
        for j in range(N):
            if L[N-1-i][N-1-j].color==white and L[N-1-i][N-1-j].caneli:
                check=0  
                for factor in range(N-1-i): #由下往上找，如果找到不是白色的，交換
                    if L[N-2-i-factor][N-1-j].color!=white:
                        L[N-1-i][N-1-j].color,L[N-2-i-factor][N-1-j].color=L[N-2-i-factor][N-1-j].color,white
                        L[N-1-i][N-1-j].type,L[N-2-i-factor][N-1-j].type=L[N-2-i-factor][N-1-j].type,L[N-1-i][N-1-j].type
                        check=1
                        break
                if  check==0: #如果找不到的話，就生成新的
                    L[N-1-i][N-1-j].color=random.choice(color)
                    L[N-1-i][N-1-j].type=normal
                    candy_fall=1
    if  candy_fall==1:
        sound_land.play()
                  

            
L=[[0 for col in range(N)] for row in range(N)]
#建構隨機顏色地圖
for i in range(N):
    for j in range(N):
        C=random.choice(color)
        L[i][j]=Candy(j,i,C)

press=0 #初始狀態

white_pic=pygame.transform.scale(pygame.image.load(f"Candy_Crush素材\white_normal.jpg").convert_alpha(),(width, height))
step=10
goal=10000


while Run:
    pygame.time.delay(10)
    window_surface = pygame.display.set_mode(size)
    #輸出地圖
    show(L)
    show_text("Score",str(score), 600,600)
    show_text("Goal",str(goal),600,620)
    show_text("Step",str(step),600,580)
    if press==1:
        window_surface.blit(white_pic,(470,600) )
    
    fall(L)
    show(L,500)
    check_all(L)
    #計分
    for i in range(N):
        for j in range(N):
            if L[i][j].color==white:
                score+=count_score(L[i][j].type)
    
    eliminate_special(L)
    show(L)
    
    change=0
    while not renew(L):
        change=1
        for i in range(N):
            for j in range(N):
                if L[i][j].type==normal:
                    C=random.choice(color)
                    L[i][j].color=C
    
    if change==1:
        pygame.time.delay(1000)
        for i in range(N):
            for j in range(N):
                L[i][j].display_image()
                window_surface.blit(L[i][j].image, pygame.Rect(j*(width+space),i*(height+space), width, height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (step<=0 and score>goal):
            pygame.mixer.music.stop()
            fall(L)
            show(L) 
            pygame.mixer.music.load(f"music/win.OGG")
            pygame.mixer.music.play(0)
            pygame.time.delay(4000)
            Run=0
            break

        if step<=0 and score<goal:
            pygame.mixer.music.stop()
            fall(L)
            window_surface = pygame.display.set_mode(size)
            show(L)
            
            show_text("Score",str(score), 600,600)
            show_text("Goal",str(goal),600,620)
            show_text("Step",str(step),600,580)
            pygame.mixer.music.load(f"music/lose.OGG")
            pygame.mixer.music.play(0)
            pygame.time.delay(4000)
            Run=0
            break
        #檢視點擊
        if event.type == MOUSEBUTTONDOWN and press==0 : #第一次點
            x1=pygame.mouse.get_pos()[0]
            y1=pygame.mouse.get_pos()[1]
            j1=x1//(width+space)
            i1=y1//(height+space)
            if j1>=N or i1>=N:#不理超出範圍的點擊
                continue
            color1=L[i1][j1].color
            type1=L[i1][j1].type
            press=1
            candy1=Candy(j1,i1,color1,type1)
        
        elif event.type == MOUSEBUTTONDOWN and press==1: #第二次點
            press=0
            x2=pygame.mouse.get_pos()[0]
            y2=pygame.mouse.get_pos()[1]
            
            j2=x2//(width+space)
            i2=y2//(height+space)

            #如果不是點在相鄰的就不讓他工作
            if abs(i1-i2)+abs(j1-j2)>1:
                continue
            if j1>=N or i1>=N:
                continue            

            color2=L[i2][j2].color
            type2=L[i2][j2].type
            candy2=Candy(j2,i2,color2,type2)
            
            #交換顏色
            L[i1][j1].color,L[i2][j2].color=color2,color1
            L[i1][j1].type,L[i2][j2].type=type2,type1
            show(L)
            sound_switch.play()


            step-=1

            #檢查是否為合法交換
            if not eliminate_speswitch(candy1,candy2):
                if not eliminate_six(L,candy1) and not eliminate_six(L,candy2) and not eliminate_five(L,candy1) and not eliminate_five(L,candy2):
                    if not eliminate_four(L,candy1) and not eliminate_four(L,candy2) and not eliminate_three(L,candy1) and not eliminate_three(L,candy2):    
                        L[i1][j1].color,L[i2][j2].color=color1,color2
                        L[i1][j1].type,L[i2][j2].type=type1,type2
                        step+=1
            
            show(L)
            w_number=0
            for col in range(N):
                for row in range(N):
                    if L[col][row].color==white :
                        score+=count_score(L[col][row].type)
                        w_number=1
            if w_number==1:
                set_volume=15
                sound_elimiante.play()
            eliminate_special(L)

    pygame.display.update()



    






    
