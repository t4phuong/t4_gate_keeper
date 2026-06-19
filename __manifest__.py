{
    'name': "Gate Keeper",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/scheduler_cron.xml',
        'views/GK_company_views.xml',
        'views/gate_keeper_views.xml',
        'views/GK_menu.xml'
    ],
}
