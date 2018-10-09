from random import randint, choice
from math import gcd

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader

from time import strftime


class MathsApp(App):
    sw_started = False
    sw_seconds = 0
    result = ""
    symbol_set = "+-x/"
    count = 1
    correct = 0
    sound_correct = SoundLoader.load('correct.wav')
    sound_wrong = SoundLoader.load('wrong.wav')

    def update_time(self, nap):
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:[size=40]%S[/size]')

    def on_start(self):
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update, 0.016)
        self.root.ids.question.text = ""
        self.update_score()

    def update(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
            minutes, seconds = divmod(self.sw_seconds, 60)
            self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' % (int(minutes), int(seconds), int(seconds * 100 % 100)))

    def start_stop(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
            self.root.ids.question.text = ""
            self.count = 1
            self.correct = 0
            self.sw_seconds = 0
            minutes, seconds = divmod(self.sw_seconds, 60)
            self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' % (int(minutes), int(seconds), int(seconds * 100 % 100)))
        else:
            self.root.ids.start_stop.text = ('Start' if self.sw_started else 'Reset')
            self.sw_started = True
            self.get_question()

    def get_question(self):
        a = randint(-99, 99)
        while a % 10 == 0 or a in (-1, 0, 1):
            a = randint(-99, 99)
        b = randint(-99, 99)
        while b % 10 == 0 or b in (-1, 0, 1):
            b = randint(-99, 99)
        s = choice(self.symbol_set)
        if s == "+":
            self.result = str(a + b)
        elif s == "-":
            self.result = str(a - b)
        elif s == "x":
            self.result = str(a * b)
        else:
            self.result = "{}/{}".format(a // gcd(a, b), b // gcd(a, b))
        self.root.ids.question.text = "{} {} {} =".format(a, s, b)

    def update_score(self):
        self.root.ids.score.text = "Question: {} Correct: {} out of {}".format(self.count, self.correct, self.count)

    def next(self):
        if self.root.ids.answer.text == self.result:
            self.correct += 1
            self.sound_correct.play()
        else:
            self.sound_wrong.play()
        self.count += 1
        self.root.ids.answer.text = ""
        self.update_score()
        self.get_question()


if __name__ == '__main__':

    Window.size = (800, 510)
    Window.clearcolor = get_color_from_hex('#123456')
    MathsApp().run()
