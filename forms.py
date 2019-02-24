from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    intrf_nbr = StringField('Number of LAN interfaces : ', validators=[number_range(min=2, max=5)])
    Customer_name = StringField('Customer name : ', validators=[DataRequired()])
    vdom_name = StringField('VDOM name : ', validators=[DataRequired()])
    vlan_id_lan = StringField('VLAN ID ', validators=[DataRequired()])
    ip_adresse_lan = StringField('IP adresse ', validators=[DataRequired()])
    masque_lan = StringField('Masque ', validators=[DataRequired()])
    vlan_id_wan = StringField('VLAN ID', validators=[DataRequired()])
    ip_adresse_wan = StringField('IP adresse ', validators=[DataRequired()])
    masque_wan = StringField('Masque ', validators=[DataRequired()])
    ip_publique = StringField('Pool Settings : ', validators=[DataRequired()])
    ssh_access_lan = BooleanField()
    https_access_lan = BooleanField()
    ping_access_lan = BooleanField()
    ssh_access_wan = BooleanField()
    https_access_wan = BooleanField()
    ping_access_Wan = BooleanField()
    submit = SubmitField('validate and submit')
