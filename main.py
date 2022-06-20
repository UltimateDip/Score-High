import turtle
import random

##################### Window/Screen ###############################
window = turtle.Screen()
windowWidth,windowHeight = window.screensize()


##################### Main SET-UP #################################
# Two horizontal lines and working display
displaySize = 100

line1 = turtle.Turtle()
line1.speed(0)
line1.penup()
line1.sety(displaySize)
line1.shape("square")
line1.shapesize(stretch_wid=0.5,stretch_len=windowWidth/10)

line2 = turtle.Turtle()
line2.speed(0)
line2.penup()
line2.sety(-displaySize)
line2.shape("square")
line2.shapesize(stretch_wid=0.5,stretch_len=windowWidth/10)



# Vertical line with a gap in between to pass the ball
mainLine1=turtle.Turtle()
mainLine1.speed(0)
mainLine1.penup()
mainLine1.shape("square")
mainLine1.shapesize(stretch_wid=1, stretch_len= 0.5)
mainLine1.setheading(180)
mainLine1.setpos(0,0)
mainLineSpeed=20

mainLine2=turtle.Turtle()
mainLine2.speed(0)
mainLine2.penup()
mainLine2.shape("square")
mainLine2.shapesize(stretch_wid=1, stretch_len= 0.5)
mainLine2.setheading(180)
mainLine2.setpos(0,0)

# player
ball = turtle.Turtle()
ball.speed(0)
ball.penup()
ball.shape("circle")
ball.color("green")
ball.setposition(-50,-90)




################ Jumping physics ###################### 
# ball.velocity=10
ball.jumpHeight = 0
ball.g = 9.81
ball.u = 0
ball.time = 0
ball.nextHeight = -1

def setVelocity(h):
    ball.u = (2*(ball.g)*h)**0.5    # u = root(2gh)
    ball.jumpHeight = h




##################### Functionality ############################
def moveRight():
    # mainLine1.speed(mainLineSpeed)
    # mainLine2.speed(mainLineSpeed)
    mainLine1.forward(10)
    mainLine2.forward(10)
       

def createGapInMainLine(x):
    ratio=10/13 #mainline divided into 13 parts where 3 parts will be a gap, why 10? read the comment below.
    y=10-x; x*=ratio; y*=ratio
    mainLine1.setpos(mainLine1.xcor(), -0.5*(2*displaySize-21*x))
    mainLine2.setpos(mainLine2.xcor(), 0.5*(2*displaySize-21*y))
    mainLine1.shapesize(stretch_wid=x, stretch_len= 0.5)
    mainLine2.shapesize(stretch_wid=(10*ratio-x), stretch_len= 0.5) 
    #what is 10? distance b/w two lines=200, and turtle size=21, so we get 200/21 approximately 10
    


def moveBall():

    ########## LOGIC ##########
    ball.time+=0.5
    s = (ball.u)*(ball.time) - 0.5*ball.g*(ball.time**2)
    if s<0:
        ball.time=0
        s=0
        if ball.nextHeight!=-1:
            setVelocity(ball.nextHeight)
            ball.nextHeight=-1
        else:
            setVelocity(ball.jumpHeight/3)
    ball.sety(-90+s)

    
############################# GAME ####################################
window.listen()

def exitGame():
    window.bye()

window.onkey(exitGame,'x')

#### Keypress [0-9] by user to change ball jump height ######
def setNextJump(n):
    print(f"pressed {n}")
    ball.nextHeight=n*18

for num in range(10):
    window.onkeypress(lambda n=num: setNextJump(n), str(num))

createGapInMainLine(random.randint(1,9))

while True:
    moveRight()
    moveBall()

    x=mainLine1.xcor()
    # reset the mainLine
    if x < (-windowWidth):
        mainLine1.speed(0)
        mainLine1.setx(windowWidth)
        mainLine2.speed(0)
        mainLine2.setx(windowWidth)
        createGapInMainLine(random.randint(1,9))


# turtle.done()
