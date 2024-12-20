"""
{
  "Città": "Milano",
  "Paese": "Italia",
  "Popolazione": "2.8 milioni",
  "Monumenti_principali": "Colosseo, Fontana di Trevi"
}

"""

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
            return jsonify({"error": "Dati incompleti"}), 400  # 400 Bad Request

        citta = data["Città"]
        paese = data["Paese"]
        popolazione = data["Popolazione"]
        monumenti = data["Monumenti_principali"]

        mycursor = mydb.cursor()
        query = "INSERT INTO citta (Città, Paese, Popolazione, Monumenti_principali) VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, (citta, paese, popolazione, monumenti))
        mydb.commit()

        return jsonify({"message": "Inserimento avvenuto con successo"}), 200

    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}), 500  # 500 Internal Server Error

    except Exception as e:
        print(f"Errore durante l'inserimento: {str(e)}")
        traceback.print_exc()  # Mostra la traccia completa dell'errore
        return jsonify({"error": "Si è verificato un errore durante l'inserimento"}), 500  # 500 Internal Server Error

    except mysql.connector.Error as err:
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}), 500

    except Exception as e:
        print(f"Errore durante l'inserimento: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Si è verificato un errore durante l'inserimento"}), 500

@app.route("/elimina/<int:id>", methods=['DELETE'])
def elimina(id):
    try:
        # Crea un cursore per eseguire le query
        mycursor = mydb.cursor()

        # Controlla se l'ID esiste nel database prima di tentare di eliminarlo
        mycursor.execute("SELECT * FROM citta WHERE ID = %s", (id,))
        citta = mycursor.fetchone()

        if not citta:
            return jsonify({"error": "Città con ID specificato non trovata"}), 404  # 404 Not Found

        # Esegui la query DELETE
        mycursor.execute("DELETE FROM citta WHERE ID = %s", (id,))
        mydb.commit()

        # Restituisce una risposta di successo con il formato corretto
        return jsonify({"message": f"Città con ID {id} eliminata con successo"}), 200  # 200 OK

    except mysql.connector.Error as err:
        # Cattura errori specifici di MySQL
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}), 500  # 500 Internal Server Error

    except Exception as e:
        # Cattura qualsiasi altro errore
        print(f"Errore durante l'eliminazione: {str(e)}")
        return jsonify({"error": "Si è verificato un errore durante l'eliminazione"}), 500  # 500 Internal Server Error
@app.route("/aggiorna/<int:id>", methods=['PUT'])
def aggiorna(id):
    try:
        # Recupera i dati JSON inviati nella richiesta
        data = request.json

        # Verifica che i dati inviati siano completi
        if not data or "Città" not in data or "Paese" not in data or "Popolazione" not in data or "Monumenti_principali" not in data:
            return jsonify({"error": "Dati incompleti"}), 400  # 400 Bad Request

        # Estrai i valori dei dati
        citta = data["Città"]
        paese = data["Paese"]
        popolazione = data["Popolazione"]
        monumenti = data["Monumenti_principali"]

        # Crea un cursore per eseguire le query
        mycursor = mydb.cursor()

        # Esegui la query per verificare se l'ID esiste
        mycursor.execute("SELECT * FROM citta WHERE ID = %s", (id,))
        citta_esistente = mycursor.fetchone()

        if not citta_esistente:
            return jsonify({"error": "Città non trovata"}), 404  # 404 Not Found

        # Esegui la query di aggiornamento
        query = """
            UPDATE citta
            SET Città = %s, Paese = %s, Popolazione = %s, Monumenti_principali = %s
            WHERE ID = %s
        """
        mycursor.execute(query, (citta, paese, popolazione, monumenti, id))
        mydb.commit()

        # Restituisci una risposta di successo
        return jsonify({"message": "Città aggiornata con successo"}), 200  # 200 OK

    except mysql.connector.Error as err:
        # Gestisci errori MySQL
        print(f"Errore MySQL: {err}")
        return jsonify({"error": f"Errore MySQL: {err}"}), 500  # 500 Internal Server Error

    except Exception as e:
        # Gestisci qualsiasi altro errore
        print(f"Errore durante l'aggiornamento: {str(e)}")
        return jsonify({"error": "Si è verificato un errore durante l'aggiornamento"}), 500  # 500 Internal Server Error
if __name__ == "__main__":
    app.run(debug=True)