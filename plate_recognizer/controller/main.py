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
                    if camera_id in ['camera-1','camera-2']:
                        self.pusher_sign_route(vehicle_data)
                        self.pusher_client_all(vehicle_data) ## main route 
                        if veh.student_academic in ['y3','y4','y6','y7','y8','y9'] and veh.lane == 'l1':
                            self.pusher_lane_one(vehicle_data)
                            print(f"Coming car is{camera_id} and is sibling and lane - 1 {veh.student_academic}")

                        elif veh.student_academic in ['y1','y2','y5','preschool'] and veh.lane == 'l2':
                            self.pusher_lane_two(vehicle_data)
                            print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic} {datetime.now()}")

                        elif veh.is_sibling:
                            self.pusher_sign_route(vehicle_data)
                            print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic}")

                    elif camera_id in ["camera-3","camera-4"]:
                        self.pusher_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                        check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",real_plate ),("check_out", "=", False)], limit=1)
                        if check_in_out_obj:
                            check_in_out_obj.sudo().write({"check_out": datetime.now()})   
                            
                if camera_id in ["camera-1","camera-2"]:
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",real_plate ),("check_out", "=", False)], limit=1)
                    if not  check_in_out_obj:
                        request.env["kis.vehicle.in.out"].sudo().create({"car_no": real_plate,"check_in":datetime.now()})
            
            ## guest car
            else:
                if camera_id in ['camera-1','camera-2']:
                    format_late = f"{real_plate[:2].upper}-{real_plate[2:]}"
                    guest_data = {'license_plate':format_late,'lane':'guest'}
                    self.pusher_sign_route(guest_data)
                    request.env["kis.vehicle.in.out"].sudo().create({"car_no":real_plate,"check_in": datetime.now()})

                elif camera_id in ['camera-3','camera-4']:
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
                if camera_id in ['camera-1','camera-2']:
                    self.pusher_sign_route(vehicle_data)
                    self.pusher_client_all(vehicle_data) ## main route 
                    if veh.student_academic in ['y3','y4','y6','y7','y8','y9'] and veh.lane == 'l1':
                        self.pusher_lane_one(vehicle_data)
                        print(f"Coming car is{camera_id} and is sibling and lane - 1 {veh.student_academic}")

                    elif veh.student_academic in ['y1','y2','y5','preschool'] and veh.lane == 'l2':
                        self.pusher_lane_two(vehicle_data)
                        print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic} {datetime.now()}")

                    elif veh.is_sibling:
                        self.pusher_sign_route(vehicle_data)
                        print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic}")

                elif camera_id in ["camera-3","camera-4"]:
                    self.pusher_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
                    check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
                    print("Exit car is --------------------",check_in_out_obj)
                    if check_in_out_obj:
                        check_in_out_obj.sudo().write({"check_out": datetime.now()})   
                        
            if camera_id in ["camera-1","camera-2"]:
                check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
                if not  check_in_out_obj:
                    request.env["kis.vehicle.in.out"].sudo().create({"car_no": p['plate'],"check_in":datetime.now()})


                # elif camera_id in ['camera-3'] and  veh.lane == 'l3':
                #     if veh.student_academic in ['y10','y11'] and not veh.is_sibling:
                #         self.pusher_lane_three(vehicle_data)
                #         print(f"Coming car is{camera_id} and is sibling and lane is {veh.lane} {veh.student_academic}")

                # elif camera_id in ['camera-4'] and  veh.lane == 'l4':
                #     if veh.is_sibling:
                #         self.pusher_lane_four(vehicle_data)
                #         print(f"Coming car is{camera_id} and is sibling and lane {veh.lane} {veh.student_academic}")
                        
            ##### need looping #####
            # if camera_id in ["camera-1","camera-2","camera-3","camera-4"]:
            #     check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
            #     if not  check_in_out_obj:
            #         request.env["kis.vehicle.in.out"].sudo().create({"car_no": p['plate'],"check_in":datetime.now()})
            # else:
            #     self.pusher_departure_route({'plate':vehicle_data['raw_carno']}) ## departpure route
            #     check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=",p['plate'] ),("check_out", "=", False)], limit=1)
            #     print("Exit car is --------------------",check_in_out_obj)
            #     if check_in_out_obj:
            #         check_in_out_obj.sudo().write({"check_out": datetime.now()})   

        else:
            if camera_id in ['camera-1','camera-2']:
                format_late = f"{p['plate'][:2].upper}-{p['plate'][2:]}"
                guest_data = {'license_plate':format_late,'lane':'guest'}
                self.pusher_sign_route(guest_data)
                print("Not car ----------------------------",p['plate'][:2],camera_id)
                request.env["kis.vehicle.in.out"].sudo().create({"car_no":p['plate'],"check_in": datetime.now()})
            elif camera_id in ['camera-3','camera-4']:
                print("Not car ----------------------------",p['plate'],camera_id)
                check_in_out_obj = request.env["kis.vehicle.in.out"].search([("car_no", "=", p['plate']), ("check_out", "=", False)],limit=1)
                check_in_out_obj.sudo().write({"check_out": datetime.now()})

                            
                    
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


    def pusher_lane_two(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('lane_two', 'lp-2', {'message': data})
    
    def pusher_lane_one(self,data):
        pusher_client = pusher.Pusher(
            app_id='1804733',
            key='318074f4614f41479a6c',
            secret='64e82fb5aef3e0fc3032',
            cluster='us2',
            ssl=True
        )
        pusher_client.trigger('lane_one', 'lp-1', {'message': data})

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
    
    @http.route('/lp-2',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_two(self):
        return request.render('plate_recognizer.lane_two_template')

    @http.route('/lp-1',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_one(self):
        return request.render('plate_recognizer.lane_one_template')
    
    @http.route('/lp-3',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_thrree(self):
        return request.render('plate_recognizer.lane_three_template')

    @http.route('/lp-4',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def lane_four(self):
        return request.render('plate_recognizer.lane_four_template')

    @http.route('/route',auth="public",type="http",csrf=False,website=True,methods=['GET'])
    def sing_route(self):
        return request.render('plate_recognizer.sign_route')
