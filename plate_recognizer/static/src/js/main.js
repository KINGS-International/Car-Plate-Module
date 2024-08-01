/** @odoo-module */
const {Component,whenReady,mount,onWillStart,onMounted,useState}  = owl;
import {templates,loadJS} from '@web/core/assets'

class MainPlate extends Component{
    setup(){
        this.state =useState([])
        onWillStart(async ()=>{
            await loadJS('https://js.pusher.com/7.0/pusher.min.js')
        })

        onMounted(()=>{
            var pusher = new Pusher('318074f4614f41479a6c', {
                cluster: 'us2',
            });

            var channel = pusher.subscribe('main');
            var self = this; // Store reference to 'this'
            channel.bind('all',function(data) {
                self.updateData(data.message)
                console.log("input data --",data.message)
            });

           var dchannel =pusher.subscribe('out');
           dchannel.bind('departure',function(data){
                self.departureData(data.message)
           })
        })
        
    }
    departureData(data){
       if(data !== undefined){
            var ind = this.state.findIndex(d => d.raw_carno === data.plate)
            if(ind !== -1){
                console.log("Departure car is working",ind,data.plate)
                this.state.splice(ind,1)
            }else{
                console.log("Departure car is not working",ind,data.plate)
            }
       }
    }

    updateData(data){
        if (data){
            var ind = this.state.findIndex(d => d.car_no === data.license_plate)
            if(ind === -1){
                this.state.push({
                    'raw_carno':data.raw_carno,
                    'id': data.student_id,
                    'name':data.student_name,
                    'classroom':data.classroom,
                    'car_no':data.license_plate,
                    'camera_id':data.camera_id
                })
            }else{
                console.log("Existing Car --")
            }
        }
    }
      
}

MainPlate.template = 'plate_recognizer.Main'
whenReady(()=>{
    const element = document.querySelector('#main_plate')
    if (element){
        mount(MainPlate,element,{templates})
    }
})

/**
 * @route_sign
 */
class SignRoute extends Component{
    setup(){
        this.state =useState({})
        onWillStart(async ()=>{
            await loadJS('https://js.pusher.com/7.0/pusher.min.js')
        })

        onMounted(()=>{
            var pusher = new Pusher('318074f4614f41479a6c', {
                cluster: 'us2',
            });

            var channel = pusher.subscribe('route');
            var self = this; // Store reference to 'this'
            channel.bind('sign',function(data) {
                console.log("DATA is",data.message)
                self.updateData(data.message)
            });
        })
        
    }
     updateData(data){
        console.log("sibling academinc type is",data.sibling_academic,'studentype is',data.sibling_academic)
        if( this.state.car_no !== data.license_plate){
            this.state.car_no = data.license_plate
            this.state.lane = data.lane
            this.state.camera_id= data.camera_id
            // this.state.sibling_academic = data.sibling_academic
        }
     }
    
}

SignRoute.template = 'plate_recognizer.SignRoute'
whenReady(()=>{
    const element = document.querySelector('#sing_route')
    if (element){
        mount(SignRoute,element,{templates})
    }
})