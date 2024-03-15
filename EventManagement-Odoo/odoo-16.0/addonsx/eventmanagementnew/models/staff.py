from odoo import models, fields, api, _

# represent the staff responsible for sales and managing ticket transactions related to event
class StaffDoodex (models.Model):
    _name = 'doodex.staff'
    _description = 'page sales staff'
    _rec_name = 'ref_staff'

    ref_staff = fields.Char(string='No. Reference', required=True, readonly=True, default=lambda self:_('New'))
    name = fields.Char(string='Name', required=True)
    dof = fields.Date(string='Date of Birth')
    id_card = fields.Char(string='ID Card')
    address = fields.Char(string='Address')
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')])
    cp = fields.Char(string='Contact Information')
    staff = fields.Selection(string='Position', selection=[('sales', 'Sales'), ('accounting', 'Accounting'), ('officecleaner', 'Office Cleaner')],required=True)
    salary = fields.Integer(string='Salary')
    event_ids = fields.One2many(comodel_name='doodex.event', inverse_name='sales_staff_id', string='Event') # for sales staff only
    bag = fields.Char(compute='_compute_bag', string='Department', store=True)
    
    # action for parted away each different position
    @api.depends('staff')
    def _compute_bag(self):
        for rec in self:
            rec.bag = str(rec.staff)
    
    # for create reference staff
    @api.model
    def create(self,vals):
        if vals.get('ref_staff', _("New")) == _("New"):
            bag = vals.get('staff','sales')
            if bag == 'sales':
                vals['ref_staff'] = self.env['ir.sequence'].next_by_code('referensi.salesstaff') or _("New")
            elif bag == 'accounting':
                vals['ref_staff'] = self.env['ir.sequence'].next_by_code('referensi.accountingstaff') or _("New")
            elif bag == 'officecleaner':
                vals['ref_staff'] = self.env['ir.sequence'].next_by_code('referensi.cleanerstaff') or _("New")
        record = super(StaffDoodex, self).create(vals)
        return record

    # @api.


    