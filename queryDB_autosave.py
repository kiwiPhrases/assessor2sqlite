"""
To use queryDB.py, you first have to make sure that:
    1) Python 3+ is installed (preferrably Anaconda)
    2) The paths identifying name and location of database are correct (data_path, dbname)
    
There are 2 tables in the db: 
    1) assessor (ie SELECT * FROM assessor LIMIT 5;)
    2) history (ie SELECT * FROM history LIMIT 5;)
 
Queries:
-all column names are lower case and have underscores for spaces\n
(ie SELECT mm_fips_county_name FROM assessor LIMIT 5;)\n
-to aggregate by certain columns, you can use GROUP BY \n
(ie SELECT mm_fips_county_name count(*) as num FROM assessor GROUP BY mm_fips_county_name;)\n
-assessor and history files are joined via propid so you can load change-of-owner history 
of any property in the data.
(ie SELECT * FROM INNER JOIN assessor WITH history ON assessor.propid=history.propid LIMIT 5;)
-there is also a VIEW on the merger of assessor and history tables
so instead of the above, you can use (ie SELECT * FROM assessorHistory LIMIT 5;)
"""

# essentials
import pandas as pd
import time
import datetime
import os
import threading
import signal

# database interface/driver
import sqlite3

#conn = None
#shutdown = False

# paths of data
data_path = "F:/"
dbname = "coreLogic_dataQuick_data_ver2.db"

# query killing function
#def interrupt(signum, frame):
#    global conn
#    global shutdown
#
#    print("Interrupt requested")
#    if conn:
#        conn.interrupt()

#query function
#query function
def askAgain(response):
    while (response != 'y') & (response != 'n'):
        print("oops, try again...")
        response = input("Type y or n: ")
    return(response)
    
def accessDB(dbfile = dbname):
    dblocation = "/".join([data_path, dbfile])
    print("Presumed location of database file: %s" %dblocation)
    if os.path.exists(dblocation):
        conn =  sqlite3.connect(dblocation)

        print("Connection opened to [%s]" %dbfile)
        repeatQuery(conn)
        conn.close()
        print("\tDB connection closed")
        
    else:
        print("Can't find database file, please check the paths.")
    
def repeatQuery(conn):
    askAnother = 'y'
    while askAnother == 'y':
        try:
            query = input("\nPaste your SQlite query here: ")
            df = queryDB(query, conn)

            tp = datetime.datetime.now()
            when =  "-".join([str(i) for i in [tp.month,tp.day,tp.hour,tp.minute]])
            csvName = 'query'+when+".csv"
            fpath = "/".join([data_path, csvName])
            df.to_csv(fpath)
            askAnother='n'
            #toSaveCSV(df)
            #print("--"*30)
            #askAnother = askAgain(input("Would you like to run another query? Type y or n: "))
            #print("\tyour yesponse:", askAnother)
            #if askAnother == 'n':
            #    break
        except Exception as err:
            print("--"*30)
            print(err)
            tryAgain = askAgain(input("\nCorrect error and try again? Type y or n: "))
            print("--"*30)
            if tryAgain == 'y':
                askAnother = 'y'
            if tryAgain == 'n':
                break

def queryDB(query, conn):
    start_time = time.time()
    df = pd.read_sql_query(query, conn)
    print("\tthis query took: %.2fseconds " %((time.time() - start_time)))
    print("\tsize of file read in:", df.shape)

    #answer = askAgain(input("Want to display first 10 rows of query? Type y or n: "))
    #if (answer == 'y'):
    #    print(df.head(n=10))
    return(df)


def toSaveCSV(df):
    answer = askAgain(input("Save query to csv? Type y or n: "))

    if answer == 'n':
        return(None)
    
    if (answer == 'y'):
        csvName = input("Type CSV file to export to (ie query1.csv): ")
        fpath = "/".join([data_path, csvName])
        print("Saving query in CSV to: %s" %fpath)
        df.to_csv(fpath)
        print("\tfinished saving")
        
def getTableNames(dbfile, lookfor="'table'"):
    #open connection
    conn =  sqlite3.connect("/".join([data_path, dbfile]))
    c = conn.cursor()

    #fetch names
    res = c.execute("SELECT name FROM sqlite_master WHERE type=%s;" %lookfor)
    print(res.fetchall())
    
    #close connection
    conn.close()          
        
def main():

    #global conn
    accessDB()

if __name__ == '__main__':
    #signal.signal(signal.SIGINT, interrupt)

    #mainthread = threading.Thread(target=main)
    #mainthread.start()

    #while mainthread.isAlive():
    #    time.sleep(0.2)
    main()    
