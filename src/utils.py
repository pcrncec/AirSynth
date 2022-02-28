import cv2
import numpy as np


def get_min_max_landmarks(landmarks):
    x_landmarks = [keypoint.x for keypoint in landmarks.landmark]
    y_landmarks = [keypoint.y for keypoint in landmarks.landmark]

    min_x = max(0, min(x_landmarks))
    min_y = max(0, min(y_landmarks))
    max_x = min(1, max(x_landmarks))
    max_y = min(1, max(y_landmarks))
    return min_x, max_x, min_y, max_y


def draw_hand_bbox(image, min_x, max_x, min_y, max_y):
    cv2.rectangle(image, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (255, 0, 0), 2)
    return image


def get_pressed_keys_coords(landmarks):
    pressed_keys = []
    for hand_landmarks in landmarks:
        x_landmarks = [keypoint.x for keypoint in hand_landmarks.landmark]
        x_landmarks = np.clip(x_landmarks, 0, 1)
        y_landmarks = [keypoint.y for keypoint in hand_landmarks.landmark]
        y_landmarks = np.clip(y_landmarks, 0, 1)
        first_finger_landmarks_ind = [2, 6, 10, 14, 18]
        last_finger_landmarks_ind = [4, 8, 12, 16, 20]
        for i in range(len(first_finger_landmarks_ind)):
            if y_landmarks[last_finger_landmarks_ind[i]] > y_landmarks[first_finger_landmarks_ind[i]]:
                pressed_x_landmark = x_landmarks[last_finger_landmarks_ind[i]]
                pressed_y_landmark = y_landmarks[last_finger_landmarks_ind[i]]
                pressed_keys.append((pressed_x_landmark, pressed_y_landmark))
    return pressed_keys


def get_played_and_stopped_chords(prev_pressed_keys, new_pressed_keys):
    chords_to_play = [x for x in new_pressed_keys if x not in prev_pressed_keys]
    chords_to_stop = [x for x in prev_pressed_keys if x not in new_pressed_keys]
    return chords_to_play, chords_to_stop


def resize_img_with_aspect_ratio(img, width):
    org_h, org_w = img.shape[:2]
    ratio = width / float(org_w)
    if ratio < 1:
        resized_img = cv2.resize(img, (int(width), int(org_h * ratio)), interpolation=cv2.INTER_AREA)
    else:
        resized_img = cv2.resize(img, (int(width), int(org_h * ratio)), interpolation=cv2.INTER_LINEAR)
    return resized_img


def visualize_hand(hand_landmarks, hand_image, output_image, cfg):
    hand_img_dims = hand_image.shape[:2]
    min_x, max_x, min_y, max_y = get_min_max_landmarks(hand_landmarks)
    x_center_norm, y_center_norm = min_x + (max_x - min_x) / 2., min_y + (max_y - min_y) / 2.
    min_x, max_x, min_y, max_y = int(min_x * hand_img_dims[1]), int(max_x * hand_img_dims[1]), int(
        min_y * hand_img_dims[0]), int(max_y * hand_img_dims[0])

    cropped_hand = hand_image[min_y:max_y, min_x:max_x]
    cropped_hand = cv2.resize(cropped_hand, (int(cfg.HAND_WIDTH), 300), interpolation=cv2.INTER_AREA)
    cropped_hand_width, cropped_hand_height = cropped_hand.shape[1], cropped_hand.shape[0]

    hand_min_x = int(cfg.KEYS_IMG_WIDTH * x_center_norm - cropped_hand_width / 2.)
    hand_max_x = int(cfg.KEYS_IMG_WIDTH * x_center_norm + cropped_hand_width / 2.)
    hand_min_y = int(cfg.KEYS_IMG_HEIGHT * y_center_norm - cropped_hand_height / 2.)
    hand_max_y = int(cfg.KEYS_IMG_HEIGHT * y_center_norm + cropped_hand_height / 2.)

    if hand_min_x <= 0:
        hand_min_x = 0
        cropped_hand = cropped_hand[:, cropped_hand.shape[1] - (hand_max_x - hand_min_x):]
    if hand_min_y <= 0:
        hand_min_y = 0
        cropped_hand = cropped_hand[cropped_hand.shape[0] - (hand_max_y - hand_min_y):, :]
    if hand_max_x >= cfg.KEYS_IMG_WIDTH:
        hand_max_x = cfg.KEYS_IMG_WIDTH
        cropped_hand = cropped_hand[:, 0:hand_max_x - hand_min_x]
    if hand_max_y >= cfg.KEYS_IMG_HEIGHT:
        hand_max_y = cfg.KEYS_IMG_HEIGHT
        cropped_hand = cropped_hand[0:hand_max_y - hand_min_y, :]

    output_image[hand_min_y:hand_max_y, hand_min_x:hand_max_x] = cv2.addWeighted(
        output_image[hand_min_y:hand_max_y, hand_min_x:hand_max_x],
        cfg.ALPHA, cropped_hand, (1.0 - cfg.ALPHA), 0.0
    )
