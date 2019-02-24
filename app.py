import json
import FortigateApi
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, request
import Fortigate_Requests
from forms import LoginForm, NewCustomerWizardForm, NewCustomerCustomForm

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


@app.route("/result_nc_template", methods=['GET', 'POST'])
def result():
    return render_template('result.html', title='Contacting device')


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
    ip_lan_mask = str(form.ip_adresse_lan.data) + " " + str(form.masque_lan.data)
    ip_lan_mask_2 = str(form.ip_adresse_lan.data) + "/24"
    ip_wan_mask_2 = str(form.ip_adresse_wan.data) + "/24"
    ip_wan_mask = str(form.ip_adresse_wan.data) + " " + str(form.masque_wan.data)
    rfc_1 = "10.0.0.0/8"
    rfc_1_f = "10.0.0.0 255.0.0.0"
    rfc_2 = "172.16.0.0/12"
    rfc_3 = "192.168.0.0/16"
    ippool_name = str(form.vdom_name.data) + "_IPPool"
    obj_name = ip_lan_mask + "_LAN"
    intrf_lan_name = str(form.vdom_name.data) + "_LAN"
    intrf_wan_name = str(form.vdom_name.data) + "_WAN"

    # trucs
    if form.validate_on_submit():
        # Vdom

        flash(Fortigate_Requests.c_vdom(form.vdom_name.data, fw))

        # Admin profil

        flash(Fortigate_Requests.c_admin(form.vdom_name.data, fw, admin_name, 'testtest'))

        # Interfaces

        flash(Fortigate_Requests.c_intrf_vlan(str(form.vdom_name.data), fw,
                                              intrf_lan_name, 'AGG',
                                              str(form.vlan_id_lan.data),
                                              str(ip_lan_mask), 'https ssh ping'))

        flash(Fortigate_Requests.c_intrf_vlan(str(form.vdom_name.data), fw,
                                              intrf_wan_name, 'AGG',
                                              str(form.vlan_id_wan.data),
                                              str(ip_wan_mask), 'https ssh ping'))
        # Address Object

        flash(Fortigate_Requests.c_adr_obj(fw_vdom, str(ip_lan_mask_2), obj_name))

        # IP Pool

        flash(Fortigate_Requests.c_ippool(fw_vdom, form.ip_publique.data, ippool_name, form.vdom_name.data))

        # Routes

        flash(Fortigate_Requests.c_route(fw_vdom, rfc_1, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(fw_vdom, rfc_2, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(fw_vdom, rfc_3, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(fw_vdom, '0.0.0.0 0.0.0.0', ip_wan_mask_2, intrf_wan_name,
                                         'auto-generated route'))

        # Policies

        flash(Fortigate_Requests.c_policy(fw_vdom, intrf_lan_name, intrf_wan_name, obj_name, 'enable', 'enable',
                                          ippool_name, 'auto-generated policy'))

    return render_template('wizard_Customer.html', title='Add Customer With Wizard', form=form)


@app.route("/new/custom")
def nc_customised():
    form = NewCustomerCustomForm()
    return render_template('custom_Customer.html', title='add customer', form=form)


if __name__ == '__main__':
    app.run()
