# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from PIL import Image, ImageDraw
import random


def greyscale(image):
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            c = (pixels[x, y][0] + pixels[x, y][1] + pixels[x, y][2])//3
            pixels[x,y] = (c, c, c)
    return image


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
    intensityF = .5 - ((2*intensity - 1) ** 3)/2
    sub_area = (height * width) ** intensityF
    swidth = (sub_area * width / height) ** (1 / 2)
    sheight = (sub_area * height / width) ** (1 / 2)
    print(X, Y, width, height)
    print(image.width, image.height)
    print("----")
    for x in range(round(swidth)):
        for y in range(round(sheight)):
            r = []
            g = []
            b = []
            X1 = X + round(width * x / round(swidth))
            X2 = X + round(width * (x + 1) / round(swidth))
            Y1 = Y + round(height * y / round(sheight))
            Y2 = Y + round(height * (y + 1) / round(sheight))
            print(X1, Y1, X2, Y2)
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
        self.image = Image.new("RGB", (512, 512), 0)
        self.image.save("TEMP.jpg")
        self.coords = [(0, 0), (1, 1)]
        # self.ids.selector.bind(on_update=lambda instance, x: self.on_selection(x))

    def update(self):
        # global index
        # index = index%len(images)
        self.image = Image.open(self.ids.filename.text)
        self.image.save("TEMP.jpg")
        self.ids.image.reload()

    def on_selection(self, data):
        # if self.filter == "pixelate":
        #     self.ids.normalapply.text = "Apply Filter"
        #     self.ids.toggleapply.text = ""
        #     self.ids.normalapply.size_hint = (1,1)
        #     self.ids.toggleapply.size_hint = (0,0)
        self.filter = data
        self.applypixel = False
        if self.filter in ["pixelate", "line_drawing"]:
            self.ids.intensity.disabled = False
        else:
            self.ids.intensity.disabled = True
        # if self.filter == "pixelate":
        #     self.ids.normalapply.text = ""
        #     self.ids.toggleapply.text = "Apply Filter"
        #     self.ids.normalapply.size_hint = (0,0)
        #     self.ids.toggleapply.size_hint = (1,1)

    def apply(self):
        if self.filter != "pixelate":
            self.applypixel = False
            self.ids.applier.state = "normal"
            if self.filter != "line_drawing" and self.filter is not None:
                self.image = eval(self.filter + "(self.image)", globals(), locals())
            elif self.filter == "line_drawing":
                if self.ids.intensity.text=="":
                    self.ids.intensity.text = ".82"
                self.image = line_drawing(self.image, float(self.ids.intensity.text))
            self.image.save("TEMP.jpg")
            self.ids.image.reload()

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.coords = [(x, y)]
        touch.push()
        touch.apply_transform_2d(self.to_local)
        ret = super(RelativeLayout, self).on_touch_down(touch)
        touch.pop()
        return ret

    # def on_touch_move(self, touch):
    #     x, y = touch.x, touch.y
    #     touch.push()
    #     touch.apply_transform_2d(self.to_local)
    #     ret = super(RelativeLayout, self).on_touch_move(touch)
    #     touch.pop()
    #     return ret

    def on_touch_up(self, touch):
        x, y = touch.x, touch.y
        self.coords.append((x, y))
        if self.ids.applier.state == "down" and not self.applypixel:
            self.applypixel = True
        elif self.filter == "pixelate" and self.applypixel:
            pos = (self.ids.image.center_x - self.ids.image.norm_image_size[0] / 2, self.ids.image.center_y - self.ids.image.norm_image_size[1] / 2)
            W = self.ids.image.norm_image_size[0]
            H = self.ids.image.norm_image_size[1]
            print(pos, W, H)
            C = [i for i in self.coords[1]]
            c = [i for i in self.coords[0]]
            print(C, c)
            if pos[0]<C[0]<pos[0]+W and pos[0]<c[0]<pos[0]+W and pos[1]<C[1]<pos[1]+H and pos[1]<c[1]<pos[1]+H:
                C[0] -= pos[0]
                c[0] -= pos[0]
                C[1] = pos[1] + H - C[1]
                c[1] = pos[1] + H - c[1]
                print(C, c)
                width = abs(C[0] - c[0])
                height = abs(C[1] - c[1])
                X = min(C[0], c[0])
                Y = min(C[1], c[1])
                print(X, Y, width, height)
                if self.ids.intensity.text == "":
                    self.ids.intensity.text = ".3"
                self.image = pixelate(self.image, int(X), int(Y), int(width), int(height), float(self.ids.intensity.text))
                self.image.save("TEMP.jpg")
                self.ids.image.reload()
                self.ids.applier.state = "normal"
                self.applypixel = False

        touch.push()
        touch.apply_transform_2d(self.to_local)
        ret = super(RelativeLayout, self).on_touch_up(touch)
        touch.pop()
        return ret
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
