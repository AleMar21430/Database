from Qt_Core import *
from Query_Tool import *
from Tools import *

class Admin_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App  = App
		self.Log = Log_Tool()
		Output = Output_Tool(self.App, self.Log,True)
		self.Outliner = Outliner_Tool(self.App, self.Log, Output, True)
		self.Premade_Outliner = Premade_Outliner_Tool(self.App, self.Log,Output,True)
		Query = Query_Tool(self.App, self.Log, Output)
		Source_Editor = Source_Editor_Tool(self, self.Log)

		Restart = QT_Button()
		Restart.setText("Restart")

		Splitter = QT_Splitter(False)
		Outline_Layout = QT_Linear_Contents()
		Outline_Layout.Layout.addWidget(self.Outliner)
		Outline_Layout.Layout.addWidget(self.Premade_Outliner)
		Outline_Layout.Layout.addWidget(Restart)
		Splitter.addWidget(Outline_Layout)
		VSplitter = QT_Splitter(True)
		VSplitter.addWidget(Query)
		VSplitter.addWidget(self.Log)
		Splitter.addWidget(VSplitter)
		VOutputSplitter = QT_Splitter(True)
		VOutputSplitter.addWidget(Output)
		VOutputSplitter.addWidget(Source_Editor)
		Splitter.addWidget(VOutputSplitter)

		Splitter.setSizes([500,500,2000])
		VSplitter.setStretchFactor(0,65)
		VSplitter.setStretchFactor(1,35)
		VOutputSplitter.setSizes([2000,1000])
		Outline_Layout.Layout.setStretch(0,1)
		Outline_Layout.Layout.setStretch(1,1)
		Outline_Layout.Layout.setStretch(2,0)

		self.setCentralWidget(Splitter)
		self.setWindowIcon(QIcon("./Resources/Icon.jpg"))
		self.setWindowTitle("Neuro Chama Admin")
		self.showMaximized()
		self.Log.append("Initialized","50,250,250")

		Restart.clicked.connect(self.restart)

	def restart(self):
		self.App.start()
		self.close()
		self.deleteLater()
		self.destroy()