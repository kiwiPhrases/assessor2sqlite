"""
-there are 2 tables: 1) assessor and 2) history \n
(ie SELECT * FROM history LIMIT 5;)\n
-all column names are lower case and have underscores for spaces\n
(ie SELECT mm_fips_county_name FROM assessor LIMIT 5;)\n
-to aggregate by certain columns, you can use GROUP BY \n
(ie SELECT mm_fips_county_name count(*) as num FROM assessor GROUP BY mm_fips_county_name;)\n
"""

# essentials
import pandas as pd
import time
import os

# database interface/driver
import sqlite3

# paths of data
data_path = "H:/"
dbname = "coreLogic_dataQuick_data_ver2.db"

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
            toSaveCSV(df)
            print("--"*30)
            askAnother = askAgain(input("Would you like to run anoter query? Type y or n: "))
            if askAnother == 'n':
                break
        except Exception as err:
            print("--"*30)
            print(err)
            tryAgain = askAgain(input("\nCorrect error and try again? Type y or n: "))
            print("--"*30)
            if tryAgain == 'y':
                askAnother = 'y'

def queryDB(query, conn):
    start_time = time.time()
    df = pd.read_sql_query(query, conn)
    print("\tthis query took: %.2fseconds " %((start_time - time.time())))
    print("\tsize of file read in:", df.shape)
    
    toPrint = askAgain(input("Want to display first 10 rows of query? Type y or n: "))
    if toPrint == 'y':
        print(df.head(n=10))
    return(df)
    
def toSaveCSV(df):    
    toCSV = askAgain(input("Save query to csv? Type y or n: "))

    if toCSV == 'n':
        return(None)
    
    if toCSV == 'y':
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
    accessDB()
    
if __name__ == '__main__':
    main()    
