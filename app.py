from flask import Flask, render_template, request, redirect, session, url_for
import pyrebase
import os

app = Flask(__name__)

# Firebase configuration
config = {
    "apiKey": "AIzaSyBtCK_zN-PJ0xBdRRLxZV2fPCeJ4SAPzvU",
    "authDomain": "capture-195ad.firebaseapp.com",
    "projectId": "capture-195ad",
    "storageBucket": "capture-195ad.appspot.com",
    "messagingSenderId": "384469299749",
    "appId": "1:384469299749:web:d939af9015134aa21c05cc",
    "measurementId": "G-P0JXZ8RWGD",
    "databaseURL": "https://capture-195ad-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app.secret_key = os.urandom(24)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin_password'

# Admin login route
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('add_camera'))
        else:
            return render_template('admin.html', message='Invalid credentials')
    return render_template('admin.html', message='')

# Route to add a new camera
@app.route("/add_camera", methods=['GET', 'POST'])
def add_camera():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            brand = request.form['brand']
            model = request.form['model']
            price = request.form['price']
            camera_data = {
                'brand': brand,
                'model': model,
                'price': price,
            }
            db.child('camera').push(camera_data)
            return redirect(url_for('add_camera'))  # Redirect to the add_camera page after adding a camera
        return render_template('add_camera.html')  # Render the add_camera form
    else:
        return redirect(url_for('admin_login'))  # Redirect to admin_login if not logged in

# Home route to display camera data
@app.route("/")
def home():
    # Retrieve camera data from Firebase
    camera_data = db.child('camera').get().val()
    camera_list = list(camera_data.values()) if camera_data else []

    return render_template('home.html', camera=camera_list)  # Pass camera data to the home template

if __name__ == '__main__':
    app.run(debug=True)
