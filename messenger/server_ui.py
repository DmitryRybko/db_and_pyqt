import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from sqlalchemy import select
import database


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("server_ui.ui", self)
        self.tableWidget.setColumnWidth(0, 200)
        self.loaddata()

    def loaddata(self):
        # clients = ["client_01", "client_02"]

        engine = database.create_engine('sqlite:///database.sqlite', echo=False)
        database.Base.metadata.create_all(engine)

        Session = database.sessionmaker(bind=engine)
        session = Session()

        all_clients = session.query(database.Client).all()

        clients = []

        for record in all_clients:
            clients.append(record.__dict__["login"])

        row = 0
        self.tableWidget.setRowCount(len(clients))
        for client in clients:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(client))
            row += 1


app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
