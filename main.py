#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 20:56:57 2019

pyuic5 /Users/deniszagorodnev/untitled1/mainwindow.ui -o /Users/deniszagorodnev/Desktop/Design/design.py

@author: deniszagorodnev
"""

import sys

import sql
import find_usr
import usr_page
import start_page
import sign_in_page
import usr_info

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu




#%%

#Окошко для поиска пользователя по айди 

class find_usr(QtWidgets.QMainWindow, find_usr.Ui_MainWindow):
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
       Id = self.lineEdit.text()
       operator.db_exec('SELECT Users.Name, Users.Surname FROM whatsapp.Users where Users.id = ' + Id + ';')

       for row in operator.lookup():
          name = operator.field_names[0] +  ': ' + row[0]
          self.listWidget.addItem(name)
          sur = operator.field_names[1] +  ': ' + row[1]
          self.listWidget.addItem(sur)
#%%
          
#Окошко с инфой про юзера
class info_window(QtWidgets.QMainWindow, usr_info.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.save_changes)
        self.label.setText(user_name + ', your ID is ' + identificator)
        self.lineEdit_2.setText(user_name)
        self.lineEdit_3.setText(user_surname)


    def save_changes(self):
      new_name = self.lineEdit_2.text()
      new_surname = self.lineEdit_3.text()
      
      if type(new_name)!=0 and len(new_surname)!=0:
        global user_name
        global user_surname
        user_name = new_name
        user_surname = new_surname
        ex = 'UPDATE `whatsapp`.`Users` SET `Surname` = ' + '\'' +  new_surname + '\'' +  'WHERE (`id` = '   + '\'' +  identificator + '\'' + ');'
        operator.db_exec(ex)
        operator.db.commit()
        
        ex = 'UPDATE `whatsapp`.`Users` SET `Name` = ' + '\'' +  new_name + '\'' +  'WHERE (`id` = '   + '\'' +  identificator + '\'' + ');'
        operator.db_exec(ex)
        operator.db.commit()
        self.cams = start_window() 
        self.cams.show()
        self.close()
        
      else:
        self.cams = info_window() 
        self.cams.show()
        self.close() 

#%%
        
#Окошко стартовое, типа меню
        
class start_window(QtWidgets.QMainWindow, usr_page.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton_2.clicked.connect(self.go_search)
        self.pushButton.clicked.connect(self.logout)
        self.pushButton_3.clicked.connect(self.delete_account)
        self.pushButton_5.clicked.connect(self.manipulate_info)
        self.label.setText("Welcome to homepage, " + user_name + ' ' + user_surname + '!')
      
    def delete_account(self):
           ex = 'DELETE FROM `whatsapp`.`Users` WHERE id = ' + '\'' +  identificator + '\'' + ';'
           operator.db_exec(ex)
           operator.db.commit()
           self.cams = login_window() 
           self.cams.show()
           self.close()
        
    def go_search(self):
        #self.close()
        #app = QtWidgets.QApplication(sys.argv)  
        #window = ExampleApp() 
       # window.show() 
        #app.exec_() 
        
        #Это для открытия нового окна и закрытия старого при запучке функции
        self.cams = find_usr() 
        self.cams.show()
        self.close() 
        
    def logout(self):
        self.cams = login_window() 
        self.cams.show()
        self.close()
        
    def manipulate_info(self):
        self.cams = info_window() 
        self.cams.show()
        self.close()

#%%
class SystemTrayIcon(QSystemTrayIcon):
    def close(self):
        #self.deleteLater()
    
        #скрыть окно
        self.hide()
        #убить запущенный процесс
        #app.exit()
        sys.exit()
        
        
        
    def show_menu(self):
        #window = start_window() 
        #window.show()
        self.cams = login_window() 
        self.cams.show()

    
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.addAction("Exit", self.close)
        menu.addAction("Menu", self.show_menu)
        self.setContextMenu(menu)
   
#%%
        
        
#Окошко для регистрации пользователя        
class sign_in_window(QtWidgets.QMainWindow, sign_in_page.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.go)
        
    def go(self):
       Surname = self.lineEdit.text() 
       Number = self.lineEdit_2.text() 
       Name = self.lineEdit_3.text() 
       Password = self.lineEdit_4.text()
       
       operator.db_exec('select * from whatsapp.Users where Users.Number = ' + str(Number))  
       
       #Пользователь зарегистрирован на этот номер
       if len(operator.lookup()) != 0 and len(Name) != 0 and len (Surname) != 0:
           self.label.setText("User already exists, try another number.")
           self.lineEdit_2.clear()
           
       elif  len(Number) == 0 or len(Name) == 0 or len (Surname) == 0 or len(Password) == 0:
           self.label.setText("Wrong data, check yourself.")
           self.lineEdit_2.clear()
           self.lineEdit_4.clear()
           self.lineEdit.clear()
           self.lineEdit_3.clear()
           
       else:
           
           self.label.setText("Well done!")
           Name = '\'' + Name + '\''
           Surname = '\'' + Surname + '\''
           Number = '\'' + Number + '\''
           Password = '\'' + Password + '\''
           ex = 'INSERT INTO `whatsapp`.`Users` (`Name`, `Surname`, `Password`, `Number`, `Status`) VALUES ('   + str(Name) + ', ' + str(Surname) + ', ' + str(Password) + ', ' + str(Number) + ',\'User\'' + ');'
           operator.db_exec(ex)
           operator.db.commit()
           self.cams = login_window() 
           self.cams.show()
           self.close()
           
       
#%%
    
#Окошко самое первое. С логином и регистрацией.    
class login_window(QtWidgets.QMainWindow, start_page.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.sign_in)
    
    def login(self):
        name = self.lineEdit.text()
        pasw = self.lineEdit_2.text()
        operator.db_exec('SELECT Password FROM whatsapp.Users where id = ' + name + ';')      
        if str(operator.lookup()[0][0]) == str(pasw):
                global user_name
                global user_surname
                global identificator
                
                identificator = name
                operator.db_exec('SELECT Surname FROM whatsapp.Users where id = ' + name + ';')
                surname = operator.lookup()[0][0]
                
                operator.db_exec('SELECT Name FROM whatsapp.Users where id = ' + name + ';')
                name = operator.lookup()[0][0]
                
                user_name = name
                user_surname = surname
                
                self.cams = start_window() 
                self.cams.show()
                self.close()
        else:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
 
    def sign_in(self):
        self.cams = sign_in_window() 
        self.cams.show()
        self.close()
        
        
        
#%%        
def main(): 
    global operator
    operator = sql.database_operator()
    

    app = QtWidgets.QApplication(sys.argv)    
    app.setQuitOnLastWindowClosed(False)
    
    trayIcon = SystemTrayIcon(QtGui.QIcon("message.png"))
    trayIcon.show()
    
    window = login_window() 
    window.show() 
    
    app.exec_() 
    #sys.exit(app.exec_())
    #trayIcon.exit()
    operator.close()
    return None
    
    
if __name__ == '__main__':  
    main()
    
    #Почему здесь не прерывает?
    