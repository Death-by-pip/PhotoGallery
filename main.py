# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from PIL import Image, ImageDraw
import random


def invert(image):
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            pixels[x, y] = (255 - pixels[x, y][0], 255 - pixels[x, y][1], 255 - pixels[x, y][2])
    return image


def sepia(image):
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            red = pixels[x, y][0]
            green = pixels[x, y][1]
            blue = pixels[x, y][2]
            r = int(red * .393 + green * 0.769 + blue * 0.189)
            g = int(red * .349 + green * 0.686 + blue * 0.168)
            b = int(red * .272 + green * 0.534 + blue * 0.131)
            pixels[x, y] = (r, g, b)
    return image


def pointillism(image):
    old_pixels = image.load()
    width = image.width
    height = image.height
    image2 = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image2)
    for i in range(width * height * 10):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        c = old_pixels[x, y]
        size = random.randint(1, 5)
        draw.ellipse([(x - size, y - size), (x + size, y + size)], fill=c)
    del draw
    return image2


def line_drawing(image, sensitivity: float):
    old_pixels = image.load()
    width = image.width
    height = image.height
    image2 = Image.new("RGB", (width, height), "white")
    pixels = image2.load()
    max_ = 255 * (3 ** (1 / 2))
    for x in range(width):
        for y in range(height):
            for i in range(-1, 1):
                for n in range(-1, 1):
                    if i == 0 and n == 0:
                        continue
                    R = (old_pixels[x, y][0] - old_pixels[x + i, y + n][0]) ** 2
                    G = (old_pixels[x, y][1] - old_pixels[x + i, y + n][1]) ** 2
                    B = (old_pixels[x, y][2] - old_pixels[x + i, y + n][2]) ** 2
                    if ((R + G + B) ** (1 / 2)) / max_ >= (1 - sensitivity):
                        pixels[x, y] = (0, 0, 0)
                        break
                else:
                    break
    return image2


def rainbow_image(image):
    rainbow = []
    r = 255
    g = 0
    b = 0
    for i in range(255):
        rainbow.append((r, g, b))
        g += 1
    for i in range(255):
        rainbow.append((r, g, b))
        r -= 1
    for i in range(255):
        rainbow.append((r, g, b))
        b += 1
    for i in range(255):
        rainbow.append((r, g, b))
        g -= 1
    for i in range(255):
        rainbow.append((r, g, b))
        r += 1
    for i in range(255):
        rainbow.append((r, g, b))
        b -= 1
    width = image.width
    height = image.height
    pixels = image.load()
    max_ = width + height
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            i = (x + y) / max_
            i *= 1530
            i = rainbow[round(i)]
            pixels[x, y] = (round((r + i[0]) / 2), round((g + i[1]) / 2), round((b + i[2]) / 2))
    return image


def pixelate(image, X, Y, width, height, intensity: float):
    pixels = image.load()
    intensityF = 0.5 - ((2 * (intensity - 1) ** 3) / 2)
    sub_area = (height * width) ** intensityF
    swidth = (sub_area * width / height) ** (1 / 2)
    sheight = (sub_area * height / width) ** (1 / 2)
    for x in range(round(swidth)):
        for y in range(round(sheight)):
            r = []
            g = []
            b = []
            X1 = X + round(width * x / round(swidth))
            X2 = X + round(width * (x + 1) / round(swidth))
            Y1 = Y + round(height * y / round(sheight))
            Y2 = Y + round(height * (y + 1) / round(sheight))
            # print(X1," ",X2," ",Y1," ",Y2)
            for x1 in range(X1, X2):
                for y1 in range(Y1, Y2):
                    # print((x1,y1))
                    try:
                        r.append(pixels[x1, y1][0])
                        g.append(pixels[x1, y1][1])
                        b.append(pixels[x1, y1][2])
                    except:
                        print(x1, y1)
            if True:
                r = (sum([i ** 2 for i in r]) / len(r)) ** (1 / 2)
                g = (sum([i ** 2 for i in g]) / len(g)) ** (1 / 2)
                b = (sum([i ** 2 for i in b]) / len(b)) ** (1 / 2)
            else:
                r = (sum(r) / len(r))
                g = (sum(g) / len(g))
                b = (sum(b) / len(b))
            C = (int(r), int(g), int(b))
            for x1 in range(X1, X2):
                for y1 in range(Y1, Y2):
                    pixels[x1, y1] = C
    return image


class FilterSelect(Button):
    def __init__(self, **kwargs):
        super(FilterSelect, self).__init__(**kwargs)
        self.dropdown = Filters()
        self.text = "selected filter: None"
        self.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: self.update(x))

    def update(self, data):
        if data is not None:
            self.text = "selected: " + data
        else:
            self.text = "selected: none"
        self.parent.parent.on_selection(data)


class PhotoShopApp(App):
    pass


class Display(Screen):
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.filter = None
        # self.ids.selector.bind(on_update=lambda instance, x: self.on_selection(x))

    def update(self):
        # global index
        # index = index%len(images)
        self.ids.image.source = self.ids.filename.text

    def on_selection(self, data):
        self.filter = data

    def apply(self):
        img = self.ids.image.source
        if self.filter != None:
            img = Image.open(img)
            img = eval(self.filter+"(img)")
            img.save("TEMP.jpg")
            self.ids.image.source = "TEMP.jpg"
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
