import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "verifica"
)
mycursor = mydb.cursor()
tabella_citta = "CREATE TABLE IF NOT EXISTS citta (ID INT PRIMARY KEY  AUTO_INCREMENT,Città VARCHAR(100),Paese VARCHAR(100),Popolazione VARCHAR(50),Monumenti_principali VARCHAR(255));"
    
mycursor.execute(tabella_citta)
print("Tabella 'citta' creata con successo.")
