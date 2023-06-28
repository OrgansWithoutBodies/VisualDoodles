import math
from manim import *

SCENE_SIZE = [1920/135, 1080/135]

NUM_CYCLES = 2
PEAK_HEIGHT = 2


class SineWave(Scene):
    def construct(self):
        globalTimeline = ValueTracker(0)

        ax = Axes(
            x_range=[0, math.pi],
            y_range=[0, 4],
            x_length=SCENE_SIZE[0]
        ).move_to([-1*math.pi, -2, 0])

        # curve_1 =
        # curve_1.add_updater(lambda: ax.plot(lambda x: 1 * np.sin((x+globalTimeline.get_value())*2)+3,
        #                                     x_range=[0, 4], color=WHITE))

        def buildArea(offset):
            print("test123", offset)
            return ax.get_area(
                # ax.plot(lambda x: PEAK_HEIGHT*np.sin(offset) * np.sin(x*2*NUM_CYCLES)+3.25,
                #         x_range=[0, 4], color=WHITE),   color=WHITE, opacity=1)
                ax.plot(lambda x: PEAK_HEIGHT * np.sin(x*2*NUM_CYCLES+offset)+3.25,
                        x_range=[0, 4], color=WHITE),   color=WHITE, opacity=1)
        area = buildArea(0)
        area.add_updater(lambda mobj:

                         mobj.become(buildArea(globalTimeline.get_value()
                                               )
                                     )
                         )

        globalTimeline.add_updater(
            lambda mobject, dt: mobject.increment_value(dt))

        self.add(area, globalTimeline)
        # Cursor to make sure we're centered
        # self.add(Line(
        #     [100, 0, 0], [-100, 0, 0], color=RED), Line(
        #     [0, 100,  0], [0, -100,  0], color=RED))
        self.wait(2*math.pi)
