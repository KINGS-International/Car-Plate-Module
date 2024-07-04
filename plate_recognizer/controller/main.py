from odoo import http
from odoo.http import request, Response
import json
import pusher
from datetime import datetime, timedelta


class HookData(http.Controller):
    # webhook
    @http.route("/hook/data", type="http",auth="public", website=False, csrf=False,cors="*",methods=['POST'])
    def read_plate_from_json(self,**post):
        print("Post method is --------------------------------------------",post)
        if "json" in post:
            json_data = json.loads(post["json"])
            # # # Access the first result in the "results" list
            print("Json Data is ----------------------------",json_data)
            result = json_data["data"]["results"][0]
            plate_no = result["plate"][:6]
            camera_id = json_data["data"]["camera_id"] # 'camera-1'
            real_plate = ''
            if plate_no[1] == "0":
                real_plate = plate_no[:1] + "q" + plate_no[2:]
            else:
                real_plate = plate_no
            
            ## date format
            timestamp_local = json_data["data"]["timestamp_local"]
            format_string = "%Y-%m-%d %H:%M:%S"
            time_format = "%H:%M:%S"
            # Assuming timestamp_local is a string
            datetime_obj = datetime.strptime(timestamp_local, "%Y-%m-%d %H:%M:%S.%f%z")
            time_delta = timedelta(hours=6, minutes=30)
            new_date_time = datetime_obj - time_delta
            new_date_time_str = new_date_time.strftime(format_string)
                
            vehicle_obj =request.env["kis.vehicle.control"] .sudo().search([("car_no", "ilike", real_plate)]) ## changes
            if vehicle_obj:
                for veh in vehicle_obj:
                    vehicle_data = {
                        'raw_carno':veh.car_no,
                        "license_plate": veh.real_car_no,
                        "student_name": veh.name,
                        "student_type": veh.student_academic,
                        'student_id': veh.student_id_code,
                        "classroom": veh.classroom,
                        "is_sibling": veh.is_sibling,
                        "sibling_academic": veh.sibling_academic,
                        "camera_id":camera_id,
                    }
                    self.pusher_client_all(vehicle_data) ## main route 
                    if camera_id in ['camera-1','camera-2']:
                        if veh.student_academic == "lower_pri" or (veh.is_sibling == True and (veh.sibling_academic == "lower_pri")) and veh.vehicle_type == "car" :
                            self.pusher_extension_lane(vehicle_data) ## extension route
                            self.pusher_sign_route(vehicle_data)
                        elif veh.student_academic in ("upper_pri", "lower_sec", "upper_sec")and veh.vehicle_type == "car" :
                            self.pusher_waiting_lane(vehicle_data) ## waiting route
                            self.pusher_sign_route(vehicle_data)
                    elif camera_id == "camera-3":
                        self.pusher_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                        check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",real_plate ), ("check_out", "=", False)], limit=1)
                        if check_in_out_obj:
                            check_in_out_obj.sudo().write({"check_out": new_date_time_str})         
                # """ create history register | ungresiter & time"""
                request.env["kis.vehicle.in.out"].sudo().create({"car_no": real_plate,"check_in": new_date_time_str,}) ## changes
            else:
                if camera_id in ['camera-1','camera-2']:
                    request.env["kis.vehicle.in.out"].sudo().create({"car_no": real_plate,"check_in": new_date_time_str})
                elif camera_id == "camera-3":
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search(
                        [("car_no", "=", real_plate), ("check_out", "=", False)], limit=1
                    )
                    check_in_out_obj.sudo().write({"check_out": new_date_time_str})


    ########################################################################################################
    # If want to changes plate code or testing and deubg, use this method                                  #
    # use json data {"palte":"3r3454","camera-id":"camera-1",'time':'2024-07-03 15:31:17.266056+06:30'}    #
    ########################################################################################################

    @http.route("/hook/test", type="http",auth="public", website=False, csrf=False,cors="*",methods=['POST'])
    def test_plate_with_local(self,**post):
        data = request.httprequest.data.decode()
        p = json.loads(data)
        camera_id = p['camera-id']
        vehicle_model = request.env["kis.vehicle.in.out"]
        ####
        print("pp==============================",p)
        vehicle_obj =request.env["kis.vehicle.control"] .sudo().search([("car_no", "ilike", p['plate'])]) ## changes
        if vehicle_obj:
            print("Vehicle object is -------------------------------------",vehicle_obj)
            for veh in vehicle_obj:
                vehicle_data = {
                    'raw_carno':veh.car_no,
                    "license_plate": veh.real_car_no,
                    "student_name": veh.name,
                    "student_type": veh.student_academic,
                    'student_id': veh.student_id_code,
                    "classroom": veh.classroom,
                    "is_sibling": veh.is_sibling,
                    "sibling_academic": veh.sibling_academic,
                    "camera_id":camera_id,
                }
                self.pusher_client_all(vehicle_data) ## main route 
                if camera_id in ['camera-1','camera-2']:
                    if veh.student_academic == "lower_pri" or (veh.is_sibling == True and (veh.sibling_academic == "lower_pri")) and veh.vehicle_type == "car" :
                        self.pusher_extension_lane(vehicle_data) ## extension route
                        self.pusher_sign_route(vehicle_data)
                    elif veh.student_academic in ("upper_pri", "lower_sec", "upper_sec")and veh.vehicle_type == "car" :
                        self.pusher_waiting_lane(vehicle_data) ## waiting route
                        self.pusher_sign_route(vehicle_data)
                    print("Coming From camera 1 & 2 ---------------------------------------------",)

                elif camera_id == "camera-3":
                    self.pusher_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ), ("check_out", "=", False)], limit=1)
                    if check_in_out_obj:
                        check_in_out_obj.sudo().write({"check_out": new_date_time_str})   

            """ create history register | ungresiter & time"""
            request.env["kis.vehicle.in.out"].sudo().create({"car_no": p['plate']}) ## changes  
        else:
            if camera_id in ['camera-1','camera-2']:
                request.env["kis.vehicle.in.out"].sudo().create({"car_no":p['plate']}) ## changes  
            elif camera_id == "camera-3":
                check_in_out_obj = request.env["kis.vehicle.in.out"].search(
                    [("car_no", "=", p['plate']), ("check_out", "=", False)], limit=1
                )
                # check_in_out_obj.sudo().write({"check_out": new_date_time_str})

                            
                    
    #------------------------------------------#
    # pusher method for real data return to js #                                                             
    # ---------------------------------------- #                                                                                                  
    def pusher_client_all(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('main', 'all', {'message': data})


    def pusher_extension_lane(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('extension', 'display-1', {'message': data})
    
    def pusher_waiting_lane(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('waiting', 'display-2', {'message': data})
    
    def pusher_departure_route(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('out', 'departure', {'message': data})

    def pusher_sign_route(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('route', 'sign', {'message': data})
        
    
    #-------------------------#
    # route template method   #
    #-------------------------#
    @http.route('/main',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def main_route(self):
        return request.render('plate_recognizer.main_template')
    
    @http.route('/extension',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def extension_route(self):
        return request.render('plate_recognizer.extension_template')

    @http.route('/waiting',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def waiting_route(self):
        return request.render('plate_recognizer.waiting_template')

    @http.route('/route',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def sing_route(self):
        return request.render('plate_recognizer.sign_route')


"""

{'json':
   '{"hook": {"target": "http://172.20.2.2:8070/hook/data", "id": "camera-1",
    "event": "recognition", "filename": "camera-1_screenshots/24-07-03/15-31-17.266056.jpg"},
    "data": {"camera_id": "camera-1", "filename": "camera-1_screenshots/24-07-03/15-31-17.266056.jpg", "
    timestamp": "2024-07-03T09:01:17.266056Z", "timestamp_local": "2024-07-03 15:31:17.266056+06:30",
    "results": [{"box": {"xmin": 489, "ymin": 403, "xmax": 624, "ymax": 466}, "plate": "9p6788", 
    "region": {"code": "us-or", "score": 0.102}, "score": 0.899, 
    "candidates": [{"score": 0.899, "plate": "9p6788"}, {"score": 0.799, "plate": "9p67b8"}, {"score": 0.798, "plate": "9p678b"}, {"score": 0.698, "plate": "9p67bb"}], 
    "dscore": 0.769, "vehicle": {"score": 0.606, "type": "Pickup Truck", "box": {"xmin": 1389, "ymin": 545, "xmax": 2170, "ymax": 1183}}, "direction": "", 
    "source_url": "rtsp://admin:admin123@172.20.1.101:554/cam/realmonitor?channel=1&subtype=0", "position_sec": "23490.99195162", "user_data": ""}]}}',
     'upload': <FileStorage: '15-31-17.266056.jpg' ('image/jpeg')>
}

"""