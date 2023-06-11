import sys
import event_control
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from face_data import StartSetting


class BoxLayoutMain(BoxLayout):

    def __init__(self, **kwargs):

        super(BoxLayoutMain, self).__init__(**kwargs)
        self.get_spn_setting(init_settings)

    def get_spn_setting(self, init_settings):
        self.ids.spn_avg.text = self.ids.spn_avg.values[init_settings["avgPoint"]["avgCount"]-1]
        self.ids.spn_camera.text = self.ids.spn_camera.values[init_settings["cameraNum"]]

        self.set_spn_text(init_settings["len_lip_Lclick"], self.ids.spn_click)
        self.set_spn_text(init_settings["EAR_Ldblclick"], self.ids.spn_dbl_click)
        self.set_spn_text(init_settings["keypress"], self.ids.spn_press)

        self.set_spn_quiettime(init_settings["len_lip_Lclick"], self.ids.spn_click_quiet)
        self.set_spn_quiettime(init_settings["EAR_Ldblclick"], self.ids.spn_dbl_click_quiet)
        self.set_spn_quiettime(init_settings["keypress"], self.ids.spn_press_quiet)

        val = valueSetting.get_choose_eye().index(init_settings["chooseEye"])
        self.ids.spn_eye.text = self.ids.spn_eye.values[val]

        val = valueSetting.get_mouse_pos().index(init_settings["mouse_pos"])
        self.ids.spn_mouse_pos.text = self.ids.spn_mouse_pos.values[val]

        val = valueSetting.get_point_mouse_move().index(init_settings["point_mouse_move"])
        self.ids.spn_point_mouse_move.text = self.ids.spn_point_mouse_move.values[val]

    def set_spn_text(self, par_time, time_spinner):
        val = (par_time["deltatime"]*1000 - 500) // 250
        time_spinner.text = time_spinner.values[int(val)]

    def set_spn_quiettime(self, par_time, quiet_time_spinner):
        val = (par_time["quiettime"]*1000) // 500
        quiet_time_spinner.text = quiet_time_spinner.values[int(val)]

    def select_avg(self):
        val = self.ids.spn_avg.values.index(self.ids.spn_avg.text)
        init_settings["avgPoint"]["avgCount"] = val+1

    def select_camera(self):
        val = self.ids.spn_camera.values.index(self.ids.spn_camera.text)
        init_settings["cameraNum"] = val

    def select_click(self):
        val = self.ids.spn_click.values.index(self.ids.spn_click.text)
        init_settings["len_lip_Lclick"]["deltatime"] = (500+val*250)/1000

    def select_dbl_click(self):
        val = self.ids.spn_dbl_click.values.index(self.ids.spn_dbl_click.text)
        init_settings["EAR_Ldblclick"]["deltatime"] = (500+val*250)/1000

    def select_press(self):
        val = self.ids.spn_press.values.index(self.ids.spn_press.text)
        init_settings["keypress"]["deltatime"] = (val*500)/1000

    def select_click_quiet(self):
        val = self.ids.spn_click_quiet.values.index(self.ids.spn_click_quiet.text)
        init_settings["len_lip_Lclick"]["quiettime"] = (val*500)/1000

    def select_dbl_click_quiet(self):
        val = self.ids.spn_dbl_click_quiet.values.index(self.ids.spn_dbl_click_quiet.text)
        init_settings["EAR_Ldblclick"]["quiettime"] = (val*500)/1000

    def select_press_quiet(self):
        val = self.ids.spn_press_quiet.values.index(self.ids.spn_press_quiet.text)
        init_settings["keypress"]["quiettime"] = (val*500)/1000

    def select_eye(self):
        val = self.ids.spn_eye.values.index(self.ids.spn_eye.text)
        init_settings["chooseEye"] = valueSetting.get_choose_eye()[val]

    def select_mouse_pos(self):
        val = self.ids.spn_mouse_pos.values.index(self.ids.spn_mouse_pos.text)
        init_settings["mouse_pos"] = valueSetting.get_mouse_pos()[val]

    def select_point_mouse_move(self):
        val = self.ids.spn_point_mouse_move.values.index(self.ids.spn_point_mouse_move.text)
        init_settings["point_mouse_move"] = valueSetting.get_point_mouse_move()[val]

    def on_save_click(self):
        valueSetting.save_initial_settings(init_settings)

    def on_default_setting_click(self):
        valueSetting.save_initial_settings(valueSetting.get_default_settings())
        def_settings = valueSetting.get_initial_settings()
        self.get_spn_setting(def_settings)

    def on_start_click(self):
        self.on_save_click()
        Window.hide()
        keyboard_mouse = event_control.StartKeyboardMouse()
        keyboard_mouse.start_keyboard_mouse()
        sys.exit()


class EaseAccessApp(App):
    def build(self):
        return BoxLayoutMain()


if __name__ == "__main__":
    valueSetting = StartSetting()
    init_settings = valueSetting.get_initial_settings()
    EaseAccessApp().run()
