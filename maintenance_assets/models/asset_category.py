from odoo import fields, models

class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    asset_type_id = fields.Many2one('asset.type', string='Asset Type')

