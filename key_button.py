import enum
import cv2 as cv
import cvzone
import numpy as np
from pynput.keyboard import Controller

sizekey = 40
poskey = 50
sizefont = 1

window_key_width = 612  # 561
window_key_height = 209  # 159
name_img_key = 'KeyBoard'

keyboard_big_EN = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}"],
                   ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "'", "|"],
                   ["↑", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "\b"],
                   [".?123", "lang", " ", "Вийти", "\n"]]

keyboard_small_EN = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
                     ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\"],
                     ["↑", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "\b"],
                     [".?123", "lang", " ", "Вийти", "\n"]]

keyboard_big_UA = [["Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ї"],
                   ["Ф", "І", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Є", "/"],
                   ["↑", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ".", "\b"],
                   [".?123", "lang", " ", "Вийти", "\n"]]

keyboard_small_UA = [["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ї"],
                     ["ф", "і", "в", "а", "п", "р", "о", "л", "д", "ж", "є", "\\"],
                     ["↑", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "'", "\b"],
                     [".?123", "lang", " ", "Вийти", "\n"]]

keyboard_other = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+"],
                 ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "="],
                 ["↑", ":", ";", "<", ">", "'", "?", "~", "|", "/", "\t", "\b"],
                 [ ".?123", "lang",  " ", "Вийти", "\n"]]

control_chars = ("↑", ".?123", "lang", "Вийти")


class Button:
    def __init__(self, pos, text, size=[sizekey, sizekey]):
        self.pos = pos
        self.size = size
        self.text = text


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class StateKey(enum.IntEnum):
    keyNone = -1
    other = 0
    small_EN = 1
    big_EN = 2
    small_UA = 3
    big_UA = 4


class KeyboardState(Controller):

    def __init__(self, state=StateKey.big_UA):
        Controller.__init__(self)
        self.state = state
        self.oldstate = state
        self.keyboard_all = self.init_keyboard()
        self.curr_keyboard = self.getkeyboard(StateKey.big_UA)

    def init_keyboard(self):
        buttonAllList = []
        buttonAllList.append(self.add_keyboard(keyboard_other))
        buttonAllList.append(self.add_keyboard(keyboard_small_EN))
        buttonAllList.append(self.add_keyboard(keyboard_big_EN))
        buttonAllList.append(self.add_keyboard(keyboard_small_UA))
        buttonAllList.append(self.add_keyboard(keyboard_big_UA))
        return buttonAllList

    def drawkeyboard(self, idraw_layout, img_key):
        if idraw_layout:
            return self.transparent_layout(img_key, self.curr_keyboard)
        else:
            return self.draw(img_key, self.curr_keyboard)

    def getkeyboard(self, press_key = '', state_new=StateKey.big_UA):
        # control_chars = ("↑", ".?123", "lang")
        match press_key:
            case "lang":
                if self.state == StateKey.other:
                    self.state = self.oldstate
                else:
                    if self.state < StateKey.small_UA:
                        self.state += 2
                    else:
                        self.state -= 2
            case "↑":
                if (self.state != StateKey.other):
                    if (self.state % 2 == 0):
                        self.state -= 1
                    else:
                        self.state += 1
            case ".?123":
                if self.state != StateKey.other:
                    self.oldstate = self.state
                self.state = StateKey.other
            case _:
                self.state = state_new
                self.oldstate = self.state

        if (self.state != StateKey.other):
            self.oldstate = self.state
        return self.keyboard_all[self.state]

    def add_keyboard(self, keyboard_keys):
        buttonList = []
        for k in range(len(keyboard_keys)):
            poskeyx = 10
            for x, key in enumerate(keyboard_keys[k]):
                sizekeyx = sizekey
                if key in (".?123", "Вийти"):
                    sizekeyx = 2 * poskey - 10
                if key =="Вийти":
                    sizekeyx += poskey
                if key == " ":
                    sizekeyx = 5 * poskey - 10

                buttonList.append(Button([poskeyx, poskey * k + 10], key, [sizekeyx, sizekey]))
                poskeyx += poskey
                if key in (".?123", "Вийти"):
                    poskeyx += poskey
                if key =="Вийти":
                    poskeyx += poskey
                if key == " ":
                    poskeyx += 4*poskey

        return buttonList

    def draw(self, img, buttonList):
        img = img.copy()
        for button in buttonList:
            x, y = button.pos
            colorkey = (0, 0, 0)
            cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                       button.size[0], button.size[1]), t=4, rt=5, colorR=(255, 255, 255))
            cv.rectangle(img, button.pos, (x + button.size[0], y + button.size[1]),
                          (113, 170, 189), cv.FILLED)

            self.putkey(img, button, colorkey)

        return img

    def transparent_layout(self, img, buttonList):
        imgNew = np.zeros_like(img, np.uint8)
        for button in buttonList:
            x, y = button.pos
            colorkey = (0, 0, 0)
            cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1],
                                       button.size[0], button.size[1]), t=4, rt=5, colorR=(113, 170, 189))

            cv.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                          (113, 170, 189), cv.FILLED)
            self.putkey(imgNew, button, colorkey)
        out = img.copy()
        alpaha = 0
        mask = imgNew.astype(bool)
        out[mask] = cv.addWeighted(img, alpaha, imgNew, 1 - alpaha, 0)[mask]
        return out

    def putkey(self, imgNew, button, colorkey):
         x, y = button.pos
         w, h = button.size
         xkey = x + sizekey // 4
         ykey = y + (sizekey // 4) * 3

         match button.text:
             case "lang":
                 cv.circle(imgNew, (x + w // 2, y + h // 2), (2 * w) // 5, colorkey, 2)
                 cv.ellipse(imgNew, (x + w // 2, y + h // 2), (6, 16), 0, 90, 270, (0, 0, 255), 2)
                 cv.ellipse(imgNew, (x + w // 2, y + h // 2), (6, 16), 0, 270, -90, colorkey, 2)
                 cv.line(imgNew, (x + w // 7, y + 2 * h // 3), (x + w - w // 7, y + 2 * h // 3), colorkey, 2)
                 cv.line(imgNew, (x + w // 7, y + h // 3), (x + w - w // 7, y + h // 3), colorkey, 2)
             case "↑":
                 xkey = x + sizekey // 3 + 2
                 pts = np.array([[xkey, y + h // 2], [xkey + 4, y + h // 4],
                                 [xkey + 4, y + 3 * h // 4]], np.int32)
                 pts = pts.reshape((-1, 1, 2))
                 cv.polylines(imgNew, [pts], False, colorkey, 1)
                 cv.line(imgNew, (xkey + 4, y + h // 4), (xkey + 8, y + h // 2), colorkey, 1)
             case "\b":
                 xkey = x  # + sizekey // 3
                 pts = np.array([[xkey + 3 * w // 4, y + h // 2], [xkey + w // 4, y + h // 2], [xkey + w // 2, y + h // 3],
                                 [xkey + w // 4, y + h // 2], [xkey + w // 2, y + 2 * h // 3]], np.int32)
                 pts = pts.reshape((-1, 1, 2))
                 cv.polylines(imgNew, [pts], False, colorkey, 1)
             case "\n":
                xkey = x  # + sizekey // 3
                pts = np.array([[xkey + 3 * w // 4, y + h // 2], [xkey + w // 4, y + h // 2],
                                [xkey + w // 2, y + 2*h // 5], [xkey + w // 4, y + h // 2],
                                [xkey + w // 2, y + 3*h // 5]], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv.polylines(imgNew, [pts], False, colorkey, 1)
                cv.line(imgNew, (xkey+3*w//4, y+h//2), (xkey+3*w//4, y+h//3), colorkey, 1)
             case "Є":
                 cv.putText(imgNew, "C", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
                 cv.line(imgNew, (xkey + 4, y + w // 2), (xkey + 14, y + w // 2), colorkey, 1)
             case "є":
                 cv.putText(imgNew, "с", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
                 cv.line(imgNew, (xkey + 4, y + (3*w) // 5), (xkey + 12, y + (3*w) // 5), colorkey, 1)
             case "І":
                 cv.putText(imgNew, "I", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
             case "і":
                 cv.putText(imgNew, "i", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
             case "Ї":
                 cv.putText(imgNew, "I", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
                 cv.circle(imgNew, (x + w // 2 - 2, y + 4), 1, colorkey, 1)
                 cv.circle(imgNew, (x + w // 2 - 6, y + 4), 1, colorkey, 1)
             case "ї":
                 cv.putText(imgNew, "i", (xkey, ykey), cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
                 cv.circle(imgNew, (x + w // 2 - 2, y + w//4), 1, colorkey, 1)
                 cv.circle(imgNew, (x + w // 2 - 6, y + w//4), 1, colorkey, 1)
             case ".?123":
                 cv.putText(imgNew, button.text, (x + sizekey // 20, y + (sizekey // 4) * 3),
                        cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)
             case _:
                 cv.putText(imgNew, button.text, (x + sizekey // 4, y + (sizekey // 4) * 3),
                             cv.FONT_HERSHEY_COMPLEX, 1, colorkey, 1)

    def key_mouse_move(self, img_key, cvrect, mouse_pos, buttonList):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            xkey = x + sizekey // 4
            ykey = y + (sizekey // 4) * 3
            colorkey = (255, 255, 255)
            mouse_x, mouse_y = mouse_pos
            mwx, mwy = mouse_x - cvrect[0], mouse_y - cvrect[1]
            if x < mwx < x + w and y < mwy < y + h:
                cv.rectangle(img_key, button.pos, (x + w, y + h),
                              (67, 128, 18), cv.FILLED)
                self.putkey(img_key, button, colorkey)
                return button.text
        return ''

    def press(self, key):
        if key in control_chars:
            if key == "Вийти":
                return False
            else:
                self.curr_keyboard = self.getkeyboard(key)
        else:
            super().press(key)
        return True

    def presskey(self, img_key, cvrect, parKey, currtime, mouse_pos):
        # Обробка клавіатури
        buttonText = self.key_mouse_move(img_key, cvrect, mouse_pos, self.curr_keyboard)
        if (parKey["oldText"] != buttonText):
            parKey["oldText"] = buttonText
            parKey["acttime"] = currtime
        if (currtime - parKey["acttime"] >= parKey["deltatime"]) and (buttonText != ''):
            parKey["acttime"] = currtime
            return self.press(buttonText)
        return True
