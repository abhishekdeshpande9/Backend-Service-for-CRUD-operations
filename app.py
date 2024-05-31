from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Replace with your PostgreSQL connection details
db_host = "localhost"
db_name = "gate_information_database"
db_user = "user_1"
db_password = "abcd1234"

# Database connection function
def connect_to_db():
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

@app.route('/receive_post', methods=['POST'])
def receive_post():
    try:
        data = request.get_json()

        conn = connect_to_db()
        cursor = conn.cursor()

        # Database insertion
        cursor.execute("INSERT INTO gateway_mapping_components (gateway_srn, p1_board_srn, ble_board_srn, sd_card_batch_srn) VALUES (%s, %s, %s, %s)",
                       (data['gateway_srn'], data['p1_board_srn'], data['ble_board_srn'], data['sd_card_batch_srn']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Data received and inserted successfully"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_data/<int:pk>', methods=['GET'])
def get_data(pk):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Define the SQL query to retrieve specific data by primary key
        query = "SELECT p1_board_srn FROM gateway_mapping_components WHERE gateway_srn = %s;"
        cursor.execute(query, (pk,))

        data = cursor.fetchone()  # Retrieve one row based on the primary key

        if data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, data))
            return jsonify(data_dict), 200
        else:
            return "Data not found", 404
    except Exception as e:
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_all_data/<int:pk>', methods=['GET'])
def get_all_data(pk):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Define the SQL query to retrieve an entire row of data by primary key
        query = "SELECT * FROM gateway_mapping_components WHERE gateway_srn = %s;"
        cursor.execute(query, (pk,))

        data = cursor.fetchone()  # Retrieve one row based on the primary key

        if data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, data))
            return jsonify(data_dict), 200
        else:
            return "Data not found", 404
    except Exception as e:
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
