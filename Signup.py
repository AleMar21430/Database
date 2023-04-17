from Qt_Core import *
import sqlite3

class Signup_Window(QT_Window):
	def __init__(self, App):
		super().__init__()
		self.App = App

		self.Username = QT_Line_Editor()
		self.Username.setPlaceholderText("Username")
		self.Password = QT_Line_Editor()
		self.Password.setPlaceholderText("Password")
		self.Password_Confirm = QT_Line_Editor()
		self.Password_Confirm.setPlaceholderText("Re-enter Password")
		self.Signup = QT_Button()
		self.Signup.setText("Sign up")
		Signin = QT_Button()
		Signin.setText("Return to Sign in")
		Signin.clicked.connect(self.returnToSignIn)
		self.Username.returnPressed.connect(self.signUp)
		self.Password.returnPressed.connect(self.signUp)
		self.Password_Confirm.returnPressed.connect(self.signUp)
		self.Signup.clicked.connect(self.signUp)

		Layout = QT_Linear_Contents()
		Layout.Layout.addWidget(self.Username)
		Layout.Layout.addWidget(self.Password)
		Layout.Layout.addWidget(self.Password_Confirm)
		Layout.Layout.addWidget(Signin)
		Layout.Layout.addWidget(self.Signup)

		self.setCentralWidget(Layout)
		self.setWindowTitle("Neuro Chama Signin")
		self.setWindowIcon(QIcon("Icon.jpg"))
		self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
		self.show()

	def signUp(self):
		if self.Password.text() == self.Password_Confirm.text():
			if self.Username.text() != "" and self.Password.text() != "":
				conn = sqlite3.connect("neurochama.db") # psycopg2.connect(database="proyecto2neuro", user="postgres", password="123", host="localhost", port="5432")
				cur = conn.cursor()
				if self.Username.text() == "21430":
					Tipo = "Admin"
				else:
					Tipo = "User"

				try: cur.execute(f"INSERT INTO Credenciales (usuario,contrasenia,tipo) VALUES (?,?,?)", (self.Username.text(),self.Password.text(),Tipo))
				except sqlite3.Error as Error: # except psycopg2.Error
					Toast = QT_Toast(str(Error), self.mapToGlobal(self.Signup.pos()))
					
					return

				conn.commit()
				conn.close()

				self.App.signIn()
				self.close()
				self.deleteLater()
				self.destroy()
			else:
				Toast = QT_Toast("No dejar campos vacios", self.mapToGlobal(self.Signup.pos()))
		else:
			Toast = QT_Toast("Contraseñas son diferentes", self.mapToGlobal(self.Signup.pos()))

	def returnToSignIn(self):
		self.App.signIn()
		self.close()
		self.deleteLater()
		self.destroy()