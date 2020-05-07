# -*-coding: utf-8-*-
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
from face_recognition import face_locations, face_encodings
import json
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from TypesEnum import ProcessOperation


class FR(object):
    """
    人脸识别模块
    """

    __path_mapper = './ClientClassifierMapper.xml'

    def __init__(self, ip):
        self.ip = ip  # 客户端IP地址
        self.file_name = None
        tree = ET.parse(self.__path_mapper)  # 解析客户端信息xml
        root = tree.getroot()  # 获取根节点
        res = filter(lambda x: x.get('ip') == ip, root.findall('client'))  # 查找对应客户端信息
        if not res:  # 未查到对应的客户端信息
            raise Exception("no such a client information")
        else:  # 已查到
            for pair in res[0].items():
                if pair[0] == 'file':
                    self.file_name = pair[1]

    def getFaceFeature(self, model_type, image):
        """
        提取人脸特征向量
        :param model_type: 模型类型
        :param image: 待提取图片
        :return: feature -> [d1, ...]
        """

        if model_type == 'svm':
            location = face_locations(image, model='cnn')
            if len(location) == 0:  # 没有提取到特征向量
                raise Exception("image with low quality")
            elif len(location) == 1:
                feature = face_encodings(image, location)
                return feature
            else:  # 存在多个人脸
                raise Exception("too many people here")
        else:
            pass

    def saveSamplesToJson(self, model_type, new_samples):
        """
        存入新样本到json文件
        :param model_type: 模型类型
        :param new_samples: 新样本 -> dict{'label': [samples, ]}
        :return:
        """

        json_file = "".join(['./classification_model/', self.file_name, "/", model_type, "/", "user_feature.json"])
        # 读取之前的样本
        with open(json_file, 'r') as f:
            all_samples = json.load(f)
        # 添加新样本
        for label, samples in new_samples.items():
            all_samples[label] = samples
        # 将样本写入json文件
        with open(json_file, 'w') as f:
            json.dump(all_samples, f)

    def getSamplesFromJson(self, model_type):
        """
        获取json文件中人脸特征样本
        :param model_type: 模型类型
        :return: data -> dict{x:, y:}
        """

        json_file = "".join(['./classification_model/', self.file_name, "/", model_type, "/", "user_feature.json"])
        with open(json_file, 'r') as f:
            samples = json.load(f)
        x = []
        y = []
        for key, value in samples.items():
            for feature in value:
                x.append(feature)
                y.append(int(key))
        return {'x': x, 'y': y}

    def trainClassifier(self, model_type, samples):
        """
        训练分类器
        :param model_type: 模型类型，以便扩展多种模型
        :param samples: 样本
        :return:
        """

        # 映射
        train_mapper = {
            'svm': self.__train_svm_classifier
        }

        try:
            # 训练模型
            model = train_mapper[model_type](samples)
            # 存储模型
            self.__saveModel(model_type, model)
            return {'operation': ProcessOperation.Success, 'exception': None, 'result': None}
        except Exception as e:
            print(e)
            return {'operation': ProcessOperation.Failure, 'exception': Exception("模型训练失败"), 'result': None}

    def classifyTheSample(self, model_type, sample):
        """
        给样本分类，预测类别
        :param model_type:模型类型
        :param sample: 样本
        :return: class
        """

        try:
            model = self.__getModel(model_type)
            if model_type == 'svm':
                result = model.predict(sample)[0]
                return {'operation': ProcessOperation.Success, 'exception': None, 'result': result}
            else:
                pass
        except Exception as e:
            print(e)
            return {'operation': ProcessOperation.Failure, 'exception': Exception("预测失败"), 'result': None}

    def __train_svm_classifier(self, samples):
        """
        私有方法，训练svm分类器
        :param samples: dict{'x': 'y':}
        :return:
        """

        try:
            model = svm.SVC(C=10, gamma=20, kernel='rbf', decision_function_shape='ovr', probability=True, random_state=67)
            model.fit(samples['x'], samples['y'])
            return model
        except Exception as e:
            print(e)
            raise Exception("fail to train svm model")

    def __saveModel(self, model_type, model):
        """
        储存模型
        :param model_type: 模型类型
        :param model: 模型
        :return:
        """

        # 存储方式映射
        storage_mapper = {
            'svm': joblib.dump
        }

        try:
            model_path = "".join(['./classification_model/', self.file_name, "/", model_type, "/", "classification"])
            storage_mapper[model_type](model, model_path)
        except Exception as e:
            print(e)
            raise Exception("fail to save model")

    def __getModel(self, model_type):
        """
        加载模型
        :param model_type:模型类型
        :return:model
        """

        # 加载方式映射
        storage_mapper = {
            'svm': joblib.load
        }
        try:
            model_path = "".join(['classification_model/', self.file_name, "/", model_type, "/", "classification"])
            model = storage_mapper[model_type](model_path)
            return model
        except Exception as e:
            print(e)
            raise Exception("fail to load model")


if __name__ == '__main__':
    FR('127.0.0.1').saveSamplesToJson('svm', {'test': [['a'], ['b']]})