import turtle


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
mainLine = turtle.Turtle()
mainLine.speed(0)
mainLine.penup()
mainLine.shape("square")
mainLine.shapesize(stretch_wid= 10, stretch_len= 0.5)
mainLine.setheading(180)
mainLineSpeed = 20


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
    mainLine.speed(mainLineSpeed)
    mainLine.forward(10)


def moveBall():

    ########## LOGIC  ##########
    ball.time+=0.6
    s = (ball.u)*(ball.time) - 0.5*ball.g*(ball.time**2)


    ########## When ball hits ground again  ##########
    if s<0:
        ball.time = 0
        s=0
        height = ball.nextHeight
        if height!=-1:
            setVelocity(height)
            ball.nextHeight=-1
        else:   
            setVelocity(ball.jumpHeight/2)
    
    ball.sety(-90+s) #move ball to next position



############################# GAME ####################################
window.listen()

def exitGame():
    window.bye()

window.onkey(exitGame,'x')


#### Keypress [0-9] by user to change ball jump height ######
def setNextJump(n):
    # print(f"pressed {n}")
    ball.nextHeight=n*18

for num in range(10):
    window.onkeypress(lambda n=num: setNextJump(n), str(num))




while True:
    moveRight()
    moveBall()

    
    x=mainLine.xcor()
    # reset the mainLine to rightmost side
    if x < -windowWidth:
        mainLine.speed(0)
        mainLine.setx(windowWidth)


# turtle.done()
