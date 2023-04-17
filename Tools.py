from Qt_Core import *
from Query_Tool import *
import psycopg2
from psycopg2 import extensions
import chardet

class Search_Tool(QT_Line_Editor):
	def __init__(self):
		super().__init__()
		self.setPlaceholderText("Search")

class Outliner_Tool(QT_Tree):
	def __init__(self, App, Log: QT_Text_Stream, Output: "Output_Tool"):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output

		self.setTree()
		self.itemDoubleClicked.connect(self.itemSelect)

	def itemSelect(self, item):
		self.Output.Add_Button.show()
		self.Output.Remove_Button.show()
		item.setExpanded(False)
		self.commit(item)

	def commit(self, Item):
		conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		cur = conn.cursor()
		try:
			cur.execute(Item.Query)
			conn.commit()
			self.Data = cur.fetchall()
			Coulmn_Labels = [str(desc[0]) for desc in cur.description]
			self.Output.Set = True
			self.Output.Spreadsheet.setColumnCount(len(Coulmn_Labels))
			self.Output.Spreadsheet.setRowCount(len(self.Data))
			self.Output.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)
			self.Output.Table_Name = Item.Table_Name
			self.Output.Query = Item.Query

			for row in range(len(self.Data)):
				for column in range(len(self.Data[0])):
					item = QTableWidgetItem(str(self.Data[row][column]))
					self.Output.Spreadsheet.setItem(row, column, item)

			self.Output.Spreadsheet.resizeColumnsToContents()
			self.Output.Spreadsheet.resizeRowsToContents()
			self.Output.Set = False

		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
		for row in range(self.Output.Spreadsheet.rowCount()):
			item = self.Output.Spreadsheet.item(row, 0)
			flags = item.flags()
			flags &= Qt.ItemFlag.ItemIsEditable
			item.setFlags(flags)
		cur.close()
		conn.close()

	def setTree(self):
		with open("./Database/Db_Tables.txt", "r", encoding = "utf-8") as File:
			for Tables in File.read().split("+"):
				Table_Info = []
				for Line in Tables.split("~"):
					if Line.strip() != "-":
						Table_Info.append(Line)
				for i in range(len(Table_Info)):
					if i == 0:
						Parent = Table_Info[i].split('|')
						Parent0 = Parent[0].replace("\n", " ")
						Parent1 = Parent[1].replace("\n", " ")
						exec(f"{Parent1} = QT_Tree_Item(self,'{Parent0}','SELECT * FROM {Parent1}','{Parent1}','{Parent1}')")
					else:
						Child = Table_Info[i].split('|')
						Parent0 = Parent[0].replace("\n", " ")
						Parent1 = Parent[1].replace("\n", " ")
						Child0 = Child[0].replace("\n", " ")
						Child1 = Child[1].replace("\n", " ")
						exec(f"QT_Tree_Item({Parent1},'{Child0}','SELECT id, {Child1} FROM {Parent1}','{Child1}','{Parent1}')")

class Admin_Outliner_Tool(QT_Tree):
	def __init__(self, App, Log: QT_Text_Stream, Output: "Output_Tool"):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output

		self.setTree()
		self.itemDoubleClicked.connect(self.itemSelect)

	def itemSelect(self, item):
		self.Output.Add_Button.show()
		self.Output.Remove_Button.show()
		item.setExpanded(False)
		self.commit(item)

	def commit(self, Item):
		conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")

		cur = conn.cursor()
		try:
			cur.execute(Item.Query)
			conn.commit()
			self.Data = cur.fetchall()
			Coulmn_Labels = [str(desc[0]) for desc in cur.description]
			self.Output.Set = True
			self.Output.Spreadsheet.setColumnCount(len(Coulmn_Labels))
			self.Output.Spreadsheet.setRowCount(len(self.Data))
			self.Output.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)
			self.Output.Table_Name = Item.Table_Name
			self.Output.Query = Item.Query

			for row in range(len(self.Data)):
				for column in range(len(self.Data[0])):
					item = QTableWidgetItem(str(self.Data[row][column]))
					self.Output.Spreadsheet.setItem(row, column, item)

			self.Output.Spreadsheet.resizeColumnsToContents()
			self.Output.Spreadsheet.resizeRowsToContents()
			self.Output.Set = False

		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
		for row in range(self.Output.Spreadsheet.rowCount()):
			item = self.Output.Spreadsheet.item(row, 0)
			flags = item.flags()
			flags &= Qt.ItemFlag.ItemIsEditable
			item.setFlags(flags)
		cur.close()
		conn.close()

	def setTree(self):
		with open("./Database/Db_Tables.txt", "r", encoding = "utf-8") as File:
			Pre = File.read()
			for Tables in Pre.split("+"):
				Table_Info = []
				for Line in Tables.split("~"):
					if Line.strip() != "-":
						Table_Info.append(Line)
				for i in range(len(Table_Info)):
					if i == 0:
						Parent = Table_Info[i].split('|')
						Parent0 = Parent[0].replace("\n", " ")
						Parent1 = Parent[1].replace("\n", " ")
						exec(f"{Parent1} = QT_Tree_Item(self,'{Parent0}','SELECT * FROM {Parent1}','{Parent1}','{Parent1}')")
					else:
						Child = Table_Info[i].split('|')
						Parent0 = Parent[0].replace("\n", " ")
						Parent1 = Parent[1].replace("\n", " ")
						Child0 = Child[0].replace("\n", " ")
						Child1 = Child[1].replace("\n", " ")
						exec(f"QT_Tree_Item({Parent1},'{Child0}','SELECT id, {Child1} FROM {Parent1}','{Child1}','{Parent1}')")

class Premade_Outliner_Tool(QT_Tree):
	def __init__(self, App, Log: QT_Text_Stream, Output: "Output_Tool", Admin = False):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output
		self.Admin = Admin

		self.setTree()
		self.itemDoubleClicked.connect(self.itemSelect)

	def itemSelect(self, item:QT_Tree_Item):
		self.Output.Add_Button.hide()
		self.Output.Remove_Button.hide()
		item.setExpanded(False)
		self.commit(item)

	def commit(self, Item):
		conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		cur = conn.cursor()
		try:
			cur.execute(Item.Query)
			conn.commit()
			self.Data = cur.fetchall()
			Coulmn_Labels = [str(desc[0]) for desc in cur.description]
			self.Output.Set = True
			self.Output.Spreadsheet.setColumnCount(len(Coulmn_Labels))
			self.Output.Spreadsheet.setRowCount(len(self.Data))
			self.Output.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)
			self.Output.Table_Name = Item.Table_Name
			self.Output.Query = Item.Query

			for row in range(len(self.Data)):
				for column in range(len(self.Data[0])):
					item = QTableWidgetItem(str(self.Data[row][column]))
					self.Output.Spreadsheet.setItem(row, column, item)

			self.Output.Spreadsheet.resizeColumnsToContents()
			self.Output.Spreadsheet.resizeRowsToContents()
			self.Output.Set = False

		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
		cur.close()
		conn.close()

	def setTree(self):
		File = open("./Database/Db_Queries.txt", "r", encoding = "utf-8").read()
		if self.Admin:
			File += open("./Database/Db_Admin.txt", "r", encoding = "utf-8").read()
		for Tables in File.split("+"):
			Table_Info = []
			for Line in Tables.split("~"):
				if Line.strip() != "-":
					Table_Info.append(Line.strip())
			for i in range(len(Table_Info)):
				if i == 0:
					Parent = Table_Info[i].split('|')
					Query = Parent[2].replace("\n", " ")
					exec(f"{Parent[1]} = QT_Tree_Item(self,'{Parent[0]}','''{Query}''')")
				else:
					Child = Table_Info[i].split('|')
					Query = Child[1].replace("\n", " ")
					exec(f"QT_Tree_Item({Parent[1]},'{Child[0]}','''{Query}''')")

class Log_Tool(QT_Text_Stream):
	def __init__(self):
		super().__init__()

class Input_Tool(QT_Linear_Contents):
	def __init__(self, App, Output, Table_Name, Log):
		super().__init__()
		self.App = App
		self.Output = Output
		self.Log = Log
		self.Table_Name = Table_Name
		self.Spreadsheet = QT_Spreadsheet()
		DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		DB_cursor = DB_connector.cursor()

		try:
			DB_cursor.execute(f"SELECT * FROM {Table_Name}")
			DB_connector.commit()
		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")
		Data = DB_cursor.fetchall()
		self.Coulmn_Labels = [str(desc[0]) for desc in DB_cursor.description][1:] # Ignore PK id

		self.Spreadsheet.setColumnCount(len(self.Coulmn_Labels))
		self.Spreadsheet.setHorizontalHeaderLabels(self.Coulmn_Labels)
		self.Columns = self.Coulmn_Labels
		self.Spreadsheet.setRowCount(1)

		DB_connector.close()

		Add_Button = QT_Button()
		Add_Button.setText("Add Item")
		Add_Button.clicked.connect(self.commit)
		self.Cancel_Button = QT_Button()
		self.Cancel_Button.setText("Cancel")
		self.Cancel_Button.clicked.connect(self.quit)

		self.Layout.addWidget(Add_Button)
		self.Layout.addWidget(self.Cancel_Button)
		self.Layout.addWidget(self.Spreadsheet)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,0)
		self.Layout.setStretch(2,1)

		self.Spreadsheet.resizeColumnsToContents()
		self.Spreadsheet.resizeRowsToContents()

		self.setWindowTitle("Input")
		self.setWindowIcon(QIcon("./Resources/Icon.jpg"))
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint)
		self.show()
		self.setGeometry(QRect(self.Output.mapToGlobal(self.Output.geometry().topLeft()),QSize(self.Output.size().width(), 150)))

	def commit(self):
		DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		DB_cursor = DB_connector.cursor()

		Data = []
		for i in range(len(self.Columns)):
			try:
				if self.Spreadsheet.item(0,i).text() == "''":
					Data.append("null")
				else:
					Data.append(self.Spreadsheet.item(0,i).text())
				
			except:
				Data.append("null")

		try:
			column_type = []
			Info = [f"{item}" for item in Data]
			for i in range(len(self.Coulmn_Labels)):
				DB_cursor.execute(f"SELECT data_type FROM information_schema.columns WHERE table_name = '{self.Table_Name}' AND column_name = '{self.Coulmn_Labels[i]}'")
				column_type.append(DB_cursor.fetchone()[0])
			for i in range(len(column_type)):
				if column_type[i] == "text":
					Info[i] = f"'{Info[i]}'"

			DB_cursor.execute(f"INSERT INTO {self.Table_Name} ({','.join(self.Columns)}) VALUES ({','.join(Info)})")
			DB_connector.commit()
			
			self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
			for row in range(self.Output.Spreadsheet.rowCount()):
				item = self.Output.Spreadsheet.item(row, 0)
				flags = item.flags()
				flags &= Qt.ItemFlag.ItemIsEditable
				item.setFlags(flags)

			DB_connector.close()
			self.Output.refresh()
			self.quit()

		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

	def quit(self):
		self.close()
		self.deleteLater()
		self.destroy()

class Delete_Tool(QT_Linear_Contents):
	def __init__(self, App, Output, Table_Name, Log):
		super().__init__()
		self.App = App
		self.Output = Output
		self.Log = Log
		self.Table_Name = Table_Name
		
		self.Id = QT_Line_Editor()
		self.Id.setPlaceholderText("ID")

		Remove_Button = QT_Button()
		Remove_Button.setText("Remove Item")
		Remove_Button.clicked.connect(self.commit)
		self.Cancel_Button = QT_Button()
		self.Cancel_Button.setText("Cancel")
		self.Cancel_Button.clicked.connect(self.quit)

		self.Layout.addWidget(Remove_Button)
		self.Layout.addWidget(self.Cancel_Button)
		self.Layout.addWidget(self.Id)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,0)
		self.Layout.setStretch(2,0)


		self.setWindowTitle("Input")
		self.setWindowIcon(QIcon("./Resources/Icon.jpg"))
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint)
		self.show()
		self.setGeometry(QRect(self.Output.mapToGlobal(self.Output.geometry().topLeft()),QSize(150, 80)))

	def commit(self):
		DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		DB_cursor = DB_connector.cursor()

		try:
			DB_cursor.execute(f"DELETE FROM {self.Table_Name} WHERE id = {self.Id.text()}")
			DB_connector.commit()
		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		DB_connector.close()
		self.Output.refresh()
		self.quit()

	def quit(self):
		self.close()
		self.deleteLater()
		self.destroy()

class Output_Tool(QT_Linear_Contents):
	def __init__(self, App, Log):
		self.App = App
		super().__init__()
		self.Spreadsheet = QT_Spreadsheet()
		self.Log = Log
		self.Table_Name = ""
		self.Query = ""
		self.Set = True
		self.Add_Button = QT_Button()
		self.Add_Button.setText("Add Item")
		self.Remove_Button = QT_Button()
		self.Remove_Button.setText("Remove Item")

		self.Layout.addWidget(self.Add_Button)
		self.Layout.addWidget(self.Remove_Button)
		self.Layout.addWidget(self.Spreadsheet)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,0)
		self.Layout.setStretch(2,1)

		self.Spreadsheet.cellChanged.connect(self.updateDatabase)
		self.Add_Button.clicked.connect(self.input)
		self.Remove_Button.clicked.connect(self.removal)
		self.Remove_Button.hide()
		self.Add_Button.hide()

	def input(self):
		self.Input = Input_Tool(self.App, self, self.Table_Name, self.Log)

	def removal(self):
		self.Input = Delete_Tool(self.App, self, self.Table_Name, self.Log)

	def updateDatabase(self, row, column):
		if not self.Set:
			DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
			DB_cursor = DB_connector.cursor()
			DB_cursor.execute(f"SELECT * FROM {self.Table_Name}")
			Column_Name = self.Spreadsheet.horizontalHeaderItem(column).text()
			try:
				DB_cursor.execute(f"SELECT data_type FROM information_schema.columns WHERE table_name = '{self.Table_Name}' AND column_name = '{Column_Name}'")
				column_type = DB_cursor.fetchone()[0]
				if column_type == "text":
					DB_cursor.execute(f"UPDATE {self.Table_Name} SET {Column_Name} = '{self.Spreadsheet.item(row,column).text()}' WHERE id = {self.Spreadsheet.item(row,0).text()}")
				else:
					DB_cursor.execute(f"UPDATE {self.Table_Name} SET {Column_Name} = {self.Spreadsheet.item(row,column).text()} WHERE id = {self.Spreadsheet.item(row,0).text()}")
				DB_connector.commit()
			except psycopg2.Error as Error:
				self.Log.append("Error: " + str(Error),"250,50,50")

			DB_connector.close()

	def refresh(self):
		conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		cur = conn.cursor()
		try:
			cur.execute(self.Query)
			conn.commit()
			self.Data = cur.fetchall()
			Coulmn_Labels = [str(desc[0]) for desc in cur.description]
			self.Set = True
			self.Spreadsheet.setColumnCount(len(Coulmn_Labels))
			self.Spreadsheet.setRowCount(len(self.Data))
			self.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)

			for row in range(len(self.Data)):
				for column in range(len(self.Data[0])):
					item = QTableWidgetItem(str(self.Data[row][column]))
					self.Spreadsheet.setItem(row, column, item)

			self.Spreadsheet.resizeColumnsToContents()
			self.Spreadsheet.resizeRowsToContents()
			self.Set = False

		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		cur.close()
		conn.close()

class Source_Editor_Tool(QT_Linear_Contents):
	def __init__(self, Parent, Log):
		super().__init__()
		self.Parent = Parent
		self.Log = Log
		self.Options = QComboBox()
		Save = QT_Button()
		Save.setText("Save current File")
		Restore = QT_Button()
		Restore.setText("Restore from File")
		Wipe = QT_Button()
		Wipe.setText("Wipe database")
		self.Text = QT_Text_Editor()

		self.Options.addItem("DB_Creation_Queries")
		self.Options.addItem("DB_Tree")
		self.Options.addItem("DB_Queries")
		self.Options.addItem("DB_Triggers")

		Header = QT_Linear_Contents(False)

		Header.Layout.addWidget(self.Options)
		Header.Layout.addWidget(Save)
		Header.Layout.addWidget(Restore)
		Header.Layout.addWidget(Wipe)
		Header.Layout.setStretch(0,1)
		Header.Layout.setStretch(1,1)
		Header.Layout.setStretch(2,1)
		Header.Layout.setStretch(3,1)

		self.Layout.addWidget(Header)
		self.Layout.addWidget(self.Text)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,1)

		self.Options.currentTextChanged.connect(self.changeSource)
		Save.clicked.connect(self.save)
		Restore.clicked.connect(self.restore)
		Wipe.clicked.connect(self.wipe)

		self.Path = "./Database/Db_Create.txt"
		self.Text.setPlainText(open(self.Path,"r",encoding="utf-8").read())

	def changeSource(self):
		if self.Options.currentText() == "DB_Creation_Queries":
			self.Path = "./Database/Db_Create.txt"
		elif self.Options.currentText() == "DB_Tree":
			self.Path = "./Database/Db_Tables.txt"
		elif self.Options.currentText() == "DB_Queries":
			self.Path = "./Database/Db_Queries.txt"
		elif self.Options.currentText() == "DB_Triggers":
			self.Path = "./Database/Db_Triggers.txt"
		self.Text.clear()
		self.Text.setPlainText(open(self.Path,"r",encoding="utf-8").read())

	def save(self):
		Confirmation = QT_Confirmation(self,"Are you sure you want to SAVE THE PARAMETERS")
		if Confirmation.exec() == QMessageBox.StandardButton.Yes:
			open(self.Path,"w",encoding="utf-8").write(self.Text.toPlainText())
			self.Log.append("File Saved","50,250,50")
			self.Parent.Outliner.clear()
			self.Parent.Outliner.setTree()
			self.Parent.Premade_Outliner.clear()
			self.Parent.Premade_Outliner.setTree()

	def restore(self):
		Path = QFileDialog.getOpenFileName(self, "Restore from file","./dump.sql")
		if Path != "":
			conn = psycopg2.connect(database=self.Parent.App.DB, user=self.Parent.App.USER, password=self.Parent.App.PASSWORD, host="localhost", port="5432")
			cur = conn.cursor()

			try: cur.execute(open(Path[0], "r",encoding=chardet.detect(open(Path[0], 'rb').read())["encoding"]).read())
			except psycopg2.Error as Error: self.Log.append("Error: " + str(Error),"250,50,50")
			conn.commit()
			cur.close()
			conn.close()
	
	def wipe(self):
		Confirmation = QT_Confirmation(self,"Are you sure you want to WIPE THE DATABASE")
		if Confirmation.exec() == QMessageBox.StandardButton.Yes:
			conn = psycopg2.connect(user=self.Parent.App.USER, password=self.Parent.App.PASSWORD)
			cursor = conn.cursor()

			autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
			conn.set_isolation_level( autocommit )

			try: cursor.execute(f"DROP DATABASE {self.Parent.App.DB}")
			except psycopg2.Error as Error: print(Error)
			conn.commit()
			cursor.close()
			conn.close()
			self.Parent.restart()