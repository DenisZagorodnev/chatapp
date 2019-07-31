#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:11:13 2019

@author: deniszagorodnev
"""

import mysql.connector

class database_operator():
    
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="129056BF3hero",
            database = 'whatsapp'
            )
        self.cur = self.db.cursor()
        
    def db_exec(self, command):
        self.cur.execute(command)
#        self.field_names = [i[0] for i in self.cur.description]
        
    def lookup(self):
    
        return self.cur.fetchall()

            
    def close(self):
        self.db.close()
        
        
        
        
        
#ex = 'INSERT INTO `whatsapp`.`Users` (`Name`, `Surname`, `Password`, `Status`) VALUES ('Arina', 'Zagorodneva', '67890', 'User');'

#me = '16'
#friend = '2'



#operator = database_operator()
#ex = 'SELECT Time, Message, Sender FROM whatsapp.Dialogs where (Sender = ' + me + ' and Receiver =' + friend + ') or (Sender = ' + friend +  ' and Receiver = ' + me + ');'
#ex = 'INSERT INTO `whatsapp`.`Users` (`Name`, `Surname`, `Password`, `Number`, `Status`) VALUES ('   + str(Name) + ', ' + str(Surname) + ', ' + str(Password) + ', ' + str(Number) + ',\'User\'' + ');'
#operator.db_exec(ex)

#for row in operator.lookup():
 #   print(str(row[0]), row[1], row[2])