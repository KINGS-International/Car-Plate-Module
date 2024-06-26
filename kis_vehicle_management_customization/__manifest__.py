{
    "name": "KINGS Vehicle Management",

    'summary': """
        Car Management System and show dashboard data.""",

    'description': """
        Student Name and their car numbers register and then plate recognizer and show notice board.
    """,
   'license':'LGPL-3',
    "depends": ['base'],
    'website': "https://www.kis-mm.com",
    'author': 'Shun Lai Thu',
    "data": [
            'security/ir.model.access.csv',
            'views/vehicle_control_mgt_views.xml',
            'views/vehicle_in_out_view.xml',
    ],

}
