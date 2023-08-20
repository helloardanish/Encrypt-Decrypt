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
        self.close_button = QPushButton("Close Window", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        central_widget.setLayout(layout)



    def open_encrypt_screen(self):
        new3_window = EncryptScreenDialog(self)
        if new3_window.exec():
            print(f"hjdfgj")
        else:
            print(f"bj,bjk")

    def open_decrypt_screen(self):
        new3_window = DecryptScreenDialog(self)
        if new3_window.exec():
            print(f"hjdfgj")
        else:
            print(f"bj,bjk")

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
