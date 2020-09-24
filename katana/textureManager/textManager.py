import NodegraphAPI
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,  QVBoxLayout,
                            QHBoxLayout, QScrollArea, QWidget, QLabel, QGridLayout, QLabel, QStatusBar)
from PyQt5.QtGui import QMovie, QPixmap
import os
import re
import converter
import threading

class TextureManager(QMainWindow):
    '''
        UI tool for handling and converting texture
        to .tex renderman file format
    '''

    def __init__(self):
        super(TextureManager, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.initUI()
        self.center()

    def initUI(self):
        if self.isActiveWindow() == True:
            self.close()

        self.setGeometry(300,300,600,700)
        self.setWindowTitle('Texture Manager')

        self.main = QWidget()
        mainLayout = QVBoxLayout()
        MARGIN = 25
        mainLayout.setContentsMargins(MARGIN,MARGIN,MARGIN,MARGIN)
        mainLayout.setSpacing(25)
        self.main.setLayout(mainLayout)

        # scrollable list
        self.scroll = QScrollArea(self)
        self.populate_scroll()

        # buttons layout
        self.btnWidget = QWidget()
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(15)

        # batch convert button
        self.batchConv = QPushButton('Convert All', self)
        self.batchConv.setObjectName('batchBtn')
        self.batchConv.setFixedWidth(150)
        self.batchConv.setFixedHeight(25)
        btnLayout.addWidget(self.batchConv)
        self.batchConv.clicked.connect(self.batch_convert)

        # refresh button
        self.refreshBtn = QPushButton('Refresh', self)
        self.refreshBtn.setObjectName('refreshBtn')
        self.refreshBtn.setFixedWidth(150)
        self.refreshBtn.setFixedHeight(25)
        btnLayout.addWidget(self.refreshBtn)
        self.refreshBtn.clicked.connect(self.populate_scroll)
        self.btnWidget.setLayout(btnLayout)

        mainLayout.addWidget(self.scroll)
        mainLayout.addWidget(self.btnWidget)
        self.setCentralWidget(self.main)

        css_path = os.path.normpath(r'C:\Users\Marco\Documents\Marco\PersonalPipeline\stylesheet\texture_manager.css')
        with open(css_path) as f:
            self.setStyleSheet(f.read())

        self.show()

    def populate_scroll(self):
        texture_list = [ i for i in NodegraphAPI.GetAllNodesByType('PrmanShadingNode') if i.getParameter('nodeType').getValue(0) == 'PxrTexture' ]
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        for i in texture_list:
            val = i.getParameter('parameters.filename.value').getValue(0)
            fileName = os.path.basename(val)
            label = '{} | {}'.format(i.getName(), fileName)
            self.object = QPushButton(label)
            self.object.clicked.connect(self.single_convert)
            self.vbox.addWidget(self.object)
            self.check_color(self.object)

        self.widget.setLayout(self.vbox)
        self.scroll.setWidget(self.widget)

        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def batch_convert(self):
        btnList = [ i for i in self.widget.children() if i.__class__.__name__ == 'QPushButton']

        for i in btnList:
            if '.tex' not in i.text():
                tmp = i.text()
                anchor = tmp.split(' | ')
                node = NodegraphAPI.GetNode(anchor[0])

                oldVal = node.getParameter('parameters.filename.value').getValue(0)
                t = threading.Thread(target=converter.convertTextures, args=(oldVal,))
                t.start()

                newVal = re.sub('\.+[a-z]{3}$', '.tex',  oldVal)
                node.getParameter('parameters.filename.value').setValue(newVal,0)
                i.setText('{} | {}'.format(anchor[0], os.path.basename(newVal)))
                self.check_color(i)

            else:
                pass

    def single_convert(self):
        text = self.sender().text()
        anchor = text.split(' | ')
        oldVal = anchor[-1]
        node = NodegraphAPI.GetNode(anchor[0])
        if '.tex' not in oldVal:
            oldVal = node.getParameter('parameters.filename.value').getValue(0)
            t = threading.Thread(target=converter.convertTextures, args=(oldVal,))
            t.start()

            newVal = re.sub('\.+[a-z]{3}$', '.tex',  oldVal)
            node.getParameter('parameters.filename.value').setValue(str(newVal),0)
            self.sender().setText('{} | {}'.format(anchor[0], os.path.basename(newVal)))
            self.check_color(self.sender())
        else:
            pass

    def check_color(self, item):
        nodeName = item.text()
        anchor = nodeName.split(' | ')
        node = NodegraphAPI.GetNode(anchor[0])
        val = node.getParameter('parameters.filename.value').getValue(0)

        if '.tex' not in val:
            item.setStyleSheet("color: black; background-color: rgb(150, 50, 50)")
        elif '.tex' in val:
            item.setStyleSheet("color: black; background-color: rgb(50, 150, 50)")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
