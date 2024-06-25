import os
import yaml
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QLineEdit, QCompleter, QComboBox


class Ui_MainWindow(object):
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    project_path = path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    yaml_file_path = os.path.join(project_path, "Conf", "test_data.yaml")
    # 加载 YAML 文件
    with open(yaml_file_path, 'r+', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.device_info = QtWidgets.QLabel("摄像头信息：")
        self.verticalLayout.addWidget(self.device_info)

        # 将标签添加到水平布局中
        # 添加checkbox
        layout = QHBoxLayout()

        self.is_800_camera = QCheckBox("800万")
        self.is_500_camera = QCheckBox("500万")
        self.is_200_camera = QCheckBox("200万")
        self.is_1300_camera = QCheckBox("1300万")
        self.is_1600_camera = QCheckBox("1600万")

        layout.addWidget(self.is_800_camera)
        layout.addWidget(self.is_500_camera)
        layout.addWidget(self.is_200_camera)
        layout.addWidget(self.is_1300_camera)
        layout.addWidget(self.is_1600_camera)
        # 添加一个拉伸因子以将水平布局放在窗口底部
        layout.addStretch(1)
        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout)

        layout_product = QHBoxLayout()
        self.camera_product_name = QtWidgets.QLabel("摄像头厂家：")
        self.camera_product_edit = QtWidgets.QLineEdit()
        self.project_name = QtWidgets.QLabel("项目名称：")
        self.project_edit = QtWidgets.QLineEdit()
        layout_product.addWidget(self.camera_product_name)
        layout_product.addWidget(self.camera_product_edit)
        layout_product.addWidget(self.project_name)
        layout_product.addWidget(self.project_edit)
        self.verticalLayout.addLayout(layout_product)

        # color check 数据上传
        self.color_F_info = QtWidgets.QLabel("上传F光csv：")
        self.verticalLayout.addWidget(self.color_F_info)
        layout_F_light = QHBoxLayout()
        self.F_file_path = QtWidgets.QLineEdit()
        layout_F_light.addWidget(self.F_file_path)
        self.F_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_F_light.addWidget(self.F_data_upload_button)
        self.verticalLayout.addLayout(layout_F_light)

        self.color_D65_info = QtWidgets.QLabel("上传D65光csv：")
        self.verticalLayout.addWidget(self.color_D65_info)
        layout_D65_light = QHBoxLayout()
        self.D65_file_path = QtWidgets.QLineEdit()
        layout_D65_light.addWidget(self.D65_file_path)
        self.D65_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_D65_light.addWidget(self.D65_data_upload_button)
        self.verticalLayout.addLayout(layout_D65_light)

        self.color_TL84_info = QtWidgets.QLabel("上传TL84光csv：")
        self.verticalLayout.addWidget(self.color_TL84_info)
        layout_TL84_light = QHBoxLayout()
        self.TL84_file_path = QtWidgets.QLineEdit()
        layout_TL84_light.addWidget(self.TL84_file_path)
        self.TL84_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_TL84_light.addWidget(self.TL84_data_upload_button)
        self.verticalLayout.addLayout(layout_TL84_light)

        self.color_TL83_info = QtWidgets.QLabel("上传TL83光csv：")
        self.verticalLayout.addWidget(self.color_TL83_info)
        layout_TL83_light = QHBoxLayout()
        self.TL83_file_path = QtWidgets.QLineEdit()
        layout_TL83_light.addWidget(self.TL83_file_path)
        self.TL83_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_TL83_light.addWidget(self.TL83_data_upload_button)
        self.verticalLayout.addLayout(layout_TL83_light)

        self.color_CWF_info = QtWidgets.QLabel("上传CWF光csv：")
        self.verticalLayout.addWidget(self.color_CWF_info)
        layout_CWF_light = QHBoxLayout()
        self.CWF_file_path = QtWidgets.QLineEdit()
        layout_CWF_light.addWidget(self.CWF_file_path)
        self.CWF_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_CWF_light.addWidget(self.CWF_data_upload_button)
        self.verticalLayout.addLayout(layout_CWF_light)

        self.color_Mix_info = QtWidgets.QLabel("上传混光csv：")
        self.verticalLayout.addWidget(self.color_Mix_info)
        layout_Mix_light = QHBoxLayout()
        self.Mix_file_path = QtWidgets.QLineEdit()
        layout_Mix_light.addWidget(self.Mix_file_path)
        self.Mix_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_Mix_light.addWidget(self.Mix_data_upload_button)
        self.verticalLayout.addLayout(layout_Mix_light)

        self.color_HJ_info = QtWidgets.QLabel("上传灰阶csv：")
        self.verticalLayout.addWidget(self.color_HJ_info)
        layout_HJ_light = QHBoxLayout()
        self.HJ_file_path = QtWidgets.QLineEdit()
        layout_HJ_light.addWidget(self.HJ_file_path)
        self.HJ_data_upload_button = QtWidgets.QPushButton("点击上传")
        layout_HJ_light.addWidget(self.HJ_data_upload_button)
        self.verticalLayout.addLayout(layout_HJ_light)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 提交按钮
        self.submit_button = QtWidgets.QPushButton("开始生成报告")
        self.verticalLayout.addWidget(self.submit_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
