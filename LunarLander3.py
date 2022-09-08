# HIGH SCORES DO NOT EDIT:
# MKM 600
# ABC 500
# DEF 400
# GHI 300
# JKL 200
#
#   Final Project: Lunar Lander
#
#
#   WRITTEN BY (NAME & ANDREW ID): Matt Maciejewski mmacieje
#
#   15-110 section: I
#

import random
import math
from tkinter import *

def gameInit(canvas):
    ### This is stuff that resets on a new game ###
    canvas.data["score"] =0
    canvas.data["fuel"] = 1000.0
    canvas.data["timerCounter"] = 0
    levelInit(canvas)

def levelInit(canvas):
    ### This is stuff that resets on a new level ###
    canvas.data["landerX"] = 75
    canvas.data["landerY"] = 100
    canvas.data["landerAngle"] = 0
    canvas.data["flamer"] = 0
    canvas.data["zoom"] = False
    canvas.data["collided"] = False
    canvas.data["landed"] = False
    canvas.data["speedRight"] = 100
    canvas.data["speedDown"] = 0
    canvas.data["accelRight"] = 0
    canvas.data["accelDown"] = 0
    canvas.data["inputting"] = False
    canvas.data["nextLeveled"] = True
    generateTerrain(canvas)
    generateZoomRegion(canvas)
    redrawAll(canvas)
    timerFired(canvas)

def generateTerrain(canvas):
    ### This creates the list of the terrain by appending a list with the height, and then getting a new height by calling the getNextCoordinate function ###
    generatePatches(canvas)
    heightAndDelta = (25,3)
    terrain = []
    for i in range(101):
        terrain.append(heightAndDelta[0])
        temp = getNextCoordinate(canvas,heightAndDelta)
        heightAndDelta = temp
    canvas.data["groundHeights"] = terrain

def generateZoomRegion(canvas):
    ### This generates the region in which the game should zoom in if the lander is in
    groundHeights = canvas.data["groundHeights"]
    zoomRegionCoords = []
    for coordX in range(101):
        found = False
        for coordY in range(101):
            for z in range(27):
                if(0<=coordX+z-13<=100):
                    distance = math.sqrt(((z-13)*8)**2+(coordY*6-(600-groundHeights[coordX+z-13]*6))**2)
                    # Change 75 to change the size of the zoom region
                    if(distance<75 and not found):
                        found = True
                        zoomRegionCoords.append(coordY-1)
    canvas.data["zoomRegionCoords"] = zoomRegionCoords

def testDrawZoomRegion(canvas):
    zoomRegionCoords = canvas.data["zoomRegionCoords"]
    ### This draws the ground itself ###
    for step in range(100):
        canvas.create_line(step*8,zoomRegionCoords[step]*6,step*8+8,zoomRegionCoords[step+1]*6,fill="red")

def generatePatches(canvas):
    ### This generates 4 random patches of size 1-5, with no two patches being the same size with the location of the patches being randomly in a range of 10 at 20, 40, 60, and 80.
    patches = []
    sizes = [1,2,3,4,5]
    for i in range(4):
        x = random.randint(15,25)+20*i
        y = sizes.pop(random.randint(0,4-i))
        patches.append((x,y))
    canvas.data["patches"] = patches

def getNextCoordinate(canvas,coordinate):
    ### This function generates the next height based on delta, and then generates a new delta based on where the current height is based on the algorithm for regions and frequency of delta changes ###
    delta = coordinate[1]
    height = coordinate[0]+[-3,-2,-1,1,2,3][delta]
    x = random.random()
    count = 0
    if(41<height<51):
        if(x>0.5):
            if(x>0.6):
                count+=1
            count+=1
        count+=1
        ### The next 3 lines ensure it goes down if it goes above 47, making sure it never goes above 50 ###
        if(height>47):
            count = 1
            delta = 3
    elif(1<height<12):
        if(x>0.1):
            if(x>0.6):
                count+=1
            count+=1
        count+=1
        ### The next 3 lines ensure it goes up if it goes below 5, making sure it never goes below 2 (ensuring room for the multiplier) ###
        if(height<5):
            count = 2
            delta = 2
    elif(31<height<42):
        if(x>0.2):
            if(x>0.4):
                count+=1
            count+=1
        count+=1
    elif(11<height<22):
        if(x>0.2):
            if(x>0.4):
                count+=1
            count+=1
        count+=1
    elif(21<height<32 and delta>2):
        if(x>0.4):
            if(x>0.5):
                count+=1
            count+=1
        count+=1
    elif(21<height<32 and delta<3):
        if(x>0.1):
            if(x>0.5):
                count+=1
            count+=1
        count+=1
    if(count==1):
        delta = getNewDelta(canvas,delta,"low")
    elif(count==2):
        delta = getNewDelta(canvas,delta,"high")
    return (height,delta)
        
    

def getNewDelta(canvas,delta,highOrLow):
    ### Given a delta and if a higher or lower one is wanted, this randomly gives a new delta from the set of possible deltas (0-5) based on a set frequency of change in delta ###
    tier2Freqs = [[],[1],[.67,.33],[.5,.33,.17],[.45,.27,.18,.1],[.42,.26,.16,.11,.05]]
    x = random.random()
    if(highOrLow=="high"):
        num = 5-delta
    else:
        num = delta
    count = 1
    freq = 0
    for i in tier2Freqs[num]:
        freq += i
        if(x > freq):
            count += 1
    if(num==0):
        return delta
    elif(highOrLow=="high"):
        return delta+count
    else:
        return delta-count
    

def redrawAll(canvas):
    canvas.delete(ALL)
    drawText(canvas)
    if(not canvas.data["zoom"]):
        drawLander(canvas)
        drawGround(canvas)
        #testDrawZoomRegion(canvas)
    else:
        drawZoomedLander(canvas)
        drawZoomedGround(canvas)
    if canvas.data["collided"]:
        drawLandingText(canvas)
    if canvas.data["demo"] and canvas.data["demoBlink"]:
        canvas.create_text(400,500,text="Press any key to start.",fill="white",font=("courier",12))
    if canvas.data["demo"]:
        highScores = canvas.data["highScores"]
        canvas.create_text(400,115,text="HIGH SCORES",fill="white",font=("courier",14))
        for i in range(5):
            value = highScores[i][1]
            for zeros in range(4-len(value)):
                value = "0"+value
            text = highScores[i][0]+" "+value
            canvas.create_text(400,150+20*i,text=text,fill="white",font=("courier",14))
    if canvas.data["inputting"]:
        canvas.create_text(400,175,text="INPUT INITIALS",fill="white",font=("courier",14))
        
            

def drawText(canvas):
    score = int(canvas.data["score"])
    fuel = int(canvas.data["fuel"])
    textScore = str(score)
    textFuel = str(fuel)
    vSpeed = int(abs(canvas.data["speedDown"]))    
    hSpeed = int(abs(canvas.data["speedRight"]))
    ### Put leading zeros on score and fuel ###
    for i in range(4-len(str(score))):
        textScore = "0" + textScore
    for i in range(4-len(str(fuel))):
        textFuel = "0" + textFuel
    ### Determine sign on velocities ###
    if(canvas.data["speedRight"]>=0):
        hAngle = 0
    else:
        hAngle = math.pi
    if(canvas.data["speedDown"]>=0):
        vAngle = math.pi/2
    else:
        vAngle = math.pi*3/2
    ### Draw the text ###
    canvas.create_text(100,45,text="SCORE",fill="white",font=("courier",10))
    canvas.create_text(150,45,text=textScore,fill="white",font=("courier",10))
    canvas.create_text(95,65,text="FUEL",fill="white",font=("courier",10))
    canvas.create_text(150,65,text=textFuel,fill="white",font=("courier",10))
    canvas.create_text(500,45,text="HORIZONTAL SPEED",fill="white",font=("courier",10))
    drawArrow(canvas,595,45,hAngle)
    canvas.create_text(615,45,text=hSpeed,fill="white",font=("courier",10))
    canvas.create_text(490,65,text="VERTICAL SPEED",fill="white",font=("courier",10))
    drawArrow(canvas,595,65,vAngle)
    canvas.create_text(615,65,text=vSpeed,fill="white",font=("courier",10))

def drawArrow(canvas,x,y,angle):
    canvas.create_line(-5*math.cos(angle)+x,-5*math.sin(angle)+y,5*math.cos(angle)+x,5*math.sin(angle)+y,fill="white")
    canvas.create_line(-5*math.sin(angle)+x,-5*math.cos(angle)+y,5*math.cos(angle)+x,5*math.sin(angle)+y,fill="white")
    canvas.create_line(5*math.sin(angle)+x,5*math.cos(angle)+y,5*math.cos(angle)+x,5*math.sin(angle)+y,fill="white")
    
def drawLander(canvas):
    ###
    zoom = canvas.data["zoom"]
    if(zoom):
        color = "red"
    else:
        color = "white"
    ###
    landerX = canvas.data["landerX"]
    landerY = canvas.data["landerY"]
    landerAngle = canvas.data["landerAngle"]
    flicker = canvas.data["flicker"]
    flamer = canvas.data["flamer"]
    ### This draws the jet ###
    if(flamer>0):
        canvas.create_line(landerX+flicker*math.cos(landerAngle),landerY-flicker*math.sin(landerAngle),landerX+(flamer+5.0)*math.sin(landerAngle),landerY+(flamer+5.0)*math.cos(landerAngle),fill="white")
        canvas.create_line(landerX-flicker*math.cos(landerAngle),landerY+flicker*math.sin(landerAngle),landerX+(flamer+5.0)*math.sin(landerAngle),landerY+(flamer+5.0)*math.cos(landerAngle),fill="white")
    ### This draws the lander itself ###
    canvas.create_line(landerX+3.0*math.cos(landerAngle),landerY-3.0*math.sin(landerAngle),landerX+6.0*math.sin(landerAngle+math.atan(3.0/5.0)),landerY+6.0*math.cos(landerAngle+math.atan(3.0/5.0)),fill=color)
    canvas.create_line(landerX-3.0*math.cos(landerAngle),landerY+3.0*math.sin(landerAngle),landerX+6.0*math.sin(landerAngle-math.atan(3.0/5.0)),landerY+6.0*math.cos(landerAngle-math.atan(3.0/5.0)),fill=color)
    canvas.create_oval(landerX-3,landerY-3,landerX+3,landerY+3,outline=color,fill="black")
    
def drawZoomedLander(canvas):
    landerAngle = canvas.data["landerAngle"]
    flicker = canvas.data["flicker"]
    flamer = canvas.data["flamer"]
    factor = 3
    ### This draws the jet ###
    if(flamer>0):
        canvas.create_line(400+flicker*math.cos(landerAngle)*factor,300-flicker*math.sin(landerAngle)*factor,400+(flamer+5.0)*math.sin(landerAngle)*factor,300+(flamer+5.0)*math.cos(landerAngle)*factor,fill="white")
        canvas.create_line(400-flicker*math.cos(landerAngle)*factor,300+flicker*math.sin(landerAngle)*factor,400+(flamer+5.0)*math.sin(landerAngle)*factor,300+(flamer+5.0)*math.cos(landerAngle)*factor,fill="white")
    ### This draws the lander itself ###
    canvas.create_line(400+3.0*math.cos(landerAngle)*factor,300-3.0*math.sin(landerAngle)*factor,400+6.0*math.sin(landerAngle+math.atan(3.0/5.0))*factor,300+6.0*math.cos(landerAngle+math.atan(3.0/5.0))*factor,fill="white")
    canvas.create_line(400-3.0*math.cos(landerAngle)*factor,300+3.0*math.sin(landerAngle)*factor,400+6.0*math.sin(landerAngle-math.atan(3.0/5.0))*factor,300+6.0*math.cos(landerAngle-math.atan(3.0/5.0))*factor,fill="white")
    canvas.create_oval(400-3*factor,300-3*factor,400+3*factor,300+3*factor,outline="white",fill="black")
    
def drawGround(canvas):
    groundHeights = canvas.data["groundHeights"]
    patches = canvas.data["patches"]
    patchLefts = []
    multipliers = []
    ### This puts the patches in the ground list and draws the score multiplier for it ###
    for patch in patches:
        for i in range(patch[1]):
            patchLefts.append(patch[0]+i)
        x = patch[0]*8+patch[1]*4
        y = 606-groundHeights[patch[0]]*6
        value = str(6-patch[1])+"X"
        multipliers.append(6-patch[1])
        canvas.create_text(x,y,text=value,fill="white",font=("courier",6))
    canvas.data["multipliers"] = multipliers
    ### This draws the ground itself ###
    for step in range(100):
        if(step in patchLefts):
            groundHeights[step+1]=groundHeights[step]
            canvas.create_line(step*8,600-groundHeights[step]*6,step*8+8,600-groundHeights[step+1]*6,fill="white")
        else:
            canvas.create_line(step*8,600-groundHeights[step]*6,step*8+8,600-groundHeights[step+1]*6,fill="white")

def drawZoomedGround(canvas):
    groundHeights = canvas.data["groundHeights"]
    patches = canvas.data["patches"]
    patchLefts = []
    landerX = canvas.data["landerX"]
    landerY = canvas.data["landerY"]
    factor = 3
    ### This puts the patches in the ground list and draws the score multiplier for it ###
    for patch in patches:
        for i in range(patch[1]):
            patchLefts.append(patch[0]+i)
        x = (patch[0]*8+patch[1]*4-landerX)*factor+400
        y = (606-groundHeights[patch[0]]*6-landerY)*factor+300
        value = str(6-patch[1])+"X"
        canvas.create_text(x,y,text=value,fill="white",font=("courier",6*factor))
    ### This draws the ground itself ###
    for step in range(100):
        if(step in patchLefts):
            groundHeights[step+1]=groundHeights[step]
            canvas.create_line((step*8-landerX)*factor+400,(600-groundHeights[step]*6-landerY)*factor+300,(step*8+8-landerX)*factor+400,(600-groundHeights[step+1]*6-landerY)*factor+300,fill="white")
        else:
            canvas.create_line((step*8-landerX)*factor+400,(600-groundHeights[step]*6-landerY)*factor+300,(step*8+8-landerX)*factor+400,(600-groundHeights[step+1]*6-landerY)*factor+300,fill="white")

def drawLandingText(canvas):
    if not canvas.data["demo"]:
        if canvas.data["didLand"] == "no":
            canvas.create_text(400,150,text="Game Over",fill="white",font=("courier",12))
            canvas.create_text(400,450,text="You crashed. Your ship was destroyed.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="0 Points",fill="white",font=("courier",12))
        elif canvas.data["didLand"] == "offscreen" :
            canvas.create_text(400,150,text="Game Over",fill="white",font=("courier",12))
            canvas.create_text(400,450,text="You strayed too far from the landing zones and crashed.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="0 Points",fill="white",font=("courier",12))
        elif canvas.data["didLand"] == "tooHigh" :
            canvas.create_text(400,150,text="Game Over",fill="white",font=("courier",12))
            canvas.create_text(400,450,text="You exceeded escape velocity and drifted off into space, never to be seen again.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="0 Points",fill="white",font=("courier",12))
        elif canvas.data["didLand"] == "vertSpeed" :
            canvas.create_text(400,150,text="Game Over",fill="white",font=("courier",12))
            canvas.create_text(400,450,text="You came down too fast. The landing gear was destroyed.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="0 Points",fill="white",font=("courier",12))
        elif canvas.data["didLand"] == "horiSpeed" :
            canvas.create_text(400,150,text="Game Over",fill="white",font=("courier",12))
            canvas.create_text(400,450,text="Your horizontal speed was too great. The landing gear was destroyed.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="25 Points",fill="white",font=("courier",12))
        elif canvas.data["didLand"] == "tooFast" :
            canvas.create_text(400,450,text="You came down too fast and ruptured your fuel tanks. 50% of your fuel was lost.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="%d Points"%(50*canvas.data["multiplier"]),fill="white",font=("courier",12))
            canvas.data["fuel"] = canvas.data["fuel"]/2
        elif canvas.data["didLand"] == "yes" :
            canvas.create_text(400,450,text="You had a successful landing.",fill="white",font=("courier",12))
            canvas.create_text(400,475,text="%d Points"%(100*canvas.data["multiplier"]),fill="white",font=("courier",12))
        canvas.create_text(400,500,text="Press any key to continue.",fill="white",font=("courier",12))
    canvas.after(6000, nextRound, canvas)

def nextRound(canvas):
    if not canvas.data["nextLeveled"]:
        canvas.data["nextLeveled"] = True
        if not canvas.data["demo"]:
            if(canvas.data["didLand"]=="no" or canvas.data["didLand"]=="offscreen" or canvas.data["didLand"]=="tooHigh" or canvas.data["didLand"]=="vertSpeed" or canvas.data["didLand"]=="horiSpeed"):
                if canvas.data["didLand"]=="horispeed":
                    canvas.data["score"] += 25
                addNewHighScore(canvas)
            elif canvas.data["didLand"] == "vertSpeed":
                addNewHighScore(canvas)
            elif canvas.data["didLand"] == "horiSpeed":
                addNewHighScore(canvas)
            elif canvas.data["didLand"] == "tooFast":
                canvas.data["score"] += 50*canvas.data["multiplier"]
                levelInit(canvas)
            else:
                canvas.data["score"] += 100*canvas.data["multiplier"]
                levelInit(canvas)
        else:
            gameInit(canvas)

def getNewLanderCoordinate(canvas):
    canvas.data["landerX"] += canvas.data["speedRight"]/100
    canvas.data["landerY"] += canvas.data["speedDown"]/100

def getNewLanderVelocity(canvas):
    canvas.data["speedRight"] += canvas.data["accelRight"]/10
    canvas.data["speedDown"] += canvas.data["accelDown"]/10

def getNewLanderAcceleration(canvas):
    canvas.data["accelDown"] = 10-math.cos(canvas.data["landerAngle"])*3*canvas.data["flamer"]-canvas.data["speedDown"]/50
    canvas.data["accelRight"] = -math.sin(canvas.data["landerAngle"])*3*canvas.data["flamer"]-canvas.data["speedRight"]/50

def isZoom(canvas):
    index = int(canvas.data["landerX"]/8)
    if(canvas.data["landerY"]/6<canvas.data["zoomRegionCoords"][index] or canvas.data["landerY"]/6<canvas.data["zoomRegionCoords"][index+1]):
        canvas.data["zoom"] = False
    else:
        canvas.data["zoom"] = True

def hasCollided(canvas):
    x1 = canvas.data["landerX"]+6.0*math.sin(canvas.data["landerAngle"]+math.atan(3.0/5.0))
    y1 = canvas.data["landerY"]+6.0*math.cos(canvas.data["landerAngle"]+math.atan(3.0/5.0))
    x2 = canvas.data["landerX"]+6.0*math.sin(canvas.data["landerAngle"]-math.atan(3.0/5.0))
    y2 = canvas.data["landerY"]+6.0*math.cos(canvas.data["landerAngle"]-math.atan(3.0/5.0))
    groundHeights = canvas.data["groundHeights"]

    lowX1 = int(x1/8.0)
    groundY1 = 600-((x1 - lowX1*8)/8.0*(groundHeights[lowX1+1]-groundHeights[lowX1])*6+groundHeights[lowX1]*6)
    lowX2 = int(x2/8.0)
    groundY2 = 600-((x2 - lowX2*8)/8.0*(groundHeights[lowX2+1]-groundHeights[lowX2])*6+groundHeights[lowX2]*6)
    
    if (y1 >= groundY1 or y2 >= groundY2):
        canvas.data["collided"] = True
        canvas.data["nextLeveled"] = False
        canvas.data["didLand"] = "no"
        if (y1==y2 and groundY1==groundY2):
            getPatchMultiplier(canvas)
            didLand(canvas)

def didLand(canvas):
    if(abs(canvas.data["speedDown"])>50):
        canvas.data["didLand"] = "vertSpeed"
    elif(abs(canvas.data["speedRight"])>=1):
        canvas.data["didLand"] = "horiSpeed"
    elif(abs(canvas.data["speedDown"])>20):
        canvas.data["didLand"] = "tooFast"
    else:
        canvas.data["didLand"] = "yes"

def getPatchMultiplier(canvas):
    multipliers = canvas.data["multipliers"]
    index = 0
    for i in [240,400,560]:
        if canvas.data["landerX"]>i :
            index += 1
    canvas.data["multiplier"] = multipliers[index]

def loadHighScores(canvas):
    fileHandler = open("LunarLander3.py","rt")
    text = fileHandler.readlines()
    fileHandler.close()
    highScores = []
    for i in [1,2,3,4,5]:
        highScores.append((text[i][2:5],text[i][6:-1]))
    canvas.data["highScores"]=highScores

def saveHighScores(canvas):
    fileHandler = open("LunarLander3.py","rt")
    code = fileHandler.readlines()
    fileHandler.close()

    for line in [1,2,3,4,5]:
        text = "# "+canvas.data["highScores"][line-1][0]+" "+canvas.data["highScores"][line-1][1]+"\n"
        code[line] = text
    
    fileHandler = open("LunarLander3.py","wt")
    fileHandler.writelines(code)
    fileHandler.close()

def addNewHighScore(canvas):
    canvas.data["collided"]=True
    x = canvas.data["score"]
    y = int(canvas.data["highScores"][4][1])
    if (x > y):
        canvas.data["inputting"] = True
        canvas.data["initialBlink"] = True
        canvas.data["initialIndex"] = 0
        getInitials(canvas)
           
    else:
        canvas.data["demo"] = True
        gameInit(canvas)

def getInitials(canvas):
    canvas.data["initialBlink"] = not canvas.data["initialBlink"]
    redrawAll(canvas)

    if canvas.data["initialIndex"] == 0:
        if canvas.data["initialBlink"]:
            canvas.create_text(385,200,text=chr(canvas.data["letterInput"]),fill="white",font=("courier",14))
    elif canvas.data["initialIndex"] == 1:
        if canvas.data["initialBlink"]:
            canvas.create_text(400,200,text=chr(canvas.data["letterInput"]),fill="white",font=("courier",14))
        canvas.create_text(385,200,text=canvas.data["letter1"],fill="white",font=("courier",14))
    elif canvas.data["initialIndex"] == 2:
        if canvas.data["initialBlink"]:
            canvas.create_text(415,200,text=chr(canvas.data["letterInput"]),fill="white",font=("courier",14))
        canvas.create_text(385,200,text=canvas.data["letter1"],fill="white",font=("courier",14))
        canvas.create_text(400,200,text=canvas.data["letter2"],fill="white",font=("courier",14))

    canvas.data["initials"] = canvas.data["letter1"]+canvas.data["letter2"]+canvas.data["letter3"]
    if canvas.data["inputting"]:
        canvas.after(500,getInitials,canvas)
    else:
        canvas.data["highScores"] = canvas.data["highScores"][:-1]
        index = 4
        score = canvas.data["score"]
        for i in range(4):
            if score>int(canvas.data["highScores"][i][1]):
                index -= 1
        canvas.data["highScores"] = canvas.data["highScores"][:index]+[(canvas.data["initials"],str(score))]+canvas.data["highScores"][index:]
        saveHighScores(canvas)
        canvas.data["demo"] = True
        gameInit(canvas)

def timerFired(canvas):        
    timerCounter = canvas.data["timerCounter"]
    canvas.data["timerCounter"]+=1
    canvas.data["timerCounter"]=canvas.data["timerCounter"]%12
    if(timerCounter%3==0):
        if(canvas.data["flicker"]==2.0):
            canvas.data["flicker"]-=1
        else:
            canvas.data["flicker"]+=1
        canvas.data["demoBlink"] = not canvas.data["demoBlink"]
    getNewLanderCoordinate(canvas)
    getNewLanderVelocity(canvas)
    getNewLanderAcceleration(canvas)
    if (canvas.data["landerX"]<0 or canvas.data["landerX"]>800):
        canvas.data["collided"] = True
        canvas.data["nextLeveled"] = False
        canvas.data["didLand"] = "offscreen"
    elif (canvas.data["landerY"]<-10):
        canvas.data["collided"] = True
        canvas.data["nextLeveled"] = False
        canvas.data["didLand"] = "tooHigh"
    canvas.data["fuel"] -= canvas.data["flamer"]/7.5
    isZoom(canvas)
    if canvas.data["zoom"]:
        hasCollided(canvas)
    redrawAll(canvas)
    delay = 100
    if not canvas.data["collided"]:
        canvas.after(delay, timerFired, canvas)
    if(canvas.data["fuel"]<0):
        canvas.data["fuel"]=0
        canvas.data["flamer"]=0

def keyPressed(event):
    canvas = event.widget.canvas
    if canvas.data["inputting"]:
        if(event.keysym == "Up" or event.keysym == "Left"):
            canvas.data["letterInput"] -= 1
            if canvas.data["letterInput"] == 64:
                canvas.data["letterInput"] = 90
        elif(event.keysym == "Down" or event.keysym == "Right"):
            canvas.data["letterInput"] += 1
            if canvas.data["letterInput"] == 91:
                canvas.data["letterInput"] = 65
        else:
            if canvas.data["initialIndex"]==0:
                canvas.data["letter1"] = chr(canvas.data["letterInput"])
            elif canvas.data["initialIndex"]==1:
                canvas.data["letter2"] = chr(canvas.data["letterInput"])
            elif canvas.data["initialIndex"]==2:
                canvas.data["letter3"] = chr(canvas.data["letterInput"])
                canvas.data["inputting"] = False
            canvas.data["initialIndex"] += 1
    elif canvas.data["demo"]:
        canvas.data["demo"] = False
        gameInit(canvas)
    elif not canvas.data["nextLeveled"]:
        nextRound(canvas)
    elif (int(canvas.data["fuel"])>0):
        if(event.keysym == "Up"):
            if(canvas.data["flamer"]<10):
                canvas.data["flamer"]+=1
        elif(event.keysym == "Down"):
            if(canvas.data["flamer"]>0):
                canvas.data["flamer"]-=1
        elif(event.keysym == "Left"):
            canvas.data["landerAngle"]+=math.pi/20
            canvas.data["fuel"] -= 0.2
        elif(event.keysym == "Right"):
            canvas.data["landerAngle"]-=math.pi/20
            canvas.data["fuel"] -= 0.2

def run():
    root = Tk()
    canvas = Canvas(root, width=800, height=600, bg="black")
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas
    canvas.data = {}

    canvas.data["flicker"] = 2.0
    canvas.data["demo"] = True
    canvas.data["demoBlink"] = True
    canvas.data["letterInput"] = 65
    canvas.data["letter1"] = "A"
    canvas.data["letter2"] = "A"
    canvas.data["letter3"] = "A"
    loadHighScores(canvas)
    
############### TEST
   
    

############### /TEST
    
    gameInit(canvas)
    root.bind("<Key>", keyPressed)
    root.mainloop()



run()
