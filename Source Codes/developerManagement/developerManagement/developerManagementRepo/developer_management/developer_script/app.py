# ------------- DEVELOPERIQ DEVELOPER MANAGEMENT MICROSERVICE -------------------

# Imports
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_DATABASE_HOST'] = 'developeriq-rds-instance.clwwb7dx1ngm.us-east-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sha887655di!!'
app.config['MYSQL_DATABASE_DB'] = 'developerIQDB'

mysql = MySQL(app)

# Endpoint for user registration
@app.route('/register_developer', methods=['POST'])
def register_user():
    data = request.get_json()

    # Check if required fields are present
    required_fields = ['username', 'email', 'role', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Connect to the database
    cur = mysql.get_db().cursor()

    # Check if the username or email is already taken
    cur.execute("SELECT * FROM developers WHERE username = %s OR email = %s", (data['username'], data['email']))
    if cur.fetchone():
        return jsonify({'error': 'Username or email already taken'}), 400

    # Insert the new user into the database
    cur.execute("INSERT INTO developers (username, email, role, description) VALUES (%s, %s, %s, %s)",
                (data['username'], data['email'], data['role'], data['description']))

    # Commit the transaction
    mysql.get_db().commit()

    # Close the database connection
    cur.close()

    return jsonify({'message': 'User registered successfully'}), 201

# Endpoint for getting all users
@app.route('/get_developer', methods=['GET'])
def get_all_users():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM developers")
    users = cur.fetchall()
    cur.close()

    user_list = []
    for user in users:
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3],
            'description': user[4]
        }
        user_list.append(user_data)

    return jsonify({'users': user_list})

# Endpoint for getting a specific user by ID
@app.route('/get_specific_developer/<username>', methods=['GET'])
def get_user_by_id(username):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM developers WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3],
            'description': user[4]
        }
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

# Endpoint for updating a user by ID
@app.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Connect to the database
    cur = mysql.get_db().cursor()

    # Check if the user exists
    cur.execute("SELECT * FROM developers WHERE id = %s", (user_id,))
    existing_user = cur.fetchone()
    if not existing_user:
        cur.close()
        return jsonify({'error': 'User not found'}), 404

    # Update user data
    cur.execute("UPDATE developers SET username = %s, email = %s, role = %s, description = %s WHERE id = %s",
                (data['username'], data['email'], data['role'], data['description'], user_id))

    # Commit the transaction
    mysql.get_db().commit()

    # Close the database connection
    cur.close()

    return jsonify({'message': 'User updated successfully'})

# Endpoint for deleting a user by ID
@app.route('/delete_developer/<username>', methods=['DELETE'])
def delete_user(username):
    # Connect to the database
    cur = mysql.get_db().cursor()

    # Check if the user exists
    cur.execute("SELECT * FROM developers WHERE username = %s", (username,))
    existing_user = cur.fetchone()
    if not existing_user:
        cur.close()
        return jsonify({'error': 'User not found'}), 404

    # Delete the user from the database
    cur.execute("DELETE FROM developers WHERE username = %s", (username,))

    # Commit the transaction
    mysql.get_db().commit()

    # Close the database connection
    cur.close()

    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
