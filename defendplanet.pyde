# Well, this program is considerably long for no reason at all
from random import randrange;
import math; 
WIDTH = 960;
HEIGHT = 960;
GENERATION_CONSTANT = 300;
TRAIL_DIAMETER = 50;
playerInput = [False, False, False, False]

playerX = WIDTH/2;
playerY = HEIGHT/2;
playerState = 'none';
circleR = 122;
circleG = 122;
circleB = 122;

planetX = WIDTH/2;
planetY = HEIGHT/2;

vSpeed = 2;
hSpeed = 2;
vVel = 0;
hVel = 0;

accel = 0.06;

asteroidXY = [];
asteroidCount = 0;
orbit = [];
orbitRadius = 70;
orbitAngle = radians(5);
orbitSpeed = 0.01;

difficulty = 1;
lives = 5;
gameState = 'start';
timer = 0;
difficultyTimer = 180;
score = 0;
ranOnce = 0;
ranOnceCollision = 0;
iframe = 0;
trailVFX = [];
asteroidTrail = [];

imgPlanet = loadImage("planet.png");
imgSpaceShip = loadImage("spaceship.png");
imgBackground = loadImage("background.png");
imgAsteroid = loadImage("asteroid.png");
imgOrbit = loadImage("orbit.png");

#Setup and load images, i load images twice since for some reason if you load them only in globals it doesn't work.
def setup():
    global imgPlanet, imgSpaceShip, imgBackground, imgAsteroid, imgOrbit;
    global asteroidXY, lives;
    imgPlanet = loadImage("planet.png");
    imgSpaceShip = loadImage("spaceship.png");
    imgBackground = loadImage("background.png");
    imgAsteroid = loadImage("asteroid.png");
    imgOrbit = loadImage("orbit.png");
    background(255);
    size(WIDTH,HEIGHT);
    #Frame rate 120 for a smoother experience
    frameRate(120);
        
def draw():
    global playerState, playerInput, playerX, playerY;
    global hVel, vVel;
    global difficulty, timer, difficultyTimer, lives, score; 
    global planetX, planetY;
    global imgPlanet, imgBackground;
    if lives <= 3 and lives > 0:
        background(0);
        imageMode(CORNER);
        image(imgBackground,0,0);
        ellipseMode(CENTER);
        imageMode(CENTER);
        fill(255,255,255,100);
        circle(planetX, planetY, 100);
        image(imgPlanet, planetX, planetY);
    
        trails();
        playerMovement();
        playerStateCheck();
        level();
        orbital();
        if timer >= difficultyTimer:
            asteroidGen();
            timer = 0;
        # print(asteroidXY);
        asteroids();
        collision();
        timer += 1;
    if lives == 5:
        fill(122,122,122,122);
        rect(0,0, WIDTH, HEIGHT);
        fill(255);
        textSize(30);
        textAlign(CENTER);
        text("Press Space to Start!", WIDTH/2, HEIGHT/2 - 50);
        textSize(20);
        text("Defend your home planet from asteroids!", WIDTH/2, HEIGHT/2-30);
    if lives <= 0:
        fill(122,122,122,122);
        rect(0,0, WIDTH, HEIGHT);
        fill(255);
        textSize(30);
        textAlign(CENTER);
        text("Game over! You defended your planet from a total of: ", WIDTH/2, HEIGHT/2 -50)
        text(str(score) + " Asteroids", WIDTH/2, HEIGHT/2 - 20);
        textSize(20);
        text('Press R to play again!', WIDTH/2, HEIGHT/2+10);
    
    # Debug Brick
    fill(255);
    textAlign(LEFT);
    textSize(12);
    text('State: ' + playerState, 20,20);
    debugHVEL = "%.2f" % hVel;
    debugVVEL = "%.2f" % vVel;
    text('Horizontal Velocity: ' + str(debugHVEL),20,30);
    text('Vertical Velocity: ' + str(debugVVEL),20,40);
    text('Key Pressed: ' + str(key),20,50);
    text('Difficulty: ' + str(difficulty),20,60);
    text('Lives: ' + str(lives), 20, 70);
    text('PlayerX: ' + str("%.1f" % playerX),20,80);
    text('PlayerY: ' + str("%.1f" % playerY), 20,90);
    text('Score: ' + str(score*100),20,100);
    
def playerMovement():
    global playerInput;
    global playerY, playerX;
    global vSpeed, hSpeed, hVel, vVel;
    global accel;
    global playerState;
    global circleR, circleG, circleB;
    global imgSpaceShip;
    
    hPLRMovement =  playerInput[1] - playerInput[0];
    vPLRMovement = playerInput[2] - playerInput[3];
    
    fill(circleR, circleG, circleB);    
    # Movement based on acceleration, doesn't really work as intended, but no idea how to fix. 
    # (If you accelerate left, and just as you hit the threshold for hSpeed, and hit right, you'll keep the velocity going right instead of slowly decelerating left before moving right.) 
    if hVel < hSpeed and hVel > -hSpeed:
        hVel += (hPLRMovement * accel);
    if (hVel >= hSpeed or hVel <= -hSpeed) and hPLRMovement != 0:
        hVel = hPLRMovement * hSpeed;   
    if hPLRMovement == 0 and (hVel > 0.0001 or hVel < -0.0001):
        hVel *= 0.98;
    if vVel < vSpeed and vVel > -vSpeed:
        vVel += (vPLRMovement * accel);
    if (vVel >= vSpeed or vVel <= -vSpeed) and vPLRMovement != 0:
        vVel = vPLRMovement * vSpeed;   
    if vPLRMovement == 0 and (vVel > 0.0001 or vVel < -0.0001):
        vVel *= 0.98;
        
    # Bounds Checking
    if playerX-25 < 0 or playerX+25 > WIDTH:
        hVel = -hVel;
    if playerY-25 < 0 or playerY+25 > HEIGHT:
        vVel = -vVel;
    playerX += hVel;
    playerY += vVel;  
    
    circle(playerX,playerY,50);
    imageMode(CENTER);
    image(imgSpaceShip, playerX, playerY);

# State checker and Key presses pretty much the same as the previous iteration.    
def playerStateCheck():
    global playerState, playerInput, playerX, playerY;
    if playerInput[0] == True:
        playerState = 'Left';
    if playerInput[1] == True:
        playerState = 'Right';
    if playerInput[2] == True:
        playerState = 'Down';
    if playerInput[3] == True:
        playerState = 'Up';
    
def keyPressed():
    global playerInput;
    global debugState, lives, difficultyTimer, asteroidXY, difficulty, score, asteroidXY, orbit, orbitRadius;
    if(keyCode == LEFT):
        playerInput[0] = True;
    if(keyCode == RIGHT):
        playerInput[1] = True;
    if(keyCode == DOWN):
        playerInput[2] = True;
    if(keyCode == UP):
        playerInput[3] = True; 
    if key == ' ':
        lives = 3;
    if key == 'r' or key == 'R':
        lives = 3;
        asteroidXY = [];
        orbit = [];
        orbitRadius = 70;
        difficulty = 1;
        difficultyTimer = 180;
        score = 0;
    if key == 't' or key == 'T':
        score += 1;

def keyReleased():
    global playerInput; 
    if(keyCode == LEFT):
        playerInput[0] = False;
    if(keyCode == RIGHT):
        playerInput[1] = False;
    if(keyCode == DOWN):
        playerInput[2] = False;
    if(keyCode == UP):
        playerInput[3] = False;  
        
# Movement of asteroids after spawning in the each of the 4 quads.     
def asteroids():
    global asteroidXY;
    global debugState;
    global imgAsteroid;
    counter = 0;
    fill(255);
    for x,y,m,quadNumber in asteroidXY:
        circle(x,y,20);
        image(imgAsteroid, x, y);
        counter += 1;
        # print(counter);
    for asteroid in asteroidXY:
        if asteroid[3] == 1:
            asteroid[1] += asteroid[2];
            asteroid[0] += 1;
        if asteroid[3] == 2:
            asteroid[1] += abs(asteroid[2]);
            asteroid[0] += -1;
        if asteroid[3] == 3:
            asteroid[1] +=  -1 * abs(asteroid[2]);
            asteroid[0] += 1;
        if asteroid[3] == 4:
            asteroid[1] += -1 * abs(asteroid[2]);
            asteroid[0] += -1;
# I wanted the asteroid gen to basically spawn asteroids in one of the four quads of a cartesian plane. For each quad there are two generation statements, essentially breaking the quads up into 8 parts.             
def asteroidGen():
    global lives, difficulty, asteroidCount, asteroidXY;   
    randomCase = randrange(0,7);
    # print(randomCase);
    # Top Left Quad
    if randomCase == 0 or randomCase == 1:
        if randomCase == 0:
            x = random(0, WIDTH/2);
            y = random(-GENERATION_CONSTANT, 0);
        if randomCase == 1:
            x = random(-GENERATION_CONSTANT, 0);
            y = random(-GENERATION_CONSTANT, HEIGHT/2);
        m = (y-(HEIGHT/2))/(x-(WIDTH/2));
        quadNumber = 1;
        asteroidXY.append([x,y,m,quadNumber])
    # Top Right Quad
    if randomCase == 2 or randomCase == 3:
        if randomCase == 2:
            x = random(WIDTH,WIDTH+GENERATION_CONSTANT);
            y = random(-GENERATION_CONSTANT, HEIGHT/2);
        if randomCase == 3:
            x = random(WIDTH/2, WIDTH);
            y = random(-GENERATION_CONSTANT, 0);
        m = (y-(HEIGHT/2))/(x - (WIDTH/2))
        quadNumber = 2;
        asteroidXY.append([x,y,m, quadNumber]);
    # Bottom Left Quad
    if randomCase == 4 or randomCase == 5:
        if randomCase == 4:
            x = random(-GENERATION_CONSTANT, 0);
            y = random(HEIGHT/2, HEIGHT + GENERATION_CONSTANT);
        if randomCase == 5:
            x = random(0, WIDTH/2);
            y = random(HEIGHT, HEIGHT + GENERATION_CONSTANT);
        quadNumber = 3;
        m = (y-(HEIGHT/2))/(x - (WIDTH/2));
        asteroidXY.append([x,y,m, quadNumber]);
    # Bottom Right Quad
    if randomCase == 6 or randomCase == 7:
        if randomCase == 6:
            x = random(WIDTH, WIDTH + GENERATION_CONSTANT);
            y = random(HEIGHT/2, HEIGHT + GENERATION_CONSTANT);
        if randomCase == 7:
            x = random(WIDTH/2, WIDTH);
            y = random(HEIGHT, HEIGHT + GENERATION_CONSTANT);
        quadNumber = 4;
        m = (y-(HEIGHT/2))/(x - (WIDTH/2));
        asteroidXY.append([x,y,m, quadNumber]);
    # Since asteroids with extreme angles relative to the center can spawn, this in turn increases the speed in which the projectile travels towards the center. So it regenerates the most recent asteroid if it's slope is over that of the difficulty    
    for x,y,m,q in asteroidXY:
        if abs(m) > difficulty:
            asteroidXY.pop(len(asteroidXY)-1);
            asteroidGen();    

def level():
    global lives, difficulty, difficultyTimer, score, ranOnce, playerX, playerY, orbitRadius;
    counter = 0;
    if score % 15 == 0 and score != 0 and ranOnce == 0:
        ranOnce += 1;
        difficulty += .5;
        if difficultyTimer >= 40:
            difficultyTimer += -20;
        orbitGen();
        orbitRadius += 20;
    if score % 15 != 0 and score != 0 and ranOnce != 0:
        ranOnce = 0;
# Two sets of collision, one for the planet and one for the Spaceship
def collision():
    global planetX, planetY, playerX, playerY;
    global asteroidXY;
    global lives, difficulty, score, ranOnceCollision;
    global circleR, circleG, circleB;
    global orbit, orbitRadius;
    counter = 0;
    ranOnceCollision += -1;
    for asteroid in asteroidXY:
        if asteroid[0] + 5 <= planetX + 50 and asteroid[0] - 5 >= planetX - 50:
            if asteroid[1] + 5 <= planetY + 50 and asteroid[0] - 5 >= planetX - 50:
                if len(orbit) == 0 and ranOnceCollision <= 0:
                    ranOnceCollision = 100;
                    lives += -1;
                if len(orbit) > 0:
                    orbitRadius += -20;
                    orbit.pop(len(orbit)-1);
    for x,y,m,q in asteroidXY:
        if x + 5 <= planetX + 50  and x - 5 >= planetX - 50:
            if y + 5 <= planetY + 50 and y - 5 >= planetY - 50:
                print('planet collision');
                asteroidXY.pop(counter);
        if x + 5 <= playerX + 50  and x - 5 >= playerX - 50:
            if y + 5 <= playerY + 50 and y - 5 >= playerY - 50:
                print('player collision');
                circleR = random(0,255);
                circleG = random(0,255);
                circleB = random(0,255);
                print(counter);
                asteroidXY.pop(counter);
                score += 1;
        counter += 1;
        
def orbital():
    global orbit, orbitRadius, orbitAngle, orbitSpeed, imgOrbit;
    noFill();
    stroke(255);
    ellipseMode(CENTER);
    if len(orbit) != 0:
        for x,y,r,a in orbit:
            noFill();
            stroke(255);
            circle(WIDTH/2,HEIGHT/2, r*2);
            image(imgOrbit, x, y);
        for orbits in orbit:
            orbits[0] = orbits[0] + cos(orbits[3] + math.pi/2) * orbitSpeed * (orbits[2]);
            orbits[1] = orbits[1] - sin(orbits[3] + math.pi/2) * orbitSpeed * (orbits[2]);
            orbits[3] += orbitSpeed;
            
def orbitGen():
    global orbit, orbitRadius, orbitAngle;
    orbitX = WIDTH/2 + orbitRadius;
    orbitY = HEIGHT/2;
    orbit.append([orbitX, orbitY, orbitRadius, radians(5)]);

# Honestly surprised VFX Trails are pretty easy.     
def trails():
    global playerX, playerY, trailVFX;
    trailVFX.append([playerX, playerY, TRAIL_DIAMETER,150]);
    noStroke();
    for trail in trailVFX:
        trail[2] += -0.5;
        trail[3] += -2;
        if trail[2] <= 5:
            trailVFX.pop(0);
    for x,y,s,a in trailVFX:
        fill(0,255,255,a)
        circle(x,y,s);

        
    
    
    
