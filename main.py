#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 20:56:57 2019

pyuic5 /Users/deniszagorodnev/untitled1/mainwindow.ui -o /Users/deniszagorodnev/Desktop/Design/design.py

@author: deniszagorodnev
"""

import sys
import design
import design1
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector


#%%
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        
        self.pushButton.clicked.connect(self.get_username) 
        self.pushButton_2.clicked.connect(self.go_start)

    def go_start(self):
        self.cams = start_window() 
        self.cams.show()
        self.close() 
        
    def get_username(self):
       self.listWidget.clear()
       db = mysql.connector.connect(
               host="localhost",
               user="root",
               passwd="129056BF3hero",
               database = 'whatsapp'
               )
       cur = db.cursor()
       Id = self.lineEdit.text()
       cur.execute('SELECT Users.Name, Users.Surname FROM whatsapp.Users where Users.id = ' + Id + ';')
       field_names = [i[0] for i in cur.description]
       
       for row in cur.fetchall():
          name = field_names[0] +  ': ' + row[0]
          self.listWidget.addItem(name)
          sur = field_names[1] +  ': ' + row[1]
          self.listWidget.addItem(sur)
       #num_fields = len(cur.description)
       
       #print(field_names)
       db.close()

class start_window(QtWidgets.QMainWindow, design1.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.go_search)
        self.pushButton_2.clicked.connect(self.close)
        
    def go_search(self):
        #self.close()
        #app = QtWidgets.QApplication(sys.argv)  
        #window = ExampleApp() 
       # window.show() 
        #app.exec_() 
        
        self.cams = ExampleApp() 
        self.cams.show()
        self.close() 
        
    def close(self):
        self.deleteLater()
        
#%%        
def main():
    app = QtWidgets.QApplication(sys.argv)  
    window = start_window() 
    window.show() 
    app.exec_() 
    
if __name__ == '__main__':  
    main()  
    
    