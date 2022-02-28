from cv2 import imread
import os


class Config:
    def __init__(self, normal_keys_image):
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        if normal_keys_image:
            keys_image_path = os.path.join(parent_dir, 'keys_images', 'keys_normal.png')
            self.TOTAL_WHITE_KEYS = 52
            self.TOTAL_BLACK_KEYS = 36
            self.SOUNDS_PATH = os.path.join(parent_dir, 'sounds_normal')
        else:
            keys_image_path = os.path.join(parent_dir, 'keys_images', 'keys_small.png')
            self.TOTAL_WHITE_KEYS = 24
            self.TOTAL_BLACK_KEYS = 17
            self.SOUNDS_PATH = os.path.join(parent_dir, 'sounds_small')
        self.KEYS_IMG = imread(keys_image_path)
        self.KEYS_IMG_WIDTH = self.KEYS_IMG.shape[1]
        self.KEYS_IMG_HEIGHT = self.KEYS_IMG.shape[0]
        self.WHITE_KEYS_WIDTH = self.KEYS_IMG_WIDTH / self.TOTAL_WHITE_KEYS
        self.WHITE_KEYS_WIDTH_NORMALIZED = self.WHITE_KEYS_WIDTH / self.KEYS_IMG_WIDTH
        self.HAND_WIDTH = 5. / self.TOTAL_WHITE_KEYS * self.KEYS_IMG_WIDTH * 0.8
        self.ALPHA = 0.1
