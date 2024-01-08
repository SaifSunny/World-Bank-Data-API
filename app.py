from flask import Flask


app = Flask(__name__)

from routes import wb_blueprint
app.register_blueprint(wb_blueprint, url_prefix='/v1/api')

app.static_folder = 'static'
    

if __name__ == "__main__":
    app.run(debug=True)
