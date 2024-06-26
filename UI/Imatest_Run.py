# -*- coding: utf-8 -*-
import subprocess
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool
from Tree_Widget import Ui_MainWindow
import yaml
import os
import shutil
import re
import time
import zipfile


class tree(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(tree, self).__init__()
        self.setupUi(self)
        self.intiui()
        self.camera_param = 0

    def intiui(self):
        self.group.buttonClicked[int].connect(self.on_check_box_clicked)
        self.F_data_upload_button.clicked.connect(self.upload_F_csv_file)
        self.D65_data_upload_button.clicked.connect(self.upload_D65_csv_file)
        self.TL84_data_upload_button.clicked.connect(self.upload_TL84_csv_file)
        self.TL83_data_upload_button.clicked.connect(self.upload_TL83_csv_file)
        self.CWF_data_upload_button.clicked.connect(self.upload_CWF_csv_file)
        self.Mix_data_upload_button.clicked.connect(self.upload_Mix_csv_file)
        self.HJ_data_upload_button.clicked.connect(self.upload_HJ_csv_file)

        self.submit_button.clicked.connect(self.handle_submit)

    def get_message_box(self, text):
        QMessageBox.warning(self, "错误提示", text)

    def handle_submit(self):
        # 文本框非空检查
        if not self.is_800_camera.isChecked() and not self.is_500_camera.isChecked() and not self.is_200_camera.isChecked() \
                and not self.is_1600_camera.isChecked() and not self.is_1300_camera.isChecked():
            self.get_message_box("请勾选其中一个摄像头参数!!!")
            return
        if len(self.camera_product_edit.text()) == 0:
            # 显示错误消息框
            self.get_message_box("摄像头厂家不能为空,请输入!!!")
            return
        if len(self.project_edit.text()) == 0:
            self.get_message_box("项目名称不能为空, 请输入!!!")
            return
        F_path_length = len(self.F_file_path.text())
        D65_path_length = len(self.D65_file_path.text())
        TL84_path_length = len(self.TL84_file_path.text())
        TL83_path_length = len(self.TL83_file_path.text())
        CWF_path_length = len(self.CWF_file_path.text())
        Mix_path_length = len(self.Mix_file_path.text())
        HJ_path_length = len(self.HJ_file_path.text())
        if F_path_length == 0 and D65_path_length == 0 and TL83_path_length == 0 and TL84_path_length == 0 and CWF_path_length == 0 and Mix_path_length == 0 and HJ_path_length == 0:
            self.get_message_box("请上传测试的csv!!!")

        # # 检设备名字，检查check box 属性
        self.data["CameraData"]["pixels"] = self.camera_param
        self.data["CameraData"]["project_name"] = self.project_edit.text()
        self.data["CameraData"]["camera_product"] = self.camera_product_edit.text()
        self.data["CameraData"]["is_f_test"] = "true" if F_path_length != 0 else "false"
        self.data["CameraData"]["is_d65_test"] = "true" if D65_path_length != 0 else "false"
        self.data["CameraData"]["is_tl84_test"] = "true" if TL84_path_length != 0 else "false"
        self.data["CameraData"]["is_tl83_test"] = "true" if TL83_path_length != 0 else "false"
        self.data["CameraData"]["is_cwf_test"] = "true" if CWF_path_length != 0 else "false"
        self.data["CameraData"]["is_hj_test"] = "true" if HJ_path_length != 0 else "false"
        self.data["CameraData"]["is_mix_test"] = "true" if Mix_path_length != 0 else "false"
        #
        # # 保存修改后的内容回 YAML 文件
        with open(self.yaml_file_path, 'w') as file:
            yaml.safe_dump(self.data, file)
        # self.close()
        # subprocess.run([os.path.join(self.project_path, "run.bat")])
        # 拷贝csv文件到相应的目录
        test_data_path = os.path.join(self.project_path, "TestData")
        if F_path_length != 0:
            des_folder = os.path.join(test_data_path, "F")
            des_file = os.path.join(des_folder, "F.csv")
            file_copied_path = os.path.join(des_folder, os.path.basename(self.F_file_path))
            self.remove_file_directory(des_file)
            self.copy_file(self.F_file_path, des_folder)
            self.rename_file(file_copied_path, des_file)
        # package_path = os.path.join(self.project_path, "APK")
        # low_ver_apk_name = self.low_ver_apk_file_path.text()
        # high_ver_apk_name = self.low_ver_apk_file_path.text()
        # if self.has_path_symbol(low_ver_apk_name):
        #     real_low_ver_apk_name = low_ver_apk_name.split("/")[-1]
        #     # 修改字段值
        #     self.data["DeviceTestData"]["apk"]["low_version_app"] = real_low_ver_apk_name
        #     self.copy_file(low_ver_apk_name, package_path + real_low_ver_apk_name)
        # if self.has_path_symbol(high_ver_apk_name):
        #     real_high_ver_apk_name = high_ver_apk_name.split("/")[-1]
        #     # 修改字段值
        #     self.data["DeviceTestData"]["apk"]["high_version_app"] = real_high_ver_apk_name
        #     self.copy_file(high_ver_apk_name, package_path + real_high_ver_apk_name)

    def deal_csv_file(self, light, csv_name, file_path):
        test_data_path = os.path.join(self.project_path, "TestData")
        des_folder = os.path.join(test_data_path, light)
        des_file = os.path.join(des_folder, csv_name)
        file_copied_path = os.path.join(des_folder, os.path.basename(file_path))
        self.remove_file_directory(des_file)
        self.copy_file(file_path, des_folder)
        self.rename_file(file_copied_path, des_file)


    def on_check_box_clicked(self, id):
        # 处理复选框点击事件
        if id == 1:
            self.camera_param = 800
        elif id == 2:
            self.camera_param = 500
        elif id == 3:
            self.camera_param = 200
        elif id == 4:
            self.camera_param = 1300
        elif id == 5:
            self.camera_param = 1600

    def copy_file(self, origin, des):
        self.remove_file_directory(des)
        shutil.copy(origin, des)

    def rename_file(self, origin, des):
        shutil.move(origin, des)

    def remove_file_directory(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def path_is_existed(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def upload_F_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.F_file_path.setText(file_name)

    def upload_D65_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.D65_file_path.setText(file_name)

    def upload_TL84_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.TL84_file_path.setText(file_name)

    def upload_TL83_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.TL83_file_path.setText(file_name)

    def upload_CWF_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.CWF_file_path.setText(file_name)

    def upload_Mix_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.Mix_file_path.setText(file_name)

    def upload_HJ_csv_file(self):
        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                             "All Files (*);;Text Files (*.txt)",
                                                             options=self.options)
        if file_name:
            self.HJ_file_path.setText(file_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = tree()
    myshow.show()
    sys.exit(app.exec_())
