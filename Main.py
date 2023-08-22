import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog
from EncryptScreenDialog import EncryptScreenDialog
from DecryptScreenDialog import DecryptScreenDialog 


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encrypt Decrypt")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create a button to open the text editor dialog
        self.open_dialog_button = QPushButton("Encrypt Text", self)
        self.open_dialog_button.clicked.connect(self.open_encrypt_screen)
        layout.addWidget(self.open_dialog_button)

        # Create a button to open the text editor dialog
        self.open_dialog_button = QPushButton("Decrypt Text", self)
        self.open_dialog_button.clicked.connect(self.open_decrypt_screen)
        layout.addWidget(self.open_dialog_button)

        # Create the close window button
        self.close_button = QPushButton("Exit", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        central_widget.setLayout(layout)



    def open_encrypt_screen(self):
        encrypt_window = EncryptScreenDialog(self)
        if encrypt_window.exec():
            print("Encrypt Screen Closed")
        else:
            print("Encrypt Screen Closed Without Operation")

    def open_decrypt_screen(self):
        decrypt_window = DecryptScreenDialog(self)
        if decrypt_window.exec():
            print("Decrypt Screen Closed")
        else:
            print("Decrypt Screen Closed Without Operation")
            

    def open_text_editor_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Text Editor Dialog")

        # Create an instance of TwoTextBoxApp inside the dialog
        text_editor_app = TwoTextBoxApp()
        text_editor_app.setParent(dialog)

        layout = QVBoxLayout()
        layout.addWidget(text_editor_app)

        dialog.setLayout(layout)

        # Show the dialog as a modal dialog
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec())
