from app import create_app

app = create_app()
app.static_folder = 'static'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # app.run(host="192.168.0.242", debug=True, port=8000)
