from Qt_Core import *

class Startup_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App = App

		self.Username = QT_Line_Editor()
		self.Username.setPlaceholderText("Database Username")
		self.Username.setText("postgres")
		self.Password = QT_Line_Editor()
		self.Password.setPlaceholderText("Password")
		Startup = QT_Button()
		Startup.setText("Connect")
		Startup.clicked.connect(self.start)
		self.Username.returnPressed.connect(self.start)
		self.Password.returnPressed.connect(self.start)

		Layout = QT_Linear_Contents()
		Layout.Layout.addWidget(self.Username)
		Layout.Layout.addWidget(self.Password)
		Layout.Layout.addWidget(Startup)

		self.setCentralWidget(Layout)
		self.setWindowTitle("Neuro Chama Startup")
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
		self.show()

	def start(self):
		self.App.USER = self.Username.text()
		self.App.PASSWORD = self.Password.text()
		self.App.startTry()
		self.close()
		self.deleteLater()
		self.destroy()