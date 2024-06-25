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

    def checkDeviceOnline(self):
        if self.checkbox_serial.isChecked():
            device_name = self.edit_device_name_COM.text()
        else:
            device_name = self.edit_device_name.currentText()
        if len(device_name) == 0:
            self.get_message_box("设备名称为空，输入设备名称")
            return

        # 需要串口的情况
        if self.checkbox_serial.isChecked():
            # pass
            COM_name = self.COM_name.currentText()
            if COM_name.strip() in self.serial.get_current_COM():
                self.serial.loginSer(COM_name)
                if self.serial.check_usb_adb_connect_serial(device_name):
                    current_firmware_version = self.serial.invoke(
                        "adb -s %s shell getprop ro.product.version" % device_name)
                    self.device_state_tips.setText("设备当前的版本：%s" % self.serial.remove_space(current_firmware_version))
                    self.device_state_tips.setVisible(True)
                else:
                    self.device_state_tips.setText("设备%s不在线， 请再次测试！！！" % device_name)
                    self.device_state_tips.setVisible(True)
                self.serial.confirm_relay_closed()
                self.serial.logoutSer()
            else:
                self.get_message_box("没有可用的串口，请检查！！！")
        else:
            # 不需要串口的情况下
            if self.serial.check_usb_adb_connect_no_serial(device_name):
                current_firmware_version = self.serial.invoke(
                    "adb -s %s shell getprop ro.product.version" % self.edit_device_name.currentText())
                self.device_state_tips.setText(
                    "设备当前的版本：%s" % self.serial.remove_space(current_firmware_version))
                self.device_state_tips.setVisible(True)
            else:
                self.device_state_tips.setText("设备%s不在线， 请再次测试！！！" % device_name)
                self.device_state_tips.setVisible(True)

    def handle_submit(self):

        # 获取文本框中的文本内容
        tree_status = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            # print(item)
            # 2 表示已勾选，0 表示未勾选，1 表示半选中
            tree_status.append(self.get_tree_item_status(item))

        # 修改yaml 数据的属性值
        if 'TestCase' not in self.data:
            self.data["TestCase"] = {}

        for slave in tree_status[0]["children"]:
            # print(slave)
            if slave["text"] == '维护测试用例':
                base_test = "Base_Test"
                if base_test not in self.data["TestCase"]:
                    self.data["TestCase"][base_test] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"][base_test]["%s-case%d" % (base_test, i)] = int(child["status"])
                    i += 1
            elif slave["text"] == '配置包测试':
                config_test = "Config_Test"
                if config_test not in self.data["TestCase"]:
                    self.data["TestCase"][config_test] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"][config_test]["%s-case%d" % (config_test, i)] = int(child["status"])
                    i += 1

        # 拷贝上传的apk文件并且改变yaml 里字段的值
        package_path = os.path.join(self.project_path, "APK")
        # work_path = self.project_path + "\\Param\\Work_APP\\"
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

        # 检测到有勾选到配置包测试再执行
        if "Config_Test-case" in self.data["Run_Cases"]:
            # 拷贝上传的向导包并且改变yaml 里字段的值
            config_path = os.path.join(self.project_path, "ConfigPackage")
            # 解压的路径
            expectConfigResultPath = os.path.join(self.project_path, "ExpectTestResult", "ConfigPackageRelate",
                                                  "ExpectResult")
            original_config_package_path = self.config_package_path.text()
            if original_config_package_path:
                if self.has_path_symbol(original_config_package_path):
                    config_package_name = os.path.basename(original_config_package_path)
                    self.data['DeviceTestData']['config_package'] = config_package_name
                    # 复制，解压
                    print("原来的路径为： %s" % original_config_package_path)
                    print("复制后的路径为： %s" % os.path.join(config_path, config_package_name))
                    self.copy_file(original_config_package_path, os.path.join(config_path, config_package_name),
                                   over_write=True)
                else:
                    config_package_name = original_config_package_path.strip()
                # 解压
                # 先清空里面的文件文件夹，再解压， 保持文件夹干净
                for i in os.listdir(expectConfigResultPath):
                    self.remove_file_directory(os.path.join(expectConfigResultPath, i))
                self.unzip(os.path.join(config_path, config_package_name), expectConfigResultPath)

        # 需要测试的数据：General_Test - case0, General_Test - case4, General_Test - case5, General_Test - case6
        # 保存修改后的内容回 YAML 文件
        with open(self.yaml_file_path, 'w') as file:
            yaml.safe_dump(self.data, file)
        self.close()
        subprocess.run([os.path.join(self.project_path, "run.bat")])

    # 获取所有节点的状态
    def get_tree_item_status(self, tree_item):
        status = tree_item.checkState(0)
        if status == 2:
            self.cases_selected_sum += 1
        result = {
            "text": tree_item.text(0),
            "status": status,
            "children": []
        }
        # 我添加的
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            # print(child_item.text())
            # print(self.get_tree_item_status(child_item))
            result["children"].append(self.get_tree_item_status(child_item))
        return result

    def handle_selection_changed(self):
        tree_status = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            tree_status.append(self.get_tree_item_status(item))

    def handlechanged(self, item, column):
        # 获取选中节点的子节点个数
        count = item.childCount()
        # 如果被选中
        if item.checkState(column) == Qt.Checked:
            # 连同下面子子节点全部设置为选中状态
            for f in range(count):
                if item.child(f).checkState(0) != Qt.Checked:
                    item.child(f).setCheckState(0, Qt.Checked)
        # 如果取消选中
        if item.checkState(column) == Qt.Unchecked:
            # 连同下面子子节点全部设置为取消选中状态
            for f in range(count):
                if item.child(f).checkState != Qt.Unchecked:
                    item.child(f).setCheckState(0, Qt.Unchecked)

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

    def has_path_symbol(self, input_string):
        pattern = r'[\\/]'
        return bool(re.search(pattern, input_string))

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

    def onSerialCheckboxStateChanged(self, state):
        if state == 2:  # 选中状态
            self.COM_name.setEnabled(True)
            self.edit_device_name_COM.setEnabled(True)
            self.edit_device_name.setDisabled(True)
            ports = self.serial.get_current_COM()
            for port in ports:
                self.COM_name.addItem(port)
            if len(ports) == 0:
                self.err_COM_Tips.setText("没有可用的COM口, 请检查！！！")
                self.err_COM_Tips.setVisible(True)
                self.COM_name.setEnabled(True)
            elif len(ports) == 1:
                pass
            else:
                self.err_COM_Tips.setText("当前多个COM可用, 请选择需测试COM口！！！")
                self.err_COM_Tips.setVisible(True)
        else:
            self.edit_device_name_COM.setDisabled(True)
            self.edit_device_name.setEnabled(True)
            self.err_COM_Tips.setVisible(False)
            self.COM_name.setDisabled(True)

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
