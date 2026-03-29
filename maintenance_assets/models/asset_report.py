from odoo import models, fields, tools

class AssetReportAnalysis(models.Model):
    _name = 'asset.report.analysis'
    _description = 'Asset Reporting Analysis'
    _auto = False
    _rec_name = 'asset_name'

    asset_type_id = fields.Many2one('asset.type', 'Asset Type', readonly=True)
    asset_name = fields.Char('Asset Name', readonly=True)
    category_id = fields.Many2one('maintenance.equipment.category', 'Category', readonly=True)
    cost = fields.Float('Total Cost', readonly=True)
    asset_count = fields.Integer('Quantity', readonly=True)
    purchase_date = fields.Date('Purchase Date', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    me.id as id,
                    me.asset_type_id as asset_type_id,
                    COALESCE(me.name->>'en_US', me.name->>'en_GB', 'Unnamed Asset') as asset_name,
                    me.category_id as category_id,
                    COALESCE(me.cost, 0) as cost,
                    1 as asset_count,
                    me.purchase_date as purchase_date
                FROM maintenance_equipment me
            )
        """ % self._table)
