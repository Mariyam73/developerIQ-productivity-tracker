# --------- DASHBOARD APP ------------------

from flask import Flask, render_template
import pandas as pd
import mysql.connector
import plotly.express as px

app = Flask(__name__)

# Function to fetch data from the MySQL database
def fetch_data():
    # Replace the placeholder values with your actual MySQL connection details
    connection = mysql.connector.connect(
        host="developeriq-rds-instance.clwwb7dx1ngm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Sha887655di!!",
        database="developerIQDB"
    )

    query = "SELECT username, total_commits, total_pull_requests, total_issue_count FROM metrics"
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch the data
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the data as a Pandas DataFrame
    columns = ["Developer", "Commits", "Pulls", "Issues"]
    df = pd.DataFrame(data, columns=columns)
    return df

# Route to get and visualize the plots
@app.route('/')
def plots():
    # Fetch data from the database
    data = fetch_data()

    # Bar Plot
    fig1 = px.bar(data, x='Developer', y=['Commits', 'Pulls', 'Issues'],
                  labels={'value': 'Count', 'variable': 'Metric'},
                  )

    # Pie Chart
    total = data["Commits"].fillna(0) + data["Pulls"].fillna(0) + data["Issues"].fillna(0)
    productivity = data["Commits"].fillna(0) / total.replace(0, 1) * 100

    fig2 = px.pie(data, names='Developer', values=productivity,
                  labels={'value': 'Productivity (%)'})

    # Update layout for better visualization
    fig1.update_layout(barmode='group')
    fig2.update_traces(textposition='inside', textinfo='percent+label')

    # Convert plots to JSON representation
    plot1_json = fig1.to_json()
    plot2_json = fig2.to_json()

    # Return the JSON representation of plots
    return render_template('plots.html', plot1_json=plot1_json, plot2_json=plot2_json)

if __name__ == '__main__':
    app.run(debug=True)
