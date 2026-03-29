from odoo import fields, models

class AssetType(models.Model):
    _name = 'asset.type'
    _description = 'Asset Type'
    _rec_name = 'description'

    description = fields.Char(string='Asset', required=True)