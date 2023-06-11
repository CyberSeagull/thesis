from key_button import *
import face_data as fd
import time
import pyautogui


class StartKeyboardMouse:
    def __init__(self):
        self.keyboard = KeyboardState()
        self.detector = fd.MeshDetector(minDetection=0.7)


    def start_keyboard_mouse(self):
        init_settings = self.detector.get_initial_settings()

        lp = []
        for i in range(init_settings["avgPoint"]["avgCount"]):
            lp.append(Point(0, 0))

        Nkadr = 0  #кадр - обличчя в фокусі і обробляється
        cap = cv.VideoCapture(init_settings["cameraNum"])

        pyautogui.PAUSE = 0.01
        # роздільна здатність та позиція
        Pmon = pyautogui.size()
        if init_settings["mouse_pos"] == 'center':
            pyautogui.moveTo(int(Pmon.width / 2), int(Pmon.height / 2), duration=0.5)
        if init_settings["keyboard_pos"] == 'down':
            img_key = np.zeros((window_key_height, window_key_width, 3), dtype=np.uint8)
            # img_key[:, :] = (192, 192, 192)
            cv.imshow(name_img_key, img_key)
            cv.moveWindow(name_img_key, int(Pmon.width / 2), int(Pmon.height-window_key_height-70))

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image, multi_face_landmarks = self.detector.get_face_landmarks(image)
            img_height, img_width, _ = image.shape
            img_key = image[0:window_key_height, 0:window_key_width]
            # if multi_face_landmarks is not detected, the user can only see image from his camera
            # otherwise the camera image is in the background

            if multi_face_landmarks:
                for face_landmarks in multi_face_landmarks:
                    landmarks = face_landmarks.landmark  # only using one face
                    currtime = time.time()

                    # doubleclick  Eye Aspect Ratio (EAR) for one eye. [0.0, 0.40].
                    l, coords = self.detector.get_ear(landmarks, init_settings["chooseEye"], img_width, img_height)
                    if l is None:  # or ll==None):
                        continue
                    eventres = self.detector.getReactionToEvent(l, init_settings["EAR_Ldblclick"], currtime, True)
                    if eventres:
                        pyautogui.doubleClick()

                    # click mouse відкритий рот FacePoint.LOWER_LIP, FacePoint.UPPER_LIP
                    l, coord2 = self.detector.get_distance_lips(landmarks, img_width, img_height)
                    if l is None:
                        continue
                    coords.extend(coord2)
                    eventres = self.detector.getReactionToEvent(l, init_settings["len_lip_Lclick"], currtime)
                    if eventres:
                        # print('"len_lip_Lclick"=', init_settings["len_lip_Lclick"])
                        pyautogui.click()

                    # mouse move and key press
                    mouse_key = self.detector.key_point_coord(landmarks, init_settings["point_mouse_move"], img_width, img_height)
                    coords.append(mouse_key)
                    if mouse_key is None:
                        continue

                    mx, my = pyautogui.position()
                    dx, dy = self.detector.average_point(mouse_key, lp, init_settings["avgPoint"], Nkadr)#, countaverage)
                    mx = mx - dx * init_settings["delta_mousex"]  # mouse X
                    my = my + dy * init_settings["delta_mousey"]  # mouse Y

                    img_key = self.keyboard.drawkeyboard(init_settings["transparent_layout"], img_key)
                    if (Nkadr > init_settings["avgPoint"]["avgCount"]):
                        if (Pmon.width > mx) and (Pmon.height > my) and (mx > 0) and (my > 0):
                            pyautogui.moveTo(mx, my)#, duration=0)
                            try:
                                cvrect = cv.getWindowImageRect(name_img_key)
                            except:
                                continue

                            if not self.keyboard.presskey(img_key, cvrect, init_settings["keypress"],
                                             currtime, pyautogui.position()):
                                cap.release()
                                cv.destroyAllWindows()

                    Nkadr +=1
                    if init_settings["showimage"]:
                        for coord in coords:
                            cv.circle(image, coord, 1, (0, 255, 255), 1)

            cv.namedWindow(name_img_key, flags=cv.WINDOW_GUI_NORMAL)
            cv.setWindowProperty(name_img_key, cv.WND_PROP_TOPMOST, 1)
            cv.resizeWindow(name_img_key, window_key_width, window_key_height)
            cv.imshow(name_img_key, img_key)
            if init_settings["showimage"]:
                cv.imshow('Face Tracking', cv.flip(image, 1))
            if cv.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv.destroyAllWindows()
