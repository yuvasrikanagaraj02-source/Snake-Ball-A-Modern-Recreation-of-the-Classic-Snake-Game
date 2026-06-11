"""
GAME 5: SNAKE BALL
- Control the head ball with your mouse
- Collect glowing orbs to grow a longer chain of balls
- Avoid hitting your own tail!
- Also avoid the red obstacle balls that bounce around
- Longer chain = more score per orb collected
"""

import cv2
import numpy as np
import random
import math

W, H = 600, 600
SEGMENT_R = 10
SEGMENT_DIST = 24
ORBS_ON_SCREEN = 3

mx, my = float(W//2), float(H//2)

def mouse_cb(event, x, y, flags, param):
    global mx, my
    mx, my = float(x), float(y)

cv2.namedWindow("Game 5 - Snake Ball")
cv2.setMouseCallback("Game 5 - Snake Ball", mouse_cb)

SEGMENT_COLORS = [
    (120,100,255),(140,120,255),(160,140,255),(180,160,255),(200,180,255)
]

def new_orb():
    margin = 30
    cols = [(60,255,180),(255,200,60),(60,200,255),(255,120,200)]
    c = random.choice(cols)
    return {
        'x': float(random.randint(margin, W-margin)),
        'y': float(random.randint(margin, H-margin)),
        'r': 10,
        'color': c,
        'pulse': random.uniform(0, math.pi*2),
        'val': 1
    }

def new_obstacle():
    r = random.randint(10,18)
    return {
        'x': float(random.randint(r,W-r)),
        'y': float(random.randint(r,H-r)),
        'vx': random.choice([-1,1])*random.uniform(1.5,3.5),
        'vy': random.choice([-1,1])*random.uniform(1.5,3.5),
        'r': r
    }

def draw_segment(frame, x, y, r, color, idx, total):
    t = idx/max(1,total)
    bright = tuple(int(c*(1-t*0.5)) for c in color)
    cv2.circle(frame,(int(x),int(y)),r,bright,-1)
    if idx == 0:  # head
        cv2.circle(frame,(int(x),int(y)),r,(220,210,255),2)
        cv2.circle(frame,(int(x)-r//3,int(y)-r//3),r//3,(255,255,255),-1)
    else:
        cv2.circle(frame,(int(x),int(y)),r,(100,80,180),1)

def draw_orb(frame, o, tick):
    x,y=int(o['x']),int(o['y'])
    pulse = 1+0.18*math.sin(tick*0.1+o['pulse'])
    r=int(o['r']*pulse)
    cv2.circle(frame,(x,y),r+6,tuple(int(c*0.25) for c in o['color']),-1)
    cv2.circle(frame,(x,y),r,o['color'],-1)
    cv2.circle(frame,(x-r//3,y-r//3),r//3,(255,255,255),-1)

def draw_obstacle(frame, o, tick):
    x,y=int(o['x']),int(o['y'])
    spin=tick*0.07
    for i in range(3):
        a=spin+i*2*math.pi/3
        ex=x+int(math.cos(a)*o['r'])
        ey=y+int(math.sin(a)*o['r'])
        cv2.circle(frame,(ex,ey),o['r']//3,(80,60,200),-1)
    cv2.circle(frame,(x,y),o['r']-3,(50,40,160),-1)
    cv2.circle(frame,(x,y),o['r'],(100,80,220),2)

def draw_hud(frame, score, length, level):
    cv2.rectangle(frame,(0,0),(W,44),(18,14,30),-1)
    cv2.putText(frame,f"SCORE: {score}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(160,130,255),2)
    cv2.putText(frame,f"LEN: {length}",(W//2-30,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(160,130,255),2)
    cv2.putText(frame,f"LEVEL: {level}",(W-130,30),cv2.FONT_HERSHEY_SIMPLEX,0.65,(160,130,255),2)

def draw_particles(frame, particles):
    for p in particles:
        cv2.circle(frame,(int(p['x']),int(p['y'])),max(1,int(3*p['life'])),p['color'],-1)

def spawn_particles(x, y, color, n=10):
    pts=[]
    for _ in range(n):
        a=random.uniform(0,2*math.pi); s=random.uniform(1,5)
        pts.append({'x':float(x),'y':float(y),'vx':math.cos(a)*s,'vy':math.sin(a)*s,'color':color,'life':1.0})
    return pts

# Snake: list of (x,y) positions — index 0 = head
INIT_LEN = 5
segments = [(float(W//2 - i*SEGMENT_DIST), float(H//2)) for i in range(INIT_LEN)]
orbs = [new_orb() for _ in range(ORBS_ON_SCREEN)]
obstacles = [new_obstacle() for _ in range(2)]
particles = []
score = 0
level = 1
game_over = False
best = 0
tick = 0
grow_pending = 0
HEAD_SPEED = 4.5

while True:
    frame = np.zeros((H,W,3),dtype=np.uint8)
    cv2.rectangle(frame,(0,0),(W,H),(14,10,22),-1)
    for gx in range(0,W,50): cv2.line(frame,(gx,0),(gx,H),(20,14,32),1)
    for gy in range(0,H,50): cv2.line(frame,(0,gy),(W,gy),(20,14,32),1)

    if game_over:
        cv2.rectangle(frame,(100,190),(500,410),(20,14,40),-1)
        cv2.rectangle(frame,(100,190),(500,410),(140,100,255),2)
        cv2.putText(frame,"GAME OVER",(155,270),cv2.FONT_HERSHEY_SIMPLEX,1.4,(140,100,255),3)
        cv2.putText(frame,f"Score: {score}",(185,318),cv2.FONT_HERSHEY_SIMPLEX,0.9,(180,160,255),2)
        cv2.putText(frame,f"Best:  {best}",(205,358),cv2.FONT_HERSHEY_SIMPLEX,0.8,(100,80,180),2)
        cv2.putText(frame,"R=Restart   Q=Quit",(155,400),cv2.FONT_HERSHEY_SIMPLEX,0.55,(80,60,140),1)
        cv2.imshow("Game 5 - Snake Ball",frame)
        key=cv2.waitKey(30)&0xFF
        if key==ord('q'): break
        if key==ord('r'):
            segments=[(float(W//2-i*SEGMENT_DIST),float(H//2)) for i in range(INIT_LEN)]
            orbs=[new_orb() for _ in range(ORBS_ON_SCREEN)]
            obstacles=[new_obstacle() for _ in range(2)]
            particles=[]; score=0; level=1; game_over=False; tick=0; grow_pending=0
        continue

    tick+=1
    level = min(10, 1 + score//5)
    spd = HEAD_SPEED + level*0.2

    # Move head toward mouse (capped speed)
    hx,hy = segments[0]
    dx,dy = mx-hx, my-hy
    dist=math.sqrt(dx*dx+dy*dy)
    if dist>spd:
        hx+=dx/dist*spd; hy+=dy/dist*spd
    else:
        hx,hy=mx,my
    hx=max(SEGMENT_R,min(W-SEGMENT_R,hx))
    hy=max(44+SEGMENT_R,min(H-SEGMENT_R,hy))
    segments[0]=(hx,hy)

    # Follow chain
    for i in range(1,len(segments)):
        px,py=segments[i-1]
        cx,cy=segments[i]
        dx2,dy2=px-cx,py-cy
        d=math.sqrt(dx2*dx2+dy2*dy2)
        if d>SEGMENT_DIST:
            cx+=dx2/d*(d-SEGMENT_DIST)
            cy+=dy2/d*(d-SEGMENT_DIST)
        segments[i]=(cx,cy)

    # Grow
    if grow_pending>0:
        last=segments[-1]
        segments.append(last)
        grow_pending-=1

    # Orb collection
    for o in orbs[:]:
        dx2,dy2=hx-o['x'],hy-o['y']
        if math.sqrt(dx2*dx2+dy2*dy2)<SEGMENT_R+o['r']+2:
            particles+=spawn_particles(o['x'],o['y'],o['color'],16)
            score+=len(segments)
            grow_pending+=3
            orbs.remove(o)
            orbs.append(new_orb())

    # Tail self-collision (skip first 6 segments = buffer)
    for seg in segments[6:]:
        dx2,dy2=hx-seg[0],hy-seg[1]
        if math.sqrt(dx2*dx2+dy2*dy2)<SEGMENT_R*1.6:
            particles+=spawn_particles(hx,hy,(200,100,255),20)
            best=max(best,score); game_over=True; break

    # Obstacles
    for obs in obstacles:
        obs['x']+=obs['vx']; obs['y']+=obs['vy']
        if obs['x']<obs['r'] or obs['x']>W-obs['r']: obs['vx']*=-1
        if obs['y']<44+obs['r'] or obs['y']>H-obs['r']: obs['vy']*=-1
        dx2,dy2=hx-obs['x'],hy-obs['y']
        if math.sqrt(dx2*dx2+dy2*dy2)<SEGMENT_R+obs['r']:
            particles+=spawn_particles(hx,hy,(60,60,200),18)
            best=max(best,score); game_over=True; break

    # Particles
    for p in particles[:]:
        p['x']+=p['vx']; p['y']+=p['vy']; p['vy']+=0.12; p['life']-=0.04
        if p['life']<=0: particles.remove(p)

    draw_hud(frame,score,len(segments),level)
    for o in orbs: draw_orb(frame,o,tick)
    for obs in obstacles: draw_obstacle(frame,obs,tick)
    draw_particles(frame,particles)

    # Draw snake back to front
    for i in range(len(segments)-1,-1,-1):
        cidx=min(i,len(SEGMENT_COLORS)-1)
        draw_segment(frame,segments[i][0],segments[i][1],SEGMENT_R,
                     SEGMENT_COLORS[cidx],i,len(segments))

    # Draw line from head to mouse cursor
    cv2.line(frame,(int(hx),int(hy)),(int(mx),int(my)),(80,60,140),1)
    cv2.circle(frame,(int(mx),int(my)),5,(160,130,255),-1)

    cv2.imshow("Game 5 - Snake Ball",frame)
    key=cv2.waitKey(16)&0xFF
    if key==ord('q'): break

cv2.destroyAllWindows()
