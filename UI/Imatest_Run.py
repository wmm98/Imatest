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
import threading


class tree(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(tree, self).__init__()
        self.setupUi(self)
        self.intiui()
        self.camera_param = 0
        self.final_report_name = ""

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
        self.data["CameraData"]["is_f_test"] = True if F_path_length != 0 else False
        self.data["CameraData"]["is_d65_test"] = True if D65_path_length != 0 else False
        self.data["CameraData"]["is_tl84_test"] = True if TL84_path_length != 0 else False
        self.data["CameraData"]["is_tl83_test"] = True if TL83_path_length != 0 else False
        self.data["CameraData"]["is_cwf_test"] = True if CWF_path_length != 0 else False
        self.data["CameraData"]["is_hj_test"] = True if HJ_path_length != 0 else False
        self.data["CameraData"]["is_mix_test"] = True if Mix_path_length != 0 else False
        #
        # # 保存修改后的内容回 YAML 文件
        with open(self.yaml_file_path, 'w') as file:
            yaml.safe_dump(self.data, file)

        # 拷贝csv文件到相应的目录
        if HJ_path_length != 0:
            HJ_file_path = self.HJ_file_path.text()
            if not self.check_file_extension_name(HJ_file_path, "灰阶"):
                return
            else:
                self.deal_csv_file("HJ", HJ_file_path)
        if F_path_length != 0:
            f_file_path = self.F_file_path.text()
            if not self.check_file_extension_name(f_file_path, "F"):
                return
            else:
                self.deal_csv_file("F", f_file_path)
        if D65_path_length != 0:
            D65_file_path = self.D65_file_path.text()
            if not self.check_file_extension_name(D65_file_path, "D65"):
                return
            else:
                self.deal_csv_file("D65", D65_file_path)
            self.deal_csv_file("D65", self.D65_file_path.text())
        if TL84_path_length != 0:
            TL84_file_path = self.TL84_file_path.text()
            if not self.check_file_extension_name(TL84_file_path, "TL84"):
                return
            else:
                self.deal_csv_file("TL84", TL84_file_path)
        if TL83_path_length != 0:
            TL83_file_path = self.TL83_file_path.text()
            if not self.check_file_extension_name(TL83_file_path, "TL83"):
                return
            else:
                self.deal_csv_file("TL83", TL83_file_path)
        if CWF_path_length != 0:
            CWF_file_path = self.CWF_file_path.text()
            if not self.check_file_extension_name(CWF_file_path, "CWF"):
                return
            else:
                self.deal_csv_file("CWF", CWF_file_path)
        if Mix_path_length != 0:
            Mix_file_path = self.Mix_file_path.text()
            if not self.check_file_extension_name(Mix_file_path, "混"):
                return
            else:
                self.deal_csv_file("Mix", Mix_file_path)

        # 删除已存在的报告

        if self.path_is_existed(self.final_report_name):
            self.remove_file(self.final_report_name)

        # 显示报告正在生成中
        self.tips.setText("正在生成报告,请等待.....")

        # 单独线程运行,避免阻塞主线程和 PyQt5 的事件
        thread = threading.Thread(target=self.run_process)
        thread.start()

        # 检测报告的生成
        self.final_report_name = "招投标规格参数确认-%s-%s-%d万摄像头-指标测试报告.csv" % (self.data["CameraData"]["camera_product"],
                                                                        self.data["CameraData"]["project_name"],
                                                                        int(self.data["CameraData"]["pixels"]))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_report)

        self.check_interval = 1000  # 定时器间隔，单位毫秒
        self.timeout_limit = 60 * 1000  # 超时限制，单位毫秒, 10秒超时
        self.elapsed_time = 0  # 已经过的时间

        self.timer.start(self.check_interval)  # 启动定时器

    def check_report(self):
        path = os.path.join(self.project_path, self.final_report_name)  # 要检查的路径
        if os.path.exists(path):
            self.tips.setText("报告已经生成:  %s" % self.final_report_name)
            self.timer.stop()  # 如果报告存在，停止定时器
        else:
            self.elapsed_time += self.check_interval
            if self.elapsed_time >= self.timeout_limit:
                self.tips.setText("生成报告失败,请再次生成")
                self.timer.stop()  # 如果超时，停止定时器

    def closeEvent(self, event):
        self.timer.stop()  # 在窗口关闭时停止定时器
        event.accept()

    def run_process(self):
        subprocess.run([os.path.join(self.project_path, "Run", "bat_run.bat")])

    def check_file_extension_name(self, file_name, light):
        if ".csv" != os.path.splitext(file_name)[1].strip():
            self.get_message_box("%s光数据请上传csv格式的数据!!!" % light)
            return False
        return True

    def deal_csv_file(self, light, file_path):
        csv_name = light + os.path.splitext(file_path)[1]
        test_data_path = os.path.join(self.project_path, "TestData")
        des_folder = os.path.join(test_data_path, light)
        des_file = os.path.join(des_folder, csv_name)
        file_copied_path = os.path.join(des_folder, os.path.basename(file_path))
        self.remove_file(des_file)
        self.remove_file(des_file)
        self.copy_file(file_path, des_folder)
        if not self.path_is_existed(des_file):
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
        shutil.copy(origin, des)

    def rename_file(self, origin, des):
        shutil.move(origin, des)

    def remove_file(self, path):
        if os.path.isfile(path):
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
