from manim import *
import numpy as np


class Intro(Scene):
    def construct(self):
        brown = AnnularSector(inner_radius=1, outer_radius=2, angle=-PI / 2 * 3, start_angle=-PI / 2 * 3,
                              color=DARK_BROWN).shift(UP)
        blue = AnnularSector(inner_radius=1, outer_radius=2, angle=PI / 2, start_angle=PI / 2, color=DARK_BLUE).shift(
            UP)
        title = Text("3Brown1Blue", font_size=100).align_to(brown, DOWN).shift(DOWN)
        self.play(Write(title, run_time=2), Write(brown), Write(blue))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(brown), FadeOut(blue))


class Classroom(Scene):
    def __init__(
            self,
            renderer=None,
            camera_class=Camera,
            always_update_mobjects=False,
            random_seed=None,
            skip_animations=False,
    ):
        super().__init__(renderer, camera_class, always_update_mobjects, random_seed, skip_animations)
        self.stick = None
        self.atomtext = None
        self.whiteboard = None
        self.blue = None
        self.brown3 = None
        self.brown2 = None
        self.brown1 = None
        self.atom = None
        self.cartext = None

    def construct(self):
        self.brown1 = SVGMobject("static/sigmaBrown.svg", height=5)
        self.brown2 = SVGMobject("static/sigmaBrown.svg", height=5)
        self.brown3 = SVGMobject("static/sigmaBrown.svg", height=5)
        self.blue = SVGMobject("static/sigmaBlue.svg", height=5).flip()

        group = VGroup(self.brown1, self.brown2, self.brown3, self.blue).arrange(buff=0.5).move_to(DOWN * 5)

        self.whiteboard = Rectangle(width=10, height=5, fill_color=WHITE, fill_opacity=1).next_to(group, UP).shift(0.5*UP)
        self.atom = SVGMobject("static/atom.svg", height=2).align_to(self.whiteboard, UP).shift(DOWN)
        self.atomtext = Text('This is an atom.', color=BLACK).scale(1).next_to(self.atom, DOWN)
        self.cartext = Text('This is a CAR', color=BLACK).scale(1).next_to(self.atom, DOWN)

        dot_holder = Dot(fill_opacity=0).align_to(group, UP).shift((self.blue.width * 1.5 + 0.5) * RIGHT).shift(0.4 * LEFT)
        dot_text = Dot(fill_opacity=0)
        dot_text.set_x(dot_holder.get_center()[0])
        dot_text.set_y(dot_holder.get_center()[1])

        x = ValueTracker(dot_holder.get_center()[0])
        y = ValueTracker(dot_holder.get_center()[1])

        def newStick(obj: Mobject):
            dot_text.set_x(x.get_value())
            dot_text.set_y(y.get_value())
            obj.become(Line(dot_holder, dot_text, color=LIGHT_BROWN, stroke_width=10))

        self.stick = Line(dot_holder, dot_text, color=LIGHT_BROWN, stroke_width=10)


        self.play(
            FadeIn(group),
            *create_eyes(self.brown1, (self.brown1.width * 1.5 + 0.5) * LEFT),
            *create_eyes(self.brown2, 0.5 * LEFT),
            *create_eyes(self.brown3, (self.brown3.width * 0.5 + 0.5) * RIGHT),
            *create_eyes(self.blue, (self.blue.width * 1.5 + 0.5) * RIGHT, flip=True),
            FadeIn(self.whiteboard),
            FadeIn(self.atom),
            FadeIn(self.stick)
        )
        self.stick.add_updater(newStick)
        self.wait(0.5)
        self.play(x.animate.set_value(-self.atomtext.width / 2), y.animate.set_value(self.atomtext.get_center()[1] - 0.5))
        self.wait(0.5)
        self.play(Write(self.atomtext), x.animate.set_value(self.atomtext.width / 2))
        self.wait(0.5)

        confused_text = Text("?!!?!1?!?!!?!???", color=RED, font_size=50).next_to(group, UP).shift(0.2*UP)
        self.play(FadeIn(confused_text))
        self.play(FadeOut(confused_text))
        self.wait(0.5)

        self.play(y.animate.set_value(self.atomtext.get_center()[1] + 0.5), x.animate.set_value(self.atomtext.width / 2 + 0.5))
        self.play(Unwrite(self.atomtext), x.animate.set_value(-self.cartext.width / 2))

        self.play(Write(self.cartext), x.animate.set_value(self.cartext.width / 2))
        self.wait(0.5)

        confused_text = Text("I see", color=GREEN, font_size=50).next_to(group, UP).shift(0.2*UP)
        self.play(FadeIn(confused_text))
        self.play(FadeOut(confused_text))
        self.wait(0.5)


def create_eyes(obj, buffer, *, flip=False):
    left_eye = Circle(radius=0.1, color=WHITE, fill_opacity=1)
    right_eye = Circle(radius=0.1, color=WHITE, fill_opacity=1)

    group = VGroup(left_eye, right_eye).arrange(buff=0.2).align_to(obj, UP).shift(0.2 * UP).shift(buffer)

    left_eye_circle = Circle(radius=0.05, color=DARKER_GRAY, fill_opacity=1).align_to(group, UP).shift(buffer).shift((0.15 if not flip else 0.25) * LEFT)
    right_eye_circle = Circle(radius=0.05, color=DARKER_GRAY, fill_opacity=1).align_to(group, UP).shift(buffer).shift((0.15 if flip else 0.25) * RIGHT)

    return FadeIn(group), FadeIn(left_eye_circle), FadeIn(right_eye_circle)


class Overview(Scene):
    def construct(self):
        intro_title = Text("1. What is Car Theory?", color=WHITE, font_size=60)
        self.play(FadeIn(intro_title))
        self.wait(1)
        self.play(FadeOut(intro_title))


class Video(Scene):
    def construct(self):
        self.add_sound("static/sounds/Heartbeat.mp3")
        Intro.construct(self)
        Classroom.construct(self)

