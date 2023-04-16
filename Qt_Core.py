from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtOpenGL import *
from PySide6.QtOpenGLWidgets import *

class QT_Application(QApplication):
	def __init__(self, Args):
		super().__init__(Args)

class QT_Slider(QSlider):
	def __init__(self, Vertical: bool = False):
		if Vertical:
			super().__init__(Qt.Orientation.Vertical)
		else:
			super().__init__(Qt.Orientation.Horizontal)
		super().setContentsMargins(0,0,0,0)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class QT_Grid_Layout(QGridLayout):
	def __init__(self):
		super().__init__()

class QT_Button(QPushButton):
	def __init__(self):
		super().__init__()
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class QT_Toggle(QT_Button):
	def __init__(self):
		super().__init__()
		super().setCheckable(True)
		super().setChecked(False)

class QT_Linear_Contents(QWidget):
	def __init__(self, Vertical: bool = True):
		super().__init__()
		super().setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
		super().setContentsMargins(0,0,0,0)
		super().setObjectName("borderless")
		self.Layout = QT_Linear_Layout(Vertical)
		super().setLayout(self.Layout)

class QT_Line_Editor(QLineEdit):
	def __init__(self):
		super().__init__()
		super().setContentsMargins(0,0,0,0)

class QT_Spreadsheet(QTableWidget):
	def __init__(self):
		super().__init__()
		super().setContentsMargins(0,0,0,0)
		super().verticalHeader().setObjectName("borderless")
		super().horizontalHeader().setObjectName("borderless")

class QT_Text_Editor(QTextEdit):
	def __init__(self):
		super().__init__()
		super().setContentsMargins(0,0,0,0)
		super().setTabStopDistance(40)

class QT_Linear_Layout(QBoxLayout):
	def __init__(self, Vertical: bool = True):
		if Vertical: 
			super().__init__(QBoxLayout.Direction.TopToBottom)
			super().setAlignment(Qt.AlignmentFlag.AlignTop)
		else: 
			super().__init__(QBoxLayout.Direction.LeftToRight)
			super().setAlignment(Qt.AlignmentFlag.AlignLeft)
		super().setSpacing(2)
		super().setContentsMargins(0,0,0,0)

class QT_Scroll_Area(QScrollArea):
	def __init__():
		super().__init__()
		super().setWidgetResizable(True)
		super().setContentsMargins(0,0,0,0)

class QT_File_Explorer(QFileDialog):
	def __init__(self):
		super().__init__()

class QT_Text_Stream(QTextBrowser):
	def __init__(self):
		super().__init__()
		super().setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

	def append(self, Text = "Hello", RGB = "250,250,250"):
		super().append(f'<p style="color:rgb({RGB})">{Text}</p>')

class QT_Splitter(QSplitter):
	def __init__(self, Vertical: bool = True):
		if Vertical: super().__init__(Qt.Orientation.Vertical)
		else: super().__init__(Qt.Orientation.Horizontal)
		super().setHandleWidth(2)
		super().setContentsMargins(0,0,0,0)
		super().setObjectName("borderless")

class QT_Label(QLabel):
	def __init__(self, Text):
		super().__init__()
		super().setContentsMargins(0,0,0,0)
		super().setScaledContents(True)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		super().setText(Text)

class QT_Widget(QWidget):
	def __init__(self):
		super().__init__()
		super().setContentsMargins(0,0,0,0)
		super().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class QT_Menu(QMenu):
	def __init__(self, Title = "Title"):
		super().__init__(Title)
		super().setContentsMargins(0,0,0,0)

class QT_Window(QMainWindow):
	def __init__(self):
		super().__init__()
		super().setDockNestingEnabled(True)

class QT_Tree(QTreeWidget):
	def __init__(self):
		super().__init__()
		super().setHeaderHidden(True)
		super().setDragEnabled(True)

	def mousePressEvent(self, event):
		item = self.itemAt(event.pos())
		if item is not None:
			mime_data = QMimeData()
			mime_data.setText(item.Database_Name)

			drag = QDrag(self)
			drag.setMimeData(mime_data)
			drag.exec_()
		super().mousePressEvent(event)

class QT_Tree_Item(QTreeWidgetItem):
	def __init__(self, Parent, Display_Name = "", Query = "", DB_Name = "NULL", Table_Name = ""):
		super().__init__(Parent)
		super().setText(0,Display_Name)
		self.Display_Name = Display_Name
		self.Query = Query
		self.Table_Name = Table_Name
		if DB_Name == "NULL":
			self.Database_Name = Query
		else:
			self.Database_Name = DB_Name

class QT_Toolbar(QMenuBar):
	def __init__(self):
		super().__init__()
		super().setContentsMargins(0,0,0,0)

class QT_Toast(QT_Menu):
	def __init__(self, Message = "Message", Position = QPoint(0,0), color = "250,50,50"):
		super().__init__()
		Layout = QT_Linear_Layout()
		Label = QT_Label(Message)
		Layout.addWidget(Label)
		self.setLayout(Layout)
		self.setWindowTitle(Message)
		self.setStyleSheet(f"color:rgb({color}); font-size:26px;")
		self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.SplashScreen)
		self.setFixedSize(Label.sizeHint())

		timer = QTimer()
		timer.timeout.connect(self.close)
		timer.start(750)
		self.exec(Position)