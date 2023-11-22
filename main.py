import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWebEngineWidgets, QtGui, QtWidgets, QtWebEngineCore
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent,*args, *kwargs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setStyleSheet("QTabBar::tab {  height: 20px;}")
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        navbar = QToolBar("Navigation")
        self.addToolBar(navbar)
        self.setWindowIcon(QtGui.QIcon("Icons/icon.png"))
        self.setWindowTitle("Bowser")
        self.browser = QtWebEngineWidgets.QWebEngineView()
        # self.browser.setUrl(QtCore.QUrl('http://www.google.com'))
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
        self.setCentralWidget(self.tabs)
        navbar.addSeparator()
        
        self.showMaximized()

        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        global_settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()

        for attr in (
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,
            QtWebEngineWidgets.QWebEngineSettings.FullScreenSupportEnabled,
        ):
            global_settings.setAttribute(attr, True)
        for index in range(self.tabs.count()):
            self.tabs.widget(index).page().fullScreenRequested.connect(self.FullscreenRequest)

        
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
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('icons/forward.png'), 'Avançar', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('icons/reload.png'), 'Recarregar', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
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

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()
    
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        # self.update_title(self.tabs.currentWidget())
        # self.update_urlbar(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.browser.page().title()
        self.setWindowTitle("%s - Bowser" % title)
    
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    @QtCore.pyqtSlot("QWebEngineFullScreenRequest")
    def FullscreenRequest(self, request):
        request.accept()
        if request.toggleOn():
            self.tabs.setParent(None)
            self.tabs.showFullScreen()
            self.tabs.setStyleSheet("QTabBar::tab { height: 0px;}")

        else:
            self.tabs.showNormal()
            self.setCentralWidget(self.tabs)
            self.tabs.setStyleSheet("QTabBar::tab {  height: 20px;}")



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()





