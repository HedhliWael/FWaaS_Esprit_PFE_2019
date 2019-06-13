import json
import FortigateApi, pyfortiapi
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, flash, request
import Fortigate_Requests
from forms import LoginForm, NewCustomerWizardForm, NewCustomerCustomForm, AddCustomerVDOM, AddAdminVDOM, \
    AddVdomInterface, AddVdomIPPool, AddVdomObject, AddVdomRoute, AddVdomPolicy, MigrationForm

app = Flask(__name__)

# app configuration
app.config['SECRET_KEY'] = 'PFE_ESPRIT_2019'
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


@app.route('/test', methods=['GET', 'POST'])
def testing():
    data = "test"
    return render_template('test.html', title='test', data=data)


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
            flash('Login unsuccessful', 'danger')

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


@app.route("/new/custom/vdom", methods=['GET', 'POST'])
def nc_customised_vdom():
    form = AddCustomerVDOM()
    ip_fgt = "192.168.136.129"
    fortigate = FortigateApi.Fortigate(ip_fgt, "root", "PFE", "pfepfe")
    if form.validate_on_submit():
        flash(Fortigate_Requests.c_vdom(form.vdom_name.data, fortigate))
    return render_template('Add_Vdom.html', title='Ajouter Vdom', form=form)


@app.route("/new/custom/admin", methods=['GET', 'POST'])
def nc_customised_admin():
    form = AddAdminVDOM()
    ip_fgt = "192.168.136.129"
    fortigate = FortigateApi.Fortigate(ip_fgt, "root", "PFE", "pfepfe")
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate)]
    if form.submit_admin.data:
        print("VDOM selected = " + str(form.vdom_list.data))
        flash(Fortigate_Requests.c_admin(str(form.vdom_list.data), fortigate, str(form.admin_username.data),
                                         str(form.admin_password.data)))
    return render_template('Add_Vdom_Admin.html', title='Ajouter Admin', form=form)


@app.route("/new/custom/interface", methods=['GET', 'POST'])
def nc_customised_interface():
    form = AddVdomInterface()
    ip_fgt = "192.168.136.129"
    fortigate = FortigateApi.Fortigate(ip_fgt, "root", "PFE", "pfepfe")
    ip_lan_mask = str(form.ip_adresse_lan.data) + " " + str(form.masque_lan.data)
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate)]
    if form.submit_lan.data:
        access = ''
        if form.https_access_lan.data:
            access = access + ' ' + 'https'
        if form.ping_access_lan.data:
            access = access + ' ' + 'ping'
        if form.ssh_access_lan.data:
            access = access + ' ' + 'ssh'
        print("http" + str(form.https_access_lan.data))
        print("access = " + str(access))
        flash(Fortigate_Requests.c_intrf_vlan(str(form.vdom_list.data), fortigate, str(form.intrf_lan_name.data), 'AGG',
                                              str(form.vlan_id_lan.data), str(ip_lan_mask),
                                              allowed_access=" http ping ssh"))

    return render_template('Add_Vdom_Interface.html', title='Ajouter Interface', form=form)


@app.route("/new/custom/ippool", methods=['GET', 'POST'])
def nc_customised_ippool():
    form = AddVdomIPPool()
    ip_fgt = "192.168.136.129"
    fortigate = FortigateApi.Fortigate(ip_fgt, 'root', "PFE", "pfepfe")
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate)]
    if form.submit_pool.data:
        fortigate_vdom = FortigateApi.Fortigate(ip_fgt, str(form.vdom_list.data), "PFE", "pfepfe")
        flash(Fortigate_Requests.c_ippool(fortigate_vdom, str(form.ip_publique.data), str(form.ip_publique_name.data),
                                          str(form.vdom_list.data)))
    return render_template('Add_Vdom_IPPool.html', title='Ajouter IP Pool', form=form)


@app.route("/new/custom/objet", methods=['GET', 'POST'])
def nc_customised_object():
    form = AddVdomObject()
    ip_fgt = "192.168.136.129"
    fortigate = FortigateApi.Fortigate(ip_fgt, 'root', "PFE", "pfepfe")
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate)]
    if form.submit_obj.data:
        fortigate_vdom = FortigateApi.Fortigate(ip_fgt, str(form.vdom_list.data), "PFE", "pfepfe")
        flash(Fortigate_Requests.c_adr_obj(fortigate_vdom, str(form.ojbct_adr.data), str(form.adr_name.data)))

    return render_template('Add_Vdom_Objet.html', title='Ajouter Objet IP', form=form)


@app.route("/new/custom/route", methods=['GET', 'POST'])
def nc_customised_route():
    form = AddVdomRoute()
    fortigate_ip = "192.168.136.129"
    masque_list = ['/8', '/12', '/18', '/20', '/22', '/23', '/24', '/25', '/26', '/27', '/28', '/29', '/30', '/31',
                   '/32']
    fortigate_vdom = FortigateApi.Fortigate(fortigate_ip, 'root', "PFE", "pfepfe")
    form.gw_intrf.choices = [(intrf, str(intrf.split('*')[1])) for intrf in Fortigate_Requests.g_all_vdom_intef()]
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate_vdom)]
    form.dst_masque.choices = [(msq, msq) for msq in masque_list]
    if form.submit_route.data:
        fortigate_vdom = FortigateApi.Fortigate(fortigate_ip, str(form.vdom_list.data), "PFE", "pfepfe")
        print(form.gw_intrf.data.split('*')[1])
        print("selected vdom : " + str(form.vdom_list.data))
        dst_masque = str(form.destination.data) + str(form.dst_masque.data)
        flash(Fortigate_Requests.c_route(2, fortigate_vdom, dst_masque, str(form.gw.data),
                                         str(form.gw_intrf.data.split('*')[1]),
                                         "Added from Custom Vdom Form"))

    return render_template('Add_Vdom_Route.html', title='Ajouter Route', form=form)


@app.route("/new/custom/policy", methods=['GET', 'POST'])
def nc_customised_policy():
    form = AddVdomPolicy()
    fortigate_ip = "192.168.136.129"
    # form.vdom_list.data = "VDOM_11"
    fortigate_root = FortigateApi.Fortigate(fortigate_ip, 'root', "PFE", "pfepfe")
    fortigate_vdom = FortigateApi.Fortigate(fortigate_ip, str(form.vdom_list.data), "PFE", "pfepfe")
    fortigate_pyfortiapi = pyfortiapi.FortiGate(ipaddr=fortigate_ip, username="admin", password="admin",
                                                vdom=str(form.vdom_list.data))
    form.vdom_list.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate_root)]
    form.src_intrf.choices = [(intrf, str(intrf.split('*')[1])) for intrf in Fortigate_Requests.g_all_vdom_intef()]
    form.dst_intrf.choices = [(intrf, str(intrf.split('*')[1])) for intrf in Fortigate_Requests.g_all_vdom_intef()]
    print(form.vdom_list.data)
    form.src_adr.choices = [(adr, str(adr.split('*')[1])) for adr in Fortigate_Requests.g_all_vdoms_adr()]
    form.dst_adr.choices = [(adr, str(adr.split('*')[1])) for adr in Fortigate_Requests.g_all_vdoms_adr()]
    form.services.choices = [(srv, str(srv.split('*')[1])) for srv in Fortigate_Requests.g_all_vdoms_srv()]
    form.nat.choices = [(pool, str(pool.split('*')[1])) for pool in Fortigate_Requests.g_all_vdoms_ippool()]

    if form.submit_pol.data:
        fortigate_root = FortigateApi.Fortigate(fortigate_ip, str(form.vdom_list.data), "PFE", "pfepfe")
        if form.nat_option.data:
            flash(Fortigate_Requests.c_policy(fortigate_root, srcintf=str(form.src_intrf.data.split('*')[1]),
                                              dstintf=str(form.dst_intrf.data.split('*')[1]),
                                              srcaddr=str(form.src_adr.data[0].split('*')[1]),
                                              dstaddr=str(form.dst_adr.data[0].split('*')[1]),
                                              services=str(form.services.data[0].split('*')[1]),
                                              nat='enable', ipool='enable',
                                              poolname=str(form.nat.data.split('*')[1]),
                                              comment='added from flask app'))
        else:
            flash(Fortigate_Requests.c_policy(fortigate_root, srcintf=str(form.src_intrf.data.split('*')[1]),
                                              dstintf=str(form.dst_intrf.data.split('*')[1]),
                                              srcaddr=str(form.src_adr.data[0].split('*')[1]),
                                              dstaddr=str(form.dst_adr.data[0].split('*')[1]), poolname='[]',
                                              ipool='disable', services=str(form.services.data[0].split('*')[1]),
                                              nat='disable', comment='added from flask app'))

    return render_template('Add_Vdom_Policy.html', title='Ajouter Policy', form=form)


@app.route("/new/wizard", methods=['GET', 'POST'])
def nc_w_template():
    # declarations

    form = NewCustomerWizardForm()
    FGT_Root = "192.168.136.129"
    FGT_Vdom = "192.168.1.83"
    admin_name = str(form.vdom_name.data) + "_admin"
    fw = FortigateApi.Fortigate(FGT_Root, "root", "PFE", "pfepfe")
    fw_vdom = FortigateApi.Fortigate(FGT_Root, form.vdom_name.data, "admin", "admin")
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

        flash(Fortigate_Requests.c_route(1, fw_vdom, rfc_1, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(1, fw_vdom, rfc_2, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(1, fw_vdom, rfc_3, ip_lan_mask_2, intrf_lan_name, 'auto-generated route'))
        flash(Fortigate_Requests.c_route(1, fw_vdom, '0.0.0.0 0.0.0.0', ip_wan_mask_2, intrf_wan_name,
                                         'auto-generated route'))

        # Policies

        flash(Fortigate_Requests.c_policy(fw_vdom, srcintf=intrf_lan_name, dstaddr='all', services='ALL',
                                          dstintf=intrf_wan_name, srcaddr=obj_name,
                                          nat='enable', ipool='enable',
                                          poolname=ippool_name, comment='auto-generated policy'))

    return render_template('wizard_Customer.html', title='Add Customer With Wizard', form=form)


@app.route("/new/custom", methods=['GET', 'POST'])
def nc_customised():
    # Declarations
    form = NewCustomerCustomForm()
    form2 = NewCustomerWizardForm()
    FGT_Root = "192.168.136.129"
    FGT_Vdom = "192.168.1.83"
    selected_vdom = "root"
    Dest_masque = str(form.destination.data) + "/24"
    print('------------------ vdom data : ' + str(form.vdom_name.data))
    fw = FortigateApi.Fortigate(FGT_Root, "root", "PFE", "pfepfe")
    fw_vdom = FortigateApi.Fortigate(FGT_Root, str(form.vdom_name.data), "PFE", "pfepfe")
    # fw_vdom = FortigateApi.Fortigate(FGT_Root, 'root', "PFE", "pfepfe")

    Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin",
                                            vdom=str(form.vdom_name.data))
    """Firewall_v2_api2 = pyfortiapi.FortiGate(ipaddr=FGT_Root, username="admin", password="admin",
                                            vdom='root')"""

    # fw_vdom = FortigateApi.Fortigate(FGT_Root, selected_vdom, "PFE", "pfepfe")
    ip_lan_mask = str(form.ip_adresse_lan.data) + " " + str(form.masque_lan.data)
    ip_wan_mask = str(form.ip_adresse_wan.data) + " " + str(form.masque_wan.data)

    # GET POST

    if form.submit_vdom.data:
        flash(Fortigate_Requests.c_vdom(str(form.vdom_name.data), fw))
    if form.submit_admin.data:
        flash(Fortigate_Requests.c_admin(str(form.vdom_name.data), fw, str(form.admin_username.data),
                                         str(form.admin_password.data)))
    if form.submit_lan.data:
        flash(Fortigate_Requests.c_intrf_vlan(str(form.vdom_name.data), fw, str(form.intrf_lan_name.data), 'AGG',
                                              str(form.vlan_id_lan.data), str(ip_lan_mask),
                                              allowed_access=" http ping ssh"))
    if form.submit_wan.data:
        flash(Fortigate_Requests.c_intrf_vlan(str(form.vdom_name.data), fw, str(form.intrf_wan_name.data), 'AGG',
                                              str(form.vlan_id_wan.data), str(ip_wan_mask),
                                              allowed_access=" http ping ssh"))
    if form.submit_pool.data:
        flash(Fortigate_Requests.c_ippool(fw_vdom, str(form.ip_publique.data), str(form.ip_publique_name.data),
                                          str(form.vdom_name.data)))

    form.gw_intrf.choices = [(intrf, intrf) for intrf in Fortigate_Requests.g_intrf_list(fw_vdom)]

    if form.submit_route.data:
        flash(Fortigate_Requests.c_route(2, fw_vdom, Dest_masque, str(form.gw.data), str(form.gw_intrf.data),
                                         "Added from Custom Vdom Form"))

    form.src_intrf.choices = [(intrf, intrf) for intrf in Fortigate_Requests.g_intrf_list(fw_vdom)]
    form.dst_intrf.choices = [(intrf, intrf) for intrf in Fortigate_Requests.g_intrf_list(fw_vdom)]
    form.src_adr.choices = [(adr, adr) for adr in Fortigate_Requests.g_adr_list(Firewall_v2_api2)]
    form.dst_adr.choices = [(adr, adr) for adr in Fortigate_Requests.g_adr_list(Firewall_v2_api2)]
    form.services.choices = [(srv, srv) for srv in Fortigate_Requests.g_srv_list(Firewall_v2_api2)]
    form.nat.choices = [(pool, pool) for pool in Fortigate_Requests.g_ippool_list(fw_vdom)]

    if form.submit_obj.data:
        flash(Fortigate_Requests.c_adr_obj(fw_vdom, str(form.ojbct_adr.data), str(form.adr_name.data)))

    if form.submit_pol.data:

        print(form.nat_option.data)
        print(form.nat.data)
        print(form.src_intrf.data)
        print(form.src_adr.data)
        print(form.services.data)
        print(form.dst_intrf.data)
        print(form.dst_adr.data)
        id = 15
        if form.nat_option.data:
            flash(Fortigate_Requests.c_policy(fw_vdom, srcintf=str(form.src_intrf.data),
                                              dstintf=str(form.dst_intrf.data),
                                              srcaddr=str(form.src_adr.data[0]), dstaddr=str(form.dst_adr.data[0]),
                                              services=str(form.services.data[0]),
                                              nat='enable', ipool='enable',
                                              poolname=str(form.nat.data), comment='added from flask app'))
            """flash(Fortigate_Requests.c_policy_m(fw_vdom,  srcintf=str(form.src_intrf.data),
                                              dstintf=str(form.dst_intrf.data),
                                              srcaddr=form.src_adr.data, dstaddr=form.dst_adr.data,
                                              services=form.services.data,
                                              nat='enable', ipool='enable',
                                              poolname=str(form.nat.data), comment='added from flask app'))"""
        else:
            flash(Fortigate_Requests.c_policy(fw_vdom, srcintf=str(form.src_intrf.data),
                                              dstintf=str(form.dst_intrf.data),
                                              srcaddr=str(form.src_adr.data[0]), dstaddr=str(form.dst_adr.data[0]),
                                              ipool='disable'
                                              , poolname='[]', services=str(form.services.data[0]),
                                              nat='disable', comment='added from flask app'))
            """flash(Fortigate_Requests.c_policy_m(fw_vdom,  srcintf=str(form.src_intrf.data),
                                              dstintf=str(form.dst_intrf.data),
                                              srcaddr=form.src_adr.data, dstaddr=form.dst_adr.data,
                                              ipool='disable'
                                              , poolname='[]', services=form.services.data,
                                              nat='disable', comment='added from flask app'))"""

    return render_template('custom_Customer.html', title='add customer', form=form)


@app.route("/migrate", methods=['GET', 'POST'])
def migrate():
    form = MigrationForm()
    ip_fgt = "192.168.136.129"
    fortigate_root = FortigateApi.Fortigate(ip_fgt, 'root', "PFE", "pfepfe")
    form.vdom_v1.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate_root)]
    form.vdom_v1.default = 'root'
    form.vdom_v2.choices = [(vd, vd) for vd in Fortigate_Requests.g_vdom_list(fortigate_root)]
    form.vdom_v2.default = 'root'
    form.vdom_v1_Interfaces.choices = [(interface, str(interface.split('*')[1])) for interface in
                                       Fortigate_Requests.g_all_vdom_intef()]
    form.vdom_v2_Interfaces.choices = [(interface, str(interface.split('*')[1])) for interface in
                                       Fortigate_Requests.g_all_vdom_intef()]

    if form.submit_param.data:
        print("from web")
        print(form.interface_Mapping.data)
        print(Fortigate_Requests.param_extract(form.interface_Mapping.data))
        print("param 1 : " + str(Fortigate_Requests.param_extract(form.interface_Mapping.data)[0].get('vdom')))
        print("param 2 : " + str(Fortigate_Requests.param_extract(form.interface_Mapping.data)[1].get('vdom')))
        vdom_v1 = Fortigate_Requests.param_extract(form.interface_Mapping.data)[0].get('vdom_v1')
        print('vdom v1 : ' + str(vdom_v1))
        vdom_v2 = Fortigate_Requests.param_extract(form.interface_Mapping.data)[1].get('vdom_v2')
        fortigate_v1 = FortigateApi.Fortigate(ip_fgt, str(vdom_v1), "PFE", "pfepfe")
        fortigate_v2 = FortigateApi.Fortigate(ip_fgt, str(vdom_v2), "PFE", "pfepfe")
        interface_mapping = Fortigate_Requests.param_extract(form.interface_Mapping.data)

        # Importing objects
        fortigate_pyfortiapi = pyfortiapi.FortiGate(ipaddr=ip_fgt, username="admin", password="admin", vdom=vdom_v1)
        for element in Fortigate_Requests.g_objects_elements(fortigate_pyfortiapi):
            Fortigate_Requests.c_adr_obj2(fortigate_v2, element.get('subnet'), element.get('name'))

        # Importing IPPool
        for element in Fortigate_Requests.g_ippool_elements(fortigate_v1):
            Fortigate_Requests.c_ippool(fortigate_v2, element.get('startip'), element.get('name'), vdom_v2)

        # importing Admin accounts / creating new admin
        """for element in Fortigate_Requests.g_admin_accounts_elements(fortigate_v1):
            if element['vdom'] == str(form.vdom_v1.data):
                print('element vdom : ' + str(element['vdom']))
                Fortigate_Requests.c_admin(str(form.vdom_v2.data), fortigate_v2, str(element['name']), '12345678')"""

        flash(
            Fortigate_Requests.c_admin(str(form.vdom_v2.data), fortigate_v2, str("a" + form.vdom_v2.data), '12345678'))

        # importing routes
        masque = {'255.255.255.0': '/24',
                  '255.255.255.128': '/25'
                  }
        mask = masque['255.255.255.0']
        print("hedha el masque mi Dict = " + str(mask))
        for route in Fortigate_Requests.g_routes_elements(fortigate_v1):
            for int_map in interface_mapping:
                if route.get('device') == int_map.get('interface_v1'):
                    device = int_map.get('interface_v2')
                    new_gw = Fortigate_Requests.g_intrf_adr_list(fortigate_v2, int_map.get('interface_v2'))
                    print("new gw = " + new_gw)
                    print("interface v2 = " + str(int_map.get('interface_v2')))

                try:
                    print("dst = " + str(route.get('dst')))
                    print("gw = " + str(new_gw))
                    print("device = " + str(device))
                    print("gw with mask = " + str(new_gw.split()[0]) + str(masque.get(new_gw.split()[1])))
                    gw_mask = str(new_gw.split()[0]) + str(masque.get(new_gw.split()[1]))
                    print("what is this = " + masque.get(new_gw.split()[1]))
                    Fortigate_Requests.c_route(1, fortigate_v2, route.get('dst'), gw_mask, device,
                                               'exported from fortigate v1')
                    break
                except:
                    print('no route to export')

        # Importing Policies
        for policy in Fortigate_Requests.g_policy_elements(fortigate_v1):
            print('pol : ' + str(policy))
            if policy.get('poolname') == '':
                for int_map in interface_mapping:
                    if policy.get('srcintf') == int_map.get('interface_v1'):
                        print('map.get src interface v1 : ', int_map.get('interface_v1'))
                        print('source pol : ' + str(policy.get('srcintf')))
                        srcintf = int_map.get('interface_v2')
                        print('source interface ' + str(srcintf))
                    if policy.get('dstintf') == int_map.get('interface_v1'):
                        print('map.get interface v1 : ', int_map.get('interface_v1'))
                        dstintf = int_map.get('interface_v2')
                        print('destination pol : ' + str(policy.get('dstintf')))
                        print('map.get dst interface v1 : ', int_map.get('interface_v1'))
                        print('Destination interface ' + str(dstintf))

                try:
                    Fortigate_Requests.c_policy(fortigate_v2, srcintf=srcintf, dstintf=dstintf,
                                                srcaddr=policy.get('srcaddr'), dstaddr=policy.get('dstaddr'),
                                                services=policy.get('service'), nat='disable',
                                                poolname=policy.get('poolname'),
                                                comment='migration vdom_v1', ipool='')

                except:
                    print("not today")
            else:
                for int_map in interface_mapping:
                    if policy.get('srcintf') == int_map.get('interface_v1'):
                        print('map.get src interface v1 : ', int_map.get('interface_v1'))
                        print('source pol : ' + str(policy.get('srcintf')))
                        srcintf = int_map.get('interface_v2')
                        print('source interface ' + str(srcintf))
                    if policy.get('dstintf') == int_map.get('interface_v1'):
                        print('map.get interface v1 : ', int_map.get('interface_v1'))
                        dstintf = int_map.get('interface_v2')
                        print('destination pol : ' + str(policy.get('dstintf')))
                        print('map.get dst interface v1 : ', int_map.get('interface_v1'))
                        print('Destination interface ' + str(dstintf))
                        print('******** pool name = ' + str(policy.get('poolname')))

                try:
                    Fortigate_Requests.c_policy(fortigate_v2, srcintf=srcintf, dstintf=dstintf,
                                                srcaddr=policy.get('srcaddr'), dstaddr=policy.get('dstaddr'),
                                                services=policy.get('service'), nat='enable',
                                                poolname=policy.get('poolname'),
                                                comment='migration vdom_v1 with nat enabled',
                                                ipool='enable')
                except:
                    print("not to daaaaayyy")
    form.process()
    return render_template('migration.html', title='Migration', form=form)


if __name__ == '__main__':
    app.run(debug=True)
