from Qt_Core import *
from Query_Tool import *
from Tools import *

class Admin_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.Log = Log_Tool()
		Output = Output_Tool(self.Log)
		Outliner = Admin_Outliner_Tool(self.Log, Output)
		Query = Query_Tool(self.Log, Output)

		Splitter = QT_Splitter(False)
		Splitter.addWidget(Outliner)
		VSplitter = QT_Splitter(True)
		VSplitter.addWidget(Query)
		VSplitter.addWidget(self.Log)
		Splitter.addWidget(VSplitter)
		VOutputSplitter = QT_Splitter(True)
		VOutputSplitter.addWidget(Output)
		Source_Editor = Source_Editor_Tool(self.Log)
		VOutputSplitter.addWidget(Source_Editor)
		Splitter.addWidget(VOutputSplitter)

		Splitter.setStretchFactor(0,15)
		Splitter.setStretchFactor(1,25)
		Splitter.setStretchFactor(2,60)
		VSplitter.setStretchFactor(0,65)
		VSplitter.setStretchFactor(1,35)
		VOutputSplitter.setSizes([50,50])

		self.setCentralWidget(Splitter)
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.setWindowTitle("Neuro Chama Admin")
		self.showMaximized()
		self.Log.append("Initialized","50,250,250")