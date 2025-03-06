from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem
import json

class SchoolApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 600, 400)
        
        self.stacked_widget = QStackedWidget()
        self.login_page = LoginPage(self.stacked_widget)
        self.registration_page = RegistrationPage(self.stacked_widget)
        self.dashboard = Dashboard(self.stacked_widget)
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.dashboard = self.dashboard
        
        self.setCentralWidget(self.stacked_widget)

class LoginPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter Username:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.role_label = QLabel("Select Role:")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Teacher", "Parent"])
        
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combo)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()
        
        if username and password:
            QMessageBox.information(self, "Login Successful", f"Welcome, {role} {username}!")
            self.stacked_widget.dashboard.update_user_info(username, role)
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter valid credentials.")
    
    def register(self):
        self.stacked_widget.setCurrentIndex(2)

class RegistrationPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Register New Account")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter Password")
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Teacher", "Parent"])
        
        self.register_button = QPushButton("Submit")
        self.register_button.clicked.connect(self.register_user)
        
        layout.addWidget(self.label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_combo)
        layout.addWidget(self.register_button)
        
        self.setLayout(layout)
    
    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()
        
        if username and password:
            QMessageBox.information(self, "Registration Successful", "You can now login!")
            self.stacked_widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Registration Failed", "Please fill in all fields.")

class Dashboard(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()
        self.label = QLabel("User Dashboard")
        self.user_info = QLabel("No user logged in")
        
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(2)
        self.student_table.setHorizontalHeaderLabels(["Student Name", "Attendance (%)"])
        
        self.upload_data_button = QPushButton("Upload Student Data")
        self.mark_attendance_button = QPushButton("Mark Attendance")
        self.logout_button = QPushButton("Logout")
        
        self.upload_data_button.clicked.connect(self.upload_student_data)
        self.mark_attendance_button.clicked.connect(self.mark_attendance)
        self.logout_button.clicked.connect(self.logout)
        
        layout.addWidget(self.label)
        layout.addWidget(self.user_info)
        layout.addWidget(self.student_table)
        layout.addWidget(self.upload_data_button)
        layout.addWidget(self.mark_attendance_button)
        layout.addWidget(self.logout_button)
        
        self.setLayout(layout)
        self.current_role = ""
        self.load_student_data()
    
    def update_user_info(self, username, role):
        self.user_info.setText(f"Logged in as: {role} {username}")
        self.current_role = role
        
        if role == "Teacher":
            self.upload_data_button.show()
            self.mark_attendance_button.show()
        else:
            self.upload_data_button.hide()
            self.mark_attendance_button.hide()
        self.load_student_data()
    
    def upload_student_data(self):
        if self.current_role == "Teacher":
            students = {"Rahul Sharma": "Not Marked", "Priya Verma": "Not Marked", "Amit Kumar": "Not Marked", "Neha Singh": "Not Marked"}
            with open("student_data.json", "w") as f:
                json.dump(students, f)
            self.load_student_data()
            QMessageBox.information(self, "Upload Successful", "Student data uploaded successfully.")
    
    def mark_attendance(self):
        if self.current_role == "Teacher":
            with open("student_data.json", "r+") as f:
                data = json.load(f)
                for student in data.keys():
                    data[student] = "Present"
                f.seek(0)
                json.dump(data, f)
            self.load_student_data()
            QMessageBox.information(self, "Attendance Marked", "All students marked present.")
    
    def load_student_data(self):
        try:
            with open("student_data.json", "r") as f:
                data = json.load(f)
            self.student_table.setRowCount(len(data))
            for row, (student, attendance) in enumerate(data.items()):
                self.student_table.setItem(row, 0, QTableWidgetItem(student))
                self.student_table.setItem(row, 1, QTableWidgetItem(attendance))
        except FileNotFoundError:
            pass
    
    def logout(self):
        self.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication([])
    window = SchoolApp()
    window.show()
    app.exec()
