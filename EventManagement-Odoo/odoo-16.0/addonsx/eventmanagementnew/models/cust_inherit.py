from odoo import _, api, fields, models


class CustInherit(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string='Customer Name', required=True)
    phone = fields.Char(string='Phone Number')  
    email = fields.Char(string='Email')
    id_card = fields.Char(string='ID Card')
    # gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])

    sales_ids = fields.One2many(comodel_name='doodex.sales', inverse_name='cust_id', string='Ticket') # for sales staff only