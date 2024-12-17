from flask import Flask, render_template
import pandas as pd

# Create the Flask app
app = Flask(__name__)

df = pd.read_excel('Output/shows.xlsx')
# Route for the homepage
@app.route('/')
def home():
    # Convert DataFrame to a list of dictionaries for easier use in the template
    events = df.to_dict(orient='records')
    return render_template('index.html', events=events)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


#http://127.0.0.1:5000/