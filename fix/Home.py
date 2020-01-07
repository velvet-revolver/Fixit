from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QTabWidget, QWidget, QVBoxLayout, QPushButton, \
    QGridLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QRect
import sys
from random import randint
import socket
import config
import os


class TabWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fix it")
        self.setGeometry(50, 50, 640, 480)
        # self.setFixedSize(600, 600)
        self.setWindowIcon(QIcon('logo.png'))

        # Adding all the necessary tabs
        qtabwidget = QTabWidget()
        qtabwidget.addTab(Hometab(), "Home")
        qtabwidget.addTab(servertab(), "Server(Host)")
        qtabwidget.addTab(clienttab(), "client")

        # Add a vertical box
        vbox = QVBoxLayout()
        vbox.addWidget(qtabwidget)
        # vbox.addWidget(self.label)

        self.setLayout(vbox)


class Hometab(QWidget):
    def __init__(self):
        super().__init__()

        newfont = QFont("Times", 15, QFont.Bold)

        self.desc = QLabel()
        self.desc.setText(
            'Welcome to FixIt! To make your device able to host, please go in the Host tab and to connect to a server please go to the client tab')
        self.desc.setFont(newfont)

        self.label = QLabel()
        self.label.setPixmap(QPixmap('logo.png'))
        self.label.setAlignment(Qt.AlignCenter)

        HomeLayout = QVBoxLayout()
        HomeLayout.addWidget(self.label)
        HomeLayout.addWidget(self.desc)

        self.setLayout(HomeLayout)


class servertab(QWidget):
    def __init__(self):
        super().__init__()

        self.security_key = randint(9999999, 99999999)
        print(self.security_key)

        skeyname = QLabel('The key to access this computer is : ')
        skeyname.setFont(QFont("Times", 12, QFont.Bold))

        skey = QLabel()
        skey.setText(str(self.security_key))
        skey.setFont(QFont("Times", 12, QFont.Bold))

        generatebtn = QPushButton('Start Hosting')
        # generatebtn.setText("Start Hosting")
        generatebtn.setFixedSize(80, 50)
        generatebtn.clicked.connect(self.generate_click)

        text = QLabel('Your device can be accessed by:')
        text.setFont(QFont("Times", 12, QFont.Bold))

        self.key = QLabel()
        Ipname = socket.gethostname()
        Ipshow = socket.gethostbyname(Ipname)
        self.key.setText(str(Ipshow))
        self.key.setFont(QFont("Times", 12, QFont.Bold))

        serverlayout = QGridLayout()
        serverlayout.addWidget(skeyname, 0, 0)
        serverlayout.addWidget(skey, 0, 1)
        serverlayout.addWidget(text, 1, 0)
        serverlayout.addWidget(self.key, 1, 1)
        serverlayout.addWidget(generatebtn, 2, 0)

        self.setLayout(serverlayout)

    def generate_click(self):
        config.key_getter(self.security_key)

        import server


class clienttab(QWidget):
    def __init__(self):
        super().__init__()

        ip = QLabel("IP:", self)
        self.ipedit = QLineEdit()

        key_name = QLabel('Type the key displayed in the Host : ')

        self.key_input = QLineEdit()

        btn = QPushButton()
        btn.setFixedSize(50, 30)
        btn.setText("Connect")
        btn.clicked.connect(self.on_click)

        layout = QGridLayout()
        layout.addWidget(key_name, 0, 0)
        layout.addWidget(self.key_input, 0, 1)
        layout.addWidget(ip, 1, 0)
        layout.addWidget(self.ipedit, 1, 1)
        layout.addWidget(btn, 2, 0)

        self.setLayout(layout)

    def on_click(self):
        self.ipaddr = self.ipedit.text()
        print(self.ipaddr)

        self.key_take = self.key_input.text()
        print('The key is : ', int(self.key_take))

        config.ip_getter(self.ipaddr)

        config.client_keygetter(int(self.key_take))
        import client


app = QApplication(sys.argv)
tabwidget = TabWidget()
tabwidget.show()
app.exec()
