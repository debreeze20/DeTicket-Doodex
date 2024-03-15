from odoo import models, fields, api

#represents individuals/entities regist for attending the event
class CustomerDoodex (models.Model):
    _name = 'doodex.customer'
    _description = 'page customer'

    name = fields.Char(string='Customer Name', required=True)
    dob = fields.Date(string='Date of Birth')
    id_card = fields.Char(string='ID Card')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    ci = fields.Char(string='Phone Number (Whatsapp)')
    
    # to show ticket have been purchased
    sales_ids = fields.One2many(comodel_name='doodex.sales', inverse_name='cust_id', string='Ticket') # for sales staff only