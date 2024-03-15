from odoo import models, fields, api, _

# represents location of event 
class VenueDoodex (models.Model):
    _name = 'doodex.venue'
    _description = 'page venue'
    _rec_name = 'ref_venue'

    ref_venue = fields.Char(string='No. Reference', required=True, readonly=True, default=lambda self:_('New'))

    name = fields.Char(string='Venue Name', required=True)
    alamat = fields.Char(string='Address')
    event_ids = fields.One2many(comodel_name='doodex.event', inverse_name='venue_id', string='Event')
    
    # reference for 
    @api.model
    def create(self,vals):
        if vals.get('ref_venue', _("New")) == _("New"):
            vals['ref_venue'] = self.env['ir.sequence'].next_by_code('referensi.venue') or _("New")
        record = super(VenueDoodex, self).create(vals)
        return record