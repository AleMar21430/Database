from Qt_Core import *
import sqlite3

class Signin_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App = App

		self.Username = QT_Line_Editor()
		self.Username.setPlaceholderText("Username")
		self.Password = QT_Line_Editor()
		self.Password.setPlaceholderText("Password")
		Signin = QT_Button()
		Signin.setText("Sign in")
		self.Signup = QT_Button()
		self.Signup.setText("Sign up")
		Signin.clicked.connect(self.signIn)
		self.Username.returnPressed.connect(self.signIn)
		self.Password.returnPressed.connect(self.signIn)
		self.Signup.clicked.connect(self.signUp)

		Layout = QT_Linear_Contents()
		Layout.Layout.addWidget(self.Username)
		Layout.Layout.addWidget(self.Password)
		Layout.Layout.addWidget(Signin)
		Layout.Layout.addWidget(self.Signup)

		self.setCentralWidget(Layout)
		self.setWindowTitle("Neuro Chama Signin")
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
		self.show()

	def signIn(self):
		if self.Username.text() != "" and self.Password.text() != "":
			conn = sqlite3.connect("neurochama.db") # psycopg2.connect(database="proyecto2neuro", user="postgres", password="123", host="localhost", port="5432")
			cur = conn.cursor()

			try:
				cur.execute("SELECT * FROM Credenciales")
				rows = cur.fetchall()
			except sqlite3.Error as Error: # except psycopg2.Error
				Toast = QT_Toast(str(Error), self.mapToGlobal(self.Signup.pos()))

			conn.close()
			Success = False

			for Item in rows:
				if self.Username.text() == Item[1] and self.Password.text() == Item[2]:
					Success = True
					Toast = QT_Toast(f"Login with credentials: {Item[1]}  { Item[2]}  {Item[3]}" , self.mapToGlobal(self.Signup.pos()),"50,250,50")
					if Item[3] == "Admin":
						self.App.launchAdmin()
						self.close()
						self.deleteLater()
						self.destroy()
					else:
						self.App.launchUser()
						self.close()
						self.deleteLater()
						self.destroy()
				else:
					Success = False
			if not Success: Toast = QT_Toast("Usuario o Contraseña Incorrectos", self.mapToGlobal(self.Signup.pos()))
		else:
			Toast = QT_Toast("No dejar campos vacios", self.mapToGlobal(self.Signup.pos()))

	def signUp(self):
		self.App.signUp()
		self.close()
		self.deleteLater()
		self.destroy()

