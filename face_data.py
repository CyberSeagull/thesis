import json
import enum
from math import hypot
import cv2 as cv
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates as normalize


class FacePoint(enum.IntEnum):
    NOSE_TIP = 2
    CENTER_FOREHEAD = 9
    UPPER_LIP = 15
    LOWER_LIP = 13


class StartSetting:
    # indexes for eye points, that are going to be used in the further calculation of EAR
    EAR_eye_ind = {
        "left": [362, 385, 387, 263, 373, 380],
        "right": [33, 160, 158, 133, 153, 144]
    }

    default_initial_settings = {
        "chooseEye": "left",  # "right",  two parameters: left and right
        "cameraNum": 0,
        "avgPoint": {"avgCount": 5, "avgOld": [0, 0]},
        "delta_mousex": 9,
        "delta_mousey": 9,
        # "point_mouse_move": FacePoint.NOSE_TIP, #  CENTER_FOREHEAD, NOSE_TIP
        "point_mouse_move": 'nose_tip',  # NOSE_TIP, CENTER_FOREHEAD
        "mouse_pos": 'center', #['default', 'center'],
        "keyboard_pos": 'down', #['default', 'down'],
        "transparent_layout": False,
        "showimage": True,
        "keypress": {"deltatime": 1, "quiettime": 0, "acttime": 0, "oldquiettime": 0, "oldText": ''},  # Key  press,
        "EAR_Ldblclick":
            {"deltatime": 1, "quiettime": 2, "acttime": 0, "oldquiettime": 0, "Val": 0.2},  # [0.0, 0.40] # Left mouse dblclick
        "len_lip_Lclick": {"deltatime": 1, "quiettime": 2, "acttime": 0, "oldquiettime": 0, "Val": 9},  # [1,  40]       # Left mouse click
    }

    def __init__(self):
        self.initial_settings = self.get_initial_settings()
        self.chooseEye = ["right", "left"]
        self.mouse_pos = ['center', 'default']
        self.point_mouse_move = ['nose_tip', 'center_forehead']

    # @property
    def get_default_settings(self):
        return self.default_initial_settings

    def get_choose_eye(self):
        return self.chooseEye

    def get_mouse_pos(self):
        return self.mouse_pos

    def get_point_mouse_move(self):
        return self.point_mouse_move

    def get_initial_settings(self):
        try:
            with open("face_initial_settings.json", "r") as my_file:
                initial_settings_json = my_file.read()
                initial_settings = json.loads(initial_settings_json)
                if len(initial_settings) != len(self.default_initial_settings):
                    initial_settings = self.default_initial_settings.copy()
                    self.save_initial_settings(initial_settings)
        except:
            initial_settings = self.default_initial_settings.copy()
            self.save_initial_settings(initial_settings)
        return initial_settings

    def save_initial_settings(self, initial_settings):
        try:
            initial_settings_json = json.dumps(initial_settings)
            with open("face_initial_settings.json", "w") as my_file:
                my_file.write(initial_settings_json)
        except Exception:
            return False
        return True


class MeshDetector(StartSetting):

    def __init__(self, mode=False, maxFaces=1, minDetection=0.5, minTracking=0.5):
        self.mode = mode
        self.maxFaces = maxFaces
        self.minDetection = minDetection
        self.minTracking = minTracking
        self.initial_settings = {}
        self.chosen_mouse_rclick = [FacePoint.LOWER_LIP, FacePoint.UPPER_LIP]

        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=self.mode,
            max_num_faces=self.maxFaces,
            refine_landmarks=True,
            min_detection_confidence=self.minDetection,
            min_tracking_confidence=self.minTracking)

    def getReactionToEvent(self, criterion, initpar, currentime, ear=False):  # ear =True - open eye
        if currentime - initpar["oldquiettime"] < initpar["quiettime"]:
            return False
        if (criterion < initpar["Val"] and not ear) or (criterion > initpar["Val"] and ear):
            initpar["acttime"] = 0
        elif initpar["acttime"] == 0:
            initpar["acttime"] = currentime
        else:
            if currentime - initpar["acttime"] > initpar["deltatime"]:
                initpar["acttime"] = 0
                initpar["oldquiettime"] = currentime
                return True
        return False

    def get_face_landmarks(self, image):
        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        img_height, img_width, _ = image.shape
        results = self.face_mesh.process(image)

        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        return image, results.multi_face_landmarks

    def distance(self, p1, p2):
        return hypot(p2[0] - p1[0], p2[1] - p1[1])

    def key_point_coord(self, landmarks, par_point, frame_width, frame_height):
        try:
            # Compute the coord на фреймі в пікселях
            if par_point == 'nose_tip':
                key_point_enum = FacePoint.NOSE_TIP
            else:
                key_point_enum = FacePoint.CENTER_FOREHEAD

            lm = landmarks[key_point_enum]
            coord = normalize(lm.x, lm.y, frame_width, frame_height)
        except:
            coord = None
        return coord

    def get_ear(self, landmarks, par_name, frame_width, frame_height):
        refer_ind = self.EAR_eye_ind[par_name]
        try:
            # Compute the euclidean distance between the horizontal
            coords_points = []
            for i in refer_ind:
                lm = landmarks[i]
                coord = normalize(lm.x, lm.y, frame_width, frame_height)
                coords_points.append(coord)

            P1_P4 = self.distance(coords_points[0], coords_points[3])
            P2_P6 = self.distance(coords_points[1], coords_points[5])
            P3_P5 = self.distance(coords_points[2], coords_points[4])

            ear = (P2_P6 + P3_P5) / (2.0 * P1_P4)
        except:
            ear = None
            coords_points = None
        return ear, coords_points

    def get_distance_lips(self, landmarks, frame_width, frame_height,
                        LOWER_LIP=FacePoint.LOWER_LIP, UPPER_LIP=FacePoint.UPPER_LIP):
        try:
            lm = landmarks[LOWER_LIP]
            P1 = normalize(lm.x, lm.y,
                                         frame_width, frame_height)
            lm = landmarks[UPPER_LIP]
            P2 = normalize(lm.x, lm.y,
                                         frame_width, frame_height)
            length = self.distance(P1, P2)
            return length, (P1, P2)
        except:
            return None, None

    def average_point(self, mouse_key, lp, paravg, iterationnum):
        lp[iterationnum % paravg["avgCount"]].x = mouse_key[0]
        lp[iterationnum % paravg["avgCount"]].y = mouse_key[1]
        savg = [0, 0]
        for lpi in lp:
            savg[0] += lpi.x
            savg[1] += lpi.y
        if iterationnum < paravg["avgCount"]:
            paravg["avgOld"] = savg.copy()
        dx = int((savg[0] - paravg["avgOld"][0]) / paravg["avgCount"])
        dy = int((savg[1] - paravg["avgOld"][1]) / paravg["avgCount"])
        paravg["avgOld"] = savg.copy()
        return dx, dy
