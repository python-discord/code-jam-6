from kivy.animation import AnimationTransition

KEYFRAME = 0


class Trans(AnimationTransition):
    @staticmethod
    def trans(progress):
        global KEYFRAME
        return max(0, min(KEYFRAME, 1))

    def norm(progress):
        return progress + progress
