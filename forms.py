from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
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
    vdom_name = StringField('VDOM name : ')
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

    submit_policy = SubmitField('Add policy')
