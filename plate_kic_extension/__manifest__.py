{
    "name" : "Plate Recoginzer Kic & Extension",
    "author" : "KINGS",
    "version": "16.0.1",
    "license":"LGPL-3",
    "summary": "Plate reconginzer Kic & Extension",
    "application": True,
    "auto_install": False,
    "depends":['base','website','web','kis_vehicle_management_customization'],
    "data":[
        'views/all_template.xml',
    ],
    "assets":{
        'web.assets_frontend' : [
            'plate_kic_extension/static/src/js/*',
            'plate_kic_extension/static/src/scss/*',
            'plate_kic_extension/static/src/template/*'
        ],
    }
}
