from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, IPAddress, length, number_range


class LoginForm(FlaskForm):
    username = StringField('Username : ', validators=[DataRequired()])
    password = PasswordField('Password : ', validators=[DataRequired()])
    submit = SubmitField('Login')


class NewCustomerWizardForm(FlaskForm):
    Customer_name = StringField('Customer name : ', validators=[DataRequired()])
    vdom_name = StringField('VDOM name : ', validators=[DataRequired()])
    vlan_id_lan = StringField('VLAN ID ', validators=[DataRequired()])
    ip_adresse_lan = StringField('IP adresse ', validators=[DataRequired()])
    masque_lan = StringField('Masque ', validators=[DataRequired()])
    vlan_id_wan = StringField('VLAN ID', validators=[DataRequired()])
    ip_adresse_wan = StringField('IP adresse ', validators=[DataRequired()])
    masque_wan = StringField('Masque ', validators=[DataRequired()])
    ip_publique = StringField('IP Publique : ', validators=[DataRequired()])
    ssh_access_lan = BooleanField()
    https_access_lan = BooleanField()
    ping_access_lan = BooleanField()
    ssh_access_wan = BooleanField()
    https_access_wan = BooleanField()
    ping_access_Wan = BooleanField()
    submit = SubmitField('validate and submit')


class NewCustomerCustomForm(FlaskForm):
    # Vdom Form
    Customer_name = StringField('Customer name : ')
    vdom_name = StringField('VDOM name : ', default='root')
    submit_vdom = SubmitField('Add vdom')

    # Interfaces Form
    intrf_lan_name = StringField('Interface LAN/DMZ name : ')
    intrf_wan_name = StringField('Interface WAN name : ')
    vlan_id_lan = StringField('VLAN ID ')
    ip_adresse_lan = StringField('IP adresse ')
    masque_lan = StringField('Masque ')
    vlan_id_wan = StringField('VLAN ID')
    ip_adresse_wan = StringField('IP adresse ')
    masque_wan = StringField('Masque ')
    ssh_access_lan = BooleanField()
    https_access_lan = BooleanField()
    ping_access_lan = BooleanField()
    ssh_access_wan = BooleanField()
    https_access_wan = BooleanField()
    ping_access_Wan = BooleanField()
    submit_lan = SubmitField('Add LAN/DMZ interface ')
    submit_wan = SubmitField('Add WAN interface ')

    # IP Pool Form
    ip_publique = StringField('Pool Adresse : ')
    ip_publique_name = StringField('IP Pool Name')
    submit_pool = SubmitField('Add IPPool')

    # Admin Local form
    admin_username = StringField('Username ', validators=[length(min=5, max=15)])
    admin_password = PasswordField('Password')
    submit_admin = SubmitField('Add Admin')

    # Route form
    destination = StringField('Destination', validators=[IPAddress(ipv4=True)])
    dst_masque = StringField('Masque', validators=[IPAddress(ipv4=True)])
    gw = StringField('gw', validators=[IPAddress(ipv4=True)])
    gw_intrf = SelectField('Available interfaces', choices=[('lan1', 'lan1'), ('lan2', 'lan2')])
    submit_route = SubmitField('Add route')

    # Adresse object
    ojbct_adr = StringField('Adresse object (adresse/mask : ')
    adr_name = StringField('Adresse Object Name : ')
    submit_obj = SubmitField('Add Object')

    # Policies
    src_intrf = SelectField('Available interfaces', choices=[('lan1_src', 'lan1_src'), ('lan2_src', 'lan2_src')])
    src_adr = SelectMultipleField('Source Adresse/group', choices=[('lan1_src', 'lan1_src')])
    dst_adr = SelectMultipleField('Destination Adresse/group', choices=[('lan1_src', 'lan1_src')])
    services = SelectMultipleField('Services', choices=[('lan1_src', 'lan1_src')])
    dst_intrf = SelectField('Available interfaces', choices=[('lan1_src', 'lan1_src'), ('lan2_src', 'lan2_src')])
    nat = SelectField('Addresse Translation', choices=[('disabled', 'disabled')])
    nat_option = BooleanField(label='Nat')
    action = SelectField('Action', choices=[('permit', 'permit'), ('deny', 'deny')])
    submit_pol = SubmitField('Add Policy')


class AddCustomerVDOM(FlaskForm):
    Customer_name = StringField('Client : ', validators=[length(min=5, max=12), DataRequired()])
    vdom_name = StringField('Nom du VDOM : ', default='root', validators=[length(min=5, max=12), DataRequired()])
    submit_vdom = SubmitField('Ajouter VDOM')


class AddAdminVDOM(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')])
    admin_username = StringField('Nom admin ', validators=[length(min=5, max=12), DataRequired()])
    admin_password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit_admin = SubmitField('Add Admin local')


class AddVdomInterface(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')])
    intrf_lan_name = StringField("Nom de l'interface : ", validators=[length(min=5, max=12), DataRequired()])
    vlan_id_lan = StringField('VLAN ID ', validators=[length(min=5, max=12), DataRequired()])
    ip_adresse_lan = StringField(" l'adresse : ", validators=[IPAddress(ipv4=True), DataRequired()])
    masque_lan = StringField("Masque : ")
    ssh_access_lan = BooleanField()
    https_access_lan = BooleanField()
    ping_access_lan = BooleanField()
    submit_lan = SubmitField('Ajouter interface')


class AddVdomIPPool(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')])
    ip_publique = StringField('Pool Adresse : ', validators=[length(min=5, max=12), DataRequired()])
    ip_publique_name = StringField("Nom d'objet IPPool : ", validators=[length(min=5, max=12), DataRequired()])
    submit_pool = SubmitField('Ajouter IPPool')


class AddVdomObject(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')])
    ojbct_adr = StringField('Objet IP (adresse/masque) : ', validators=[length(min=5, max=12), DataRequired()])
    adr_name = StringField("Nom de l'objet IP : ", validators=[length(min=5, max=12), DataRequired()])
    submit_obj = SubmitField("Ajouter objet")


class AddVdomRoute(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')],
                            default=('root', 'root'))
    destination = StringField('Destination', validators=[IPAddress(ipv4=True)])
    dst_masque = SelectField('Masque', choices=[('lan1', 'lan1'), ('lan2', 'lan2')])
    gw = StringField('Passerrelle', validators=[IPAddress(ipv4=True)])
    gw_intrf = SelectField('Available interfaces', choices=[('lan1', 'lan1'), ('lan2', 'lan2')])
    submit_route = SubmitField('Add route')


class AddVdomPolicy(FlaskForm):
    vdom_list = SelectField('La liste de VDOM', choices=[('echec_de_connexion', 'echec_de_connexion'),
                                                         ('echec_de_connexion', 'echec_de_connexion')],
                            default=('root', 'root'))
    src_intrf = SelectField('Source interface', choices=[('lan1_src', 'lan1_src'), ('lan2_src', 'lan2_src')],
                            validators=[DataRequired()])
    src_adr = SelectMultipleField('Source Adresse/group', choices=[('lan1_src', 'lan1_src')],
                                  validators=[DataRequired()])
    dst_adr = SelectMultipleField('Destination Adresse/group', choices=[('lan1_src', 'lan1_src')],
                                  validators=[DataRequired()])
    services = SelectMultipleField('Services', choices=[('lan1_src', 'lan1_src')], validators=[DataRequired()])
    dst_intrf = SelectField('Destination interface', choices=[('lan1_src', 'lan1_src'), ('lan2_src', 'lan2_src')],
                            validators=[DataRequired()])
    nat = SelectField('Addresse Translation', choices=[('disabled', 'disabled')], validators=[DataRequired()])
    nat_option = BooleanField(label='Nat')
    action = SelectField('Action', choices=[('permit', 'permit'), ('deny', 'deny')], validators=[DataRequired()])
    submit_pol = SubmitField('Add Policy')
