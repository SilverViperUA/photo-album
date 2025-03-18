from database import create_app
from auth import auth_bp
from routes import routes_bp
from models import db, User, Photo, Folder  # Використовуємо існуючий db

app = create_app()
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
 
