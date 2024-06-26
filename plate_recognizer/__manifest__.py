{
    "name" : "Plate Recoginzer",
    "author" : "KINGS",
    "version": "16.0.1",
    "license":"LGPL-3",
    "summary": "Plate reconginzer",
    "application": True,
    "auto_install": False,
    "depends":['base','website','web','kings_vehicle_management'],
    "data":[
        'views/all_template.xml',
    ],
    "assets":{
        'web.assets_frontend' : [
            'plate_recognizer/static/src/js/*',
            'plate_recognizer/static/src/scss/*',
            'plate_recognizer/static/src/template/*'
        ],
    
    }
}
