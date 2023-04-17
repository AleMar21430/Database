from Qt_Core import *
from Query_Tool import *
import os
import psycopg2

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
		item.setExpanded(False)
		self.Log.append(f"{item.Display_Name} | {item.Query} | {item.Database_Name} | {item.Table_Name}","250,250,250")
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
		cur.close()
		conn.close()

	def setTree(self):
		with open("Db_GUI_Create.txt", "r", encoding = "utf-8") as File:
			for Tables in File.read().split("+"):
				Table_Info = []
				for Line in Tables.split("\n"):
					try:
						if Line[0] != "-":
							Table_Info.append(Line)
					except: pass
				for i in range(len(Table_Info)):
					if i == 0:
						Parent = Table_Info[i].split('|')
						exec(f"{Parent[1]} = QT_Tree_Item(self,'{Parent[0]}','SELECT * FROM {Parent[1]}','{Parent[1]}','{Parent[1]}')")
					else:
						Child = Table_Info[i].split('|')
						exec(f"QT_Tree_Item({Parent[1]},'{Child[0]}','SELECT {Child[1]} FROM {Parent[1]}','{Child[1]}','{Parent[1]}')")

class Admin_Outliner_Tool(QT_Tree):
	def __init__(self, App, Log: QT_Text_Stream, Output: "Output_Tool"):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output

		self.setTree()
		self.itemDoubleClicked.connect(self.itemSelect)

	def itemSelect(self, item):
		item.setExpanded(False)
		self.Log.append(f"{item.Display_Name} | {item.Query} | {item.Database_Name} | {item.Table_Name}","250,250,250")
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
		cur.close()
		conn.close()

	def setTree(self):
		with open("Db_GUI_Create.txt", "r", encoding = "utf-8") as File:
			Pre = File.read()
			Pre += '''+Credenciales|credenciales
ID|id
Usuario|usuario
Contraseña|contrasenia
Tipo|tipo
-'''
			for Tables in Pre.split("+"):
				Table_Info = []
				for Line in Tables.split("\n"):
					try:
						if Line[0] != "-":
							Table_Info.append(Line)
					except: pass
				for i in range(len(Table_Info)):
					if i == 0:
						Parent = Table_Info[i].split('|')
						exec(f"{Parent[1]} = QT_Tree_Item(self,'{Parent[0]}','SELECT * FROM {Parent[1]}','{Parent[1]}','{Parent[1]}')")
					else:
						Child = Table_Info[i].split('|')
						exec(f"QT_Tree_Item({Parent[1]},'{Child[0]}','SELECT {Child[1]} FROM {Parent[1]}','{Child[1]}','{Parent[1]}')")

class Premade_Outliner_Tool(QT_Tree):
	def __init__(self, App, Log: QT_Text_Stream, Output: "Output_Tool"):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output

		self.setTree()
		self.itemDoubleClicked.connect(self.itemSelect)

	def itemSelect(self, item:QT_Tree_Item):
		item.setExpanded(False)
		self.Log.append(f"{item.Display_Name} | {item.Query} | {item.Database_Name} | {item.Table_Name}","250,250,250")
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
		cur.close()
		conn.close()

	def setTree(self):
		with open("Db_GUI_Custom.txt", "r", encoding = "utf-8") as File:
			for Tables in File.read().split("+"):
				Table_Info = []
				for Line in Tables.split("\n"):
					try:
						if Line[0] != "-":
							Table_Info.append(Line)
					except: pass
				for i in range(len(Table_Info)):
					if i == 0:
						Parent = Table_Info[i].split('|')
						exec(f"{Parent[1]} = QT_Tree_Item(self,'{Parent[0]}','{Parent[2]}')")
					else:
						Child = Table_Info[i].split('|')
						exec(f"QT_Tree_Item({Parent[1]},'{Child[0]}','{Child[1]}')")

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
		Coulmn_Labels = [str(desc[0]) for desc in DB_cursor.description][1:] # Ignore PK id

		self.Spreadsheet.setColumnCount(len(Coulmn_Labels))
		self.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)
		self.Columns = Coulmn_Labels
		self.Spreadsheet.setRowCount(1)

		DB_connector.close()

		Add_Button = QT_Button()
		Add_Button.setText("Add Item")
		Add_Button.clicked.connect(self.commit)
		Cancel_Button = QT_Button()
		Cancel_Button.setText("Cancel")
		Cancel_Button.clicked.connect(self.quit)

		self.Layout.addWidget(Add_Button)
		self.Layout.addWidget(Cancel_Button)
		self.Layout.addWidget(self.Spreadsheet)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,0)
		self.Layout.setStretch(2,1)

		self.Spreadsheet.resizeColumnsToContents()
		self.Spreadsheet.resizeRowsToContents()

		self.setWindowTitle("Input")
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.showMaximized()

	def commit(self):
		DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
		DB_cursor = DB_connector.cursor()

		Data = []
		for i in range(len(self.Columns)):
			try:
				Data.append(self.Spreadsheet.item(0,i).text())
			except:
				Data.append("Null")

		try:
			Info = [f"'{item}'" for item in Data]
			self.Log.append(f"INSERT INTO {self.Table_Name} ({','.join(self.Columns)}) VALUES ({','.join(Info)})")
			DB_cursor.execute(f"INSERT INTO {self.Table_Name} ({','.join(self.Columns)}) VALUES ({','.join(Info)})")
			DB_connector.commit()
		except psycopg2.Error as Error:
			self.Log.append("Error: " + str(Error),"250,50,50")

		self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

		DB_connector.close()
		self.Output.refresh()
		self.close()
		self.deleteLater()
		self.destroy()
	
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
		Add_Button = QT_Button()
		Add_Button.setText("Add Item")

		self.Layout.addWidget(Add_Button)
		self.Layout.addWidget(self.Spreadsheet)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,1)

		self.Spreadsheet.cellChanged.connect(self.updateDatabase)
		Add_Button.clicked.connect(self.input)

	def input(self):
		self.Input = Input_Tool(self.App, self, self.Table_Name, self.Log)

	def updateDatabase(self, row, column):
		if not self.Set:
			DB_connector = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
			DB_cursor = DB_connector.cursor()

			DB_cursor.execute(f'PRAGMA table_info({self.Table_Name})')
			rows = DB_cursor.fetchall()
			Column_Name = rows[column][1]
			try:
				DB_cursor.execute(f"UPDATE {self.Table_Name} SET {Column_Name} = '{self.Spreadsheet.item(row,column).text()}' WHERE id = {self.Spreadsheet.item(row,0).text()}")
				DB_connector.commit()
				self.Log.append(f"UPDATE {self.Table_Name} SET {Column_Name} = '{self.Spreadsheet.item(row,column).text()}' WHERE id = {self.Spreadsheet.item(row,0).text()}")
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
		Save.setText("Save")
		Wipe = QT_Button()
		Wipe.setText("Wipe")
		self.Text = QT_Text_Editor()

		self.Options.addItem("DB_Creation_Queries")
		self.Options.addItem("DB_Tree")
		self.Options.addItem("DB_Queries")

		Header = QT_Linear_Contents(False)

		Header.Layout.addWidget(self.Options)
		Header.Layout.addWidget(Save)
		Header.Layout.addWidget(Wipe)

		self.Layout.addWidget(Header)
		self.Layout.addWidget(self.Text)
		self.Layout.setStretch(0,0)
		self.Layout.setStretch(1,1)

		self.Options.currentTextChanged.connect(self.changeSource)
		Save.clicked.connect(self.save)
		Wipe.clicked.connect(self.wipe)

		self.Path = "./Db_Create.txt"
		self.Text.setPlainText(open(self.Path,"r",encoding="utf-8").read())

	def changeSource(self):
		if self.Options.currentText() == "DB_Creation_Queries":
			self.Path = "./Db_Create.txt"
		elif self.Options.currentText() == "DB_Tree":
			self.Path = "./Db_GUI_Create.txt"
		elif self.Options.currentText() == "DB_Queries":
			self.Path = "./Db_GUI_Custom.txt"
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
	
	def wipe(self):
		Confirmation = QT_Confirmation(self,"Are you sure you want to WIPE THE DATABASE")
		if Confirmation.exec() == QMessageBox.StandardButton.Yes:
			conn = psycopg2.connect(database=self.Parent.App.DB, user=self.Parent.App.USER, password=self.Parent.App.PASSWORD, host="localhost", port="5432")
			cursor = conn.cursor()
			try: cursor.execute(f"DROP DATABASE {self.Parent.App.DB}")
			except psycopg2.Error as Error: print(Error)
			conn.commit()
			cursor.close()
			conn.close()
			self.Parent.restart()