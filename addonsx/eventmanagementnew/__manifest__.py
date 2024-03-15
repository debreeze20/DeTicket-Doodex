# -*- coding: utf-8 -*-
{
    'name': "eventmanagementnew",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx', 'web_responsive'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/referensi_sales.xml',
        'data/referensi_staff.xml',
        'data/referensi_event.xml',
        'data/referensi_venue.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/event_view.xml',
        'views/staff_view.xml',
        'views/bag_accounting_staff_view.xml',
        'views/bag_office_cleaner_view.xml',
        'views/bag_sales_staff_view.xml',
        'views/venue_view.xml',
        'views/customer_view.xml',
        'views/sales_view.xml',
        'views/cust_inherit_view.xml',
        'report/report.xml',
        'report/report_sales.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
