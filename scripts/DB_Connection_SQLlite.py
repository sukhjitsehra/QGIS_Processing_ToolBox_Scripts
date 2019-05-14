##[Sehra]=group
from PyQt4.QtSql import *
db = QSqlDatabase('QPSQL')
if db.isValid():
    # string
    db.setHostName('localhost')
    # string
    db.setDatabaseName('here')
    # string
    db.setUserName('postgres')
    # string
    db.setPassword('a')
    # integer e.g. 5432
    db.setPort('5432')
    if db.open():
        # assume you have a table called 'users'
        query = db.exec_("""select * from users""")
        # iterate over the rows
        while query.next(): 
            record = query.record()
            # print the value of the first column
            print record.value(0) 