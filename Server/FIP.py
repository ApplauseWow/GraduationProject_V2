# -*-coding:utf-8-*-
from cv2.cv2 import getRotationMatrix2D, warpAffine, addWeighted
import numpy as np


class FIP(object):
    """
    人脸图像处理模块
    """

    def __init__(self):
        pass

    def __contrastAndBrightness(self, alpha, beta, image):
        """
        调整亮度和对比度
        :param alpha:影响对比度 =1原图 >1对比度增强更加清晰 <1对比度减弱更加模糊
        :param beta:影响亮度 (>0) 增加或减少 灰度值增加或降低 变亮或变暗
        :param image:待处理图像
        :return:
        """

        blank = np.zeros(image.shape, image.dtype)
        changed = addWeighted(image, alpha, blank, 1 - alpha, beta)  # 融合两张图片
        return changed

    def __rotation(self, image, angle, center=None, scale=1.0):
        """
        旋转图片
        :param image:待处理图像
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

    def createMoreImage(self, image):
        """
        生成更多的经过处理的人脸图像，旋转，亮度，对比度等
        :return:generator
        """

        # 原图
        yield image
        # 旋转后的
        for angle in [-2, -1, 1, 2]:
            yield self.__rotation(image, 15*angle)
        # 调整对比度和亮度后的
        for alpha in [1.8, 0.8]:
            yield self.__contrastAndBrightness(alpha, 1.3, image)


if __name__ == '__main__':
    f = FIP()
    from cv2.cv2 import imread, imshow, waitKey
    img = imread('./img_cache/ch.jpg')
    for p in f.createMoreImage(img):
        imshow('image', p)
        waitKey(0)
