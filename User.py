from Qt_Core import *
from Query_Tool import *
from Tools import *

class User_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App = App
		self.Log = Log_Tool()
		Output = Output_Tool(self.App, self.Log)
		Premade_Outliner = Premade_Outliner_Tool(self.App, self.Log, Output)
		Outliner = Outliner_Tool(self.App, self.Log, Output)
		Restart = QT_Button()
		Restart.setText("Restart")

		Splitter = QT_Splitter(False)

		InputSplitter = QT_Splitter(True)
		InputSplitter.addWidget(Premade_Outliner)
		InputSplitter.addWidget(Outliner)
		InputSplitter.addWidget(Restart)

		OutputSplitter = QT_Splitter(True)
		OutputSplitter.addWidget(Output)
		OutputSplitter.addWidget(self.Log)

		Splitter.addWidget(InputSplitter)
		Splitter.addWidget(OutputSplitter)

		Splitter.setSizes([2000,8000])
		InputSplitter.setSizes([1000,1000,1])
		OutputSplitter.setSizes([100,0])

		self.setCentralWidget(Splitter)
		self.setWindowTitle("Neuro Chama")
		self.setWindowIcon(QIcon("./Resources/Icon.jpg"))
		self.showMaximized()
		self.Log.append("Initialized","50,250,250")

		Restart.clicked.connect(self.restart)

	def restart(self):
		self.App.start()