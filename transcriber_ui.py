# coding=utf-8
# Copyright (c) 2023 byeyang
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidgetItem, \
    QMessageBox, QPushButton, QHBoxLayout, QListWidget, QLabel, QTextBrowser, QTabWidget, \
    QDockWidget, QLineEdit, QCheckBox, QComboBox, QGroupBox, QGridLayout, QTextEdit
from PySide2.QtGui import QIcon, QTextCursor
from PySide2.QtCore import Qt
import sys

file_dir = os.path.dirname(os.path.realpath(__file__))
delete_png = os.path.join(file_dir, "icon_png", "delete.png")
help_path = os.path.join(file_dir, "transcriber_help.txt").replace("\\", "/").replace("//", "/")
asset_effect_png = os.path.join(file_dir, "icon_png", "moon.png")
style_file = os.path.join(file_dir, "flatgray.css")


class TranscriberHandleUi(QMainWindow):

    def __init__(self):
        super(TranscriberHandleUi, self).__init__()
        app_icon = QIcon(asset_effect_png)
        self.setWindowIcon(app_icon)
        self.setWindowTitle(u'音频转换器(Transcriber Tool)')
        self.resize(1197, 600)
        table_widget = QTabWidget()
        self.text_browser = QTextBrowser()
        self.text_browser.insertPlainText('')
        self.cursor = self.text_browser.textCursor()
        self.cursor.movePosition(QTextCursor.End)
        self.dockWidget_browser = QDockWidget("过程信息")
        self.dockWidget_browser.setStyleSheet("font-family: Microsoft YaHei;font-size: 8pt;")
        self.dockWidget_browser.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.dockWidget_browser.setWidget(self.text_browser)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_browser)

        self.target_label = QLabel("wav路径:")
        self.target_wav = QLineEdit("")
        self.target_wav.setReadOnly(True)
        self.browse_btn = QPushButton("选择")

        self.model_combo = QComboBox()
        self.model_combo.addItem("en_us_small")
        self.model_combo.addItem("en_us")
        self.model_combo.addItem("en_us_gigaspeech")
        self.model_combo.addItem("en_us_lgraph")

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("english to chinese")
        self.mode_combo.addItem("chinese to english")

        wav_grp_box = QGroupBox("音频选择")
        wav_grp_layout = QGridLayout(wav_grp_box)
        self.transcribe_button = QPushButton("音频转文字")

        wav_grp_layout.addWidget(self.target_label, 1, 1)
        wav_grp_layout.addWidget(self.target_wav, 1, 2)
        wav_grp_layout.addWidget(self.browse_btn, 1, 3)
        wav_grp_layout.addWidget(self.model_combo, 2, 2)
        wav_grp_layout.addWidget(self.transcribe_button, 2, 3)
        button_layout = QHBoxLayout()
        translate_text_layout = QHBoxLayout()

        translate_grp_box = QGroupBox("结果输出")
        translate_show_layout = QVBoxLayout(translate_grp_box)
        self.no_net_translate_button = QPushButton("无网翻译")
        self.translate_button = QPushButton("连网翻译")
        self.transcribe_text_edit = QTextEdit()
        self.translate_text_edit = QTextEdit()
        button_layout.addWidget(self.mode_combo)
        button_layout.addWidget(self.no_net_translate_button)
        button_layout.addWidget(self.translate_button)
        translate_text_layout.addWidget(self.transcribe_text_edit)
        translate_text_layout.addWidget(self.translate_text_edit)
        translate_show_layout.addLayout(button_layout)
        translate_show_layout.addLayout(translate_text_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(wav_grp_box)
        main_layout.addWidget(translate_grp_box)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.help = QTextBrowser()
        self.help.setReadOnly(True)
        content = read_help_text(help_path)
        self.help.setText(content)

        table_widget.addTab(main_widget, "主页")
        table_widget.addTab(self.help, "帮助")
        self.setCentralWidget(table_widget)

        with open(style_file, "r", encoding="UTF-8") as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)


def read_help_text(help_path):
    try:
        with open(help_path, "r", encoding='UTF-8') as f:
            data = str(f.read())
            return data
    except:
        return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_ui = TranscriberHandleUi()
    app_ui.show()
    sys.exit(app.exec_())
