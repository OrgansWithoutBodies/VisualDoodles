import math
from manim import *

SCENE_SIZE = [1920/135, 1080/135]

NUM_CIRCLES = [20, 15]
# TODO calculate center based on these constraints
CENTER = [5, 3]
BOX_SIZE = [5, 10]

CIRCLE_SIZE_DIAM = 0.25

SPACING_BETWEEN_CIRCLES = 0.25

REGION_SIZE = [NUM_CIRCLES[0]*(CIRCLE_SIZE_DIAM+SPACING_BETWEEN_CIRCLES),
               NUM_CIRCLES[1]*(CIRCLE_SIZE_DIAM+SPACING_BETWEEN_CIRCLES)]


# return [ii-,jj-SCENE_SIZE[1],0]
CIRC = math.pi*2
C1 = CIRC
C2 = CIRC/2
C3 = CIRC/3
C4 = CIRC/4
C6 = CIRC/6
C8 = CIRC/8
C12 = CIRC/12
C16 = CIRC/16

SPEED = C8

D_RAD_D_X = 0
D_RAD_D_Y = 0

D_SPEED_D_X = C6
D_SPEED_D_Y = C6

# TODO can do some factorization here to figure out minimal number of times
TIMES_TO_LOOP = (CIRC/D_SPEED_D_X)/2 if D_SPEED_D_X == D_SPEED_D_Y else (CIRC /
                                                                         D_SPEED_D_X)*(CIRC/D_SPEED_D_Y)
#
SLOWEST_LOOPS_ONCE = (CIRC/SPEED)
ANIM_LEN = SLOWEST_LOOPS_ONCE*TIMES_TO_LOOP

# since this is meant as a mask generator, the only colors we expect are Black, White, and None
DOT_FILL = WHITE
RING_FILL = None
RING_STROKE = None
# MoveAlongPath


def get_circle_position(ii, jj):
    corner_pos = [
        ii*(CIRCLE_SIZE_DIAM+SPACING_BETWEEN_CIRCLES)+SPACING_BETWEEN_CIRCLES/2 -
        SCENE_SIZE[0]/2+CIRCLE_SIZE_DIAM/2,
        jj*(CIRCLE_SIZE_DIAM+SPACING_BETWEEN_CIRCLES) + SPACING_BETWEEN_CIRCLES/2 -
        SCENE_SIZE[1]/2+CIRCLE_SIZE_DIAM/2,
        0]
    return [corner_pos[0]+(SCENE_SIZE[0]-REGION_SIZE[0])/2, corner_pos[1]+(SCENE_SIZE[1]-REGION_SIZE[1])/2, 0]


def circleObject(center, diameter, dotInitialPhaseRadians, speed, timelineTracker):
    def updateCircle(d):
        d.move_to(getPositionAlongCircleOutside(
            center, diameter, (dotInitialPhaseRadians+timelineTracker.get_value()*speed) % (2*math.pi)))
    circleObjGroup = VGroup()
    ring = Circle(diameter/2, stroke_opacity=1 if RING_STROKE != None else 0, fill_opacity=1 if RING_FILL != None else 0).move_to(
        center)
    ring.set_stroke(RING_STROKE)
    ring.set_fill(RING_FILL)
    dot = Dot(getPositionAlongCircleOutside(
        center, diameter, dotInitialPhaseRadians))
    circleObjGroup.add(ring)
    circleObjGroup.add(dot)
    dot.set_fill(DOT_FILL)
    # print(speed)
    dot.add_updater(
        lambda d: updateCircle(d))
    return circleObjGroup


def getPositionAlongCircleOutside(center, diameter, dotInitialPhaseRadians):
    return [center[0]+math.sin(dotInitialPhaseRadians)*diameter/2,
            center[1]+math.cos(dotInitialPhaseRadians)*diameter/2, 0]


class GridWave(Scene):
    def construct(self):
        globalTimeline = ValueTracker(0)
        circleGroup = VGroup()
        for cx in range(NUM_CIRCLES[0]):
            for cy in range(NUM_CIRCLES[1]):
                circle = circleObject(get_circle_position(cx, cy), CIRCLE_SIZE_DIAM, (
                    D_RAD_D_X*cx+D_RAD_D_Y*cy), (SPEED+D_SPEED_D_X*cx+D_SPEED_D_Y*cy), globalTimeline)
                circleGroup.add(circle)
        self.add(circleGroup)
        self.add(globalTimeline)
        globalTimeline.add_updater(
            lambda mobject, dt: mobject.increment_value(dt))
        # subtract last frame so loops nicely, do here bc it doesnt matter the details of calculation so cleaner imo
        self.wait(ANIM_LEN - 1/60)
