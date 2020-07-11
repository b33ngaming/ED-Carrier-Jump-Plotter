1) Dowwnload the systems.csv from https://eddb.io/api
2) I stripped most of the columns from the csv to make the database I would create smaller.  The only columnns needed are the name, x, y, & z columns.  I used https://stackoverflow.com/questions/7588934/how-to-delete-columns-in-a-csv-file as a guide
3) Created a SQLExpress Server, and used the SSMS import flatfile option to import the data.  https://www.microsoft.com/en-us/sql-server/sql-server-downloads
4) The python script is created in Python 3.7, and you will need Pyodc and numpy packages installed as well
5) Edit the python file to add your servername, database, and the start and end systems, and run.  It will take some time, and output a text file with your waypoints

Issues
1) there is no error handling, so you will return null if there is no systems within 500ly, and could cause a perpetual loop.  I should have this sorted soon.
2) There's no plotting around permit locked systems, also could/should be added, but not a p[riority for me at the moment.