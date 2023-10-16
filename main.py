# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown


class FilterSelect(Button):
    def __init__(self, **kwargs):
        super(FilterSelect, self).__init__(**kwargs)
        self.dropdown = Filters()
        self.text = "selected filter: none"
        self.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, "text", "selected filter: "+x))


class PhotoShopApp(App):
    pass


class Display(Screen):
    def update(self):
        # global index
        # index = index%len(images)
        self.ids.image.source = self.ids.filename.text

    # def display_image(self):
    #     return images[index]

    # def advance(self):
    #     global index
    #     index+=1
    #     self.update()
    #
    # def retreat(self):
    #     global index
    #     index -= 1
    #     self.update()


class Filters(DropDown):
    pass


# images = [i+".jpg" for i in "group,group_hug,hug,mari,open_door,orchestra,smile,something".split(",")]
# index = 0
PhotoShopApp().run()
