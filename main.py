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
import dialog
import time
from threading import Thread
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu



#%%

global friend
global me

friend = None
me = None
def show_dialog_2(wdt, friend, me): 
    
    if me != None and friend != None:
        time.sleep(1)
        wdt.clear()
        ex = 'SELECT Time, Message, Sender FROM whatsapp.Dialogs where (Sender = ' + me + ' and Receiver =' + friend + ') or (Sender = ' + friend +  ' and Receiver = ' + me + ');'
        operator.db_exec(ex)
        for row in operator.lookup():   
                 if str(row[2]) == me:
                     msg = str(row[0]) + '           ' + 'You: ' + row[1]    
                 else: 
                     msg = str(row[0]) + '           ' + 'Opponent: ' + row[1]
                     
                 wdt.addItem(msg)

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
        self.pushButton_4.clicked.connect(self.go_chat)
        self.label.setText("Welcome to homepage, " + user_name + ' ' + user_surname + '!')
      
    def go_chat(self):
        self.cams = dialog_window() 
        self.cams.show()
        self.close()
        
        
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
        
#Окошко для чатика
class dialog_window(QtWidgets.QMainWindow, dialog.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.pushButton.clicked.connect(self.go_back)
        self.pushButton_2.clicked.connect(self.collect_data)
        self.pushButton_3.clicked.connect(self.send_msg)
        #self.pushButton_3.clicked.connect(self.test_connect)
        
        self.me = None
        self.friend = None
        
        self.test_list = []
        self.test_time_list = []
        self.test_status_list = []
        
        self.stop_thread = False
        
        
        #QtCore.QTimer.singleShot(3000, self.show_dialog)
        #self.checkThreadTimer = QtCore.QTimer(self)
        #self.checkThreadTimer.setInterval(500)
        #self.checkThreadTimer.timeout.connect(self.show_dialog)


    def go_back(self):
        self.cams = start_window() 
        self.cams.show()
        self.close()
        self.stop_thread = True
        self.thread.join()
        #self.thread._Thread_stop_()
       
    
    def collect_data(self):

        me = identificator
        self.me = str(me)
        self.friend = str(self.lineEdit_2.text())
        #self.show_dialog(self.me, self.friend)
        self.thread = Thread(target = self.show_dialog, args = (self.friend, self.me))
        self.thread.start()
        #thread.join()
        
    def test_connect(self):
        
        me = '16'
        friend = '2'   
        self.listWidget.clear()
        ex = 'SELECT Time, Message, Sender FROM whatsapp.Dialogs where (Sender = ' + me + ' and Receiver =' + friend + ') or (Sender = ' + friend +  ' and Receiver = ' + me + ');'
        #ex = 'INSERT INTO `whatsapp`.`Users` (`Name`, `Surname`, `Password`, `Number`, `Status`) VALUES ('   + str(Name) + ', ' + str(Surname) + ', ' + str(Password) + ', ' + str(Number) + ',\'User\'' + ');'
        self.operator.db_exec(ex)
        for row in self.operator.lookup():  
            msg = str(row[0]) + '           ' + 'You: ' + row[1]
            self.listWidget.addItem(msg)
        
        
        
        
        
    def show_dialog(self, friend, me): 
      
      if me != None and friend != None:
          while(True):
            #self.listWidget.scrollToBottom()
            operator = sql.database_operator()
            time.sleep(1)
            #self.listWidget.clear()
            ex = 'SELECT Time, Message, Sender FROM whatsapp.Dialogs where (Sender = ' + me + ' and Receiver =' + friend + ') or (Sender = ' + friend +  ' and Receiver = ' + me + ');'
            operator.db_exec(ex)
            
            arr = np.array(operator.lookup())
            #operator.db.commit()
            if len(arr) != 0:

                cur_list = list(arr[:,1])
                
                diff = len(cur_list) - len(self.test_list)
                
                
                if diff > 0:
                    new_msgs = list(cur_list[-diff:])
                    
                    
                    
                    cur_time_list = list(arr[:,0])
                    for i in range (len(cur_time_list)):
                        cur_time_list[i] = str(cur_time_list[i])
                        
                    new_times = list(cur_time_list[-diff:])
                    
                    cur_status_list = list(arr[:,2])
                    new_statuses = list(cur_status_list[-diff:])
                    
                    for i in range(len(new_msgs)):   
                             if str(new_statuses[i]) == me:
                                 msg = str(new_times[i]) + '           ' + 'You: ' + new_msgs[i]    
                             else: 
                                 msg = str(new_times[i]) + '           ' + 'Opponent: ' + new_msgs[i]
                              
                             self.listWidget.addItem(msg)
                        
                    self.test_list = cur_list
                    self.test_time_list = cur_time_list
                    self.test_status_list = cur_status_list
                    if self.stop_thread:
                        break
                self.listWidget.scrollToBottom() 
            #else:
              # self.listWidget.addItem('Нou have not started a dialogue with this person!') 
            operator.close()
          #self.show_dialog(self.friend, self.me)           
            #time.sleep(5)       
            #self.show_dialog(self.friend, self.me)
            

         
    def send_msg(self):

        msg = str(self.lineEdit.text())
        if len(msg) != 0:
            operator_2 = sql.database_operator()
            msg = '\'' + msg + '\''
            me = '\'' + self.me + '\''
            friend = '\'' + self.friend + '\''
            ex = 'INSERT INTO `whatsapp`.`Dialogs` (`Message`, `Sender`, `Receiver`) VALUES ('   + str(msg)  + ', ' + str(me)  + ', ' + str(friend) +  ');'
            operator_2.db_exec(ex)
            operator_2.db.commit()
            #self.show_dialog(self.friend, self.me)
            self.lineEdit.clear()
            operator_2.close()
       




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

    