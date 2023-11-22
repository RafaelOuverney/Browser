import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWebEngineWidgets, QtGui, QtWidgets
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        navbar = QToolBar()
        self.addToolBar(navbar)
        self.setWindowIcon(QtGui.QIcon("Icons/icon.png"))
        self.setWindowTitle("Bowser")
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setUrl(QtCore.QUrl('http://www.google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        global_settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()

        for attr in (
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,
            QtWebEngineWidgets.QWebEngineSettings.FullScreenSupportEnabled,
        ):
            global_settings.setAttribute(attr, True)
        self.browser.page().fullScreenRequested.connect(self.FullscreenRequest)

        
        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)

        

        back_btn = QAction(QIcon('icons/back.png'), 'Voltar', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('icons/forward.png'), 'Avançar', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('icons/reload.png'), 'Recarregar', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('./icons/home.png'), 'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        self.setStyleSheet("""
            QToolBar {
                background-color: #f1f1f1;
                color: white;
                border: none;
            }
            QAction {
                color: black;
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

    @QtCore.pyqtSlot("QWebEngineFullScreenRequest")
    def FullscreenRequest(self, request):
        request.accept()
        if request.toggleOn():
            self.browser.setParent(None)
            self.browser.showFullScreen()
        else:
            self.setCentralWidget(self.browser)
            self.browser.showNormal()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


