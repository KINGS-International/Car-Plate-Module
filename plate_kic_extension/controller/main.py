from odoo import http
from odoo.http import request, Response
import json
import pusher
from datetime import datetime, timedelta


class HookData(http.Controller):
    # webhook
    @http.route("/hook/data", type="http",auth="public", website=False, csrf=False,methods=['POST'])
    def read_plate_from_json(self,**post):
        if "json" in post:
            json_data = json.loads(post["json"])
            # # # Access the first result in the "results" list
            print("Json Data is ----------------------------",json_data)
            result = json_data["data"]["results"][0]
            plate_no = result["plate"][:6]
            camera_id = json_data["data"]["camera_id"]
            real_plate = ''
            if plate_no[1] == "0":
                real_plate = plate_no[:1] + "q" + plate_no[2:]
            else:
                real_plate = plate_no

            vehicle_obj =request.env["kis.vehicle.control"] .sudo().search([("car_no", "ilike", real_plate)]) ## changes
            if vehicle_obj:
                for veh in vehicle_obj:
                    vehicle_data = {
                        'raw_carno':str(veh.car_no),
                        "license_plate": str(veh.real_car_no),
                        "student_name": veh.name,
                        "classroom": veh.classroom,
                        'lane':veh.lane,
                        "is_sibling": veh.is_sibling,
                        "camera_id":camera_id,
                    }
                    if camera_id in ['camera-5','camera-6']:
                        if veh.student_academic in ['y10','y11',] and veh.lane == 'l3':
                            self.pusher_lane_three(vehicle_data)
                            print(f"Coming car is{camera_id} and is sibling and lane - 3 {veh.student_academic}")

                        elif veh.is_sibling and veh.lane == 'l4':
                            self.pusher_lane_four(vehicle_data)
                            print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic} {datetime.now()}")

                    elif camera_id in ["camera-7","camera-8"]:
                        self.pusher_ext_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                        check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",real_plate ),("check_out", "=", False)], limit=1)
                        print("Exit car is --------------------",check_in_out_obj)
                        if check_in_out_obj:
                            check_in_out_obj.sudo().write({"check_out": datetime.now()})   
                            
                if camera_id in ["camera-5","camera-6"]:
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",real_plate ),("check_out", "=", False)], limit=1)
                    if not  check_in_out_obj:
                        request.env["kis.vehicle.in.out"].sudo().create({"car_no": real_plate,"check_in":datetime.now()})

            else:
                if camera_id in ['camera-5','camera-6']:
                    request.env["kis.vehicle.in.out"].sudo().create({"car_no":real_plate,"check_in": datetime.now()})
                elif camera_id in ['camera-7','camera-8']:
                    print("Not car ----------------------------",real_plate,camera_id)
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=", real_plate), ("check_out", "=", False)],limit=1)
                    check_in_out_obj.sudo().write({"check_out": datetime.now()})


    ########################################################################################################
    # If want to changes plate code or testing and deubg, use this method                                  #
    # use json data {"palte":"3r3454","camera-id":"camera-1",'time':'2024-07-03 15:31:17.266056+06:30'}    #
    ########################################################################################################

    @http.route("/hook/test", type="http",auth="public", website=False, csrf=False,methods=['POST'])
    def test_plate_with_local(self,**post):
        data = request.httprequest.data.decode()
        p = json.loads(data)
        camera_id = p['camera-id']
        vehicle_obj =request.env["kis.vehicle.control"] .sudo().search([("car_no", "ilike", p['plate'])]) ## changes
        
        if vehicle_obj:
            for veh in vehicle_obj:
                vehicle_data = {
                    'raw_carno':str(veh.car_no),
                    "license_plate": str(veh.real_car_no),
                    "student_name": veh.name,
                    "classroom": veh.classroom,
                    'lane':veh.lane,
                    "is_sibling": veh.is_sibling,
                    "camera_id":camera_id,
                }
                if camera_id in ['camera-5','camera-6']:
                    if veh.student_academic in ['y10','y11',] and veh.lane == 'l3':
                        self.pusher_lane_three(vehicle_data)
                        print(f"Coming car is{camera_id} and is sibling and lane - 3 {veh.student_academic}")

                    elif veh.is_sibling and veh.lane == 'l4':
                        self.pusher_lane_four(vehicle_data)
                        print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic} {datetime.now()}")

                elif camera_id in ["camera-7","camera-8"]:
                    self.pusher_ext_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
                    print("Exit car is --------------------",check_in_out_obj)
                    if check_in_out_obj:
                        check_in_out_obj.sudo().write({"check_out": datetime.now()})   
                        
            if camera_id in ["camera-5","camera-6"]:
                check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
                if not  check_in_out_obj:
                    request.env["kis.vehicle.in.out"].sudo().create({"car_no": p['plate'],"check_in":datetime.now()})

        else:
            if camera_id in ['camera-5','camera-6']:
                request.env["kis.vehicle.in.out"].sudo().create({"car_no":p['plate'],"check_in": datetime.now()})
            elif camera_id in ['camera-7','camera-8']:
                print("Not car ----------------------------",p['plate'],camera_id)
                check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=", p['plate']), ("check_out", "=", False)],limit=1)
                check_in_out_obj.sudo().write({"check_out": datetime.now()})

                            
                    
    #------------------------------------------#
    # pusher method for real data return to js #                                                             
    # ---------------------------------------- #                                                                                                  

    def pusher_lane_three(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('lane_three', 'lp-3', {'message': data})

    def pusher_lane_four(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('lane_four', 'lp-4', {'message': data})
    
    def pusher_ext_departure_route(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('ext-out', 'ext-departure', {'message': data})

    
    #-------------------------#
    # route template method   #
    #-------------------------#
    @http.route('/lp-3',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_thrree(self):
        return request.render('plate_kic_extension.lane_three_template')

    @http.route('/lp-4',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_four(self):
        return request.render('plate_kic_extension.lane_four_template')

