from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_default_action(self):
        return self.env.ref('maintenance.action_maintenance_company_dashboard', raise_if_not_found=False)

    action_id = fields.Many2one(
        'ir.actions.actions',
        string='Home Action',
        default=_get_default_action,
    )
