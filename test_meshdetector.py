# Ctrl+Alt+S
# https://docs.python.org/3/library/unittest.html
import time
from unittest import TestCase
import face_data
from key_button import Point


class TestDetector(TestCase):

    def setUp(self):
        self.detector = face_data.MeshDetector(minDetection=0.7)
        self.init_def = self.detector.get_default_settings()

    def test_Lip_ReactionToEvent(self):  # Left mouse click event
        criterion = 35
        current_time = time.time()
        init_par = self.init_def["len_lip_Lclick"].copy()
        init_par["acttime"] = current_time - init_par["deltatime"]*1.1
        self.assertTrue(self.detector.getReactionToEvent(criterion, init_par, current_time))

    def test_Lip_ReactionToEventQuietTime(self):  # Left mouse click event QuietTime after click
        criterion = 35
        curr_time = time.time()
        init_par = self.init_def["len_lip_Lclick"].copy()
        init_par["acttime"] = curr_time - init_par["deltatime"]*1.1
        self.detector.getReactionToEvent(criterion, init_par, curr_time)  # Left click
        self.assertFalse(self.detector.getReactionToEvent(criterion, init_par, curr_time))  # Quiet Time

    def test_EAR_ReactionToEvent(self):
        criterion = 0.12
        curr_time = time.time()
        init_par = self.init_def["EAR_Ldblclick"].copy()
        init_par["acttime"] = curr_time - init_par["deltatime"]*1.1
        self.assertTrue(self.detector.getReactionToEvent(criterion, init_par, curr_time, True))

    def test_AveragePoint(self):
        avg_point = [Point(1, 5), Point(2, 4), Point(2, 3)]
        init_par = {"avgCount": 3, "avgOld": [3, 4]}
        # print(self.detector.AveragePoint(xx, avg_point, avg_par, 5))
        self.assertCountEqual(self.detector.average_point([7, 5], avg_point, init_par, 5), (2, 3))


    '''
    def test_EAR_ReactionToEvent2(self):
        criterion = 0.1
        currentTime = time.time()
        "EAR_Ldblclick":
            {"deltatime": 1, "quiettime": 2, "acttime": 0, "oldquiettime": 0, "Val": 0.2},  # [0.0, 0.40] # Left mouse dblclick

        self.initpar["acttime"] = currentTime - self.initpar["deltatime"] * 1.1
        self.detector.getReactionToEvent(l, init_settings["EAR_Ldblclick"], currtime, True)
        self.assertFalse(self.detector.getReactionToEvent(criterion, self.initpar, currentTime))


# if __name__ == '__main__':
#     unittest.main()

def test_ReactionToEvent2(self):
     initpar ={"deltatime": 1, "quiettime": 2, "acttime": 0, "oldquiettime": time.time(),
      "Val": 9}  # [1,  40]       # Left mouse click
     criterion = 35
     currentTime = time.time()
     initpar["acttime"] =currentTime - initpar["deltatime"]
     self.assertEqual(self.detector.getReactionToEvent(criterion, self.initpar, currentTime), False)

class TestStartSetting(TestCase):
 def test_get_default_settings(self):
     self.fail()

 def test_get_initial_settings(self):
     self.fail()

 def test_save_initial_settings(self):
     self.fail()
'''