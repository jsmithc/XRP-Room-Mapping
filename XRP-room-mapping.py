from XRPLib.defaults import *
import time

visited = set()
x,y = 0,0
Direction = 0
LEFT_BASE = 0.47 ## Initial motor powers based on visual
RIGHT_BASE = 0.485
ObjL = False
ObjR = False
turnTime = 1 ## Helpful later to fix proportional rotation accuracy

def move(turn):
    global x ,y , Direction
    drivetrain.turn(turn)
    drivetrain.set_effort(LEFT_BASE, RIGHT_BASE)
    drivetrain.stop()
    
    ## WIP - For mapping later on
    if Direction == 0:
        y+=1
    if Direction == (90 or -270):
        x+=1
    if Direction == (180 or -180):
        y-=1
    if Direction == (270 or -90):
        x-=1
    visited.add((x,y))
    print("Visited", x,y)
    print(Direction)
    
#def turn(target): ## Turns until target angle to fix motor inaccuracy, slowing when close to avoid overshooting. 
    #gyro.reset()
    #if gyro.getAngle() < target:
        #while gyro.getAngle() - target < 15:
           # drivetrain.set_effort(LEFT_BASE/2, -RIGHT_BASE/2)
        #while gyro.getAngle() < target:
           # drivetrain.set_effort(LEFT_BASE, -RIGHT_BASE)
   # else:
       # while gyro.getAngle() - target < 15:
       #     drivetrain.set_effort(-LEFT_BASE/2, RIGHT_BASE/2)
       # while gyro.getAngle() > target:
          #  drivetrain.set_effort(-LEFT_BASE, RIGHT_BASE)
        
            



    
def sense():
    global ObjL, ObjR
    print("Sensing right")
    drivetrain.turn(90)
    right = rangefinder.distance()
    print(rangefinder.distance())
    print("Sensing left")
    left = extra.distance()
    print(extra.distance())
    time.sleep(0.01)
    drivetrain.turn(-90)
    
    if right < 40:
        ObjR = True
        print("Obstacle on Right")
    else:
        ObjR = False
    if left < 40:
        ObjL = True
        print("Obstacle on Left")
    else:
        ObjL = False
    return(left, right)

def calibrate():
    gyro.reset()
    print("Calibrating")
    origin = gyro.getAngle() ## Always 0 since gyro just reset, but just to be safe
    drivetrain.set_effort(LEFT_BASE,RIGHT_BASE)
    time.sleep(1)
    drivetrain.stop()
    diff = gyro.getAngle() - origin ## Difference between actual and expected angle (0)
    print(diff)
    k = 0.05 ## Constant for proportional motor adjustment
    print("Adjusting left motor by ", diff * k * -1)
    LEFT_BASE -= diff * k
    print("Adjusting right motor by ", diff * k)
    RIGHT_BASE += diff * k
    
## MAIN ----------------------------------------------------------------------------------

calibrate()

while True:
    if rangefinder.distance() < 40:
        print("Obstacle ahead, sensing...")
        sense()
        if not ObjL:
            Direction -= 90
            print("Turning left")
            move(-90)
        elif not ObjR:
            Direction += 90
            print("Turning right")
            move(90)
        else:
            Direction += 180
            print("Turning around")
            move(180)
    else:
        print("Moving straight")
        move(0)
            
    while Direction > 360:
        Direction -= 360
    while Direction < -360:
        Direction +=360
    if Direction < 0:
        Direction = 360 + Direction
    
##TO-DO:
        ## Matrix display for mapping
            ## Intentional mapping / no backtracking
        ## Rotational correction/calibration using turnTime
        ## POIs / Routing
        ## Implement PI Controller for forward movement
        
        
        
        
            
        
    
    
    
    

