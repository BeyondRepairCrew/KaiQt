# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        if not frm_main.objectName():
            frm_main.setObjectName(u"frm_main")
        frm_main.resize(800, 643)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frm_main.sizePolicy().hasHeightForWidth())
        frm_main.setSizePolicy(sizePolicy)
        self.action_pick_download_location = QAction(frm_main)
        self.action_pick_download_location.setObjectName(u"action_pick_download_location")
        self.centralwidget = QWidget(frm_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tv_queue = QTableWidget(self.centralwidget)
        self.tv_queue.setObjectName(u"tv_queue")
        self.tv_queue.setGeometry(QRect(10, 50, 781, 161))
        self.tv_queue.horizontalHeader().setStretchLastSection(True)
        self.tv_queue.verticalHeader().setStretchLastSection(False)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 281, 31))
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.txt_edit_url = QTextEdit(self.centralwidget)
        self.txt_edit_url.setObjectName(u"txt_edit_url")
        self.txt_edit_url.setGeometry(QRect(10, 250, 431, 31))
        font1 = QFont()
        font1.setPointSize(9)
        self.txt_edit_url.setFont(font1)
        self.bt_analyse = QPushButton(self.centralwidget)
        self.bt_analyse.setObjectName(u"bt_analyse")
        self.bt_analyse.setEnabled(True)
        self.bt_analyse.setGeometry(QRect(620, 250, 171, 31))
        self.cb_format = QComboBox(self.centralwidget)
        self.cb_format.addItem("")
        self.cb_format.addItem("")
        self.cb_format.setObjectName(u"cb_format")
        self.cb_format.setEnabled(True)
        self.cb_format.setGeometry(QRect(450, 250, 61, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 230, 211, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(450, 230, 61, 16))
        self.tv_results = QTableWidget(self.centralwidget)
        self.tv_results.setObjectName(u"tv_results")
        self.tv_results.setGeometry(QRect(10, 330, 781, 161))
        self.tv_results.horizontalHeader().setStretchLastSection(True)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 290, 281, 31))
        self.label_4.setFont(font)
        self.bt_dl_convert = QPushButton(self.centralwidget)
        self.bt_dl_convert.setObjectName(u"bt_dl_convert")
        self.bt_dl_convert.setGeometry(QRect(10, 550, 371, 28))
        self.bt_cancel = QPushButton(self.centralwidget)
        self.bt_cancel.setObjectName(u"bt_cancel")
        self.bt_cancel.setGeometry(QRect(410, 550, 381, 28))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QRect(10, 510, 781, 23))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.lb_analyse_log = QLabel(self.centralwidget)
        self.lb_analyse_log.setObjectName(u"lb_analyse_log")
        self.lb_analyse_log.setGeometry(QRect(620, 219, 171, 31))
        self.lb_progress = QLabel(self.centralwidget)
        self.lb_progress.setObjectName(u"lb_progress")
        self.lb_progress.setGeometry(QRect(345, 515, 100, 16))
        self.lb_progress.setAlignment(Qt.AlignCenter)
        self.cb_quality = QComboBox(self.centralwidget)
        self.cb_quality.addItem("")
        self.cb_quality.addItem("")
        self.cb_quality.addItem("")
        self.cb_quality.addItem("")
        self.cb_quality.addItem("")
        self.cb_quality.addItem("")
        self.cb_quality.setObjectName(u"cb_quality")
        self.cb_quality.setEnabled(True)
        self.cb_quality.setGeometry(QRect(520, 250, 91, 31))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(520, 230, 61, 16))
        self.check_auto_download = QCheckBox(self.centralwidget)
        self.check_auto_download.setObjectName(u"check_auto_download")
        self.check_auto_download.setGeometry(QRect(680, 290, 111, 20))
        self.check_auto_download.setChecked(True)
        frm_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frm_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menuPick_download_folder = QMenu(self.menubar)
        self.menuPick_download_folder.setObjectName(u"menuPick_download_folder")
        frm_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frm_main)
        self.statusbar.setObjectName(u"statusbar")
        frm_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuPick_download_folder.menuAction())
        self.menuPick_download_folder.addAction(self.action_pick_download_location)

        self.retranslateUi(frm_main)

        QMetaObject.connectSlotsByName(frm_main)
    # setupUi

    def retranslateUi(self, frm_main):
        frm_main.setWindowTitle(QCoreApplication.translate("frm_main", u"KaiQt", None))
        self.action_pick_download_location.setText(QCoreApplication.translate("frm_main", u"Pick download location", None))
        self.label.setText(QCoreApplication.translate("frm_main", u"Queue", None))
        self.txt_edit_url.setPlaceholderText(QCoreApplication.translate("frm_main", u"dank music links or playlist links", None))
        self.bt_analyse.setText(QCoreApplication.translate("frm_main", u"Analyse and add to queue", None))
        self.cb_format.setItemText(0, QCoreApplication.translate("frm_main", u".mp3", None))
        self.cb_format.setItemText(1, QCoreApplication.translate("frm_main", u".flac", None))

        self.label_2.setText(QCoreApplication.translate("frm_main", u"URL ", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("frm_main", u"Format", None))
        self.label_4.setText(QCoreApplication.translate("frm_main", u"Results", None))
        self.bt_dl_convert.setText(QCoreApplication.translate("frm_main", u"Download and convert", None))
        self.bt_cancel.setText(QCoreApplication.translate("frm_main", u"Cancel", None))
        self.lb_analyse_log.setText("")
        self.lb_progress.setText("")
        self.cb_quality.setItemText(0, QCoreApplication.translate("frm_main", u"320 kbps", None))
        self.cb_quality.setItemText(1, QCoreApplication.translate("frm_main", u"192 kbps", None))
        self.cb_quality.setItemText(2, QCoreApplication.translate("frm_main", u"128 kbps", None))
        self.cb_quality.setItemText(3, QCoreApplication.translate("frm_main", u"96 kbps", None))
        self.cb_quality.setItemText(4, QCoreApplication.translate("frm_main", u"32 kbps", None))
        self.cb_quality.setItemText(5, QCoreApplication.translate("frm_main", u"16 kbps", None))

#if QT_CONFIG(tooltip)
        self.label_5.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("frm_main", u"Quality", None))
        self.check_auto_download.setText(QCoreApplication.translate("frm_main", u"Auto-Download", None))
        self.menuPick_download_folder.setTitle(QCoreApplication.translate("frm_main", u"Settings", None))
    # retranslateUi

