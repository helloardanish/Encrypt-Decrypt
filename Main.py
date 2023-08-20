from PyQt6.QtCore import (QDate,Qt)

from ExcelData import ExcelData

import openpyxl

from PyQt6.QtWidgets import ( 
    QMainWindow,
    QDateEdit, 
    QVBoxLayout, 
    QWidget,
    QPushButton,
    QDialog,
    QLabel,
    QMessageBox,
    QComboBox,
    QLineEdit
    )



class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Individual Settlement")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Create the date input widget
        #self.date_edit = QDateEdit(self)
        self.date_edit = QDateEdit(QDate.currentDate(), self)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")  # Set the date format
        layout.addWidget(self.date_edit)

        # Create the number dropdown from 1 to 100
        self.number_dropdown = QComboBox(self)
        self.number_dropdown.setMaximumHeight(15)  # Adjust the dropdown height
        for i in range(1, 101):
            self.number_dropdown.addItem(str(i))
        self.number_dropdown.setCurrentIndex(2)
        layout.addWidget(self.number_dropdown)


        # Create the cab fill button
        self.ok_button = QPushButton("Start Cab Fill", self)
        self.ok_button.clicked.connect(self.open_cab_booked_window)
        layout.addWidget(self.ok_button)

        # Create the da button button
        self.da_button = QPushButton("Start DA Fill", self)
        self.da_button.clicked.connect(self.open_da_fill_window)
        layout.addWidget(self.da_button)

        # Create the Submit button
        self.count_days = QPushButton("Count Days", self)
        self.count_days.clicked.connect(self.open_count_days_window)
        layout.addWidget(self.count_days)
        

        # Create the Close Window button
        close_button = QPushButton("Close Window", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Center the main window
        #self.center_window()

    
    def open_da_fill_window(self):
        selected_number = int(self.number_dropdown.currentText())*2
        #selected_date = self.date_edit.date().toString("dd/MM/yyyy")
        selected_date_d = self.date_edit.date()
        new_window = DABillWindow(selected_date_d)
        result = new_window.exec()
        #new_window.loop_show()




        
    def on_submit(self):
        selected_date = self.date_edit.date().toString("dd/MM/yyyy")
        selected_number = int(self.number_dropdown.currentText())
        print(f"Selected date: {selected_date}")
        print(f"Selected number: {selected_number}")

    def open_cab_booked_window(self):
        selected_number = int(self.number_dropdown.currentText())*2
        #selected_date = self.date_edit.date().toString("dd/MM/yyyy")
        selected_date_d = self.date_edit.date()
        new_window = CabBookedWindow(selected_number, selected_date_d)
        result = new_window.exec()
        #new_window.loop_show()

        if result == QMessageBox.StandardButton.Yes:
            print("User clicked Yes.")
        elif result == QMessageBox.StandardButton.No:
            print("User clicked No.")

    def open_count_days_window(self):
        new_window = NoOfDaysWindow()
        result = new_window.exec()
        #new_window.loop_show()

        if result == QMessageBox.StandardButton.Yes:
            print("User clicked Yes.")
        elif result == QMessageBox.StandardButton.No:
            print("User clicked No.")


class DABillWindow(QDialog):
    def __init__(self, inputfromsecondscreen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DA Fill")
        self.setGeometry(200, 200, 400, 400)
        
        self.setList = ["1st","2nd", "3rd","4th","5th","6th","7th","8th","9th","10th"]

        #self.accept()
        #self.reject()

        self.totalNoOfSet = 3
        self.noOfSet = 0
        
        
        self.finalDADBillsLst=[]

        layout = QVBoxLayout()

        #self.date_edit.setDate(self.date_edit.date().addDays(1))

        self.cabbookedlabel = QLabel(f"Start DA")
        layout.addWidget(self.cabbookedlabel)

        # Create the Yes and No buttons
        self.yes_button = QPushButton(f"Start {self.setList[self.noOfSet]} Set", self)
        self.yes_button.clicked.connect(self.loop_yes_show)
        layout.addWidget(self.yes_button)

        no_button = QPushButton("All set done", self)
        no_button.clicked.connect(self.loop_no_show)
        layout.addWidget(no_button)

        self.setLayout(layout)


    def loop_yes_show(self):
        if self.noOfSet == self.totalNoOfSet:
            for singLst in self.finalDADBillsLst:
                singleSetString = ""
                for data in singLst:
                    if data == singLst[-1]:
                        singleSetString += data
                        continue
                    singleSetString += data
                    singleSetString += "+"

                print(f"Set {self.totalNoOfSet-self.noOfSet+1}"+ " : ", end="")
                print(singleSetString)
                self.noOfSet -= 1
                print("")

            self.accept()
        else:
            self.noOfSet += 1
            self.yes_button.setText(f"Start {self.setList[self.noOfSet]} Set")
            #tempIndex = 10-self.noOfSet
            self.open_da_bill_window()
            
        

    def loop_no_show(self):
        self.reject()
        #self.show()

    def open_da_bill_window(self):
        new3_window = DAAmountWindow(self)
        #self.finalDADBillsLst.append(new3_window.get_one_set_list())
        if new3_window.exec():
            self.finalDADBillsLst.append(new3_window.get_one_set_list())
        else:
            self.finalDADBillsLst.append(new3_window.get_one_set_list())

        #result3 = new3_window.exec()




class CabBookedWindow(QDialog):
    def __init__(self, selected_number, starting_date, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cab Screen")
        self.setGeometry(200, 200, 400, 400)

        self.loop_counter = selected_number - 1
        self.starting_date = starting_date

        self.finalCabDetailsLst=[]

        layout = QVBoxLayout()

        self.count_set = 2
        self.show_date_str = starting_date.toString("dd/MM/yyyy")
        self.mor_eve = "Morning" if not self.loop_counter%2==0 else "Evening"
        self.hotelOrOffice = "Taxi(Hotel to Office)" if not self.loop_counter%2==0 else "Taxi(Office to Hotel)"

        #self.date_edit.setDate(self.date_edit.date().addDays(1))

        self.cabbookedlabel = QLabel(f"Is cab booked on {self.show_date_str} { self.mor_eve}")
        layout.addWidget(self.cabbookedlabel)

        # Create the Yes and No buttons
        yes_button = QPushButton("Yes", self)
        yes_button.clicked.connect(self.on_yes)
        layout.addWidget(yes_button)

        no_button = QPushButton("No", self)
        no_button.clicked.connect(self.on_no)
        layout.addWidget(no_button)

        self.setLayout(layout)


        

    def on_yes(self):
        self.count_set -= 1
        if self.count_set==0:
            self.starting_date = self.starting_date.addDays(1)
            self.count_set = 2
        self.loop_yes_show()
        
    def on_no(self):
        self.count_set -= 1
        if self.count_set==0:
            self.starting_date = self.starting_date.addDays(1)
            self.count_set = 2
        self.loop_no_show()

    def loop_yes_show(self):
        self.show_date_str = self.starting_date.toString("dd/MM/yyyy")
        self.mor_eve = "Morning" if self.loop_counter%2==0 else "Evening"
        self.hotelOrOffice = "Taxi(Hotel to Office)" if not self.loop_counter%2==0 else "Taxi(Office to Hotel)"
        self.loop_counter -= 1
        if self.loop_counter<0:
            self.generate_excel(self.finalCabDetailsLst)
            self.accept()
        else:
            self.open_cab_booked_window()
            self.cabbookedlabel.setText(f"Is cab booked on {self.show_date_str} { self.mor_eve}")
            self.show()

    def loop_no_show(self):
        print(self.loop_counter)
        self.show_date_str = self.starting_date.toString("dd/MM/yyyy")
        self.mor_eve = "Morning" if self.loop_counter%2==0 else "Evening"
        self.hotelOrOffice = "Taxi(Hotel to Office)" if not self.loop_counter%2==0 else "Taxi(Office to Hotel)"
        self.loop_counter -= 1
        if self.loop_counter<0:
            self.generate_excel(self.finalCabDetailsLst)
            self.reject()
        else:
            self.cabbookedlabel.setText(f"Is cab booked on {self.show_date_str} { self.mor_eve}")
            self.show()

    def open_cab_booked_window(self):
        new3_window = CabAmountWindow(self)
        if new3_window.exec():
            input_amount_val = new3_window.get_text_input()
            amount_decimal = "{:.2f}".format(float(input_amount_val))
            row = ExcelData(self.show_date_str, self.hotelOrOffice, amount_decimal, "{:.2f}".format(1), amount_decimal, "Bolt","YES")
            self.finalCabDetailsLst.append(row)
            print(f"User clicked Bolt. Text input value: {input_amount_val}")
        else:
            input_amount_val = new3_window.get_text_input()
            amount_decimal = "{:.2f}".format(float(input_amount_val))
            row = ExcelData(self.show_date_str, self.hotelOrOffice, amount_decimal, "{:.2f}".format(1), amount_decimal, "Uber","YES")
            self.finalCabDetailsLst.append(row)
            print(f"User clicked Uber. Text input value: {input_amount_val}")

        #result3 = new3_window.exec()


    def generate_excel(self, excelDataLst):
        dataofAllRow = []

        for i in range(len(excelDataLst)):
            dataOfRow = []
            if excelDataLst[i].booked=="YES":
                dataOfRow.append(excelDataLst[i].date)
                dataOfRow.append(excelDataLst[i].hotelOffice)
                dataOfRow.append(excelDataLst[i].amount)
                dataOfRow.append(excelDataLst[i].exchRate)
                dataOfRow.append(excelDataLst[i].amountFC)
                dataOfRow.append(excelDataLst[i].remarks)
                #dataOfRow.append(excelDataLst[i].booked)
                
                dataofAllRow.append(dataOfRow)

        self.saveExcel(dataofAllRow)
        
    def saveExcel(self,dataofAllRow):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Add headers to the sheet
        #sheet.append(['Date','Paticulars(From-To)' , 'Amount', 'Exch. Rate', 'Amount(FC)','Remarks(with bill/without bill)', 'Booked'])
        sheet.append(['Date','Paticulars(From-To)' , 'Amount', 'Exch. Rate', 'Amount(FC)','Remarks(with bill/without bill)'])

        # Add sample data rows
        #data = [
         #   ['Alice', 30, 50000.0],
          #  ['Bob', 25, 60000.0],
           # ['Charlie', 35, 55000.0]
        #]

        for row in dataofAllRow:
            sheet.append(row)

        # Save the workbook to a file
        workbook.save('FinalExcel.xlsx')
        print("Excel file generated successfully!")



class CabAmountWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cab Amount Screen")
        self.setGeometry(200, 200, 300, 100)

        self.finalCabDetailsLst = []

        layout = QVBoxLayout()

        label = QLabel("Please enter cab charge ")
        layout.addWidget(label)

        # Add a one-line text input (QLineEdit)
        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        # Create the Yes and No buttons
        yes_button = QPushButton("Bolt", self)
        yes_button.clicked.connect(self.on_yes)
        layout.addWidget(yes_button)

        no_button = QPushButton("Uber", self)
        no_button.clicked.connect(self.on_no)
        layout.addWidget(no_button)

        self.setLayout(layout)

    def on_yes(self):
        self.accept()
        
    def on_no(self):
        self.reject()

    def get_text_input(self):
        return self.text_input.text()


class DAAmountWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DA Amount Screen")
        self.setGeometry(200, 200, 300, 100)

        self.finalDABillsLst = []

        self.counter = 25

        self.continueLoop = True

        layout = QVBoxLayout()

        label = QLabel("Please enter DA Amount ")
        layout.addWidget(label)

        # Add a one-line text input (QLineEdit)
        self.text_input = QLineEdit(self)
        layout.addWidget(self.text_input)

        # Create the Yes and No buttons
        yes_button = QPushButton("Ok", self)
        yes_button.clicked.connect(self.on_yes)
        layout.addWidget(yes_button)

        no_button = QPushButton("Cancel", self)
        no_button.clicked.connect(self.on_no)
        layout.addWidget(no_button)

        self.setLayout(layout)

    def on_yes(self):
        if self.text_input.text() == "":
            print("Please enter some value")
            self.show()

        elif self.continueLoop == False or self.counter == 0:
            totalSum = 0
            for x in self.finalDABillsLst:
                if x == "":
                    print("None found")
                print(x, end=" : ")
                totalSum += int(x)
            print("Total sum : "+str(totalSum))
            self.accept()
        else:
            self.finalDABillsLst.append(self.text_input.text())
            self.text_input.setText("")
            self.counter -= 1
            self.show()
        
    def on_no(self):
        self.continueLoop = False
        totalSum = 0
        #for x in self.finalCabDetailsLst:
            #print(x, end=" : ")

        for x in self.finalDABillsLst:
            if x != '':
                print("Value : "+x)
                totalSum += int(x)
        print("Total sum : "+str(totalSum))
        self.text_input.setText("")
        #self.reject()
        self.accept()

    def get_one_set_list(self):
        return self.finalDABillsLst

    def get_text_input(self):
        return self.text_input.text()



class NoOfDaysWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("No. of Days Calculator")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Create two date input widgets
        self.start_date_edit = QDateEdit(QDate.currentDate(), self) 
        self.start_date_edit.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit(QDate.currentDate(), self)
        self.end_date_edit.setDisplayFormat("dd/MM/yyyy")
        layout.addWidget(self.end_date_edit)

        # Create the Calculate button
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.calculate_days)
        layout.addWidget(self.calculate_button)

        # Create the Close button
        self.close_button = QPushButton("Close Window", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        # Create a label to display the result
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate_days(self):
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        # Calculate the number of days between the two dates
        days = start_date.daysTo(end_date)

        # Update the result label
        self.result_label.setText(f"Number of days: {days}")

        my_key = b'hhjqNbBRyt97gaya_88-v3UvLXlQUNLYjiJfMKn_2p0='

        print(my_key)

        # Create a Fernet cipher with your key
        cipher_suite = Fernet(my_key)

        # The message to encrypt
        message = "I was very obsessed with creating content over social platform.".encode("utf-8")

        # Encrypt the message
        encrypted_text = cipher_suite.encrypt(message)
        print("Encrypted Text:", encrypted_text)

        # Decrypt the message
        decrypted_text = cipher_suite.decrypt(encrypted_text)
        print("Decrypted Text:", decrypted_text.decode("utf-8"))



        # Open the QDialog window above the parent window within the area
        #dialog = CustomDialog(self)
        #parent_geometry = self.geometry()
        #dialog.setGeometry(parent_geometry.left() + 50, parent_geometry.top() + 50, 300, 250)
        #dialog.exec()


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Dialog")
        layout = QVBoxLayout()

        label = QLabel("This is a custom dialog.")
        layout.addWidget(label)

        self.setLayout(layout)

