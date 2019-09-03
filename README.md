# Assessor and property history data to SQLite

Through a partnership, some subsidiaries of USC Price gained access to Corelogic's assessor and history files, as well as, the older assessor and history files of DataQuick (that CoreLogic bought). However, the data were tedious to work with because each of the 4 data sets were scattered among 28GB+ files. The goal of this project was to transfer the data to a database to facilitate its use. In the code herein, I transfer the data from the files into an SQLite database and provide an easy python [app](https://github.com/kiwiPhrases/assessor2sqlite/blob/master/queryDB.py) with which one can query the db. 
