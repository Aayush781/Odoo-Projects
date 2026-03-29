{
    'name': 'Asset Management',
    'version': '19.0.1.0.1',
    'category': 'Maintenance',
    'summary': 'Rename Equipment to Assets in Maintenance module',
    'description': """
        This module renames:
        - Equipment menu to Assets
        - Equipment view titles to Assets
        - Equipment Category field to Asset Category
        - Hides all other apps from non-admin users
    """,
    'depends': ['maintenance', 'hr', 'stock', 'mail', 'contacts'],
    'data': [
        'security/maintenance_security.xml',
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
        'views/asset_types.xml',
        'views/menu_hide.xml',
        'views/maintenance_dashboard_views.xml',
        'views/asset_report.xml',
        'data/home_action.xml',
        'data/asset_assignment_email.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'maintenance_assets/static/src/css/hide_odoo_account.css',
            'maintenance_assets/static/src/js/hide_odoo_account.js',
        ],
    },
    'installable': True,
    'application' : True,
    'auto_install': False,
    'license': 'LGPL-3',
}
