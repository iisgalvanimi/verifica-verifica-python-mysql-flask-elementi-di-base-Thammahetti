from flask import Flask, jsonify, request
import mysql.connector
import json
import pymysql
import traceback
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database= "verifica"
)

app = Flask(__name__)
mycursor = mydb.cursor(dictionary=True)
def get_citta():
    mycursor.execute("SELECT * FROM citta")
    rows = mycursor.fetchall()
    return rows

@app.route("/")

def index():
    return "Hello world!"

@app.route("/dati")
def dati():
    data = get_citta()
    return jsonify({'Citta':data})  

@app.route("/aggiungi", methods=['POST'])
def aggiungi():
    try:
        data = request.json

    
        if not data or "Città" not in data or "Paese" not in data or "Popolazione" not in data or "Monumenti_principali" not in data:
            return jsonify({"error": "Dati incompleti"}), 

        citta = data["Città"]
        paese = data["Paese"]
        popolazione = data["Popolazione"]
        monumenti = data["Monumenti_principali"]

        mycursor = mydb.cursor()
        query = "INSERT INTO citta (Città, Paese, Popolazione, Monumenti_principali) VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, (citta, paese, popolazione, monumenti))
        mydb.commit()

        return jsonify({"message": "Inserimento avvenuto con successo"}),

    except mysql.connector.Error as err:
       
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}),  

    except Exception as e:
       
        print(f"Errore durante l'inserimento: {str(e)}")
        traceback.print_exc()  
        return jsonify({"error": "Si è verificato un errore durante l'inserimento"}), 

@app.route("/elimina/<int:id>", methods=['DELETE'])
def elimina(id):
    try:
        mycursor = mydb.cursor()
        print(f"ID ricevuto per l'eliminazione: {id}")
        mycursor.execute("SELECT * FROM citta WHERE ID = %s", (id,))
        citta = mycursor.fetchone()

        if not citta:
            return jsonify({"error": "Città con ID specificato non trovata"}),
        mycursor.execute("DELETE FROM citta WHERE ID = %s", (id,))
        mydb.commit()


        return jsonify({"message": f"Città con ID {id} eliminata con successo"}),

    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}), 

    except Exception as e:
        print(f"Errore durante l'eliminazione: {str(e)}")
        return jsonify({"error": "Si è verificato un errore durante l'eliminazione"}),

if __name__ == "__main__":
    app.run(debug=True)