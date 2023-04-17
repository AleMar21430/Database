from Qt_Core import *
import psycopg2

class Query_Tool(QT_Text_Editor):
	def __init__(self, App, Log: QT_Text_Stream, Output):
		super().__init__()
		self.App = App
		self.Log = Log
		self.Output = Output
		self.setPlaceholderText("Press F5 to run Query")

	def keyPressEvent(self, event: QKeyEvent):
		if event.key() == Qt.Key.Key_F5:
			self.commit()
		else:
			return super().keyPressEvent(event)

	def commit(self):
		if len(self.textCursor().selectedText()) < 1:
			conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
			cur = conn.cursor()
			try: 
				cur.execute(self.toPlainText())
				conn.commit()
				self.Data = cur.fetchall()
				try:
					Coulmn_Labels = [str(desc[0]) for desc in cur.description]
					self.Output.Set = True
					self.Output.Spreadsheet.setColumnCount(len(Coulmn_Labels))
					self.Output.Spreadsheet.setRowCount(len(self.Data))
					self.Output.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)

					for row in range(len(self.Data)):
						for column in range(len(self.Data[0])):
							item = QTableWidgetItem(self.Data[row][column])
							self.Output.Spreadsheet.setItem(row, column, item)

					self.Output.Spreadsheet.resizeColumnsToContents()
					self.Output.Spreadsheet.resizeRowsToContents()
					self.Output.Set = False
					self.Log.append("Query executed succesfully!","150,250,150")
					self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
				except:
					self.Output.refresh()

			except psycopg2.Error as Error: 
				self.Log.append("Error: " + str(Error),"250,50,50")

			cur.close()
			conn.close()
		else:
			conn = psycopg2.connect(database=self.App.DB, user=self.App.USER, password=self.App.PASSWORD, host="localhost", port="5432")
			cur = conn.cursor()
			try: 
				cur.execute(self.textCursor().block().text())
				conn.commit()
				self.Data = cur.fetchall()
				try:
					Coulmn_Labels = [str(desc[0]) for desc in cur.description]
					self.Output.Spreadsheet.setColumnCount(len(Coulmn_Labels))
					self.Output.Spreadsheet.setRowCount(len(self.Data))
					self.Output.Spreadsheet.setHorizontalHeaderLabels(Coulmn_Labels)

					for row in range(len(self.Data)):
						for column in range(len(self.Data[0])):
							item = QTableWidgetItem(self.Data[row][column])
							self.Output.Spreadsheet.setItem(row, column, item)

					self.Output.Spreadsheet.resizeColumnsToContents()
					self.Output.Spreadsheet.resizeRowsToContents()
					self.Log.append("Query Fragment executed succesfully!","150,250,150")
					self.Output.Spreadsheet.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
				except:
					self.Output.refresh()
			except psycopg2.Error as Error: 
				self.Log.append("Error: " + str(Error),"250,50,50")

			cur.close()
			conn.close()