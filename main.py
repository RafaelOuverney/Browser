import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://www.google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # barra de navegação
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('icons/back.png'), 'Voltar', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('icons/forward.png'), 'Avançar', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('icons/reload.png'), 'Recarregar', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('icons/home.png'), 'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Adicionando estilos CSS
        self.setStyleSheet("""
            QToolBar {
                background-color: #f1f1f1;
                color: white;
                border: none;
            }
            QAction {
                color: white;
            }
            QLineEdit {
                border: 2px solid #555;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                color: grey;
            }
        """)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://www.google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName('Navegador')
window = MainWindow()
app.exec_()
