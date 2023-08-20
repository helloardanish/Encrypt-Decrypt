import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QPlainTextEdit, QDialog, QMessageBox
from cryptography.fernet import Fernet
import pyperclip
from KeyManager import my_key  # Import the key



class DecryptScreenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.cipher_suite = Fernet(my_key)

        self.setWindowTitle("Decrypt Text")
        self.setGeometry(100, 100, 400, 800)

        #central_widget = QWidget()
        #self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create the first text box
        self.text_to_be_decrypted = QPlainTextEdit(self)
        self.text_to_be_decrypted.setPlaceholderText("Enter text to decrypt.")
        self.text_to_be_decrypted.setFixedWidth(400)  # Set custom width
        self.text_to_be_decrypted.setFixedHeight(300)  # Set custom height
        self.text_to_be_decrypted.textChanged.connect(self.check_text_limit)  # Connect to custom slot
        layout.addWidget(self.text_to_be_decrypted)


        # Create the button
        self.button = QPushButton("Decrypt", self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        # Create the second text box
        self.text_decrypted = QPlainTextEdit(self)
        self.text_decrypted.setPlaceholderText("Decrypted text will appear here.")
        self.text_decrypted.setFixedWidth(400)  # Set custom width
        self.text_decrypted.setFixedHeight(300)  # Set custom height
        self.text_decrypted.setReadOnly(True)  # Set the text box as non-editable
        layout.addWidget(self.text_decrypted)



        # Create the "Copy to Clipboard" button
        self.copy_button = QPushButton("Copy Decrypted Text", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)


        # Create the close window button
        self.close_button = QPushButton("Close Window", self)
        #self.close_button.clicked.connect(self.close)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        #central_widget.setLayout(layout)

        # Set the text limit (adjust this limit as needed)
        self.text_limit1 = 1000
        self.setLayout(layout)

    def decryptMessage(self, encrypted_text):
        decoded_encoded_encrypted_text = encrypted_text.encode("utf-8")
        #decrypted_text = self.cipher_suite.decrypt(b'encrypted_text').decode("utf-8")
        decrypted_text_bytes = self.cipher_suite.decrypt(decoded_encoded_encrypted_text)
        decrypted_text = decrypted_text_bytes.decode("utf-8")
        return decrypted_text

    def copy_to_clipboard(self):
        text_to_copy = self.text_decrypted.toPlainText()
        if text_to_copy:
            pyperclip.copy(text_to_copy)
            self.show_copy_success_message()

    def show_copy_success_message(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Success")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Text copied to clipboard.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def check_text_limit(self):
        # Get the current text from the QPlainTextEdit
        current_text = self.text_to_be_decrypted.toPlainText()
        
        # Check if the text exceeds the limit
        if len(current_text) > self.text_limit1:
            # Trim the text to the limit
            self.text_to_be_decrypted.setPlainText(current_text[:self.text_limit1])






    def on_button_click(self):
        text1 = self.text_to_be_decrypted.toPlainText()
        #my_key = b'hhjqNbBRyt97gaya_88-v3UvLXlQUNLYjiJfMKn_2p0='
        #cipher_suite = Fernet(my_key)
        #encrypted_text = text1.encode("utf-8")
        #encrypted_text = text1

        #decrypted_text = self.decryptMessage(text1)
        
        #decrypted_text = cipher_suite.decrypt(encrypted_text)
        #self.text_decrypted.setPlainText(decrypted_text.decode("utf-8"))  # Copy text from text_editor1 to text_editor2

        decrypted_text = self.decryptMessage(text1)
        self.text_decrypted.setPlainText(decrypted_text)  # Copy text from text_editor1 to text_editor2


        
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwoTextBoxApp()
    window.show()
    sys.exit(app.exec())

'''