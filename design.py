# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Tue Nov  1 21:59:16 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(837, 841)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.letterList = QtGui.QListView(self.centralwidget)
        self.letterList.setMinimumSize(QtCore.QSize(500, 0))
        self.letterList.setMaximumSize(QtCore.QSize(16777215, 30))
        self.letterList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.letterList.setFlow(QtGui.QListView.LeftToRight)
        self.letterList.setObjectName(_fromUtf8("letterList"))
        self.horizontalLayout_2.addWidget(self.letterList)
        self.searchBox = QtGui.QLineEdit(self.centralwidget)
        self.searchBox.setObjectName(_fromUtf8("searchBox"))
        self.horizontalLayout_2.addWidget(self.searchBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.artistList = QtGui.QListView(self.centralwidget)
        self.artistList.setMaximumSize(QtCore.QSize(250, 16777215))
        self.artistList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.artistList.setObjectName(_fromUtf8("artistList"))
        self.horizontalLayout.addWidget(self.artistList)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabAlbums = QtGui.QWidget()
        self.tabAlbums.setObjectName(_fromUtf8("tabAlbums"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabAlbums)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.albumList = QtGui.QListView(self.tabAlbums)
        self.albumList.setObjectName(_fromUtf8("albumList"))
        self.verticalLayout_3.addWidget(self.albumList)
        self.tabWidget.addTab(self.tabAlbums, _fromUtf8(""))
        self.tabBoots = QtGui.QWidget()
        self.tabBoots.setObjectName(_fromUtf8("tabBoots"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabBoots)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.bootList = QtGui.QListView(self.tabBoots)
        self.bootList.setObjectName(_fromUtf8("bootList"))
        self.verticalLayout_4.addWidget(self.bootList)
        self.tabWidget.addTab(self.tabBoots, _fromUtf8(""))
        self.tabVideos = QtGui.QWidget()
        self.tabVideos.setObjectName(_fromUtf8("tabVideos"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabVideos)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.videoList = QtGui.QListView(self.tabVideos)
        self.videoList.setObjectName(_fromUtf8("videoList"))
        self.verticalLayout_5.addWidget(self.videoList)
        self.tabWidget.addTab(self.tabVideos, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.songList = QtGui.QListView(self.centralwidget)
        self.songList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.songList.setObjectName(_fromUtf8("songList"))
        self.verticalLayout.addWidget(self.songList)
        self.videoPlayer = phonon.Phonon.VideoPlayer(self.centralwidget)
        self.videoPlayer.setEnabled(True)
        self.videoPlayer.setMaximumSize(QtCore.QSize(200, 200))
        self.videoPlayer.setObjectName(_fromUtf8("videoPlayer"))
        self.verticalLayout.addWidget(self.videoPlayer)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.fullscreenButton = QtGui.QCheckBox(self.centralwidget)
        self.fullscreenButton.setObjectName(_fromUtf8("fullscreenButton"))
        self.horizontalLayout_3.addWidget(self.fullscreenButton)
        self.pauseButton = QtGui.QCheckBox(self.centralwidget)
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.horizontalLayout_3.addWidget(self.pauseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 837, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.letterList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onLetterClick)
        QtCore.QObject.connect(self.artistList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onArtistClick)
        QtCore.QObject.connect(self.songList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onSongClick)
        QtCore.QObject.connect(self.albumList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onAlbumClick)
        QtCore.QObject.connect(self.bootList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onAlbumClick)
        QtCore.QObject.connect(self.videoList, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), MainWindow.onAlbumClick)
        QtCore.QObject.connect(self.fullscreenButton, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), MainWindow.onFullscreen)
        QtCore.QObject.connect(self.pauseButton, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), MainWindow.onPause)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Laudable", None))
        self.searchBox.setPlaceholderText(_translate("MainWindow", "Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAlbums), _translate("MainWindow", "Albums", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBoots), _translate("MainWindow", "Bootlegs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVideos), _translate("MainWindow", "Videos", None))
        self.fullscreenButton.setText(_translate("MainWindow", "Fullscreen", None))
        self.pauseButton.setText(_translate("MainWindow", "Pause", None))

from PyQt4 import phonon
