
import sys
import sqlite3
from os.path import dirname, join      
from PyQt5.Qt import *           # PyQt5
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel




class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.current_dir = dirname(__file__)
        self.load_ui()
        
        
    def load_ui(self):
        #os.chdir('F:\Project\Py\Widget_art')
        
        file_path = join(self.current_dir, "./1.ui")
        uic.loadUi(file_path , self)
        self.upd()
        self.B_Add.clicked.connect(self.onClicked_add)
        self.B_del.clicked.connect(self.onClicked_del)
        self.B_upd.clicked.connect(self.onClicked_upd)
        self.B_upd_t.clicked.connect(self.upd)

    
    def onClicked_add(self):
    
        self.w2 = Window_add()
        self.w2.show()
        
    def onClicked_del(self):
        self.w2 = Window_del()
        self.w2.show()

    def onClicked_upd(self):
        
        self.w2 = Window_upd()
        self.w2.show()


    def upd(self):
        
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        res = self.conn.cursor().execute("SELECT * from Заказы ").fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.conn.close()


class Window_add(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dir = dirname(__file__)
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        self.load_ui()
        
        
    def load_ui(self):
        #os.chdir('F:\Project\Py\Widget_art')
        file_path = join(self.current_dir, "./w_add.ui")
        uic.loadUi(file_path , self)

        self.combo.addItem("Выполняется", userData=0)
        self.combo.addItem("Выполнено", userData=1)
        self.btn_ok.clicked.connect(self.onClicked)
        self.btn_no.clicked.connect(self.onClicked_no)

    
    def onClicked_no(self):
        self.close()

    def onClicked(self):
        #self.conn = sqlite3.connect('1.db')
        self.conn.cursor().execute(f'INSERT INTO Заказы (Дата, Колво_товара, Выполнено) values("{self.date.selectedDate().toPyDate()}", {self.col.toPlainText()},{self.combo.currentData()})')
        self.conn.commit()
        self.conn.close()

class Window_upd(QWidget):

    def __init__(self):
        super().__init__()
        
        self.current_dir = dirname(__file__)
        self.load_ui()
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        cur = self.conn.cursor()
        genre = cur.execute('SELECT distinct Код_заказа FROM Заказы').fetchall()
        genre_txt = cur.execute('SELECT distinct Код_заказа FROM Заказы').fetchall()
        for i in range(len(genre_txt)):
            genre[i] = str(genre[i])[1:-2]
            genre_txt[i] = str(genre_txt[i])[1:-2]
            genre[i] = self.tr((genre[i]))
            genre_txt[i] = self.tr(genre_txt[i])
            self.combo_id.addItem(genre_txt[i], userData=genre[i])
        self.conn.close()
        self.combo_id.currentTextChanged.connect(self.set_zn)
        
        
    def set_zn (self):
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        cur = self.conn.cursor()
        date = cur.execute('SELECT Дата FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
        kol = cur.execute('SELECT Колво_товара FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
        cont = cur.execute('SELECT Выполнено FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
        date[0] = str(date[0])[2:-3]
        kol[0] = int(str(kol[0])[1:-2])
        cont[0] = int(str(cont[0])[1:-2])
        print(date, kol, cont)
        self.combo.setCurrentIndex(cont[0])
        self.col.clear()
        self.col.append(str(kol[0]))
        self.date.setSelectedDate(QDate.fromString(date[0], "yyyy-MM-dd"))

    def load_ui(self):
        #os.chdir('F:\Project\Py\Widget_art')
        file_path = join(self.current_dir, "./w_upd.ui")
        uic.loadUi(file_path , self)

        self.combo.addItem("Выполняется", userData=0)
        self.combo.addItem("Выполнено", userData=1)
        self.btn_ok.clicked.connect(self.onClicked)
        self.btn_no.clicked.connect(self.onClicked_no)

    
    def onClicked_no(self):
        self.close()

    def onClicked(self):
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        self.conn.cursor().execute(f'update Заказы set Дата ="{self.date.selectedDate().toPyDate()}" , Колво_товара={self.col.toPlainText()}, Выполнено = {self.combo.currentData()} Where Код_заказа='+self.combo_id.currentData())
        self.conn.commit()
        self.conn.close()

class Window_del(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dir = dirname(__file__)
        self.load_ui()
        self.combo_add()
        self.conn.close()
        self.combo_id.currentTextChanged.connect(self.set_zn)
        
    def combo_add(self):
        self.combo_id.clear()
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        cur = self.conn.cursor()
        genre = cur.execute('SELECT distinct Код_заказа FROM Заказы').fetchall()
        genre_txt = cur.execute('SELECT distinct Код_заказа FROM Заказы').fetchall()
        for i in range(len(genre_txt)):
            genre[i] = str(genre[i])[1:-2]
            genre_txt[i] = str(genre_txt[i])[1:-2]
            genre[i] = self.tr((genre[i]))
            genre_txt[i] = self.tr(genre_txt[i])
            self.combo_id.addItem(genre_txt[i], userData=genre[i])
        
        
    def set_zn (self):
        if self.combo_id.currentData() !=None:
            self.conn = sqlite3.connect(self.current_dir + './1.db')
            cur = self.conn.cursor()
            date = cur.execute('SELECT Дата FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
            kol = cur.execute('SELECT Колво_товара FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
            cont = cur.execute('SELECT Выполнено FROM Заказы where Код_заказа='+self.combo_id.currentData()).fetchall()
            date[0] = str(date[0])[2:-3]
            kol[0] = int(str(kol[0])[1:-2])
            cont[0] = int(str(cont[0])[1:-2])
            print(date, kol, cont)
            self.combo.setCurrentIndex(cont[0])
            self.col.clear()
            self.col.append(str(kol[0]))
            self.date.setSelectedDate(QDate.fromString(date[0], "yyyy-MM-dd"))

    def load_ui(self):
        #os.chdir('F:\Project\Py\Widget_art')
        
        file_path = join(self.current_dir, "./w_upd.ui")
        uic.loadUi(file_path , self)

        self.combo.addItem("Выполняется", userData=0)
        self.combo.addItem("Выполнено", userData=1)
        self.btn_ok.clicked.connect(self.onClicked)
        self.btn_no.clicked.connect(self.onClicked_no)

    
    def onClicked_no(self):
        self.close()

    def onClicked(self):
        self.conn = sqlite3.connect(self.current_dir + './1.db')
        self.conn.cursor().execute(f'delete from Заказы where Код_заказа={self.combo_id.currentData()}')
        self.conn.commit()
        self.conn.close()
        self.combo_add()
        

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
