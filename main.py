import requests
import sqlite3
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication, QWidget, QLabel, QGraphicsView, QTableWidget
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import threading
from pyqtgraph import plot
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Nastroiki(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('smena_nastroek.ui', self)
        self.pushButton.clicked.connect(self.extr)
        self.pushButton_2.clicked.connect(self.prinat)
        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(T)
        self.spinBox_2.setRange(0, 100)
        self.spinBox_2.setValue(H)
        self.spinBox_3.setRange(0, 100)
        self.spinBox_3.setValue(Hb)
        self.spinBox_4.setRange(0, 100)
        self.spinBox_4.setValue(Ch)

    def prinat(self):
        global T, H, Hb, Ch, nas
        T = self.spinBox.value()
        H = self.spinBox_2.value()
        Hb = self.spinBox_3.value()
        Ch = self.spinBox_4.value()
        que = f"UPDATE Nast SET T={T}"
        cur.execute(que)
        que = f"UPDATE Nast SET H={H}"
        cur.execute(que)
        que = f"UPDATE Nast SET Hb={Hb}"
        cur.execute(que)
        que = f"UPDATE Nast SET Ch_obn_dan={Ch}"
        cur.execute(que)
        con.commit()
        self.hide()

    def extr(self):
        global extrn_r
        extrn_r = True
        self.hide()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        super().__init__()
        self.proxy_widget = None
        uic.loadUi('Main_window.ui', self)  # Загружаем дизайн
        MainWindow = uic.loadUi('Main_window.ui', self)
        self.retranslateUi(MainWindow)
        self.obnov()
        self.pushButton.clicked.connect(self.Fortochka)
        self.pushButton_2.clicked.connect(self.Uvlajnenie)
        self.pushButton_3.clicked.connect(lambda: self.Borozdi(3))
        self.pushButton_4.clicked.connect(lambda: self.Borozdi(4))
        self.pushButton_5.clicked.connect(lambda: self.Borozdi(5))
        self.pushButton_6.clicked.connect(lambda: self.Borozdi(6))
        self.pushButton_7.clicked.connect(lambda: self.Borozdi(7))
        self.pushButton_8.clicked.connect(lambda: self.Borozdi(8))
        self.x = [i for i in range(0, -100, -10)]
        self.y = [[0] * 10, [0] * 10, [0] * 10, [0] * 10]
        self.pushButton_9.clicked.connect(self.Nast)
        self.rowPosition = -1
        self.Obnov_tabl()

    def Obnov_tabl(self):
        if self.rowPosition == 10:
            self.rowPosition = 0
            self.tableWidget_3.setRowCount(0)
            self.tableWidget.setRowCount(0)
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_4.setRowCount(0)
        self.tableWidget_3.setRowCount(1+self.rowPosition)
        self.tableWidget.setRowCount(1 + self.rowPosition)
        self.tableWidget_2.setRowCount(1 + self.rowPosition)
        self.tableWidget_4.setRowCount(1 + self.rowPosition)
        con = sqlite3.connect("Теплица.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Vho_dan;""").fetchall()[-1]
        con.commit()
        self.tableWidget_3.setItem(self.rowPosition, 1, QTableWidgetItem(str(float('{:.1f}'.format(result[11])))))
        self.tableWidget_3.setItem(self.rowPosition, 0, QTableWidgetItem(str(float('{:.1f}'.format(result[10])))))
        self.tableWidget.setItem(self.rowPosition, 0, QTableWidgetItem(str(result[0]).split('_')[0]))
        self.tableWidget.setItem(self.rowPosition, 1, QTableWidgetItem(str(result[1]).split('_')[0]))
        self.tableWidget.setItem(self.rowPosition, 2, QTableWidgetItem(str(result[2]).split('_')[0]))
        self.tableWidget.setItem(self.rowPosition, 3, QTableWidgetItem(str(result[3]).split('_')[0]))
        self.tableWidget_4.setItem(self.rowPosition, 0, QTableWidgetItem(str(result[0]).split('_')[1]))
        self.tableWidget_4.setItem(self.rowPosition, 1, QTableWidgetItem(str(result[1]).split('_')[1]))
        self.tableWidget_4.setItem(self.rowPosition, 2, QTableWidgetItem(str(result[2]).split('_')[1]))
        self.tableWidget_4.setItem(self.rowPosition, 3, QTableWidgetItem(str(result[3]).split('_')[1]))
        self.tableWidget_2.setItem(self.rowPosition, 0, QTableWidgetItem(str(result[4])))
        self.tableWidget_2.setItem(self.rowPosition, 1, QTableWidgetItem(str(result[5])))
        self.tableWidget_2.setItem(self.rowPosition, 2, QTableWidgetItem(str(result[6])))
        self.tableWidget_2.setItem(self.rowPosition, 3, QTableWidgetItem(str(result[7])))
        self.tableWidget_2.setItem(self.rowPosition, 4, QTableWidgetItem(str(result[8])))
        self.tableWidget_2.setItem(self.rowPosition, 5, QTableWidgetItem(str(result[9])))
        self.rowPosition += 1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def Nast(self):
        nas.show()

    def Fortochka(self):
        global OpenF
        if extrn_r or srt > T:
            OpenF = not OpenF
            con = sqlite3.connect("Теплица.db")
            cur = con.cursor()
            que = f"UPDATE Sost SET fortochka={OpenF}"
            cur.execute(que)
            con.commit()
            if OpenF:
                requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', params={"state": 1}, headers=headers)
            else:
                requests.patch('https://dt.miet.ru/ppo_it/api/fork_drive/', params={"state": 0}, headers=headers)
            self.obnov()

    def Uvlajnenie(self):
        global Obch_uvl
        if extrn_r or srv < H:
            Obch_uvl = not Obch_uvl
            con = sqlite3.connect("Теплица.db")
            cur = con.cursor()
            que = f"UPDATE Sost SET Edin_sist_up_v={Obch_uvl}"
            cur.execute(que)
            con.commit()
            if Obch_uvl:
                requests.patch('https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 1}, headers=headers)
            else:
                requests.patch('https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 0}, headers=headers)
            self.obnov()

    def Borozdi(self, i):
        global Bor
        try:
            if extrn_r or dvp[i - 3]['humidity'] < Hb:
                Bor[i - 3] = not Bor[i - 3]
                con = sqlite3.connect("Теплица.db")
                cur = con.cursor()
                que = f"UPDATE Sost SET sist_av_pol_gr{i - 2}={Bor[i - 3]}"
                cur.execute(que)
                con.commit()
                if Bor[i - 3]:
                    requests.patch('https://dt.miet.ru/ppo_it/api/watering', params={"id": i-2, "state": 1}, headers=headers)
                else:
                    requests.patch('https://dt.miet.ru/ppo_it/api/watering', params={"id": i-2, "state": 0}, headers=headers)
                self.obnov()
        except BaseException:
            time.sleep(0.1)
            self.Borozdi(i)

    def obnov(self):
        global OpenF, Obch_uvl, Bor
        if OpenF:
            self.pushButton.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                          'border-radius:  10px;}')
            self.pushButton.setText('Открыта')
        else:
            self.pushButton.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                          'border-radius:  10px;}')
            self.pushButton.setText('Закрыта')
        if Obch_uvl:
            self.pushButton_2.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_2.setText('Включено')
        else:
            self.pushButton_2.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_2.setText('Выключено')
        if Bor[0]:
            self.pushButton_3.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_3.setText('Включена')
        else:
            self.pushButton_3.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_3.setText('Выключена')
        if Bor[1]:
            self.pushButton_4.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_4.setText('Включена')
        else:
            self.pushButton_4.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_4.setText('Выключена')
        if Bor[2]:
            self.pushButton_5.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_5.setText('Включена')
        else:
            self.pushButton_5.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_5.setText('Выключена')
        if Bor[3]:
            self.pushButton_6.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_6.setText('Включена')
        else:
            self.pushButton_6.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_6.setText('Выключена')
        if Bor[4]:
            self.pushButton_7.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_7.setText('Включена')
        else:
            self.pushButton_7.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_7.setText('Выключена')
        if Bor[5]:
            self.pushButton_8.setStyleSheet('QPushButton {background-color: green; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_8.setText('Включена')
        else:
            self.pushButton_8.setStyleSheet('QPushButton {background-color: grey; color: white; font-size:  33px; '
                                            'border-radius:  10px;}')
            self.pushButton_8.setText('Выключена')


    def closeEvent(self, event):
        global Cl
        Cl = True


class MplCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(MplCanvas, self).__init__(self.fig, *args, **kwargs)

    def plot(self, x, y, c=[]):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(x, y)
        for i in range(0, len(c), 2):
            self.ax.plot(c[i], c[i+1])
        self.draw()

    def _clear(self):
        self.fig.clear()
        self.draw()


class TEST(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(TEST, self).__init__()
        self.setupUi(self)

        self.canavas1 = MplCanvas()  # !!! canavas
        self.canavas1.setMinimumSize(1, 1)
        self.toolbar1 = NavigationToolbar(self.canavas1, self)

        self.canavas2 = MplCanvas()  # !!! canavas
        self.canavas2.setMinimumSize(300, 300)
        self.toolbar2 = NavigationToolbar(self.canavas2, self)

        self.canavas3 = MplCanvas()  # !!! canavas
        self.canavas3.setMinimumSize(300, 300)
        self.toolbar3 = NavigationToolbar(self.canavas3, self)

        self.canavas4 = MplCanvas()  # !!! canavas
        self.canavas4.setMinimumSize(300, 200)
        self.toolbar4 = NavigationToolbar(self.canavas4, self)

        self.canavas5 = MplCanvas()  # !!! canavas
        self.canavas5.setMinimumSize(300, 200)
        self.toolbar5 = NavigationToolbar(self.canavas5, self)

        self.canavas6 = MplCanvas()  # !!! canavas
        self.canavas6.setMinimumSize(300, 200)
        self.toolbar6 = NavigationToolbar(self.canavas6, self)

        self.canavas7 = MplCanvas()  # !!! canavas
        self.canavas7.setMinimumSize(300, 200)
        self.toolbar7 = NavigationToolbar(self.canavas7, self)

        self.canavas8 = MplCanvas()  # !!! canavas
        self.canavas8.setMinimumSize(300, 200)
        self.toolbar8 = NavigationToolbar(self.canavas8, self)

        self.canavas9 = MplCanvas()  # !!! canavas
        self.canavas9.setMinimumSize(300, 200)
        self.toolbar9 = NavigationToolbar(self.canavas9, self)

        self.canavas10 = MplCanvas()  # !!! canavas
        self.canavas10.setMinimumSize(10, 10)
        self.toolbar10 = NavigationToolbar(self.canavas10, self)

        self.verticalLayout.addWidget(self.canavas1)
        self.verticalLayout.addWidget(self.toolbar1)
        self.verticalLayout_2.addWidget(self.canavas2)
        self.verticalLayout_2.addWidget(self.toolbar2)
        self.verticalLayout_3.addWidget(self.canavas3)
        self.verticalLayout_3.addWidget(self.toolbar3)
        self.verticalLayout_4.addWidget(self.canavas4)
        self.verticalLayout_4.addWidget(self.toolbar4)
        self.verticalLayout_5.addWidget(self.canavas5)
        self.verticalLayout_5.addWidget(self.toolbar5)
        self.verticalLayout_6.addWidget(self.canavas6)
        self.verticalLayout_6.addWidget(self.toolbar6)
        self.verticalLayout_7.addWidget(self.canavas7)
        self.verticalLayout_7.addWidget(self.toolbar7)
        self.verticalLayout_8.addWidget(self.canavas8)
        self.verticalLayout_8.addWidget(self.toolbar8)
        self.verticalLayout_9.addWidget(self.canavas9)
        self.verticalLayout_9.addWidget(self.toolbar9)
        self.verticalLayout_10.addWidget(self.canavas10)
        self.verticalLayout_10.addWidget(self.toolbar10)
        self.toolbar1.hide()
        self.toolbar2.hide()
        self.toolbar3.hide()
        self.toolbar4.hide()
        self.toolbar5.hide()
        self.toolbar6.hide()
        self.toolbar7.hide()
        self.toolbar8.hide()
        self.toolbar9.hide()
        self.toolbar10.hide()

    def _plot(self):
        con = sqlite3.connect("Теплица.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM Vho_dan;""").fetchall()
        con.commit()
        y = [i for i in range(-20, 0, 2)]
        cx1 = [i[11] for i in result][-10:]
        cx2 = [i[10] for i in result][-10:]
        cx3 = [i[9] for i in result][-10:]
        cx4 = [i[8] for i in result][-10:]
        cx5 = [i[7] for i in result][-10:]
        cx6 = [i[6] for i in result][-10:]
        cx7 = [i[5] for i in result][-10:]
        cx8 = [i[4] for i in result][-10:]
        cx9 = [i[3] for i in result][-10:]
        cx10 = [i[2] for i in result][-10:]
        cx11 = [i[1] for i in result][-10:]
        cx12 = [i[0] for i in result][-10:]
        cx9t = [float(i[0]) for i in [i.split('_') for i in cx9]]
        cx9v = [float(i[1]) for i in [i.split('_') for i in cx9]]
        cx10t = [float(i[0]) for i in [i.split('_') for i in cx10]]
        cx10v = [float(i[1]) for i in [i.split('_') for i in cx10]]
        cx11t = [float(i[0]) for i in [i.split('_') for i in cx11]]
        cx11v = [float(i[1]) for i in [i.split('_') for i in cx11]]
        cx12t = [float(i[0]) for i in [i.split('_') for i in cx12]]
        cx12v = [float(i[1]) for i in [i.split('_') for i in cx12]]
        self.canavas1.plot(y, cx1)
        self.toolbar1.show()
        self.canavas2.plot(y, cx9t, [y, cx10t, y, cx11t, y, cx12t])
        self.toolbar2.show()
        self.canavas3.plot(y, cx9v, [y, cx10v, y, cx11v, y, cx12v])
        self.toolbar3.show()
        self.canavas4.plot(y, cx8)
        self.toolbar4.show()
        self.canavas5.plot(y, cx7)
        self.toolbar5.show()
        self.canavas6.plot(y, cx6)
        self.toolbar6.show()
        self.canavas7.plot(y, cx5)
        self.toolbar7.show()
        self.canavas8.plot(y, cx4)
        self.toolbar8.show()
        self.canavas9.plot(y, cx3)
        self.toolbar9.show()
        self.canavas10.plot(y, cx2)
        self.toolbar10.show()

    def button_clear(self):
        self.canavas1._clear()
        self.canavas2._clear()
        self.canavas3._clear()
        self.canavas4._clear()
        self.canavas5._clear()
        self.canavas6._clear()
        self.canavas7._clear()
        self.canavas8._clear()
        self.canavas9._clear()
        self.canavas10._clear()


def f():
    global srt, srv, dtv4, dvp
    if not Cl:
        threading.Timer(Ch, f).start()
    con = sqlite3.connect("Теплица.db")
    cur = con.cursor()
    dtv4 = []
    for i in range(1, 5):
        pageURL = f"https://dt.miet.ru/ppo_it/api/temp_hum/{i}"
        req = requests.get(pageURL, headers=headers)
        dtv4.append(req.json())
    dvp = []
    for i in range(1, 7):
        pageURL = f"https://dt.miet.ru/ppo_it/api/hum/{i}"
        req = requests.get(pageURL, headers=headers)
        dvp.append(req.json())
    srt = sum([i['temperature'] for i in dtv4]) / 4
    srv = sum([i['humidity'] for i in dtv4]) / 4
    que = """INSERT INTO Vho_dan(Dat_t_and_v1,Dat_t_and_v2,Dat_t_and_v3,Dat_t_and_v4,Dat_vl_p1,Dat_vl_p2,Dat_vl_p3,
    Dat_vl_p4,Dat_vl_p5,Dat_vl_p6,srt,srv) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
    it = [str(i['temperature'])+'_'+str(i['humidity']) for i in dtv4] + [i['humidity'] for i in dvp] + [srt, srv]
    if len(it) == 12 and len(dvp) == 6 and len(dtv4) == 4:
        cur.execute(que, it)
        con.commit()
        if ui is not None:
            ui.Obnov_tabl()
            ui.button_clear()
            ui._plot()


ui = None
Cl = False
token = 'wAruBW'
headers = {"X-Auth-Token": token}
con = sqlite3.connect("Теплица.db")
cur = con.cursor()
result = cur.execute("""SELECT * FROM Nast;""").fetchall()
result1 = cur.execute("""SELECT * FROM Sost;""").fetchall()
con.commit()
T = result[0][0]
H = result[0][1]
Hb = result[0][2]
Ch = result[0][3]
extrn_r = False
OpenF = result1[0][0]
Obch_uvl = result1[0][1]
Bor = [result1[0][2], result1[0][3], result1[0][4], result1[0][5], result1[0][6], result1[0][7]]
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TEST()
    f()
    ui.show()
    nas = Nastroiki()
    sys.exit(app.exec_())