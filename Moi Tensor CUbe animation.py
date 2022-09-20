#  Importing LIbraries Used to install use commands given
from turtle import Screen    # pip install tk
import pygame                # pip install pygame
import numpy as np           # pip install numpy
import sympy as sp           # pip install sympy
from numpy.linalg import eig
from math import cos,sin,pi

#                               //////////////////////////////// Usage ////////////////////////////////////////

#                   first the programm will ask the Mass of cube.
#                   After specifying the Mass it'll prompt user to enter side of the cube.
#                   After entering side you can see the animation of cube with interactable coordinates 

# 

# Input of Mass and Side
mass=float(input("Mass = "))
side=float(input("Side length ="))

# Colors Used in Pygame in RGB format

Green = (50,255,50)
Red = (255,0,0)
Blue = (50,50,255)
Color = [Red,Green,Blue]
gray = (50,50,50)
B1=(0,0,0)
W1=(200,200,200)


# Symbols Used by Sympy for Calculation of MOI Tensor.

x=sp.Symbol("x")
y=sp.Symbol("y")
z=sp.Symbol("z")
a=sp.Symbol("a")
m=sp.Symbol("m")

#  Rho i.e mass per unit Volume
rho = mass/a**3

# Since Cube is Symmetric i'm taking the origin as Center of Cube so these points are used as limits of integration.

Ux=a/2
Uy=a/2
Uz=a/2

Lx=-a/2
Ly=-a/2
Lz=-a/2

#  Integrator Function

def integral(integrand,var):
    return sp.integrate(integrand,var[0],var[1],var[2])

# Integration of MOI array 

Iarray=[   [  integral(y**2+z**2,[x,y,z]) , -integral(y*x,[x,y,z])        , -integral(x*z,[x,y,z])],
            [ -integral(y*x,[x,y,z])       ,  integral(y**2+z**2,[x,y,z])  , -integral(y*z,[x,y,z])],
            [-integral(x*z,[x,y,z])        , -integral(y*z,[x,y,z])        ,  integral(y**2+z**2,[x,y,z])  ] ]

#  Putting Upper and Lower limits in integrated functions

temp=[]
Isubarray=[]

for i in Iarray:
    
    for j in i:

        k=(j.subs([(x,Ux)])-j.subs([(x,Lx)]))  #Putting xlims
        l=(k.subs([(y,Uy)])-k.subs([(y,Ly)]))  #Putting ylims
        n=(l.subs([(z,Uz)])-l.subs([(z,Lz)]))  #Putting zlims
        n=n*rho                                 #multiplying density
        temp.append(n.subs([(a,side)]))
    Isubarray.append(temp)
    temp=[]
    k,l,n=0,0,0

Isubarray=np.array(Isubarray,dtype=float)
print(" Inertia Tensor " )
print(Isubarray)

val,vec=eig(Isubarray)
print("Principle axis ")
print(vec)
print(" Eigenvalue  ")
print(val)

# /////////////////////////////////// Cube ////////////////////////////

#  Setting up the width and Height of Program you can change it for changing window size.

width,height=600,600
gameDisplay=pygame.display.set_mode((width,height))
pygame.display.set_caption("Moment of inertia of Cube")         # Setting window title
pygame.font.init()                                              #initializing Font style to use in pygame


#  Functions Used for Drawing 3D cube on 2D surface

def X(x):
    return(x+width/2)

def Y(y):
    return(y+height/2)

def connect(a,b,LineVec):
    pygame.draw.line(gameDisplay,B1,(X(LineVec[a][0]),Y(LineVec[a][1])),( X(LineVec[b][0]),Y(LineVec[b][1])),5)
# 

#  Calculation of MOI vector

def Rvec(vec,theta):
    return np.array([ [cos(theta) + vec[0]**2*(1-cos(theta))  ,  vec[1]*vec[0]*(1-cos(theta)) - vec[2]*sin(theta)  ,  vec[0]*vec[2]*(1-cos(theta))+vec[1]*sin(theta) ],
             [  vec[1]*vec[0]*(1-cos(theta)) + vec[2]*sin(theta),  cos(theta) + vec[1]**2*(1-cos(theta))  ,  vec[1]*vec[2]*(1-cos(theta))-vec[0]*sin(theta) ], 
             [  vec[2]*vec[0]*(1-cos(theta)) - vec[1]*sin(theta)  ,  vec[1]*vec[2]*(1-cos(theta))+vec[0]*sin(theta) , cos(theta) + vec[2]**2*(1-cos(theta))   ]])

# Function for writing Text on Pygame window

def text_objects(text,font):
    textSurface=font.render(text,True,W1)
    return textSurface,textSurface.get_rect()

def Button(msg,x,y,w,h,ic,ac,H):

    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))

        if click[0]==True and H ==0:
            Xr()
        if click[0]==True and H ==1:
            Yr()
        if click[0]==True and H ==2:
            Zr()
    else :
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    smalltext = pygame.font.SysFont("comicsansms",20)
    textSurf,textRect = text_objects(msg,smalltext)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

def Banner(msg,Color,x,y,w,h):

    pygame.draw.rect(gameDisplay,Color,(x,y,w,h))
    smalltext = pygame.font.SysFont("comicsansms",20)
    textSurf,textRect = text_objects(msg,smalltext)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

def Xr():
    B.append(0)
    B.pop(0)
def Yr():
    B.append(1)
    B.pop(0)
def Zr():
    B.append(2)
    B.pop(0)


# Calculating points of cube by substituting mass and side value

ux,uy,uz,lx,ly,lz = Ux.subs(a,side),Uy.subs(a,side),Uz.subs(a,side),Lx.subs(a,side),Ly.subs(a,side),Lz.subs(a,side)

# Converting sides into Points for drawing in 3D space.
Point=[ 
        [   lx*100  ,  uy*100  ,  lz*100  ],
        [   ux*100  ,  uy*100  ,  lz*100  ],
        [   ux*100  ,  ly*100  ,  lz*100  ],
        [   lx*100  ,  ly*100  ,  lz*100  ],       
        [   lx*100  ,  uy*100  ,  uz*100  ],
        [   ux*100  ,  uy*100  ,  uz*100  ],
        [   ux*100  ,  ly*100  ,  uz*100  ],
        [   lx*100  ,  ly*100  ,  uz*100  ],
        [(ux+lx)/2 *100,(uy+ly)/2*100,(uz+lz)/2*100]
]

# Calculation Axes vector
Projectline = np.zeros((9,2))
theta =0 
Axes = [ [200,0,0 ], [0,200,0 ], [0,0,200 ]]
B = [0]

scale =1  # Change this if cube is too large or too small for your window.

# Pygame Loop to render Animation.

while True:

# /////////////////////////////////////////////////// Display Grid Setup ////////////////////////////
    H = B[-1]

    # Calculation of Projection Matrix i.e it is used to Project a 3D shape on 2D surface if you want to know more refrence with the video given in description.

    Projectionmatrix = [ [scale/(2)**(0.5),0,-scale/(2)**(0.5)], 
                         [scale/(6)**(0.5),2*scale/(6)**(0.5),scale/(6)**(0.5)]]

    # Drawing on Pygame Surface

    gameDisplay.fill(W1)
    Banner("Principle axis Vector",B1,25,50,200,50)
    Button("X axis",60,105,100,50,B1,Color[0],0)    
    Button("Y axis",60,160,100,50,B1,Color[1],1)    
    Button("Z axis",60,215,100,50,B1,Color[2],2)

    # Used for quitting out of Pygame if clicked on cross button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
 
    # Calculating and animating Rotation Vectors

    RotationX=[[1,0,0],[0,-cos(theta),-sin(theta)],[0,-sin(theta),cos(theta)]]
    RotationY=[[cos(theta),0,sin(theta)],[0,-1,0],[-sin(theta),0,cos(theta)]]
    RotationZ=[[cos(theta),-sin(theta),0],[sin(theta),cos(theta),0],[0,0,1]]
    NoRotation=[[1,0,0],[0,-1,0],[0,0,1]]

    # Updating the Projection Matrix and Rotation Matrix

    for i in range(len(Point)):

        Rotated2D = np.dot((Rvec(vec[:,H],theta)),Point[i])
        # Rotated2D = np.dot(RotationX,Point[i])
        # Rotated2D = np.dot(RotationY,Rotated2D)
        # Rotated2D = np.dot(RotationZ,Rotated2D)
        Projection2D =np.dot(Projectionmatrix,Rotated2D)
        pygame.draw.circle(gameDisplay,B1,(X(Projection2D[0]),Y(Projection2D[1])),10)
        Projectline[i] = Projection2D
    
    #  Making Cube with Projection Matrix
    
    for i in range(4):
        connect(i,(i+1)%4,Projectline)
        connect(i+4,((i+1)%4)+4,Projectline)
        connect(i,i+4,Projectline)

    # drawing axes of cubes
       
    for i in range(len(Axes)):   

        Rotated2D = np.dot(NoRotation,Axes[i])

        Projection2D =np.dot(Projectionmatrix,Rotated2D)
        pygame.draw.circle(gameDisplay,(0,30,255),(X(Projection2D[0]),Y(Projection2D[1])),10)
        pygame.draw.line(gameDisplay,Color[i],(X(0),Y(0)),(X(Projection2D[0]),Y(Projection2D[1])),5)
    
    # Drawing Circles on the end of vectors

    for i in range(len(vec)):
            
        Rotated2D = np.dot((Rvec(vec[:,H],theta)),vec[i]*100)
        # Rotated2D = np.dot((Rvec(np.linalg.norm(vec[:,H]),theta)),vec[i]*100)
        # Rotated2D = np.dot(RotationX,vec[i]*100)
        # Rotated2D = np.dot(RotationY,Rotated2D)
        # Rotated2D = np.dot(RotationZ,Rotated2D)
        Projection2D =np.dot(Projectionmatrix,Rotated2D)
        pygame.draw.line(gameDisplay,Color[i],(X(Projection2D[0]),Y(Projection2D[1])),(X(Projectline[-1][0]),Y(Projectline[-1][1])),5)
        pygame.draw.circle(gameDisplay,Color[i],(X(Projection2D[0]),Y(Projection2D[1])),10)
    
    # Updating Drawings on Display
     
    Banner("Principle MOI",B1,25,645-50,200,50)
    Banner('Ixx ='+str(round(val[0],4)),Color[0],50,650,150,30)    
    Banner('Iyy ='+str(round(val[1],4)),Color[1],50,685,150,30)    
    Banner('Izz ='+str(round(val[2],4)),Color[2],50,720,150,30)    

    #  incrementing theta with very small steps to make an animation i.e similar to delT.
    theta-=0.02

    # Updating the Pygame
    pygame.display.update()

#  Created By Harsh Maurya with 💖 ............ :)