{
    "name" : "Plate Recoginzer",
    "author" : "KINGS",
    "version": "16.0.1",
    "license":"LGPL-3",
    "summary": "Plate reconginzer",
    "application": True,
    "auto_install": False,
    "depends":['base','website','web','kis_vehicle_management_customization'],
    "data":[
        'views/all_template.xml',
    ],
    "assets":{
        'web.assets_frontend' : [
            'plate_recognizer/static/src/js/lp_one.js',
            'plate_recognizer/static/src/js/lp_two.js',
            'plate_recognizer/static/src/js/main.js',
            'plate_recognizer/static/src/scss/*',
            'plate_recognizer/static/src/template/lane-one.xml',
            'plate_recognizer/static/src/template/lane-two.xml',
            'plate_recognizer/static/src/template/main.xml',
            'plate_recognizer/static/src/template/route.xml',
          
        ],
    }
}
