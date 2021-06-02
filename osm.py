import os
import re
import sys
import requests
from PySide2 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel, QtGui

# https://www.youtube.com/watch?v=6c6KX0GjUI8&ab_channel=TKST1102 интересный пример использования карт
# https://leafletjs.com/index.html - сервис для работы со слоями карты (маркеры и прочее)
# https://www.mapbox.com/ - поставщик карт
# http://ip-api.com/ - инфо по IP - адресам


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initMap()

    def initUi(self):
        _taranslate = QtCore.QCoreApplication.translate
        widgetLeftPanel = QtWidgets.QWidget()
        widgetRightPanel = QtWidgets.QWidget()
        splitterMain = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        layoutMain = QtWidgets.QHBoxLayout()
        layoutLeftPanel = QtWidgets.QVBoxLayout()
        layoutRightPanel = QtWidgets.QVBoxLayout()

        # widgetLeftPanel
        self.labelCoords = QtWidgets.QLabel()
        self.view = QtWebEngineWidgets.QWebEngineView()

        # widgetRightPanel
        labelCheckIP = QtWidgets.QLabel("Проверить IP")
        self.lineEditCheckIP = QtWidgets.QLineEdit()
        self.lineEditCheckIP.setPlaceholderText("Введите IP для проверки")
        self.pushButtonCheckIP = QtWidgets.QPushButton("Проверить")

        self.lblstatus = QtWidgets.QLabel()
        self.lblstatus.setObjectName("lblstatus")
        self.lblstatus.setText("Status:")
        self.lblstatus1 = QtWidgets.QLabel()
        self.lblstatus1.setObjectName("lblstatus1")
        self.lblstatus1.setText("")
        self.lblcountry = QtWidgets.QLabel()
        self.lblcountry.setObjectName("lblcountry")
        self.lblcountry.setText("Country")
        self.lblcountry1 = QtWidgets.QLabel()
        self.lblcountry1.setObjectName("lblcountry1")
        self.lblcountry1.setText("")
        self.lblregion = QtWidgets.QLabel()
        self.lblregion.setObjectName("lblregion")
        self.lblregion.setText("Region:")
        self.lblregion1 = QtWidgets.QLabel()
        self.lblregion1.setObjectName("lblregion1")
        self.lblregion1.setText("")
        self.lblcity = QtWidgets.QLabel()
        self.lblcity.setObjectName("lblcity")
        self.lblcity.setText("City:")
        self.lblcity1 = QtWidgets.QLabel()
        self.lblcity1.setObjectName("lblcity1")
        self.lblcity1.setText("")
        self.lblzip = QtWidgets.QLabel()
        self.lblzip.setObjectName("lblzip")
        self.lblzip.setText("ZIP Code:")
        self.lblzip1 = QtWidgets.QLabel()
        self.lblzip1.setObjectName("lblzip1")
        self.lblzip1.setText("")
        self.lbllatelong = QtWidgets.QLabel()
        self.lbllatelong.setObjectName("lbllatelong")
        self.lbllatelong.setText("Coordinates:")
        self.lbllatelong1 = QtWidgets.QLabel()
        self.lbllatelong1.setObjectName("lbllatelong1")
        self.lbllatelong1.setText("")
        self.lbltz = QtWidgets.QLabel()
        self.lbltz.setObjectName("lbltz")
        self.lbltz.setText("Time Zone:")
        self.lbltz1 = QtWidgets.QLabel()
        self.lbltz1.setObjectName("lbltz1")
        self.lbltz1.setText("")
        self.lblorg = QtWidgets.QLabel()
        self.lblorg.setObjectName("lblorg")
        self.lblorg.setText("Organization:")
        self.lblorg1 = QtWidgets.QLabel()
        self.lblorg1.setObjectName("lblorg1")
        self.lblorg1.setText("")

        layoutLeftPanel.addWidget(self.labelCoords)
        layoutLeftPanel.addWidget(self.view)

        layoutRightPanel.addWidget(labelCheckIP)
        layoutRightPanel.addWidget(self.lineEditCheckIP)
        layoutRightPanel.addWidget(self.pushButtonCheckIP)
        layoutRightPanel.addWidget(self.lblstatus)
        layoutRightPanel.addWidget(self.lblstatus1)
        layoutRightPanel.addWidget(self.lblcountry)
        layoutRightPanel.addWidget(self.lblcountry1)
        layoutRightPanel.addWidget(self.lblregion)
        layoutRightPanel.addWidget(self.lblregion1)
        layoutRightPanel.addWidget(self.lblcity)
        layoutRightPanel.addWidget(self.lblcity1)
        layoutRightPanel.addWidget(self.lblzip)
        layoutRightPanel.addWidget(self.lblzip1)
        layoutRightPanel.addWidget(self.lbllatelong)
        layoutRightPanel.addWidget(self.lbllatelong1)
        layoutRightPanel.addWidget(self.lbltz)
        layoutRightPanel.addWidget(self.lbltz1)
        layoutRightPanel.addWidget(self.lblorg)
        layoutRightPanel.addWidget(self.lblorg1)
        layoutRightPanel.addStretch(1)

        widgetLeftPanel.setLayout(layoutLeftPanel)
        widgetRightPanel.setLayout(layoutRightPanel)

        splitterMain.addWidget(widgetLeftPanel)
        splitterMain.addWidget(widgetRightPanel)

        layoutMain.addWidget(splitterMain)

        self.setLayout(layoutMain)

        self.pushButtonCheckIP.clicked.connect(self.getIPInfo)

    def initMap(self):
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "map.html",)

        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject("MainWindow", self)

        self.view.page().setWebChannel(self.channel)
        self.view.setUrl(QtCore.QUrl.fromLocalFile(file))
        self.view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    @QtCore.Slot(float, float)
    def onMapMove(self, lat, lng):
        self.labelCoords.setText("Текущие координаты:\nДолгота: {:.5f}, Широта: {:.5f}".format(lng, lat))

    def getIPInfo(self):
        def getIPValidation(ip_):
            if len(ip) != 0:
                reg = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}" \
                      "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
                if re.match(reg, ip_) is None:
                    return False
                return True

        ip = self.lineEditCheckIP.text()

        if getIPValidation(ip) is False:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введенные данные не являются IP - адресом")
            return

        response = requests.get(f"http://ip-api.com/json/{ip}")
        response = response.json()
        print(response)

        if response.get('status') != 'success':
            QtWidgets.QMessageBox.about(self, "Уведомление", "Информация по IP - адресу не найдена")
            self.lblstatus1.setText("")
            self.lblcountry1.setText("")
            self.lblregion1.setText("")
            self.lblcity1.setText("")
            self.lblzip1.setText("")
            self.lbllatelong1.setText("")
            self.lbltz1.setText("")
            self.lblorg1.setText("")
            return

        self.lblstatus1.setText(response.get('status'))
        self.lblcountry1.setText(response.get('country'))
        self.lblregion1.setText(response.get('regionName'))
        self.lblcity1.setText(response.get('city'))
        self.lblzip1.setText(response.get('zip'))
        self.lbllatelong1.setText(str(response.get('lat'))+":"+str(response.get('lon')))
        self.lbltz1.setText(response.get('timezone'))
        self.lblorg1.setText(response.get('org'))

        page = self.view.page()

        page.runJavaScript(f"map.setView([{response.get('lat')}, {response.get('lon')}], 16);")
        page.runJavaScript(f"L.marker([{response.get('lat')}, {response.get('lon')}]).addTo(map)"
                           f".bindPopup('<b>Провайдер:</b>{response.get('isp')}<br><b>Организация:</b> {response.get('org')}')"
                           f".openPopup();")
        circleOpt = "{color: 'blue', fillColor: '#B8E1E9', fillOpacity: 0.4, radius: 500}"
        page.runJavaScript("L.circle([{0}, {1}], {2}).addTo(map);"
                           .format(response.get('lat'), response.get('lon'), circleOpt))


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = MainWindow()
    w.show()
    app.exec_()
