import mysql.connector
import json


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="verifica"  #
)


def carica_dati_json():

        with open('citta.json', 'r') as f:
            dati = json.load(f)

     
        mycursor = mydb.cursor()

   
        for record in dati:
            ID = record['ID']
            città = record['Città']
            paese = record['Paese']
            popolazione = record['Popolazione']
            monumenti = record['Monumenti principali']

          
            mycursor.execute("""
                INSERT INTO citta (ID, Città, Paese, Popolazione, Monumenti_principali)
                VALUES (%s, %s, %s, %s, %s)
            """, (ID, città, paese, popolazione, monumenti))

      
        mydb.commit()
        print("Dati caricati con successo!")
        
 
        mycursor.close()
    
 


if __name__ == '__main__':
    carica_dati_json()