from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Get the current date
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    return render_template('index.html', today_date=today_date)

@app.route('/about')
def about():
    # Get the current date
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    return render_template('about.html', today_date=today_date)

if __name__ == '__main__':
    app.run(debug=True)
