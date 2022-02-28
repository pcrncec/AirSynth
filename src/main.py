import cv2
import mediapipe as mp
import numpy as np
import argparse
import utils
from sys import platform
from config import Config
from player import SynthPlayer


def main(cfg):
    mp_hands = mp.solutions.hands

    player = SynthPlayer(cfg.SOUNDS_PATH)
    player.daemon = True
    player.start()

    if platform == "win32":
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)
    cv2.namedWindow('Synthesizer', cv2.WINDOW_NORMAL)

    prev_pressed_keys = []
    new_pressed_keys = []

    with mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.4) as hands:
        while cap.isOpened():
            success, camera_frame = cap.read()
            if not success:
                continue
            camera_frame.flags.writeable = False
            camera_frame = cv2.cvtColor(camera_frame, cv2.COLOR_BGR2RGB)
            results = hands.process(camera_frame)

            camera_frame.flags.writeable = True
            camera_frame = cv2.cvtColor(camera_frame, cv2.COLOR_RGB2BGR)

            keys_with_hand_img = cfg.KEYS_IMG.copy()

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    utils.visualize_hand(hand_landmarks, camera_frame, keys_with_hand_img, cfg)

                pressed_keys_coords = utils.get_pressed_keys_coords(results.multi_hand_landmarks)
                pressed_x = [coord[0] for coord in pressed_keys_coords]
                pressed_y = [coord[1] for coord in pressed_keys_coords]
                new_pressed_keys = [np.clip(int(x / cfg.WHITE_KEYS_WIDTH_NORMALIZED), 0, cfg.TOTAL_WHITE_KEYS - 1)
                                    for x in pressed_x]
                chords_to_play, chords_to_stop = utils.get_played_and_stopped_chords(prev_pressed_keys,
                                                                                     new_pressed_keys)
                prev_pressed_keys = new_pressed_keys

                player.set_chords_to_play(chords_to_play)
                player.set_chords_to_stop(chords_to_stop)
            else:
                all_keys = np.arange(0, cfg.TOTAL_WHITE_KEYS).tolist()
                player.set_chords_to_play([])
                player.set_chords_to_stop(all_keys)

            cv2.imshow('Synthesizer', keys_with_hand_img)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('keys_image_size', type=str,
                        help='Normal image of keys (88 keys) or small image of keys (41 keys) to play on', default='N')
    args = parser.parse_args()
    if args.keys_image_size != 'N' and args.keys_image_size != 'S':
        parser.error('keys_image_size argument must be N or S')
    if args.keys_image_size == 'N':
        config = Config(normal_keys_image=True)
    else:
        config = Config(normal_keys_image=False)
    main(config)
