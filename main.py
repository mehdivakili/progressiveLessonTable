import sys
import os.path
from distutils.core import setup
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QWidget, QProgressBar, QScrollArea, QCheckBox, QRadioButton,
                             QAction, qApp, QMessageBox,
                             QVBoxLayout, QLabel, QHBoxLayout, QApplication, QPushButton, QLineEdit, QMainWindow,
                             QTabWidget)
from PyQt5.QtGui import QIcon
import pickle
import os


class DataBase:
    FILE_DATA_PATH = f"C:/Users/{os.getlogin()}/AppData/Local/mehdiApp/lessonApp/lessonData.conf"
    FILE_SETTING_PATH = f"C:/Users/{os.getlogin()}/AppData/Local/mehdiApp/lessonApp/setting.conf"
    lastSavedLessonLists = {}
    lessonLists = []
    lessonListList = []
    setting = {}

    @staticmethod
    def saveSetting():
        dbfile = open(DataBase.FILE_SETTING_PATH, 'wb')
        pickle.dump({'tabIndex': Mainwin.tabwidget.currentIndex()}, dbfile)
        dbfile.close()

    @staticmethod
    def saveData():
        dbfile = open(DataBase.FILE_DATA_PATH, 'wb')
        pickle.dump(DataBase.lessonLists, dbfile)
        DataBase.lastSavedLessonLists = DataBase.lessonLists
        dbfile.close()

    @staticmethod
    def initData():
        if os.path.isfile(DataBase.FILE_DATA_PATH):

            DataBase.lastSavedLessonLists = pickle.load(open(DataBase.FILE_DATA_PATH, "rb"))
            DataBase.lessonLists = pickle.load(open(DataBase.FILE_DATA_PATH, "rb"))
            if DataBase.lessonLists == []:
                DataBase.lessonLists.append({})
        if os.path.isfile(DataBase.FILE_SETTING_PATH):
            DataBase.setting = pickle.load(open(DataBase.FILE_SETTING_PATH, "rb"))


def sortBylesson(lessons):
    tmplessonList = {}
    m = {}
    for l in lessons:
        l = lessons[l]
        linfo = l['name'].split()
        if len(linfo) == 2:
            if tmplessonList.get(linfo[0]) == None:
                tmplessonList[linfo[0]] = []
            tmplessonList[linfo[0]].append(l)
        else:
            if tmplessonList.get("else") == None:
                tmplessonList["else"] = []
            tmplessonList["else"].append(l)

    for i in tmplessonList:
        i = tmplessonList[i]

        if not isinstance(i, list):
            m[i['name']] = {'name': i['name'], 'percent': str(int(i['percent']))}
            continue
        for ke in i:
            m[ke['name']] = {'name': ke['name'], 'percent': str(int(ke['percent']))}
    return m


class Mainwin(QMainWindow):
    tabwidget = None

    def __init__(self):
        super().__init__()
        Mainwin.tabwidget = QTabWidget()

        self.status = 0
        DataBase.initData()
        self.initUI()

    def initUI(self):
        self.settingIcon = QPushButton(self)
        self.settingIcon.move(540, 0)
        self.settingIcon.setFixedSize(20, 20)
        p = QIcon('setting.png')

        self.settingIcon.setIcon(p)
        self.settingIcon.setIconSize(QSize(20, 20))
        self.settingIcon.setStyleSheet('background-color: #00000000')

        self.settingIcon.clicked.connect(self.settingf)
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        saveAct = QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(DataBase.saveData)
        backAct = QAction('Undo', self)
        backAct.setShortcut('Ctrl+Z')
        backAct.triggered.connect(self.backfunc)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(backAct)
        save = QPushButton("ذخیزه")
        save.clicked.connect(DataBase.saveData)
        add_dor = QPushButton("اضافه کردن دور")
        add_dor.clicked.connect(self.adddorfunc)
        add = QPushButton("اضافه کردن درس")
        add.clicked.connect(self.addfunc)

        self.etext = QLineEdit()

        self.scroll = QScrollArea()
        hbox = QHBoxLayout()
        hbox.addWidget(save)
        hbox.addWidget(add_dor)
        hbox.addWidget(add)
        hbox.addWidget(self.etext)
        vbox = QVBoxLayout()

        # self.tabwidget.setTabPosition(QTabWidget.West)

        vbox.addWidget(self.tabwidget)
        vbox.addLayout(hbox)
        w = QWidget()
        self.settingIcon.setParent(self.tabwidget)
        # self.settingIcon.raise_()
        w.setLayout(vbox)
        i = 1
        if DataBase.lessonLists == []:
            DataBase.lessonListList.append(LessonList())
            self.tabwidget.addTab(DataBase.lessonListList[i - 1], "       دور " + str(i) + "  ")

        for lList in DataBase.lessonLists:
            DataBase.lessonListList.append(LessonList(llist=lList, n=i - 1))
            self.tabwidget.addTab(DataBase.lessonListList[i - 1], "       دور " + str(i) + "  ")
            i += 1
        #        Mainwin.tabwidget.setCurrentIndex(DataBase.setting['tabIndex'])
        Mainwin.tabwidget.currentChanged.connect(DataBase.saveSetting)
        Mainwin.tabwidget.setTabsClosable(True)
        Mainwin.tabwidget.tabCloseRequested.connect(self.tabClose)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(w)
        self.setCentralWidget(self.scroll)
        # self.setLayout(vbox)

        # print(app.desktop().availableGeometry())
        # geometry.setHeight(geometry.height() - (titleBarHeight*2))

        self.setGeometry(1000, 50, 600, 900)
        self.setWindowTitle('جدول ب‍‍‍‍‍یشرفت درسی')
        self.show()

    def tabClose(self, n):
        Mainwin.tabwidget.removeTab(n)
        del (DataBase.lessonLists[n])

    def addfunc(self, a):

        for n in DataBase.lessonLists:
            n = DataBase.lessonLists.index(n)

            DataBase.lessonListList[n].lessonList[self.etext.text()] = Lesson(self.etext.text(),
                                                                              DataBase.lessonListList[n].lessonLayout,
                                                                              count=len(
                                                                                  DataBase.lessonListList[n].llist) + 1,
                                                                              n=n)
            DataBase.lessonLists[n][self.etext.text()] = {'name': self.etext.text(), 'percent': "0"}

    def adddorfunc(self, a):
        tmp = {}
        for l in DataBase.lessonLists[0]:
            tmp[DataBase.lessonLists[0][l]['name']] = {'name': DataBase.lessonLists[0][l]['name'], 'percent': "۰"}
        DataBase.lessonLists.append(tmp)
        DataBase.lessonListList.append(LessonList(llist=tmp, n=len(DataBase.lessonListList)))
        self.tabwidget.addTab(DataBase.lessonListList[len(DataBase.lessonListList) - 1],
                              "       دور " + str(len(DataBase.lessonLists)) + "  ")

    def backfunc(self, a):
        for li in DataBase.lessonListList:
            lList = li

            for i in lList.lessonList:
                lList.lessonList[i].setPercent(DataBase.lastSavedLessonLists[lList.n][i]["percent"])

    def settingf(self, a):
        w = QWidget()
        self.scroll.setWidget(w)

    def closeEvent(self, event):
        tmp = None
        if os.path.isfile(DataBase.FILE_DATA_PATH):
            tmp = pickle.load(open(DataBase.FILE_DATA_PATH, "rb"))
        else:
            DataBase.saveData()
            event.accept()
        if tmp != DataBase.lessonLists:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure to quit without save?", QMessageBox.Save |
                                         QMessageBox.Ignore | QMessageBox.Cancel)

            if reply == QMessageBox.Save:
                DataBase.saveData()
                event.accept()
            elif reply == QMessageBox.Ignore:

                event.accept()
            else:
                event.ignore()


class LessonList(QWidget):

    def __init__(self, llist={}, n=0):
        super().__init__()
        self.llist = llist
        self.n = n
        self.lessonLayout = QVBoxLayout()
        self.lessonList = {}
        self.status = 0
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        search = QHBoxLayout()

        self.searchEdit = QLineEdit()
        self.searchEdit.textChanged.connect(self.searchFunc)
        no = QRadioButton(" ")
        no.setChecked(True)
        no.toggled.connect(lambda: self.btnstate(no))
        is_full = QRadioButton("کامل شده")
        is_full.toggled.connect(lambda: self.btnstate(is_full))
        is_empty = QRadioButton("شروع نشده")
        is_empty.toggled.connect(lambda: self.btnstate(is_empty))
        is_started = QRadioButton("نصفه")
        is_started.toggled.connect(lambda: self.btnstate(is_started))
        is_sort = QCheckBox("ترتیب")
        is_sort.toggled.connect(lambda v: self.sort(v))

        search.addWidget(is_sort)
        search.addWidget(is_started)
        search.addWidget(is_empty)

        search.addWidget(is_full)
        search.addWidget(no)

        search.addWidget(self.searchEdit)

        search.addWidget(QLabel("جستجو"))

        vbox.addLayout(search)

        vbox.addLayout(self.lessonLayout)

        vbox.setAlignment(Qt.AlignTop)

        self.setLayout(vbox)

        f = 0
        for k in self.llist:
            f += 1
            self.lessonList[self.llist[k]['name']] = Lesson(self.llist[k]['name'], self.lessonLayout,
                                                            percent=str(int(self.llist[k]['percent'])), count=f,
                                                            n=self.n)

    def checkboxFull(self, a):
        f = 0
        for v in self.lessonList:
            if self.lessonList[v].pBar.value() >= 99 or a == 0:
                f += 1
                self.lessonList[v].count = f
                self.lessonList[v].c.setText("-" + str(f))
                self.lessonList[v].Cshow()
            else:
                self.lessonList[v].Chide()

    def checkboxNotFull(self, a):
        f = 0
        for v in self.lessonList:

            if self.lessonList[v].pBar.value() == 0 or a == 0:
                f += 1
                self.lessonList[v].count = f
                self.lessonList[v].c.setText("-" + str(f))
                self.lessonList[v].Cshow()
            else:
                self.lessonList[v].Chide()

    def checkboxOnProgress(self, a):
        f = 0
        for v in self.lessonList:
            if (self.lessonList[v].pBar.value() < 99 and self.lessonList[v].pBar.value() != 0) or a == 0:
                f += 1
                self.lessonList[v].count = f
                self.lessonList[v].c.setText("-" + str(f))
                self.lessonList[v].Cshow()
            else:
                self.lessonList[v].Chide()

    def sort(self, sort):
        if not sort:
            tmp = self.llist
        else:
            tmp = sortBylesson(self.llist)
        i = 0
        j = 0
        for l in self.lessonList:
            for ls in tmp:
                if i == j:
                    self.lessonList[l].name = tmp[ls]["name"]
                    self.lessonList[l].percent = tmp[ls]["percent"]
                    self.lessonList[l].title.setText(tmp[ls]["name"])
                    self.lessonList[l].sp.setText(str(int(tmp[ls]["percent"])))
                    self.lessonList[l].pBar.setValue(int(tmp[ls]["percent"]))

                j = j + 1
            j = 0
            i = i + 1

        if self.status == 0:

            self.checkboxFull(0)

        elif self.status == 1:
            self.checkboxFull(1)

        elif self.status == 2:
            self.checkboxNotFull(1)

        elif self.status == 3:
            self.checkboxOnProgress(1)

    def searchFunc(self, text):
        self.setStatus()
        for v in self.lessonList:
            if text in v:
                pass
            else:
                self.lessonList[v].Chide()

    def btnstate(self, b):

        if b.text() == " ":
            self.checkboxFull(0)
            self.status = 0
        elif b.text() == "کامل شده":
            self.checkboxFull(1)
            self.status = 1
        elif b.text() == "شروع نشده":
            self.checkboxNotFull(1)
            self.status = 2
        elif b.text() == "نصفه":
            self.checkboxOnProgress(1)
            self.status = 3
        self.searchFunc(self.searchEdit.text())

    def setStatus(self):

        if self.status == 0:
            self.checkboxFull(0)
        elif self.status == 1:
            self.checkboxFull(1)
        elif self.status == 2:
            self.checkboxNotFull(1)
        elif self.status == 3:
            self.checkboxOnProgress(1)


class Lesson(QWidget):
    name = ""
    percent = 0
    main_layout = None

    def __init__(self, lesson_name, layout, percent="0", ishide=0, count=1, n=0):
        super().__init__()
        self.name = lesson_name
        self.main_layout = layout
        self.percent = percent
        self.count = count
        self.n = n
        self.ishide = int(ishide)
        self.initUi()

    def initUi(self):

        self.title = QLabel(self.name)
        self.title.setFixedSize(50, 20)
        self.title.setTextInteractionFlags(Qt.TextSelectableByMouse);

        self.c = QLabel("-" + str(self.count))
        self.c.setFixedSize(18, 20)
        self.sp = QLineEdit()
        self.sp.setText(str(int(self.percent)))
        self.sp.setFixedSize(50, 20)
        self.delete = QPushButton("حذف کردن")
        self.delete.clicked.connect(lambda v: remove(self, n=self.n))
        self.pBar = QProgressBar()
        self.pBar.setValue(int(self.percent))
        self.sp.textChanged.connect(lambda v: update(v, self, n=self.n))
        # self.cp = QSpinBox()
        # self.cp.setFixedSize(18,20)
        # self.cp.setMaximum(1)
        # self.cp.setMinimum(-1)
        # self.cp.valueChanged.connect(lambda v: cpf(self.name,v))
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.delete)
        self.hbox.addWidget(self.sp)
        self.hbox.addWidget(self.pBar)

        self.hbox.addWidget(self.title)
        self.hbox.addWidget(self.c)
        # self.hbox.addWidget(self.cp)

        # self.setLayout(self.hbox)
        # self.hbox.setSpacing(-10)
        # self.main_layout.setSpacing(-10)
        # self.main_layout.addWidget(self)
        self.main_layout.addLayout(self.hbox)

        if self.ishide == 1:
            self.Chide()
        # self.main_layout.addLayout(self.hbox)

    def setPercent(self, p):
        self.percent = str(int(p))
        self.sp.setText(str(int(p)))
        self.pBar.setValue(int(self.percent))

    def Chide(self):
        self.title.hide()
        self.sp.hide()
        self.delete.hide()
        self.pBar.hide()
        self.c.hide()

    def Cshow(self):
        self.title.show()
        self.sp.show()
        self.delete.show()
        self.pBar.show()
        self.c.show()

    def cpf(self, item, i):

        item = self.lessonList[item]
        tmp = 0
        if i == 0:
            return
        elif i == -1:
            for l in self.lessonList:
                if tmp == 1:
                    tmp = l
                if l == item.name:
                    t2 = l
                    tmp = 1
                    continue

                if tmp == 0:
                    continue
                else:

                    self.lessonList[t2].name, self.lessonList[tmp].name = self.lessonList[tmp].name, self.lessonList[
                        t2].name
                    self.lessonList[t2].percent, self.lessonList[tmp].percent = self.lessonList[tmp].percent, \
                                                                                self.lessonList[t2].percent

                    self.lessonList[t2].title.setText(self.lessonList[t2].name)
                    self.lessonList[t2].sp.setText(str(int(self.lessonList[t2].percent)))
                    self.lessonList[t2].pBar.setValue(int(self.lessonList[t2].percent))

                    self.lessonList[tmp].title.setText(self.lessonList[tmp].name)
                    self.lessonList[tmp].sp.setText(str(int(self.lessonList[tmp].percent)))
                    self.lessonList[tmp].pBar.setValue(int(self.lessonList[tmp].percent))
                    item.cp.setValue(0)
                    break

        elif i == 1:
            for l in self.lessonList:
                if l == item.name:
                    t2 = l
                    self.lessonList[t2].name, self.lessonList[tmp].name = self.lessonList[tmp].name, self.lessonList[
                        t2].name
                    self.lessonList[t2].percent, self.lessonList[tmp].percent = self.lessonList[tmp].percent, \
                                                                                self.lessonList[t2].percent

                    self.lessonList[t2].title.setText(self.lessonList[t2].name)
                    self.lessonList[t2].sp.setText(str(int(self.lessonList[t2].percent)))
                    self.lessonList[t2].pBar.setValue(int(self.lessonList[t2].percent))

                    self.lessonList[tmp].title.setText(self.lessonList[tmp].name)
                    self.lessonList[tmp].sp.setText(str(int(self.lessonList[tmp].percent)))
                    self.lessonList[tmp].pBar.setValue(int(self.lessonList[tmp].percent))
                    item.cp.setValue(0)
                tmp = l

        tmp = 0


def remove(l, n=0):
    l.title.hide()
    l.sp.hide()
    l.delete.hide()
    l.pBar.hide()
    l.c.hide()
    del (DataBase.lessonLists[n][l.name])
    if DataBase.lessonLists[n] == {}:
        Mainwin.tabwidget.removeTab(n)
        del (DataBase.lessonLists[n])


def update(percent, l, n=0):
    if percent == "":
        return
    tmp = ""
    for c in percent:
        if c.isdigit():
            tmp += c
    percent = tmp
    if int(percent) > 100 and int(percent) < 0:
        l.sp.setText(str(int(percent)))
        return
    l.pBar.setValue(int(percent))
    l.sp.setText(str(int(percent)))
    l.percent = percent
    DataBase.lessonLists[n][l.name]['percent'] = str(int(percent))


def main():
    app = QApplication(sys.argv)
    ex = Mainwin()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    setup(console=['hello.py'])
