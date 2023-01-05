# coding=utf-8
# Copyright (c) 2023 byeyang
import sys
import os
import subprocess
import wave
import json
import requests
import datetime
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from transcriber_ui import TranscriberHandleUi
from PySide2.QtCore import Qt, QThread, Signal
from vosk import Model, KaldiRecognizer, SetLogLevel
from translate import Translator


file_dir = os.path.dirname(os.path.realpath(__file__))
FFMPEG_PATH = os.path.join(file_dir, "ffmpeg.exe")
en_us_lgraph = os.path.join(file_dir, "models", "vosk-model-en-us-0.22-lgraph")
en_us_gigaspeech = os.path.join(file_dir, "models", "vosk-model-en-us-0.42-gigaspeech")
en_us_small = os.path.join(file_dir, "models", "vosk-model-small-en-us-0.15")
en_us = os.path.join(file_dir, "models", "vosk-model-en-us-0.22")


class WorkerThread(QThread):
    print_status = Signal(str)
    all_finished = Signal(bool)
    translate_show = Signal(str)
    transcribe_show = Signal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.cmd = ""
        self.tmp_wav = ""
        self.model_name = ""
        self.word = ""
        self.net_flag = ""
        self.lang_to_lang = ""

    def process_args(self, cmd="", tmp_wav="", model_name="", word="", net_flag="", lang_to_lang=""):
        self.cmd = cmd
        self.tmp_wav = tmp_wav
        self.model_name = model_name
        self.word = word
        self.net_flag = net_flag
        self.lang_to_lang = lang_to_lang

    def run(self):
        try:
            if self.cmd:
                proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
                self.print_status.emit(
                    "{} 正在进入音频文件预处理阶段".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                    self.print_status.emit("Audio file must be WAV format mono PCM.")
                    return
                self.print_status.emit(
                    "{} 正在进入音频文件转换阶段".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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

            if self.net_flag == "internet":
                self.print_status.emit(
                    "{} 正在进入连网翻译阶段".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                translateResult = translate_youdao(self.word)
                if translateResult:
                    self.translate_show.emit(u"连网翻译结果:" + "\n " + translateResult)
                else:
                    self.translate_show.emit(u"有点问题,翻译失败.")

            if self.net_flag == "No_network":
                try:
                    self.print_status.emit(
                        "{} 正在进入无网翻译阶段".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    if self.lang_to_lang == "english to chinese":
                        translateResult = Translator(from_lang="English", to_lang="Chinese").translate(self.word)
                    else:
                        translateResult = Translator(from_lang="Chinese", to_lang="English").translate(self.word)
                    self.translate_show.emit(u"无网翻译结果:" + "\n " + translateResult)
                except:
                    self.translate_show.emit(u"有点问题,翻译失败.遇到这个问题请使用其他翻译软件")

            self.all_finished.emit(True)
            self.print_status.emit(
                "{} 操作已完成 {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "*" * 20))
        except Exception as e:
            self.print_status.emit("An unknown error has occurred....!")
            self.print_status.emit(e)
            self.all_finished.emit(True)
            return

    def stop(self):
        self.terminate()


class TranscriberHandle(TranscriberHandleUi):

    def __init__(self):
        super(TranscriberHandle, self).__init__()
        self.tmp_wav = ""
        self.result = ""
        self.wav_path = ""
        self.model_name = ""
        self.mode_name = ""
        self.browse_btn.clicked.connect(self.openFileDialog)
        self.transcribe_button.clicked.connect(self.wav_transcribe)
        self.translate_button.clicked.connect(lambda: self.word_translate(net_flag=True))
        self.no_net_translate_button.clicked.connect(lambda: self.word_translate(net_flag=False))
        self.work_thread = WorkerThread()
        self.work_thread.all_finished.connect(self.button_status)
        self.work_thread.print_status.connect(self.print_status_to_gui)
        self.work_thread.transcribe_show.connect(self.transcribe_text_edit_show)
        self.work_thread.translate_show.connect(self.translate_text_edit_show)

    def button_status(self, status_bool):
        self.translate_button.setEnabled(status_bool)
        self.no_net_translate_button.setEnabled(status_bool)
        self.transcribe_button.setEnabled(status_bool)
        self.browse_btn.setEnabled(status_bool)
        self.model_combo.setEnabled(status_bool)
        self.mode_combo.setEnabled(status_bool)

    def transcribe_text_edit_show(self, text):
        self.transcribe_text_edit.setHtml("<font color=#006699 size=5 >%s</font>" % text)

    def translate_text_edit_show(self, text):
        self.translate_text_edit.setHtml("<font color=#006699 size=5 >%s</font>" % text)

    def print_status_to_gui(self, text):
        if text:
            self.result = self.result + "\n" + text
            self.text_browser.setText("%s" % self.result.strip())
            self.text_browser.setTextCursor(self.cursor)

    def word_translate(self, net_flag=True):
        self.button_status(False)
        self.result = ""
        self.print_status_to_gui("{} 操作已开始 ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        word = self.transcribe_text_edit.toPlainText()
        if net_flag:
            self.work_thread.process_args(word=word, net_flag="internet")
        else:
            self.work_thread.process_args(word=word, net_flag="No_network")
        self.work_thread.start()

    def wav_transcribe(self):
        self.result = ""
        self.print_status_to_gui("{} 操作已开始 ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.wav_path = self.target_wav.text()
        self.model_name = self.model_combo.currentText()
        self.mode_name = self.mode_combo.currentText()
        self.button_status(False)
        tmp_dir = os.path.join(os.getenv('TEMP'), "transcriber_handle")
        if not os.path.exists(tmp_dir):  # os.path can't check an existed path that contains Chinese
            try:
                os.mkdir(tmp_dir)
            except Exception:
                QMessageBox.warning(None, "warning", "无权限创建临时文件...", QMessageBox.Ok)
        self.tmp_wav = tmp_dir + "/" + "tmp_" + os.path.basename(self.wav_path)
        command = '%s -y -i %s -ac 1  %s' % (FFMPEG_PATH, self.wav_path, self.tmp_wav)
        try:
            gbk_command = command.encode('utf-8').decode('utf-8')
        except:
            QMessageBox.warning(None, "warning", u"出错!请检查相关路径,音频文件等是否有中文或特殊字符.", QMessageBox.Ok)
            return False
        self.work_thread.process_args(cmd=gbk_command, model_name=eval(self.model_name), tmp_wav=self.tmp_wav,
                                      lang_to_lang=self.mode_name)
        self.work_thread.start()

    def openFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setNameFilter("wav file(*.wav);;all file(*)")
        if file_dialog.exec_():
            wav_path = file_dialog.selectedFiles()
            self.target_wav.setText(wav_path[0])


def translate_youdao(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        result = json.loads(response.text)
        translateResult = result['translateResult'][0][0]['tgt']
        return translateResult
    else:
        print(u"有道词典调用失败")
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TranscriberHandle()
    win.show()
    sys.exit(app.exec_())
