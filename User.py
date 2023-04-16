from Qt_Core import *
from Query_Tool import *
from Tools import *

class User_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.Log = Log_Tool()
		Output = Output_Tool(self.Log)
		Search = Search_Tool()
		Premade_Outliner = Premade_Outliner_Tool(self.Log, Output)
		Outliner = Outliner_Tool(self.Log, Output)

		Splitter = QT_Splitter(False)

		InputSplitter = QT_Splitter(True)
		InputSplitter.addWidget(Search)
		InputSplitter.addWidget(Premade_Outliner)
		InputSplitter.addWidget(Outliner)

		OutputSplitter = QT_Splitter(True)
		OutputSplitter.addWidget(Output)
		OutputSplitter.addWidget(self.Log)

		Splitter.addWidget(InputSplitter)
		Splitter.addWidget(OutputSplitter)

		Splitter.setSizes([20,80])
		OutputSplitter.setSizes([100,0])

		self.setCentralWidget(Splitter)
		self.setWindowTitle("Neuro Chama")
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.showMaximized()
		self.Log.append("Initialized","50,250,250")
