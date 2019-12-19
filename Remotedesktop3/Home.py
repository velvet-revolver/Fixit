from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QTabWidget, QWidget, QVBoxLayout, QPushButton, \
    QDialogButtonBox
import sys
from random import randint
import socket
import os


class TabWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fix it")
        self.setFixedSize(600, 600)
        # self.setWindowIcon() Need to add later

        # Adding all the necessary tabs
        qtabwidget = QTabWidget()
        qtabwidget.addTab(Hometab(), "Home")
        qtabwidget.addTab(servertab(), "Server")
        qtabwidget.addTab(clienttab(), "client")

        # Add a vertical box
        vbox = QVBoxLayout()
        vbox.addWidget(qtabwidget)

        self.setLayout(vbox)


class Hometab(QWidget):
    def __init__(self):
        super().__init__()


class servertab(QWidget):
    def __init__(self):
        super().__init__()

        generatebtn = QPushButton()
        generatebtn.setText("Generate")
        generatebtn.clicked.connect(self.generate_click)

        self.key = QLabel()
        Ipname = socket.gethostname()
        Ipshow = socket.gethostbyname(Ipname)

        self.key.setText(str(Ipshow))

        serverlayout = QVBoxLayout()
        serverlayout.addWidget(generatebtn)
        serverlayout.addWidget(self.key)

        self.setLayout(serverlayout)

    def generate_click(self):
        import server






class clienttab(QWidget):
    def __init__(self):
        super().__init__()

        ip = QLabel("IP")
        self.ipedit = QLineEdit()

        btn = QPushButton()
        btn.setFixedSize(50, 30)
        btn.setText("Connect")
        btn.clicked.connect(self.on_click)

        layout = QVBoxLayout()
        layout.addWidget(ip)
        layout.addWidget(self.ipedit)
        layout.addWidget(btn)

        self.setLayout(layout)

    def on_click(self):
        self.ipaddr = self.ipedit.text()
        print(self.ipaddr)

        import config
        config.getter(self.ipaddr)
        import client


app = QApplication(sys.argv)
tabwidget = TabWidget()
tabwidget.show()
app.exec()
