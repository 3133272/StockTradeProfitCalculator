
# Longkai Zhang 3133272

# standard imports
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, \
    QDialogButtonBox
from PyQt6 import QtCore
from decimal import Decimal

from cffi.model import qualify


class StockTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    - Additional functionality

    '''

    def __init__(self):
        '''
        This method requires substantial updates
        Each of the widgets should be suitably initalized and laid out
        '''
        super().__init__()

        # Code adapted from ChatGPT (Oct 2025)
        # Original idea: create minimize and maximize option
        # implement minimize and maximize option buttons in my application

        self.setWindowFlags(
            QtCore.Qt.WindowType.Window |
            QtCore.Qt.WindowType.WindowMinimizeButtonHint |
            QtCore.Qt.WindowType.WindowMaximizeButtonHint |
            QtCore.Qt.WindowType.WindowCloseButtonHint
        )

        # setting up dictionary of stocks
        self.data = self.make_data()
        # sorting the dictionary of stocks by the keys. The keys at the high level are dates, so we are sorting by date
        self.stocks = sorted(self.data.keys())

        # the following 2 lines of code are for debugging purposee and show you how to access the self.data to get dates and prices
        # print all the dates and close prices for BTC
        print("all the dates and close prices for BTC", self.data['BTC'])
        # print the close price for BTC on 04/29/2013
        print("the close price for BTC on 04/29/2013", self.data['BTC'][QDate(2013, 4, 29)])

        # The data in the file is in the following range
        #  first date in dataset - 29th Apr 2013
        #  last date in dataset - 6th Jul 2021
        # When the calendars load we want to ensure that the default dates selected are within the date range above
        #  we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['BTC'].keys())[-1]  # Accessing the last element of a python list is explained with method 2 on https://www.geeksforgeeks.org/python-how-to-get-the-last-element-of-list/
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        # self.buyCalendarDefaultDate
        # print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)

        # create QLabel for stock purchased
        self.stock_label = QLabel("Select Stock:")
        self.stock_label.setStyleSheet("color: pink; font-size: 14px;")

        # create QComboBox and populate it with a list of stock
        self.stock_combo = QComboBox()
        self.stock_combo.addItems(self.stocks)

        # change the combo box background and text color
        self.stock_combo.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                color: darkblue;
                font-size: 13px;
                padding: 4px;
                border: 1px solid gray;
                border-radius: 5px;
            }
            QComboBox:hover {
                background-color: #e6f2ff;
            }
        """)

        # create QSpinBox to select stock quantity purchased
        self.buy_quantity_label = QLabel("Quantity Purchased:")
        self.buy_quantity_label.setStyleSheet("color: pink; font-size: 14px;")
        self.buy_quantity_spin = QSpinBox()
        self.buy_quantity_spin.setRange(1, 10000)
        self.buy_quantity_spin.setValue(1)


        # create CalendarWidgets for selection of purchase dates
        self.buy_label = QLabel("Purchase Date:")
        self.buy_calendar = QCalendarWidget()

        # create QLabels to show the stock purchase total
        self.purchase_total_label = QLabel("Purchase Total:")

        # --- create QSpin to select quantity Sold ---
        self.sell_quantity_label = QLabel("Quantity Sold:")
        self.sell_quantity_label.setStyleSheet("color: pink; font-size: 14px;")
        self.sell_quantity_spin = QSpinBox()
        self.sell_quantity_spin.setRange(1, 100000)
        self.sell_quantity_spin.setValue(1)
        # create CalendarWidgets for selection of sell dates
        self.sell_label = QLabel("Sell Date:")
        self.sell_calendar = QCalendarWidget()
        # create QLabels to show the stock sell total
        self.sell_total_label = QLabel("Sell Total: ")

        # create QLabels to show the stock profit total
        self.profit_label = QLabel("Profit: ---")
        self.profit_label.setStyleSheet("font-weight: bold;")

        # --- OK / Cancel buttons ---
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )


        #Layout
        # initialize the layout - 6 rows to start

        # row 0 - stock selection
        layout = QGridLayout()
        layout.addWidget(self.stock_label, 0, 0)
        layout.addWidget(self.stock_combo, 0, 1)
        # row 1 - quantity selection
        layout.addWidget(self.buy_quantity_label, 1, 0)
        layout.addWidget(self.buy_quantity_spin, 1, 1)
        # row 2 - purchase date selection
        layout.addWidget(self.buy_label, 2, 0)
        layout.addWidget(self.buy_calendar, 2, 1)
        # row 3 - display purchase total
        layout.addWidget(self.purchase_total_label, 3, 0, 1, 2)
        # row 4 - display sell quantity
        layout.addWidget(self.sell_quantity_label, 4, 0 )
        layout.addWidget(self.sell_quantity_spin, 4,1)
        # row 5 - sell date selection
        layout.addWidget(self.sell_label, 5, 0)
        layout.addWidget(self.sell_calendar, 5, 1)
        # row 6 - display sell total
        layout.addWidget(self.sell_total_label, 6, 0, 1, 2)
        # row 7 - display sell total
        layout.addWidget(self.profit_label, 7, 0, 1, 2)
        # row 8 - display buttons
        layout.addWidget(self.button_box, 8, 0, 1, 2)

        # set the calendar values
        # purchase: two weeks before most recent
        # sell: most recent

        # connecting signals to slots to that a change in one control updates the UI
        # --- Connect signals to update automatically ---
        self.stock_combo.currentTextChanged.connect(self.updateUi)
        self.buy_quantity_spin.valueChanged.connect(self.updateUi)
        self.buy_calendar.selectionChanged.connect(self.updateUi)
        self.sell_calendar.selectionChanged.connect(self.updateUi)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # set the window title
        self.setWindowTitle("Stock Trade Profit Calculator")
        # update the UI
        # Apply the layout to the dialog
        self.setLayout(layout)

        # --- Set default dates (last 2 available) ---
        last_date = sorted(self.data["BTC"].keys())[-1]
        two_weeks_ago = last_date.addDays(-14)
        self.sell_calendar.setSelectedDate(last_date)
        self.buy_calendar.setSelectedDate(two_weeks_ago)

        # Initialize UI
        self.updateUi()




    def updateUi(self):
        '''
        This requires substantial development
        Updates the Ui when control values are changed, should also be called when the app initializes
        :return:
        '''
        try:
            print("")
            # get selected dates from calendars: stock, quantity, buy date, sell date
            stock = self.stock_combo.currentText()
            buy_date = self.buy_calendar.selectedDate()
            sell_date = self.sell_calendar.selectedDate()
            buy_quantity = self.buy_quantity_spin.value()
            sell_quantity = self.sell_quantity_spin.value()

            # Defensive check — make sure dates exist in dataset
            if buy_date not in self.data[stock] or sell_date not in self.data[stock]:
                self.purchase_total_label.setText("Purchase Total: N/A")
                self.sell_total_label.setText("Sell Total: N/A")
                self.profit_label.setText("Profit: N/A")
                return

            # Get close prices
            buy_price = self.data[stock][buy_date]
            sell_price = self.data[stock][sell_date]

            # Compute totals
            purchase_total = buy_price * buy_quantity
            sell_total = sell_price * sell_quantity
            profit = sell_total - purchase_total

            # Update labels
            self.purchase_total_label.setText(f"Purchase Total: ${purchase_total:,.2f}")
            self.sell_total_label.setText(f"Sell Total: ${sell_total:,.2f}")

            # Change profit color dynamically
            if profit >= 0:
                color = "darkgreen"
            else:
                color = "red"
            self.profit_label.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold;")
            self.profit_label.setText(f"Profit: ${profit:,.8f}")

        except Exception as e:
            print(e)

################ YOU DO NOT HAVE TO EDIT CODE BELOW THIS POINT  ########################################################

    def make_data(self):
        '''
        This code is complete
        Data source is derived from https://www.kaggle.com/camnugent/sandp500/download but use the provided file to avoid confusion

        Converts a CSV file to a dictonary fo dictionaries like

            Stock   -> Date      -> Close
            AAL     -> 08/02/2013 -> 14.75
                    -> 11/02/2013 -> 14.46
                    ...
            AAPL    -> 08/02/2013 -> 67.85
                    -> 11/02/2013 -> 65.56

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        '''

        # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        # put our stock data here
        file = open("combined.csv", "r")  
        data = {}  # empty data dictionary
        file_rows = []  # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            file_rows.append(row.strip())  # https://www.geeksforgeeks.org/python-string-strip-2/
        print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        print("len(stocks):" + str(len(stocks)))
        print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            # include error handling code if close price is incorrect
            data[stock][date] = float(close_price)
        print("len(data):", len(data))
        return data

    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list

# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    currency_converter = StockTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec())