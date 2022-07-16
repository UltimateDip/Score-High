import queue
import threading
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

# Scorebox
scoreBox = turtle.Turtle()
scoreBox.hideturtle()
scoreBox.penup()
scoreBox.speed(0)
scoreBox.setposition(100,200)
scoreStyle = ("Normal",20,"italic")
scoreValue = "Score High"
scoreBox.write(scoreValue,font=scoreStyle)


################ Jumping physics ###################### 

ball.jumpHeight = 0
ball.g = 9.81
ball.u = 0
ball.time = 0
ball.nextHeight = -1

def setVelocity(h):
    ball.u = (2*(ball.g)*h)**0.5    # u = root(2gh)
    ball.jumpHeight = h

##################### Update the scoreboard ####################
def updateScore(newScore):
    global scoreValue
    # If it is in initial state then simple set the new value
    if scoreValue=="Score High":
        scoreValue = newScore
    else: # else add the new value of score to existing score
        scoreValue += newScore

    # Currently using this condition for some perfomance improvement
    # without this if we don't do the check and run the clear() and 
    # write() in every updateScore() it seems it drops fps of our 
    # simulation. 

    ### THIS IS A TEMPORARY SOLUTION OF A SERIOUS PROBLEM. NEED TO ##
    ### FIND SOME ALTERNATIVE TO SOLVE THIS ISSUE ###################
    if scoreValue % 100 < 10 :
        scoreBox.clear()
        scoreBox.write(scoreValue,font=scoreStyle)


##################### Functionality ############################
def moveRight():
    # mainLine.speed(mainLineSpeed)
    mainLine.forward(10)
    x=mainLine.xcor()
    # reset the mainLine to rightmost side
    if x < -windowWidth:
        mainLine.speed(0)
        mainLine.setx(windowWidth)


def moveBall():

    ########## LOGIC  ##########
    ball.time+=0.5
    s = (ball.u)*(ball.time) - 0.5*(ball.g)*(ball.time**2)


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
    
    # -90 is currently y - coordinate of ground
    ball.sety(-90+s) #move ball to next position



############################# GAME ####################################
window.listen()

def exitGame():
    window.bye()

window.onkey(exitGame,'x')


#### Keypress [0-9] by user to change ball jump height ######
def setNextJump(n):
    # ground y coordinate = -90
    # ground y coordinate = +90
    # So total height for jump = 180px
    # So , 180 distance for 10key presses [0-9] = 180/10 = 18 is unit ratio

    # If we consider 10 as the total heigh
    # and if users presses 6, it should jump till 60%
    # which is (60% of 180px) 
    #           = 6*18 = (n*18)px
    ball.nextHeight=n*18



for num in range(10):
    window.onkeypress(lambda n=num: setNextJump(n), str(num))


############## Old main code for running the game ##############
# while True:
#     moveRight()
#     moveBall()

#     # update the scoreboard
#     updateScore(int(ball.time))
#     x=mainLine.xcor()
#     # reset the mainLine to rightmost side
#     if x < -windowWidth:
#         mainLine.speed(0)
#         mainLine.setx(windowWidth)





############## New code for running main game ##############

# Problem : We want that moveRight and moveBall functions runs simultaneouslu
# and independently of each other
# So, multithreading is one of the technique to do this.
# First I broke the actual while loop to 2 independent loop 
# one is in "moveRightHelper" and another is in "moveBallHelper"
# 
# Then using multithreading we can simutaneously run these codes


# These two queues will hold our upcoming moves 
mainLineQueue = queue.Queue(5)  # It holds recent 5 moves for mainLine
ballQueue = queue.Queue(5)  # It holds recent 5 moves for ball



# This functions pushes moveRight function to the queue "mainLineQueue" for 
# further processing. About this is mentioned below
# IT WILL RUN IN A SEPARATE THREAD
def moveRightHelper():
    while True:
        mainLineQueue.put(moveRight)

# Same thing is done by this function, moves the moveBall function to
# "ballQueue" queue
# IT WILL RUN IN A SEPARATE THREAD
def moveBallHelper():
    while True:
        ballQueue.put(moveBall)



# This is where main work is done

# In this process phase we'll process the functions waiting 
# for execution in queue mainLineQueue. 
# IT WILL RUN IN A SEPARATE THREAD
def processMainLineQueue():
    while mainLineQueue:
        (mainLineQueue.get())()
    
    # This is just a delay between query for slow systems 
    if threading.active_count() > 1:
        turtle.ontimer(processMainLineQueue,100)


# Same here for ball run the functions in queue one by one
# IT WILL RUN IN A SEPARATE THREAD
def processBallQueue():
    while ballQueue:
        (ballQueue.get())()
    
    if threading.active_count() > 1:
        turtle.ontimer(processBallQueue,100)



# These are the THREADS

# Currently There are FOUR THREADS
# t1    ->  Thread for moveRightHelper, it will queue recent moveRight functions for execution
# t2    ->  Thread for moveBallHelper, same as above but for the ball
# p1    ->  Thread for processing mainline queue, executes the functions created by t1
# p2    ->  Thread for processing ball queue, executes the functions created by t2

t1 = threading.Thread(target=moveRightHelper)
t1.daemon = True
t1.start()


t2 = threading.Thread(target=moveBallHelper)
t2.daemon = True
t2.start()


p1 = threading.Thread(target=processMainLineQueue)
p1.daemon= True
p1.start()


p2 = threading.Thread(target=processBallQueue)
p2.daemon= True
p2.start()


turtle.done()