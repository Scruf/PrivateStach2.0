from kivy.app import App
from kivy.uix.button import Button
class GoodMorning(App):
	def build(self):
		return Button(text="Good morning to you all")

GoodMorning().run()
