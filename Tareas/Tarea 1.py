from pyglet import shapes
import pyglet
import numpy as np


# DATOS INICIALES
WIDTH, HEIGHT = 1200, 1000
DARK_GRAY = (100,100,100)
LIGHT_GRAY = (175,175,175)
BLACK =(0,0,0)
WHITE = (255,255,155)

window = pyglet.window.Window(WIDTH,HEIGHT)
n_estrellas = 80
nave = pyglet.graphics.Batch()
star = pyglet.graphics.Batch()


# CREACION DE ESTRELLAS INICIALES DE FORMA HOMOGENEA
estrellas_i = np.zeros((n_estrellas,3),dtype=int)
estrellas= list()
i=0
while i < n_estrellas:
    if i<n_estrellas//4:
        y1=0
        y2=250
    elif i<n_estrellas//2:
        y1=250
        y2=500
    elif i<3*n_estrellas//4:
        y1=500
        y2=750
    else:
        y1=750
        y2=1000
    estrellas_i[i] = np.array([np.random.randint(10,1190),np.random.randint(y1,y2),np.random.randint(1,4)])
    i+=1


# OBJETOS USADOS (naves y estrellas)
class halcon():
    def __init__(self):
        self.propulsor0 = pyglet.shapes.Arc(x=WIDTH//2,y=HEIGHT//2-150, radius = 67, angle = 1.58, start_angle=3.93,color=(0,255,255),batch=nave,)
        self.propulsor1 = pyglet.shapes.Arc(x=WIDTH//2,y=HEIGHT//2-150, radius = 68, angle = 1.58, start_angle=3.93,color=(0,255,255),batch=nave)
        self.propulsor2 = pyglet.shapes.Arc(x=WIDTH//2,y=HEIGHT//2-150, radius = 69, angle = 1.58, start_angle=3.93,color=(0,255,255),batch=nave)
        self.punta_nave0 = pyglet.shapes.Triangle(x=WIDTH//2-45,y=WIDTH//2-200,x2=WIDTH//2-16,y2=WIDTH//2-200,x3=WIDTH//2-16,y3=WIDTH//2-122,color = DARK_GRAY,batch= nave)
        self.punta_nave1 = pyglet.shapes.Triangle(x=WIDTH//2+45,y=WIDTH//2-200,x2=WIDTH//2+16,y2=WIDTH//2-200,x3=WIDTH//2+16,y3=WIDTH//2-122,color = DARK_GRAY,batch= nave)
        self.punta_nave3 = pyglet.shapes.Rectangle(x=WIDTH//2-16,y=HEIGHT//2-97, width = 6, height = 75, color = DARK_GRAY,batch=nave)
        self.punta_nave4 = pyglet.shapes.Rectangle(x=WIDTH//2+10,y=HEIGHT//2-97, width = 6, height = 75, color = DARK_GRAY,batch=nave)
        self.cuerpo_nave = pyglet.shapes.Circle(x=WIDTH//2,y=HEIGHT//2-150, radius = 67, color = LIGHT_GRAY, batch = nave)
        self.cuerpo_nave3 = pyglet.shapes.Rectangle(x=WIDTH//2-10,y=HEIGHT//2-151, width = 20, height = 82, color = DARK_GRAY,batch=nave)
        self.cuerpo_nave2 = pyglet.shapes.Rectangle(x=WIDTH//2-9,y=HEIGHT//2-150, width = 18, height = 80, color = LIGHT_GRAY,batch=nave)
        self.capsula_nave1 = pyglet.shapes.Rectangle(x=WIDTH//2+5,y=HEIGHT//2-160, width = 80, height = 22, color = DARK_GRAY,batch=nave)
        self.capsula_nave2 = pyglet.shapes.Rectangle(x=WIDTH//2+47,y=HEIGHT//2-111, width = 22, height = 22, color = DARK_GRAY,batch=nave)
        self.capsula_nave3 = pyglet.shapes.Rectangle(x=WIDTH//2+47,y=HEIGHT//2-89, width = 10, height = 15, color = DARK_GRAY,batch=nave)
        self.capsula_nave4 = pyglet.shapes.Rectangle(x=WIDTH//2+69,y=HEIGHT//2-89, width = 10, height = 15, color = DARK_GRAY,batch=nave)
        self.capsula_nave5 = pyglet.shapes.Rectangle(x=WIDTH//2+54,y=HEIGHT//2-90, width = 10, height = 15, color = DARK_GRAY,batch=nave)
        self.capsula_nave11 = pyglet.shapes.Rectangle(x=WIDTH//2+6,y=HEIGHT//2-158, width = 78, height = 20, color = LIGHT_GRAY,batch=nave)
        self.capsula_nave21 = pyglet.shapes.Rectangle(x=WIDTH//2+48,y=HEIGHT//2-110, width = 20, height = 20, color = LIGHT_GRAY,batch=nave)
        self.capsula_nave6 = pyglet.shapes.Line(x=WIDTH//2+49,y=HEIGHT//2-89,x2 = WIDTH//2+54,y2=HEIGHT//2-76, width = 1, color = LIGHT_GRAY, batch=nave)
        self.capsula_nave7 = pyglet.shapes.Line(x=WIDTH//2+54,y=HEIGHT//2-76, x2=WIDTH//2+62,y2=HEIGHT//2-76, width = 1, color = LIGHT_GRAY, batch=nave)
        self.capsula_nave8 = pyglet.shapes.Line(x=WIDTH//2+62,y=HEIGHT//2-76, x2=WIDTH//2+67,y2=HEIGHT//2-89, width = 1, color = LIGHT_GRAY, batch=nave)
        self.capsula_nave9 = pyglet.shapes.Line(x=WIDTH//2+49,y=HEIGHT//2-88,x2 = WIDTH//2+67,y2=HEIGHT//2-88, width = 1, color = LIGHT_GRAY, batch=nave)
        self.capsula_nave10 = pyglet.shapes.Line(x=WIDTH//2+55,y=HEIGHT//2-88,x2 = WIDTH//2+55,y2=HEIGHT//2-76, width = 1, color = LIGHT_GRAY, batch=nave)
        self.capsula_nave12 = pyglet.shapes.Line(x=WIDTH//2+62,y=HEIGHT//2-88,x2 = WIDTH//2+62,y2=HEIGHT//2-76, width = 1, color = LIGHT_GRAY, batch=nave)
        self.cuerpo_nave6 = pyglet.shapes.Line(x=WIDTH//2,y=HEIGHT//2-150,x2=WIDTH//2-47,y2=HEIGHT//2-197,width=2,color=DARK_GRAY,batch=nave)
        self.cuerpo_nave7 = pyglet.shapes.Line(x=WIDTH//2,y=HEIGHT//2-150,x2=WIDTH//2+48,y2=HEIGHT//2-198,width=2,color=DARK_GRAY,batch=nave)
        self.cuerpo_nave4 = pyglet.shapes.Circle(x=WIDTH//2,y=HEIGHT//2-150, radius = 18, color = DARK_GRAY, batch = nave)
        self.cuerpo_nave5 = pyglet.shapes.Circle(x=WIDTH//2,y=HEIGHT//2-150, radius = 16, color = LIGHT_GRAY, batch = nave)
        self.detalle_nave1 = pyglet.shapes.Circle(x=WIDTH//2-14,y=HEIGHT//2-177, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave2 = pyglet.shapes.Circle(x=WIDTH//2,y=HEIGHT//2-179, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave3 = pyglet.shapes.Circle(x=WIDTH//2+13,y=HEIGHT//2-177, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave4 = pyglet.shapes.Circle(x=WIDTH//2-20,y=HEIGHT//2-190, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave5 = pyglet.shapes.Circle(x=WIDTH//2,y=HEIGHT//2-193, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave6 = pyglet.shapes.Circle(x=WIDTH//2+19,y=HEIGHT//2-190, radius = 5, color = DARK_GRAY, batch = nave)
        self.detalle_nave7 = pyglet.shapes.Triangle(x=WIDTH//2-30,y=HEIGHT//2-130,x2=WIDTH//2-26,y2=HEIGHT//2-115,x3=WIDTH//2-47,y3=HEIGHT//2-130, color = DARK_GRAY, batch = nave)
        self.detalle_nave8 = pyglet.shapes.Line(x=WIDTH//2-32,y=HEIGHT//2-128,x2=WIDTH//2-40,y2=HEIGHT//2-117,width=2, color = DARK_GRAY, batch = nave)
        self.capsula_nave1.rotation, self.capsula_nave11.rotation = -37,-37
        self.capsula_nave3.rotation=20
        self.capsula_nave4.anchor_x = 10
        self.capsula_nave4.rotation = -20

    def update(self,n):
        self.propulsor2.angle += n*1.58

class x_wing():
    def __init__(self,pos):
        self.centro = (pos[0],pos[1])
        self.cuerpo1= pyglet.shapes.Triangle(x=self.centro[0]-11,y=self.centro[1]-50,x2=self.centro[0]-5,y2=self.centro[1]+40,x3=self.centro[0]-5,y3=self.centro[1]-50,color = LIGHT_GRAY, batch=nave)
        self.cuerpo2= pyglet.shapes.Triangle(x=self.centro[0]+11,y=self.centro[1]-50,x2=self.centro[0]+5,y2=self.centro[1]+40,x3=self.centro[0]+5,y3=self.centro[1]-50,color = LIGHT_GRAY, batch=nave)
        self.cuerpo3= pyglet.shapes.Rectangle(x=self.centro[0]-5,y=self.centro[1]-50,width = 10, height=90,color=LIGHT_GRAY,batch=nave)    
        self.punta1= pyglet.shapes.Triangle(x=self.centro[0]-6,y=self.centro[1]+39,x2=self.centro[0]-3,y2=self.centro[1]+60,x3=self.centro[0]-3,y3=self.centro[1]+39,color = DARK_GRAY,batch=nave)
        self.punta2= pyglet.shapes.Triangle(x=self.centro[0]+6,y=self.centro[1]+39,x2=self.centro[0]+3,y2=self.centro[1]+60,x3=self.centro[0]+3,y3=self.centro[1]+39,color = DARK_GRAY,batch=nave)   
        self.punta3= pyglet.shapes.Rectangle(x=self.centro[0]-3,y=self.centro[1]+39,width = 6, height=20,color=DARK_GRAY,batch=nave)
        self.alas1= pyglet.shapes.Rectangle(x=self.centro[0]-61,y=self.centro[1]-73,width=122,height=23,color=LIGHT_GRAY,batch=nave)
        self.alas2= pyglet.shapes.Triangle(x=self.centro[0]-61,y=self.centro[1]-73,x2=self.centro[0]-11,y2=self.centro[1]-73,x3=self.centro[0]-11,y3=self.centro[1]-83,color=LIGHT_GRAY,batch=nave)
        self.alas3= pyglet.shapes.Triangle(x=self.centro[0]+61,y=self.centro[1]-73,x2=self.centro[0]+11,y2=self.centro[1]-73,x3=self.centro[0]+11,y3=self.centro[1]-83,color=LIGHT_GRAY,batch=nave)
        self.alas4= pyglet.shapes.Rectangle(x=self.centro[0]-11,y=self.centro[1]-83,width=22,height=10,color=LIGHT_GRAY,batch=nave)
        self.trasera1 = pyglet.shapes.Triangle(x=self.centro[0]-11,y=self.centro[1]-83,x2=self.centro[0]-7,y2=self.centro[1]-83,x3=self.centro[0]-7,y3=self.centro[1]-90,color=LIGHT_GRAY,batch=nave)
        self.trasera2 = pyglet.shapes.Triangle(x=self.centro[0]+11,y=self.centro[1]-83,x2=self.centro[0]+7,y2=self.centro[1]-83,x3=self.centro[0]+7,y3=self.centro[1]-90,color=LIGHT_GRAY,batch=nave)
        self.trasera3 = pyglet.shapes.Rectangle(x=self.centro[0]-7,y=self.centro[1]-90,width=14,height=7,color=LIGHT_GRAY,batch=nave)
        self.canon1= pyglet.shapes.Rectangle(x=self.centro[0]+61,y=self.centro[1]-76,width=6,height=30,color= DARK_GRAY,batch=nave)
        self.canon2= pyglet.shapes.Rectangle(x=self.centro[0]-67,y=self.centro[1]-76,width=6,height=30,color= DARK_GRAY,batch=nave)
        self.canon3= pyglet.shapes.Rectangle(x=self.centro[0]+63,y=self.centro[1]-46,width=2,height=55,color=DARK_GRAY,batch=nave)
        self.canon4= pyglet.shapes.Rectangle(x=self.centro[0]-65,y=self.centro[1]-46,width=2,height=55,color=DARK_GRAY,batch=nave)
        self.canon5= pyglet.shapes.Triangle(x=self.centro[0]-65,y=self.centro[1],x2=self.centro[0]-70,y2=self.centro[1]+3,x3=self.centro[0]-65,y3=self.centro[1]+3,color=DARK_GRAY,batch=nave)
        self.canon6= pyglet.shapes.Triangle(x=self.centro[0]-63,y=self.centro[1],x2=self.centro[0]-58,y2=self.centro[1]+3,x3=self.centro[0]-63,y3=self.centro[1]+3,color=DARK_GRAY,batch=nave)
        self.canon7= pyglet.shapes.Triangle(x=self.centro[0]+65,y=self.centro[1],x2=self.centro[0]+70,y2=self.centro[1]+3,x3=self.centro[0]+65,y3=self.centro[1]+3,color=DARK_GRAY,batch=nave)
        self.canon8= pyglet.shapes.Triangle(x=self.centro[0]+63,y=self.centro[1],x2=self.centro[0]+58,y2=self.centro[1]+3,x3=self.centro[0]+63,y3=self.centro[1]+3,color=DARK_GRAY,batch=nave)
        self.cohete7= pyglet.shapes.Rectangle(x=self.centro[0]-23,y=self.centro[1]-93,width=7,height=2,color=(0,255,255),batch=nave)
        self.cohete1= pyglet.shapes.Rectangle(x=self.centro[0]-26,y=self.centro[1]-69,width=13,height=24,color=DARK_GRAY,batch=nave)
        self.cohete3= pyglet.shapes.Rectangle(x=self.centro[0]-23,y=self.centro[1]-91,width=7,height=24,color=DARK_GRAY,batch=nave)
        self.cohete2= pyglet.shapes.Rectangle(x=self.centro[0]-25,y=self.centro[1]-68,width=11,height=15,color=(145,145,145),batch=nave)
        self.cohete4= pyglet.shapes.Rectangle(x=self.centro[0]-22,y=self.centro[1]-86,width=5,height=18,color=(145,145,145),batch=nave)
        self.cohete5= pyglet.shapes.Triangle(x=self.centro[0]-23,y=self.centro[1]-91,x2=self.centro[0]-23,y2=self.centro[1]-87,x3=self.centro[0]-25,y3=self.centro[1]-87,color=DARK_GRAY,batch=nave)
        self.cohete6= pyglet.shapes.Triangle(x=self.centro[0]-16,y=self.centro[1]-91,x2=self.centro[0]-16,y2=self.centro[1]-87,x3=self.centro[0]-14,y3=self.centro[1]-87,color=DARK_GRAY,batch=nave)
        self.cohete71= pyglet.shapes.Rectangle(x=self.centro[0]+16,y=self.centro[1]-93,width=7,height=2,color=(0,255,255),batch=nave)
        self.cohete11= pyglet.shapes.Rectangle(x=self.centro[0]+13,y=self.centro[1]-69,width=13,height=24,color=DARK_GRAY,batch=nave)
        self.cohete31= pyglet.shapes.Rectangle(x=self.centro[0]+16,y=self.centro[1]-91,width=7,height=24,color=DARK_GRAY,batch=nave)
        self.cohete21= pyglet.shapes.Rectangle(x=self.centro[0]+14,y=self.centro[1]-68,width=11,height=15,color=(145,145,145),batch=nave)
        self.cohete41= pyglet.shapes.Rectangle(x=self.centro[0]+17,y=self.centro[1]-86,width=5,height=18,color=(145,145,145),batch=nave)
        self.cohete51= pyglet.shapes.Triangle(x=self.centro[0]+23,y=self.centro[1]-91,x2=self.centro[0]+23,y2=self.centro[1]-87,x3=self.centro[0]+25,y3=self.centro[1]-87,color=DARK_GRAY,batch=nave)
        self.cohete61= pyglet.shapes.Triangle(x=self.centro[0]+16,y=self.centro[1]-91,x2=self.centro[0]+16,y2=self.centro[1]-87,x3=self.centro[0]+14,y3=self.centro[1]-87,color=DARK_GRAY,batch=nave)
        self.cabina1= pyglet.shapes.Rectangle(x=self.centro[0]-4,y=self.centro[1]-48,width=8,height=36,color=BLACK,batch=nave)
        self.cabina2= pyglet.shapes.Triangle(x=self.centro[0]-5,y=self.centro[1]-48,x2=self.centro[0]-5,y2=self.centro[1]-8,x3=self.centro[0]-9,y3=self.centro[1]-48,color=BLACK,batch=nave)
        self.cabina3= pyglet.shapes.Triangle(x=self.centro[0]+5,y=self.centro[1]-48,x2=self.centro[0]+5,y2=self.centro[1]-8,x3=self.centro[0]+9,y3=self.centro[1]-48,color=BLACK,batch=nave)
        self.detalle1=pyglet.shapes.Rectangle(x=self.centro[0]-8,y=self.centro[1]-82,width=16,height=32,color=(130,130,130),batch=nave)
        self.detalle2=pyglet.shapes.Circle(x=self.centro[0],y=self.centro[1]-60,radius = 5,color=DARK_GRAY,batch=nave)
    
    def update(self,n):
        self.cohete7.y -= n
        self.cohete71.y -= n

class y_wing():
    def __init__(self,pos):
        self.centro= (pos[0],pos[1])
        self.cuerpo1=shapes.Rectangle(x=self.centro[0]-11,y=self.centro[1]-20,width=22,height=60,color=DARK_GRAY,batch=nave)
        self.cuerpo2=shapes.Rectangle(x=self.centro[0]-38,y=self.centro[1]-40,width=76,height=24,color=DARK_GRAY,batch=nave)
        self.cuerpo3=shapes.Rectangle(x=self.centro[0]-14, y=self.centro[1]-50,width=28,height=60,color=LIGHT_GRAY,batch=nave)
        self.cabina1=shapes.Triangle(x=self.centro[0]-11,y=self.centro[1]+35,x2=self.centro[0]-22,y2=self.centro[1]+38,x3=self.centro[0]-11,y3=self.centro[1]+38,color= LIGHT_GRAY, batch=nave)
        self.cabina2=shapes.Triangle(x=self.centro[0]+11,y=self.centro[1]+35,x2=self.centro[0]+22,y2=self.centro[1]+38,x3=self.centro[0]+11,y3=self.centro[1]+38,color= LIGHT_GRAY, batch=nave)
        self.cabina3=shapes.Rectangle(x=self.centro[0]-11,y=self.centro[1]+35,width = 22,height= 50,color=LIGHT_GRAY,batch=nave)
        self.cabina4=shapes.Triangle(x=self.centro[0]-22,y=self.centro[1]+38,x2=self.centro[0]-11,y2=self.centro[1]+38,x3=self.centro[0]-11,y3=self.centro[1]+85,color=LIGHT_GRAY,batch=nave)
        self.cabina5=shapes.Triangle(x=self.centro[0]+22,y=self.centro[1]+38,x2=self.centro[0]+11,y2=self.centro[1]+38,x3=self.centro[0]+11,y3=self.centro[1]+85,color=LIGHT_GRAY,batch=nave)
        self.cabina6=shapes.Rectangle(x=self.centro[0]-7,y=self.centro[1]+85,width=3,height=13,color=DARK_GRAY,batch=nave)
        self.cabina7=shapes.Rectangle(x=self.centro[0]+4,y=self.centro[1]+85,width=3,height=13,color=DARK_GRAY,batch=nave)
        self.cabina8=shapes.Rectangle(x=self.centro[0]-6,y=self.centro[1]+40,width=12,height=32,color=DARK_GRAY,batch=nave)
        self.cabina9=shapes.Rectangle(x=self.centro[0]-9,y=self.centro[1]+40,width=18,height=18,color=DARK_GRAY,batch=nave)
        self.cabina10=shapes.Triangle(x=self.centro[0]-6,y=self.centro[1]+58,x2=self.centro[0]-6,y2=self.centro[1]+72,x3=self.centro[0]-9,y3=self.centro[1]+58,color=DARK_GRAY,batch= nave)
        self.cabina11=shapes.Triangle(x=self.centro[0]+6,y=self.centro[1]+58,x2=self.centro[0]+6,y2=self.centro[1]+72,x3=self.centro[0]+9,y3=self.centro[1]+58,color=DARK_GRAY,batch= nave)
        self.cabina12=shapes.Rectangle(x=self.centro[0]-5,y=self.centro[1]+60,width=10,height=10,color=BLACK,batch=nave)
        self.cabina13=shapes.Rectangle(x=self.centro[0]-8,y=self.centro[1]+42,width=2,height=17,color= BLACK,batch=nave)
        self.cabina14=shapes.Rectangle(x=self.centro[0]+6,y=self.centro[1]+42,width=2,height=17,color= BLACK,batch=nave)
        self.coheteAni=shapes.Rectangle(x=self.centro[0]-54,y=self.centro[1]-71,width=10,height=2,color=(0,255,255),batch=nave)
        self.cohete0=shapes.Rectangle(x=self.centro[0]-60, y=self.centro[1]-50,width=22,height=49,color=LIGHT_GRAY,batch=nave)
        self.cohete1=shapes.Circle(x=self.centro[0]-49,y=self.centro[1]-1,radius=11,color=LIGHT_GRAY,batch=nave)
        self.cohete2=shapes.Triangle(x=self.centro[0]-58, y=self.centro[1]-50,x2=self.centro[0]-54,y2=self.centro[1]-50,x3=self.centro[0]-54,y3=self.centro[1]-69,color=DARK_GRAY,batch=nave)
        self.cohete3=shapes.Triangle(x=self.centro[0]-40,y=self.centro[1]-50,x2=self.centro[0]-44,y2=self.centro[1]-50,x3=self.centro[0]-44,y3=self.centro[1]-69,color=DARK_GRAY,batch=nave)
        self.cohete4=shapes.Rectangle(x=self.centro[0]-54,y=self.centro[1]-69,width=10,height=19,color=DARK_GRAY,batch=nave)
        self.cohete5=shapes.Rectangle(x=self.centro[0]-60, y=self.centro[1]-105,width=2,height=55,color=LIGHT_GRAY,batch=nave)
        self.cohete6=shapes.Rectangle(x=self.centro[0]-40, y=self.centro[1]-105,width=2,height=55,color=LIGHT_GRAY,batch=nave)
        self.cohete7=shapes.Triangle(x=self.centro[0]-61,y=self.centro[1]-105,x2=self.centro[0]-56,y2=self.centro[1]-105,x3=self.centro[0]-56,y3=self.centro[1]-112,color= LIGHT_GRAY,batch=nave)
        self.cohete8=shapes.Triangle(x=self.centro[0]-37,y=self.centro[1]-105,x2=self.centro[0]-42,y2=self.centro[1]-105,x3=self.centro[0]-42,y3=self.centro[1]-112,color= LIGHT_GRAY,batch=nave)
        self.cohete9=shapes.Rectangle(x=self.centro[0]-56,y=self.centro[1]-112,width=14,height= 7,color= LIGHT_GRAY,batch=nave)
        self.coheteAni2=shapes.Rectangle(x=self.centro[0]+44,y=self.centro[1]-71,width=10,height=2,color=(0,255,255),batch=nave)
        self.cohete10=shapes.Rectangle(x=self.centro[0]+38, y=self.centro[1]-50,width=22,height=49,color=LIGHT_GRAY,batch=nave)
        self.cohete11=shapes.Circle(x=self.centro[0]+49,y=self.centro[1]-1,radius=11,color=LIGHT_GRAY,batch=nave)
        self.cohete12=shapes.Triangle(x=self.centro[0]+58, y=self.centro[1]-50,x2=self.centro[0]+54,y2=self.centro[1]-50,x3=self.centro[0]+54,y3=self.centro[1]-69,color=DARK_GRAY,batch=nave)
        self.cohete13=shapes.Triangle(x=self.centro[0]+40,y=self.centro[1]-50,x2=self.centro[0]+44,y2=self.centro[1]-50,x3=self.centro[0]+44,y3=self.centro[1]-69,color=DARK_GRAY,batch=nave)
        self.cohete14=shapes.Rectangle(x=self.centro[0]+44,y=self.centro[1]-69,width=10,height=19,color=DARK_GRAY,batch=nave)
        self.cohete15=shapes.Rectangle(x=self.centro[0]+58, y=self.centro[1]-105,width=2,height=55,color=LIGHT_GRAY,batch=nave)
        self.cohete16=shapes.Rectangle(x=self.centro[0]+38, y=self.centro[1]-105,width=2,height=55,color=LIGHT_GRAY,batch=nave)
        self.cohete17=shapes.Triangle(x=self.centro[0]+61,y=self.centro[1]-105,x2=self.centro[0]+56,y2=self.centro[1]-105,x3=self.centro[0]+56,y3=self.centro[1]-112,color= LIGHT_GRAY,batch=nave)
        self.cohete18=shapes.Triangle(x=self.centro[0]+37,y=self.centro[1]-105,x2=self.centro[0]+42,y2=self.centro[1]-105,x3=self.centro[0]+42,y3=self.centro[1]-112,color= LIGHT_GRAY,batch=nave)
        self.cohete19=shapes.Rectangle(x=self.centro[0]+42,y=self.centro[1]-112,width=14,height= 7,color= LIGHT_GRAY,batch=nave)

    def update(self,n):
        self.coheteAni.y -=n
        self.coheteAni2.y -=n

class estrella():
    def __init__(self,pos_x,pos_y,distancia):
        self.posx = pos_x
        self.posy = pos_y
        self.distancia = distancia
        color = WHITE
        self.width = 2
        self.speed = 1.44
        if distancia >=2:
            color = (250,250,200)
            self.speed = 1.2
            self.width = 1
        self.cuerpo0 = shapes.Line(x=pos_x-10/distancia,y=pos_y,x2=pos_x+10/distancia,y2=pos_y,width = self.width,color = color,batch = star)
        self.cuerpo1 = shapes.Line(x=pos_x,y=pos_y-10/distancia,x2=pos_x,y2=pos_y+10/distancia,width = self.width,color = color,batch = star)
        self.cuerpo2 = shapes.Line(x=pos_x-6/distancia,y=pos_y+6/distancia,x2=pos_x+6/distancia,y2=pos_y-6/distancia,width = self.width,color = color,batch = star)
        self.cuerpo3 = shapes.Line(x=pos_x+6/distancia,y=pos_y+6/distancia,x2=pos_x-6/distancia,y2=pos_y-6/distancia,width = self.width,color = color,batch = star)

    def update(self):
        self.posy -=self.speed
        self.cuerpo0.y -= self.speed
        self.cuerpo1.y -= self.speed
        self.cuerpo2.y -= self.speed
        self.cuerpo2.y2 -= self.speed
        self.cuerpo3.y -= self.speed
        self.cuerpo3.y2 -= self.speed
        pass


# LLAMADO DE OBJETOS
Lider = halcon()
Wing1 = x_wing((WIDTH//2-150,HEIGHT//2-250))
Wing2 = y_wing((WIDTH//2+150,HEIGHT//2-260))

for info in estrellas_i:
    if info[2]!=0:
        estrellas.append(estrella(info[0],info[1],info[2]))

i=0
n=1
# DIBUJAR OBJETOS
@window.event
def on_draw():
    global i 
    global n
    window.clear()
    # ANIMACION NAVES
    if i==10:
        i=0
        if n == 1:
            n = -1
            Wing1.update(n)
            Wing2.update(n)
            Lider.update(n)
        else:
            n=1
            Wing1.update(n)
            Wing2.update(n)
            Lider.update(n)
    # ELIMINACION DE ESTRELLAS Y CREACION DE UNA NUEVA
    for item in estrellas:
        if item.cuerpo0.y < -10:
            estrellas.remove(item)
            estrellas.append(estrella(np.random.randint(10,1190),1010,np.random.randint(1,3)))
    # MOVER ESTRELLAS
    for item in estrellas:
        item.update()
    star.draw()
    nave.draw()
    i+=1
pyglet.app.run()