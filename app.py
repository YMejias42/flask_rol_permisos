from flask import Flask, jsonify, redirect, url_for
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'supersecretkey'

principal = Principal(app)

admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if hasattr(identity, 'roles'):
        for role in identity.roles:
            identity.provides.add(RoleNeed(role))

@app.route('/login/<role>')
def login(role):
    identity = Identity(role)
    identity.roles = [role]
    identity_changed.send(app, identity=identity)
    return f'Logueado como {role}'

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return "Bienvenido Admin."

@app.route('/user')
@user_permission.require(http_exception=403)
def user():
    return "Bienvenido Usuario."

@app.route('/')
def index():
    return "Bienvenido a la página principal."

@app.errorhandler(403)
def not_authorized(e):
    return jsonify(error="Acceso no autorizado"), 403

if __name__ == '__main__':
    app.run(debug=True)