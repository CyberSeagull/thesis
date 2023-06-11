from unittest import TestCase
from key_button import *
from face_data import StartSetting
import time


class TestKeyboardState(TestCase):

    def setUp(self):
        self.keyboard = KeyboardState()
        self.img_key = np.zeros((window_key_height, window_key_width, 3), dtype=np.uint8)

    def test_get_keyboard_digit(self):
        key = ".?123"
        self.assertEqual(self.keyboard.getkeyboard(key)[8].text, keyboard_other[0][8])

    def test_get_keyboard_UA(self):
        self.assertEqual(self.keyboard.getkeyboard(state_new=StateKey.big_UA)[7].text, keyboard_big_UA[0][7])

    def test_getKey_mouse_move(self):
        cv2rect = (968, 832, 612, 209)
        mouse_pos = (985, 866)
        btn_list = self.keyboard.getkeyboard(state_new=StateKey.small_EN)
        btn_text = self.keyboard.key_mouse_move(self.img_key, cv2rect, mouse_pos, btn_list)
        self.assertEqual(btn_text, keyboard_small_EN[0][0])

    def test_press_key_Exit(self):
        cv2rect = (968, 832, 612, 209)
        mouse_pos = (1430, 1021)
        curr_time = time.time()
        init_par = StartSetting.default_initial_settings["keypress"].copy()
        # ініціалізація parKey["oldText"]  = Вийти
        self.keyboard.presskey(self.img_key, cv2rect, init_par, curr_time, mouse_pos)
        # час нажаття на клавішу настав
        init_par["acttime"] = curr_time - init_par["deltatime"] * 1.1
        # Result = False означає, що нажата клавіша 'Вийти'
        self.assertFalse(self.keyboard.presskey(self.img_key, cv2rect, init_par, curr_time, mouse_pos))
