import json
import FortigateApi
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash
import Fortigate_Requests
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
    return render_template('New_Customer.html', title='New Customer')


@app.route("/new/wizard", methods=['GET', 'POST'])
def nc_w_template():
    # declarations

    form = NewCustomerWizardForm()
    FGT_Root = "192.168.136.129"
    FGT_Vdom = "192.168.1.83"
    admin_name = str(form.vdom_name.data) + "_admin"
    fw = FortigateApi.Fortigate(FGT_Root, "root", "PFE", "pfepfe")
    fw_vdom = FortigateApi.Fortigate(FGT_Root, form.vdom_name.data, "PFE", "pfepfe")
    ip_lan_mask = str(form.ip_adresse_lan.data) + " " + str(form.masque_lan)
    ip_lan_mask_2 = str(form.ip_adresse_lan.data) + "/24"
    ip_wan_mask = str(form.ip_adresse_wan.data) + " " + str(form.masque_wan)
    rfc_1 = "10.0.0.0/8"
    rfc_2 = "172.16.0.0/12"
    rfc_3 = "192.168.0.0/16"
    ippool_name = str(form.vdom_name.data) + "_IPPool"

    """if form.vlan_id_lan.data:
        flash("data retrieved = " + form.vlan_id_lan.data)
    if form.https_access_lan.data:
        flash('https access')"""
    # trucs
    if form.validate_on_submit():
        flash(Fortigate_Requests.Create_vdom_with_param(form.vdom_name.data, fw))
        flash(Fortigate_Requests.create_admin_local_profil(form.vdom_name.data, fw, admin_name, 'testtest'))
        flash(Fortigate_Requests.create_and_associate_interface_vlan_to_vdom(form.vdom_name.data, fw, 'LAN', 'AGG',
                                                                             form.vlan_id_lan.data,
                                                                             ip_lan_mask, 'https ssh ping'))
        flash(Fortigate_Requests.create_and_associate_interface_vlan_to_vdom(form.vdom_name.data, fw, 'WAN', 'AGG',
                                                                             ip_wan_mask,
                                                                             form.vlan_id_wan.data, 'https ssh ping'))
        flash(Fortigate_Requests.create_adresse_object(fw_vdom, '192.168.1.254/24'))
        flash(Fortigate_Requests.create_ippool(fw_vdom, form.ip_publique.data, ippool_name, form.vdom_name.data))
        flash(Fortigate_Requests.create_route(fw_vdom, rfc_1, '10.10.10.254', 'LAN', 'auto-generated route'))
        flash(Fortigate_Requests.create_route(fw_vdom, rfc_2, '10.10.10.254', 'LAN', 'auto-generated route'))
        flash(Fortigate_Requests.create_route(fw_vdom, rfc_3, '10.10.10.254', 'LAN', 'auto-generated route'))
        flash(
            Fortigate_Requests.create_route(fw_vdom, '0.0.0.0 0.0.0.0', '20.20.20.254', 'WAN', 'auto-generated route'))
        flash(Fortigate_Requests.create_policy(fw_vdom, 'LAN', 'WAN', ip_lan_mask, 'enable', 'enable', ippool_name,
                                               'auto-generated policy'))

    return render_template('wizard_Customer.html', title='Add Customer With Wizard', form=form)


@app.route("/new/custom")
def nc_customised():
    return render_template('custom_Customer.html', title='add customer')


if __name__ == '__main__':
    app.run()
