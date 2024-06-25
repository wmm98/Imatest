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

    def intiui(self):
        pass

        # self.low_ver_apk_upload_button.clicked.connect(self.low_apk_upload_file)
        # self.high_ver_apk_upload_button.clicked.connect(self.high_apk_upload_file)
        # self.config_package_button.clicked.connect(self.config_package_upload)
        #
        # # 使能COM口输入框
        # self.checkbox_serial.stateChanged.connect(self.onSerialCheckboxStateChanged)
        # # 显示设备
        # self.selectDevicesName()
        # # 测试设备状态：
        # self.devic_online_btn.clicked.connect(self.checkDeviceOnline)
        # # 连接信号和槽
        # self.submit_button.clicked.connect(self.handle_submit)

    def get_message_box(self, text):
        QMessageBox.warning(self, "错误提示", text)

    def handle_submit(self):
        # 拷贝上传的apk文件并且改变yaml 里字段的值
        package_path = os.path.join(self.project_path, "APK")
        low_ver_apk_name = self.low_ver_apk_file_path.text()
        high_ver_apk_name = self.low_ver_apk_file_path.text()
        if self.has_path_symbol(low_ver_apk_name):
            real_low_ver_apk_name = low_ver_apk_name.split("/")[-1]
            # 修改字段值
            self.data["DeviceTestData"]["apk"]["low_version_app"] = real_low_ver_apk_name
            self.copy_file(low_ver_apk_name, package_path + real_low_ver_apk_name)
        if self.has_path_symbol(high_ver_apk_name):
            real_high_ver_apk_name = high_ver_apk_name.split("/")[-1]
            # 修改字段值
            self.data["DeviceTestData"]["apk"]["high_version_app"] = real_high_ver_apk_name
            self.copy_file(high_ver_apk_name, package_path + real_high_ver_apk_name)

        # 文本框非空检查
        if len(self.edit_device_name.currentText()) == 0:
            # 显示错误消息框
            self.get_message_box("设备名称不能为空!")
            return
        if len(self.low_ver_apk_file_path.text()) == 0:
            self.get_message_box("请上传低版本APK包!")
            return
        if len(self.high_ver_apk_file_path.text()) == 0:
            self.get_message_box("请上传高版本APK包!")
            return

        # 检设备名字，检查check box 属性
        self.data["DeviceTestData"]["android_device_info"]["is_serial"] = self.checkbox_serial.isChecked()
        self.data["DeviceTestData"]["android_device_info"]["is_landscape"] = self.checkbox_screen.isChecked()
        self.data["DeviceTestData"]["android_device_info"]["is_local_kernel"] = self.is_local_kernel.isChecked()
        self.data["DeviceTestData"]["android_device_info"]["is_handheld"] = self.checkbox_handheld.isChecked()
        if self.checkbox_serial.isChecked():
            self.data["DeviceTestData"]["android_device_info"]["COM"] = self.COM_name.currentText()
            self.data["DeviceTestData"]["android_device_info"]["device_name"] = self.edit_device_name_COM.text()
        else:
            self.data["DeviceTestData"]["android_device_info"]["device_name"] = self.edit_device_name.currentText()

        testcases = []
        for cases in self.data["TestCase"]:
            for case in self.data["TestCase"][cases]:
                if self.data["TestCase"][cases][case] == 2:
                    testcases.append(case)
        # 检测用例为非空
        print("勾选case的总数： %d" % self.cases_selected_sum)
        if self.cases_selected_sum == 0:
            self.get_message_box("请勾选需要测试的用例！！！")
            return
        # 保存要跑得用例
        self.data["Run_Cases"] = ",".join(testcases)

        # 保存修改后的内容回 YAML 文件
        with open(self.yaml_file_path, 'w') as file:
            yaml.safe_dump(self.data, file)
        self.close()
        subprocess.run([os.path.join(self.project_path, "run.bat")])

    def copy_file(self, origin, des, over_write=False):
        if self.path_is_existed(origin):
            if over_write:
                if self.path_is_existed(des):
                    self.remove_file_directory(des)
        else:
            raise Exception("此路径不存在: %s, 请检查！！！" % origin)
        shutil.copy(origin, des)

        if self.path_is_existed(origin):
            # while True:
            if not over_write:
                if not self.path_is_existed(des):
                    shutil.copy(origin, des)
                # else:
                #     break
            else:
                if self.path_is_existed(des):
                    os.remove(des)
                shutil.copy(origin, des)
                # time.sleep(1)
        else:
            raise Exception("此路径不存在: %s, 请检查！！！" % origin)

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

    def low_apk_upload_file(self):
        # 打开文件选择对话框
        low_apk_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                                     "All Files (*);;Text Files (*.txt)",
                                                                     options=self.options)
        if low_apk_file_name:
            self.low_ver_apk_file_path.setText(low_apk_file_name)

    def high_apk_upload_file(self):
        # 打开文件选择对话框
        high_apk_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                                      "All Files (*);;Text Files (*.txt)",
                                                                      options=self.options)
        if high_apk_file_name:
            self.high_ver_apk_file_path.setText(high_apk_file_name)

    def config_package_upload(self):
        # 打开文件选择对话框
        config_package_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                                       "All Files (*);;Text Files (*.txt)",
                                                                       options=self.options)
        if config_package_name:
            self.config_package_path.setText(config_package_name)

    def selectDevicesName(self):
        if self.checkbox_serial.isChecked():
            self.serial.loginSer()
            self.serial.confirm_relay_opened()
            time.sleep(1)
        devices_info = self.serial.invoke("adb devices").split("\r\n")[1:-2]
        devices = [device_str.split("\t")[0] for device_str in devices_info if device_str.split("\t")[1] == "device"]
        for device in devices:
            self.edit_device_name.addItem(str(device))

    def CheckCOMBoxTextChange(self, text):
        if self.COM_name.isEnabled():
            if len(text) != 0:
                if text.strip() not in self.serial.get_current_COM():
                    self.err_COM_Tips.setText("当前COM口不可用，请重新输入！！！")
                    self.err_COM_Tips.setVisible(True)
                else:
                    self.err_COM_Tips.setVisible(False)
            else:
                self.err_COM_Tips.setText("请输入可用COM口！！！")
                self.err_COM_Tips.setVisible(True)

    def unzip(self, zip_file, extract_to, src_dir=True):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            if src_dir:
                files = zip_ref.namelist()
                # 获取配置名
                config_dir_name = os.path.splitext([file for file in files if file.endswith('.ini')][0])[0]
                # 解压路径
                unzip_path = os.path.join(extract_to, config_dir_name)
                # 如果存在先删除
                if self.path_is_existed(unzip_path):
                    self.remove_file_directory(unzip_path)
                os.makedirs(unzip_path, exist_ok=True)
                zip_ref.extractall(unzip_path)
            else:
                zip_ref.extractall(extract_to)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = tree()
    myshow.show()
    sys.exit(app.exec_())
