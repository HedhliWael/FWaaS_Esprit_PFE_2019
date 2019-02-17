import json

from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash
import FortigateApi
from forms import LoginForm, NewCustomerWizardForm

app = Flask(__name__)

# app configuration
app.config['SECRET_KEY'] = 'PFE_2019'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fwaas.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.password}')"


"""admin = User(username='admin', password='admin')
db.create_all()
db.session.add(admin)
db.session.commit()"""


@app.route('/test')
def testing():
    return render_template('test.html', title='test')


@app.route("/about")
def about():
    return render_template('About.html', title='About')


@app.route("/")
@login_required
def home():
    return render_template('Layout.html', title='home page')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        p_admin = User.query.filter_by(username=form.username.data).first()
        if p_admin and form.password.data == p_admin.password:
            login_user(p_admin)
            return redirect(url_for('home'))
        else:
            flash('login Unsuccessful', 'danger')

    return render_template('Login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/new", methods=['GET', 'POST'])
def nc_add():
    return render_template('New_Customer.html', title='new customer')


@app.route("/new/wizard", methods=['GET', 'POST'])
def nc_w_template():
    form = NewCustomerWizardForm()
    if form.vlan_id_lan.data:
        flash("data retrevied = " + form.vlan_id_lan.data)
    if form.https_access_lan.data:
        flash('https access')
    return render_template('wizard_Customer.html', title='add customer with wizard', form=form)


@app.route("/new/custom")
def nc_customised():
    return render_template('custom_Customer.html', title='add customer')


if __name__ == '__main__':
    app.run()
