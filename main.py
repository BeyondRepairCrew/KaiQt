from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QObject, QThread, Signal
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import sys
import scdl.scdl
from soundcloud import SoundCloud

from pytube import YouTube, Playlist

from frm_main import Ui_frm_main
from datetime import timedelta


def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
        print(env)
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    #
    #   Traceback (most recent call last):
    #     File "test_subprocess.py", line 58, in <module>
    #       **subprocess_args(stdout=None))
    #     File "C:\Python27\lib\subprocess.py", line 567, in check_output
    #       raise ValueError('stdout argument not allowed, it will be overridden.')
    #   ValueError: stdout argument not allowed, it will be overridden.
    #
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.DEVNULL,#subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret

class AnalyseWorker(QObject):
    finished = Signal()
    progress = Signal(int)
    url = None
    frm_main = None
    def run(self):
        
            #self.finished.append(link)
            #self.links.remove(link)
            #self.update_queue_table()
            #self.update_result_table()
        self.progress.emit(0)
        self.frm_main.lb_progress.setText("Analysing")
        self.analyse_url()
        self.progress.emit(100)
        self.frm_main.lb_progress.setText("Done")
        self.finished.emit()
    
    def result_is_playlist(self, result):
        if result["type"] == "soundcloud":
            return result["link_specific_data"]["is_soundcloud_playlist"]
        elif result["type"]== "youtube":
            return result["link_specific_data"]["is_youtube_playlist"]
        else:
            return False

    def resolve_desired_format(self):
        selected_format = self.frm_main.cb_format.currentText()
        if "aac" in selected_format:
            return "aac"
        elif "wav" in selected_format:
            return "wav"
        elif "flac" in selected_format:
            return "flac"
        else:
            return "mp3"
        
    def resolve_desired_bitrate(self):
        selected_bitrate = self.frm_main.cb_quality.currentText()
        if "320" in selected_bitrate:
            return "320"
        elif "192" in selected_bitrate:
            return "192"
        elif "128" in selected_bitrate:
            return "128"
        elif "96" in selected_bitrate:
            return "96"
        elif "32" in selected_bitrate:
            return "32"
        elif "16" in selected_bitrate:
            return "16"
        

    def analyse_url(self):
        self.frm_main.bt_analyse.setEnabled(False)
        analyse_result = self.get_hybrid_track_data(self.url)
        if analyse_result["type"] == 'error':
            self.frm_main.lb_analyse_log.setText("Nah bro, this link doesn't work") 
        else: 
            if self.result_is_playlist(analyse_result):
                self.frm_main.lb_analyse_log.setText("Looks like a playlist") 
                if analyse_result["type"]=="soundcloud":
                    client = SoundCloud("a3e059563d7fd3372b49b37f00a00bcf", None)
                    playlist = client.resolve(analyse_result["url"])
                    i = 0
                    self.progress.emit(i)
                    for track_info in playlist.tracks:
                        track = client.get_track(track_info.id)
                        self.frm_main.links.append({
                            "type": "soundcloud",
                            "title": track.title,
                            "url" : track.permalink_url,
                            "link_specific_data":{
                                "is_soundcloud_playlist": False
                            },
                            "desired_format": self.resolve_desired_format(),
                            "desired_bitrate": self.resolve_desired_bitrate(),
                            "duration" : int(track.duration/1000),

                        })
                        i+=1
                        self.progress.emit(i/len(playlist.tracks)*100)
                        self.frm_main.update_queue_table()
                elif analyse_result["type"]=="youtube":
                    video_links = Playlist(analyse_result["url"]).video_urls
                    i = 0
                    self.progress.emit(i)
                    for link in video_links:
                        i+=1
                        yt_link_to_add = self.get_hybrid_track_data(link)
                        yt_link_to_add["desired_format"] = self.resolve_desired_format()
                        self.frm_main.links.append(yt_link_to_add)
                        self.progress.emit(i/len(video_links)*100)
                        self.frm_main.update_queue_table()
                self.frm_main.lb_analyse_log.setText("Ok ready") 
            else:
                analyse_result["desired_format"] = self.resolve_desired_format()
                self.frm_main.links.append(analyse_result)
                self.frm_main.lb_analyse_log.setText("Aite mate, link added") 
        self.frm_main.update_queue_table()
        self.frm_main.bt_analyse.setEnabled(True)


    def get_hybrid_track_data(self, url):
        result = {
            "type": "",
            "title": "",
            "url" : url,
            "link_specific_data": {},
            "desired_bitrate": self.resolve_desired_bitrate()
        }
        try: 
            req = requests.get(url)
            soup = BeautifulSoup(req.text, features="lxml")
            if "soundcloud.com" in req.url:
                client = SoundCloud("a3e059563d7fd3372b49b37f00a00bcf", None)
                result["type"] = "soundcloud"
                result["title"] = str(soup.title.string).replace("Stream ","",1).replace(" | Listen online for free on SoundCloud","",1)
                if "/sets/" in req.url:
                    if "?in=" in req.url:
                        split_url = req.url.split("?in=")
                        if len(split_url)>1:
                            if "/sets/" in split_url[1]:
                                result["link_specific_data"]["is_soundcloud_playlist"] = False
                                result["duration"] = int(client.get_track(client.resolve(url).id).duration/1000)
                        else:
                            result["link_specific_data"]["is_soundcloud_playlist"] = True
                        
                else:
                    result["link_specific_data"]["is_soundcloud_playlist"] = False
                    result["duration"] = int(client.get_track(client.resolve(url).id).duration/1000)
                return result
            elif "youtube.com" in req.url:
                result["type"] = "youtube"
                result["link_specific_data"]["is_private"] = '{"simpleText":"Privates Video"}' in req.text
                result["title"] = str(soup.title.string).replace("- YouTube", "",1).strip()
                result["link_specific_data"]["is_youtube_playlist"] = "/playlist?" in req.url or "&list=" in req.url
                result["link_specific_data"]["is_youtube_channel"] = "/channel/" in req.url or "/c/" in req.url
                result["link_specific_data"]["url"] = req.url
                result["duration"] = YouTube(url).length
                return result

        except Exception as e:
            print(e)
            result["type"] = "error"
            return result


class DownloadWorker(QObject):
    finished = Signal()
    progress = Signal(int)
    download_list = []
    original_cwd = None
    frm_main = None
    def run(self):
        self.original_cwd = os.getcwd()
        i = 0
        self.progress.emit(0)
        for link in self.download_list:
            self.frm_main.lb_progress.setText("Downloading") 
            if link["type"]=="soundcloud":
                try:
                    self.download_soundcloud(link["url"],format=link["desired_format"], bitrate="320")
                except Exception as e:
                    print("Error while downloading soundcloud:", e)
                except SystemExit as e:
                    print("Error while downloading soundcloud:", e)
            elif link["type"] == "youtube":
                try:
                    self.download_youtube(link["url"], format=link["desired_format"], bitrate="320", current_progress=i)
                except Exception as e:
                    raise(e)
                    print("Error while downloading youtube:", e)
            self.frm_main.finished.append(link)
            self.frm_main.update_result_table()
            i+=1
            self.progress.emit(i/len(self.download_list)*100)
        self.frm_main.lb_progress.setText("Done") 
        self.finished.emit()
    
    def download_soundcloud(self, url, format="mp3", bitrate="320"):
        path = r"./mp3/"
        
        if os.path.exists(path):
            os.chdir(path)
        client = SoundCloud("a3e059563d7fd3372b49b37f00a00bcf", None)
        #item = client.resolve(url)
        kwargs= {
            "l" : url,
            "playlist_name_format" : "{title}",
            "name_format": "{title}",
            "flac": True,
            "onlymp3": None,
            "no_original": False,
            "overwrite": True
        }
        print(format)
        if format=="flac":
            print("Trying to download flac")
            scdl.scdl.download_url(client, **kwargs)
        else:
            kwargs["onlymp3"] = format == "mp3"

            scdl.scdl.download_url(client,**kwargs )

        os.chdir(self.original_cwd)

    def download_youtube(self, url, current_progress, format="mp3", bitrate="320", ):
        path = r"./mp3"

        #command = 'yt-dlp.exe '+url+' -x --audio-format "'+format+'" --audio-quality "'+bitrate+'K" -o '+path+'"/%(title)s.%(ext)s"'
        command = 'yt-dlp.exe '+url+' -x --audio-format '+format+' --audio-quality '+bitrate+'K -o '+path+'/%(title)s.%(ext)s'
        #
        # stream = os.popen(command,close_fds=True)
        #line = stream.readline()        
        import os

        try:
            from subprocess import DEVNULL
        except ImportError:
            DEVNULL = os.open(os.devnull, os.O_RDWR)
        
        #print(list(command.split(" ")))
        
        stream = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        #stream = subprocess.Popen(list(command.split(" ")), **subprocess_args(True))

        #line = str(stream.stdout.readline(), encoding="utf-8")        
        line = stream.stdout.read1().decode("utf-8")

        #print(line)

        while True:
            #line = str(line, encoding="utf-8")
            if line:
                if "[download]" in line:
                    try:
                        stripped = line.replace("[download]", "")
                        split_str = stripped.split('%')
                        percentage = float(split_str[0].replace(" ", ""))
                        new_progress = current_progress/len(self.download_list) + (percentage/100)*1/len(self.download_list) 
                        self.progress.emit(new_progress*100)
                    except Exception as e:
                        pass
                        #print(e)
                    #print(line)
                   #line = line.lstrip("[download]")
                elif "[ExtractAudio]" in line:
                    self.frm_main.lb_progress.setText("Converting")
                else:
                    pass
                    #print(line)
            #line = str(stream.stdout.read(), encoding="utf-8")
            line = stream.stdout.read1().decode("utf-8")
            if stream.poll() is not None:
                break
        output = stream.stdout.readlines()     
        #print("flushed yt-dlp and ffmpeg output")
        os.chdir(self.original_cwd)
        #os.close(DEVNULL)


class Frm_main(QMainWindow, Ui_frm_main):
    original_cwd = None
    links = []
    finished = []
    download_thread = None
    analyse_thread = None
    download_worker = None
    analyse_worker = None
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bt_analyse.clicked.connect(self.start_analyse_thread)
        self.bt_dl_convert.clicked.connect(self.start_download_thread)
        self.update_queue_table()
        self.progressBar.setValue(0)

    def update_queue_table(self):
        row_count =  len(self.links)
        column_count = 4  #(len(self.links[0]))

        self.tv_queue.setColumnCount(column_count) 
        self.tv_queue.setRowCount(row_count)
        self.tv_queue.setHorizontalHeaderLabels(("Title", "URL", "Format","Duration")) #list(self.links[0].keys())
        for row in range(row_count):  # add items from array to QTableWidget
            for column in range(column_count):
                if column == 0:
                    item = self.links[row]["title"]
                elif column == 1:
                    item = self.links[row]["url"]
                elif column == 2:
                    item = self.links[row]["desired_format"]
                elif column == 3:
                    td = timedelta(seconds=self.links[row]["duration"])
                    item = (str(td))              
                #else:   
                #    item = (list(self.links[row].values())[column])
                self.tv_queue.setItem(row, column, QTableWidgetItem(item))

    def update_result_table(self):
        #https://soundcloud.com/discourt/tribute-to-bass-temperature
        row_count =  len(self.finished)
        column_count = 3  #(len(self.links[0]))

        self.tv_results.setColumnCount(column_count) 
        self.tv_results.setRowCount(row_count)
        self.tv_results.setHorizontalHeaderLabels(("Source", "Title", "URL", "")) #list(self.links[0].keys())
        for row in range(row_count):  # add items from array to QTableWidget
            for column in range(column_count):
                item = (list(self.finished[row].values())[column])
                self.tv_results.setItem(row, column, QTableWidgetItem(item))


    def report_progress(self, n):
        self.progressBar.setValue(n)

    def copy_queue_to_results(self):
        self.finished = self.links
        self.links = []
        self.update_queue_table()
        self.update_result_table()

    def handle_analyse_thread_finished(self):
        self.bt_analyse.setEnabled(True)
        if self.check_auto_download.isChecked():
            self.start_download_thread()


    def start_analyse_thread(self):
        self.analyse_thread = QThread()
        self.analyse_worker = AnalyseWorker()
        self.analyse_worker.url = self.txt_edit_url.toPlainText()
        self.analyse_worker.frm_main = self
        self.analyse_worker.moveToThread(self.analyse_thread)
        self.analyse_thread.started.connect(self.analyse_worker.run)
        self.analyse_worker.finished.connect(self.analyse_thread.quit)
        self.analyse_worker.finished.connect(self.analyse_worker.deleteLater)
        self.analyse_worker.finished.connect(self.analyse_thread.deleteLater)
        self.analyse_worker.progress.connect(
            self.report_progress
        )
        self.bt_cancel.clicked.connect(self.analyse_thread.terminate)
        self.analyse_thread.start()
        self.bt_analyse.setEnabled(False)
        self.analyse_thread.finished.connect(self.handle_analyse_thread_finished)


    def start_download_thread(self):
        self.download_thread = QThread()
        self.download_worker = DownloadWorker()
        self.download_worker.frm_main = self
        self.download_worker.download_list = self.links.copy()
        self.download_worker.moveToThread(self.download_thread)
        self.download_thread.started.connect(self.download_worker.run)
        self.download_worker.finished.connect(self.download_thread.quit)
        self.download_worker.finished.connect(self.download_worker.deleteLater)
        self.download_thread.finished.connect(self.download_thread.deleteLater)
        self.download_worker.progress.connect(
            self.report_progress
        )
        self.bt_cancel.clicked.connect(self.download_thread.terminate)
        self.download_thread.start()
        self.bt_dl_convert.setEnabled(False)
        self.download_thread.finished.connect(
            lambda: self.bt_dl_convert.setEnabled(True)
        )
        self.download_thread.finished.connect(self.copy_queue_to_results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frm_main = Frm_main()
    frm_main.show()
    sys.exit(app.exec())