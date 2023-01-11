# coding=utf-8
# Copyright (c) 2023 byeyang
import os
import subprocess
import wave
import json
import datetime
import webbrowser
from PySide6.QtCore import (QThread, Signal)
from PySide6.QtWidgets import (QApplication, QFileDialog, QMessageBox, QMainWindow)
from PySide6.QtGui import QIcon
from ui.transcriberTool_ui import Ui_MainWindow
from vosk import Model, KaldiRecognizer, SetLogLevel

file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace("\\", "/").replace("//", "/")
ffmpeg_path = "/".join([file_dir, "external", "ffmpeg.exe"])
ico_path = os.path.join(file_dir, "ui", "icon", "Tripartite.png")


class TranscriberLaunch(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(TranscriberLaunch, self).__init__()
        self.setupUi(self)
        self.tmp_wav = ""
        self.wav_path = ""
        self.model_name = ""
        self.init_set()
        self.wavBrowser.clicked.connect(self.openFileDialog)
        self.downloadLinkButton.clicked.connect(self.downloadModel)
        self.transcriberButton.clicked.connect(self.wav_transcriber)
        self.modelComboBox.activated.connect(self.modelGet)
        self.work_thread = WorkerThread()
        self.work_thread.all_finished.connect(self.button_status)
        self.work_thread.print_status.connect(self.print_status_to_gui)
        self.work_thread.transcribe_show.connect(self.transcribe_text_edit_show)

    def init_set(self):
        app_icon = QIcon(ico_path)
        self.setWindowIcon(app_icon)

        model_dir = "/".join([file_dir, "models"])
        for i in os.listdir(model_dir):
            model_file = "/".join([model_dir, i])
            self.modelComboBox.addItem(model_file)

    def transcribe_text_edit_show(self, text):
        self.outputBrowser.setHtml("<font color=#180e35 size=6 >%s</font>" % text)

    def button_status(self, status_bool):
        self.wavBrowser.setEnabled(status_bool)
        self.downloadLinkButton.setEnabled(status_bool)
        self.transcriberButton.setEnabled(status_bool)
        self.wavLineEdit.setEnabled(status_bool)
        self.modelComboBox.setEnabled(status_bool)
        self.outputBrowser.setEnabled(status_bool)

    def print_status_to_gui(self, text):
        if text:
            print(text.strip())

    def openFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setNameFilter("wav file(*.wav);all file(*)")
        if file_dialog.exec():
            wav_path = file_dialog.selectedFiles()
            self.wavLineEdit.setText(wav_path[0])

    def modelGet(self):
        self.modelComboBox.clear()
        model_dir = "/".join([file_dir, "models"])
        for i in os.listdir(model_dir):
            model_file = "/".join([model_dir, i])
            self.modelComboBox.addItem(model_file)

    def downloadModel(self):
        webbrowser.open('https://alphacephei.com/vosk/models')

    def wav_transcriber(self):
        self.print_status_to_gui("{} Operation started ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.wav_path = self.wavLineEdit.text()
        self.model_name = self.modelComboBox.currentText()
        self.button_status(False)
        tmp_dir = os.path.join(os.getenv('TEMP'), "transcriber_wav")
        if not os.path.exists(tmp_dir):  # os.path can't check an existed path that contains Chinese
            try:
                os.mkdir(tmp_dir)
            except Exception:
                QMessageBox.warning(None, "warning", "Failed to create temporary file...", QMessageBox.Ok)
        self.tmp_wav = tmp_dir + "/" + "tmp_" + os.path.basename(self.wav_path)
        command = '%s -y -i %s -ac 1  %s' % (ffmpeg_path, self.wav_path, self.tmp_wav)
        try:
            gbk_command = command.encode('utf-8').decode('utf-8')
        except:
            QMessageBox.warning(None, "warning",
                                u"error!Please check whether there are Chinese or special characters in the audio file.",
                                QMessageBox.Ok)
            return False
        self.work_thread.process_args(cmd=gbk_command, model_name=self.model_name, tmp_wav=self.tmp_wav)
        self.work_thread.start()


class WorkerThread(QThread):
    print_status = Signal(str)
    all_finished = Signal(bool)
    transcribe_show = Signal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.cmd = ""
        self.tmp_wav = ""
        self.model_name = ""
        self.net_flag = ""

    def process_args(self, cmd="", tmp_wav="", model_name=""):
        self.cmd = cmd
        self.tmp_wav = tmp_wav
        self.model_name = model_name

    def run(self):
        try:
            self.print_status.emit(
                "{} Entering audio file preprocessing stage".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(self.cmd)
            while proc.poll() is None:
                try:
                    line = proc.stdout.readline()
                    self.print_status.emit(line)
                except:
                    pass
            SetLogLevel(0)
            if not os.path.exists(self.tmp_wav):
                self.print_status.emit("temp Audio file not exists")
                return

            wf = wave.open(self.tmp_wav, "rb")
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                self.print_status.emit("Audio file must be WAV format mono PCM.")
                return

            self.print_status.emit(
                "{} Entering audio file conversion phase".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            model = Model(self.model_name)
            rec = KaldiRecognizer(model, wf.getframerate())
            text = ""
            while True:
                data = wf.readframes(1000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    jres = json.loads(rec.Result())
                    text = text + " " + jres["text"]
            jres = json.loads(rec.FinalResult())
            text = " " + jres["text"]
            self.transcribe_show.emit(text)

            self.all_finished.emit(True)
            self.print_status.emit(
                "{} operation completed {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "*" * 20))
        except Exception as e:
            self.print_status.emit("An unknown error has occurred....!")
            self.print_status.emit(e)
            self.all_finished.emit(True)
            return

    def stop(self):
        self.terminate()


if __name__ == '__main__':
    app = QApplication()
    Transcriber = TranscriberLaunch()
    Transcriber.setWindowTitle("TranscriberTool")
    Transcriber.show()
    app.exec()
