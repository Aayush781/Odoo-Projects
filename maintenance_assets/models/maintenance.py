from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    _description = 'Asset Management'

    category_id = fields.Many2one('maintenance.equipment.category', string='Asset Category',
                                  tracking=True, group_expand='_read_group_category_ids')

    asset_type_id = fields.Many2one('asset.type', string='Asset Type')

    @api.onchange('asset_type_id')
    def _onchange_asset_type_id(self):
        self.category_id = False
        if self.asset_type_id:
            return {'domain': {'category_id': [('asset_type_id', '=', self.asset_type_id.id)]}}
        return {'domain': {'category_id': []}}

    employee_id = fields.Many2one('hr.employee', string='Current Employee')

    location_id = fields.Many2one(
        'stock.location',
        string='Used in Location',
        domain=[('usage', '=', 'internal')]
    )
    image_medium = fields.Binary("Equipment Image", attachment=True)

    maintenance_team_id = fields.Many2one('maintenance.team', string='Asset Team')
    maintenance_team_name = fields.Char(related='maintenance_team_id.name', string='Asset Team Name', store=True)

    purchase_date = fields.Date(string="Purchase Date")

    @api.model_create_multi
    def create(self, vals_list):
        records = super(MaintenanceEquipment, self).create(vals_list)
        for record in records:
            if record.employee_id:
                record._send_asset_assignment_email()
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'employee_id' in vals and vals.get('employee_id'):
            for record in self:
                record._send_asset_assignment_email()
        return res

    def _send_asset_assignment_email(self):
        self.ensure_one()
        template = self.env.ref(
            'maintenance_assets.email_template_asset_assigned',
            raise_if_not_found=False
        )
        if not template:
            return

        employee = self.employee_id
        if not employee or not employee.work_email:
            return

        template.send_mail(
            self.id,
            force_send=True,
            email_values={
                'email_to': employee.work_email,
                'email_from': self.env.user.email_formatted,
            }
        )