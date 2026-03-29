from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class MaintenanceCompanyDashboard(models.Model):
    _name = 'maintenance.company.dashboard'
    _description = 'Maintenance Asset Type Dashboard'
    _auto = False
    _rec_name = 'asset_type_name'

    asset_type_id = fields.Integer(string='Asset Type ID', readonly=True)
    asset_type_name = fields.Char(string='Asset Type', readonly=True)
    equipment_count = fields.Integer(string='Total Assets', readonly=True)

    def init(self):
        # Force-override the native rule (noupdate=1 blocks XML override).
        # It restricts users to only equipment they follow — we replace with
        # open access and rely on our global team-based rule for filtering.
        self.env.cr.execute("""
            UPDATE ir_rule SET domain_force = '[(1, ''='', 1)]'
            WHERE id = (
                SELECT res_id FROM ir_model_data
                WHERE module = 'maintenance' AND name = 'equipment_rule_user'
            )
        """)

        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    row_number() OVER () as id,
                    at.id as asset_type_id,
                    at.description as asset_type_name,
                    COALESCE(COUNT(me.id), 0) as equipment_count
                FROM asset_type at
                LEFT JOIN maintenance_equipment me ON at.id = me.asset_type_id
                GROUP BY at.id, at.description
            )
        """ % self._table)

    def action_view_categories(self):
        self.ensure_one()
        return {
            'name': f'Asset Categories - {self.asset_type_name}',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment.category',
            'view_mode': 'kanban,list,form',
            'domain': [('asset_type_id', '=', self.asset_type_id)],
            'context': {'default_asset_type_id': self.asset_type_id},
            'target': 'current',
        }


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.constrains('maintenance_team_id')
    def _check_team_assignment_restriction(self):
        user = self.env.user
        if user.has_group('base.group_system') or user.has_group('maintenance.group_equipment_manager'):
            return

        for record in self:
            if record.maintenance_team_id:
                if user not in record.maintenance_team_id.member_ids:
                    raise ValidationError(_(
                        "Access Denied: You cannot assign assets to the '%s' team "
                        "because you are not a member of that team."
                    ) % record.maintenance_team_id.name)
