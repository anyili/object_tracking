#!/usr/bin/python

import cv2
import usb_arm
import time
import thread


IMAGE_SCALE = 2

SHIFT_TOLERANCE_X = 50
SHIFT_TOLERANCE_Y = 20
CAPTURE_WINDOW_NAME = 'result'

RELAX_TIME = 2000


def get_center(pt1, pt2):
    x1 = pt1[0]
    x2 = pt2[0]
    y1 = pt1[1]
    y2 = pt2[1]
    center_x = x1 + ((x2 - x1) / 2)
    center_y = y1 + ((y2 - y1) / 2)
    center = (center_x, center_y)
    return center


def draw_roi(x, y, w, h, color, thickness, image):
    pt1 = (int(x * IMAGE_SCALE), int(y * IMAGE_SCALE))
    pt2 = (int((x + w) * IMAGE_SCALE), int((y + h) * IMAGE_SCALE))
    cv2.rectangle(image, pt1, pt2, color, thickness)
    return pt1, pt2


def detect_and_draw(original_image, face_cascade, fist_cascade):
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    reduced_img = cv2.resize(src=gray_image, dsize=None, fx=1.0 / IMAGE_SCALE, fy=1.0 / IMAGE_SCALE,
                             interpolation=cv2.INTER_LINEAR)
    reduced_img = cv2.equalizeHist(reduced_img)

    center = None
    faces = face_cascade.detectMultiScale(
        image=reduced_img,
        scaleFactor=1.2,
        minNeighbors=3,
        minSize=(40, 40)
    )
    for x, y, w, h in faces:
        draw_roi(x, y, w, h, (255, 0, 0), 3, original_image)

    fists = fist_cascade.detectMultiScale(
        image=reduced_img,
        scaleFactor=1.2,
        minNeighbors=3,
        minSize=(40, 40)
    )

    if len(fists) > 0:
        x, y, w, h = fists[0]
        pt1, pt2 = draw_roi(x, y, w, h, (0, 255, 0), 3, original_image)
        center = get_center(pt1, pt2)

    # for x, y, w, h in fists:
    #     pt1, pt2 = draw_roi(x, y, w, h, (0, 255, 0), 3, original_image)
    #     center = get_center(pt1, pt2)

    cv2.imshow(CAPTURE_WINDOW_NAME, original_image)
    return center


def move_arm_x(delta, arm):
    if delta > 0:
        arm.move(usb_arm.BaseClockWise, 1.0)
    elif delta < 0:
        arm.move(usb_arm.BaseCtrClockWise, 1.0)
    if delta != 0:
        print 'moving in x', delta


def move_arm_y(delta, arm):
    if delta > 0:
        arm.move(usb_arm.ShoulderDown, 1.0)
    elif delta < 0:
        arm.move(usb_arm.ShoulderUp, 1.0)
    if delta != 0:
        print 'moving in y', delta


def move_arm_test_x(delta):
    if delta > 0:
        time.sleep(2)
    elif delta < 0:
        time.sleep(2)
    if delta != 0:
        print 'moving in x', delta


def move_arm_test_y(delta):
    if delta > 0:
        time.sleep(2)
    elif delta < 0:
        time.sleep(2)
    if delta != 0:
        print 'moving in y', delta


def get_shift(original, current, tolerance):
    if abs(current - original) < tolerance:
        result = (original, 0)
    else:
        result = (current, current - original)
    return result


def main():
    try:
        arm = usb_arm.Arm()
    except:
        raise Exception("can not init robotic arm")

    face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt2.xml')
    fist_cascade = cv2.CascadeClassifier('haarcascade/fist.xml')
    capture = cv2.VideoCapture(0)
    cv2.namedWindow(CAPTURE_WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    original_x = None
    original_y = None
    start_time = int(time.time() * 1000)
    while True:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        if frame.size == 0:
            continue
        center = detect_and_draw(frame, face_cascade, fist_cascade)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if center:
            current_x, current_y = center
            if not original_x:
                original_x = current_x
            else:
                original_x, delta_x = get_shift(original_x, current_x, SHIFT_TOLERANCE_X)
                thread.start_new_thread(move_arm_x, (delta_x, arm))

            if not original_y:
                original_y = current_y
            else:
                original_y, delta_y = get_shift(original_y, current_y, SHIFT_TOLERANCE_Y)
                thread.start_new_thread(move_arm_y, (delta_y, arm))
            start_time = int(time.time() * 1000)
        else:
            end_time = int(time.time() * 1000)
            if end_time - start_time > RELAX_TIME:
                original_x = None
                original_y = None

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
