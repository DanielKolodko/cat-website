from flask import Flask, render_template
import sqlite3
import os
import random

app = Flask(__name__, static_folder='static')

# Function to create and initialize the database (if it doesn't exist)
def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create the gifs table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gif_path TEXT NOT NULL
        )
    ''')

    # Check if the database already has data to avoid duplicates
    cursor.execute('SELECT COUNT(*) FROM gifs')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Add paths of cat GIFs to the database (make sure to have GIFs in the static/gifs folder)
        gifs = [
            ('static/gifs/cat1.gif',),
            ('static/gifs/cat2.gif',),
            ('static/gifs/cat3.gif',),
            ('static/gifs/cat4.gif',)
        ]
        cursor.executemany('INSERT INTO gifs (gif_path) VALUES (?)', gifs)
        conn.commit()
    
    conn.close()

# Function to get a random cat GIF from the database
def get_random_cat_gif():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Fetch all the GIF paths from the database
    cursor.execute('SELECT gif_path FROM gifs')
    gifs = cursor.fetchall()
    
    conn.close()
    
    # Choose a random GIF from the list
    return random.choice(gifs)[0]

@app.route('/')
def index():
    random_gif = get_random_cat_gif()
    return render_template('index.html', gif_path=random_gif)

if __name__ == '__main__':
    # Create the database and add GIFs (if needed) before running the app
    create_db()
    app.run(debug=True)
