from Signin import *
from Signup import *
from Startup import *
from Admin import Admin_Window
from User import User_Window
import psycopg2
from psycopg2 import extensions
import sys

Style = '''*, *::section {
	font-family:Consolas;
	font-size:18px;
	font-weight:Bold;

	background:rgb(50,50,50);
	color:rgb(250,250,250);
	gridline-color:rgb(150,150,150);

	border-style:solid;
	border-color:rgb(0,0,0);
	border-width:2px;
	border-radius:5px;
}
*::item:selected , *::section:checked {
	background:rgb(100,100,100);
}
*::section {
	background:rgb(25,25,25);
	border-color:rgb(225,225,225);
	padding: 0 5px 0 5px;
	border-radius:0px;
	border-width:1px;
}
*#borderless{
	border-width:0px;
}
*::pressed {
	background:rgb(50,150,150);
}
QScrollBar::handle {
	background:rgb(50,250,250);
}
QScrollBar::add-line, QScrollBar::sub-line {
	background:transparent
}
QTreeWidget::branch:has-siblings:!adjoins-item {
	border-image: url(./Resources/vline.png) 0;
}

QTreeWidget::branch:has-siblings:adjoins-item {
	border-image: url(./Resources/branch-more.png) 0;
}

QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
	border-image: url(./Resources/branch-end.png) 0;
}

QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {
	border-image: none;
	image: url(./Resources/branch-closed.png);
}

QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings  {
	border-image: none;
	image: url(./Resources/branch-open.png);
}
QPlainTextEdit {
	background:rgb(25,25,25);
	color:rgb(200,250,250);
}
'''

class Main_Application(QT_Application):
	def __init__(self):
		super().__init__(sys.argv)
		self.setStyleSheet(Style)
		self.start()
		sys.exit(self.exec())

	def start(self):
		try:
			self.DB = "p2neuro"
			self.USER = "postgres"
			self.PASSWORD = "123"
			conn = psycopg2.connect(database=self.DB, user=self.USER, password=self.PASSWORD, host="localhost", port="5432")
			cursor = conn.cursor()

			autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
			conn.set_isolation_level( autocommit )

			for Queries in open("./Database/Db_Create.txt").read().split(";"):
				try: cursor.execute(Queries)
				except Exception as Error: print(Error)
			conn.commit()

			try: cursor.execute(open("./Database/Db_Triggers.txt").read())
			except Exception as Error: print(Error)
			conn.commit()

			cursor.close()
			conn.close()
			try: self.Window.close()
			except: pass
			self.Window = Signin_Window(self)
		except Exception as Error:
			print("Initial Error "+str(Error))
			self.Window = Startup_Window(self)

	def startTry(self):
		conn = psycopg2.connect(user=self.USER, password=self.PASSWORD)
		cursor = conn.cursor()
		autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
		conn.set_isolation_level( autocommit )

		try:
			cursor.execute(f"CREATE DATABASE {self.DB}")
		except Exception as Error:
			print(Error)
		conn.commit()
		cursor.close()
		conn.close()
		self.start()

	def signIn(self):
		self.Window = Signin_Window(self)
	def signUp(self):
		self.Window = Signup_Window(self)
	def launchUser(self):
		self.Window = User_Window(self)
	def launchAdmin(self):
		self.Window = Admin_Window(self)

App = Main_Application()