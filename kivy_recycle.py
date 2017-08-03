import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App

from kivy.uix.label import Label

class MyApp(App):
	def build(self):
		layout = GridLayout(cols=4, row_force_default=True, row_default_height=40)
		layout.add_widget(Label(text='title'))
		layout.add_widget(Label(text='population'))
		layout.add_widget(Label(text='size'))
		layout.add_widget(Label(text='currency'))
		layout.add_widget(Label(text='Foo'))
		layout.add_widget(Label(text='21455'))
		layout.add_widget(Label(text='Bar'))
		layout.add_widget(Label(text='dollar'))
		layout.add_widget(Label(text='Boo'))
		layout.add_widget(Label(text='4522'))
		layout.add_widget(Label(text='Boo'))
		layout.add_widget(Label(text='euro'))


		return layout

MyApp().run()
