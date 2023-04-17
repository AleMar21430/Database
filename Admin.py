from Qt_Core import *
from Query_Tool import *
from Tools import *

class Admin_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App  = App
		self.Log = Log_Tool()
		Output = Output_Tool(self.App, self.Log)
		Outliner = Admin_Outliner_Tool(self.App, self.Log, Output)
		Premade_Outliner = Premade_Outliner_Tool(self.App, self.Log,Output)
		Query = Query_Tool(self.App, self.Log, Output)

		Restart = QT_Button()
		Restart.setText("Restart")

		Splitter = QT_Splitter(False)
		Outline_Layout = QT_Linear_Contents()
		Outline_Layout.Layout.addWidget(Outliner)
		Outline_Layout.Layout.addWidget(Premade_Outliner)
		Outline_Layout.Layout.addWidget(Restart)
		Splitter.addWidget(Outline_Layout)
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
		Outline_Layout.Layout.setStretch(0,1)
		Outline_Layout.Layout.setStretch(1,1)
		Outline_Layout.Layout.setStretch(2,0)

		self.setCentralWidget(Splitter)
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.setWindowTitle("Neuro Chama Admin")
		self.showMaximized()
		self.Log.append("Initialized","50,250,250")

		Restart.clicked.connect(self.restart)

	def restart(self):
		self.App.start()