# -*-coding:utf-8-*-
from cv2.cv2 import getRotationMatrix2D, warpAffine, resize
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from face_recognition import face_locations, face_encodings

class FMP(object):
    """
    人脸图像处理
    """

    def __init__(self):
        pass

    def rotation(image, angle, center=None, scale=1.0):
        """
        旋转图片
        :param image:缓存图片
        :param angle:角度
        :param center:中心点
        :param scale:
        :return:the rotated image
        """

        (height, width) = image.shape[:2]  # 长宽
        if center is None:  # 默认中心为中点
            center = (width // 2, height // 2)
        Matrix = getRotationMatrix2D(center, angle, scale)
        rotated = warpAffine(image, Matrix, (width, height))
        return rotated


if __name__ == '__main__':
    from cv2.cv2 import VideoCapture
    flag, img = VideoCapture(0).read()
    img = resize(img, (0, 0), fx=0.3, fy=0.3)
    loc = face_locations(img, model='cnn')
    en = face_encodings(img, loc)
    print(loc[0], '\n', en[0])