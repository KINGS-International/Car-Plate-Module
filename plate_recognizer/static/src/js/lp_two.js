/** @odoo-module */
const {Component,whenReady,mount,onWillStart,onMounted,useState}  = owl;
import {templates,loadJS} from '@web/core/assets'

/**
  @lanetwo_plate template area@
  
*/
class LaneTwo extends Component{
    setup(){
        console.log("I am lane two 00")
        this.state =useState([])
        onWillStart(async ()=>{
            await loadJS('https://js.pusher.com/7.0/pusher.min.js')
        })

        onMounted(()=>{
            var pusher = new Pusher('318074f4614f41479a6c', {
                cluster: 'us2',
            });

            var channel = pusher.subscribe('lane_two');
            var self = this; // Store reference to 'this'
            channel.bind('lp-2',function(data) {
                self.updateData(data.message)
                console.log("input data --",data.message)
            });
            pusher.subscribe('out').bind('departure',function(data){
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
        if (data.camera_id === 'camera-1'){
            var ind = this.state.findIndex(d => d.car_no === data.license_plate && d.camera_id === 'camera-2')
            if(ind === -1){
                this.state.push({
                    'raw_carno':data.raw_carno,
                    'id': data.student_id,
                    'name':data.student_name,
                    'classroom':data.classroom,
                    'car_no':data.license_plate,
                    'camera_id':data.camera_id
                })
            }
        }else if(data.camera_id === 'camera-2'){
            var ind = this.state.findIndex(d => d.car_no === data.license_plate && d.camera_id === 'camera-1')
            if(ind === -1){
                this.state.push({
                    'raw_carno':data.raw_carno,
                    'id': data.student_id,
                    'name':data.student_name,
                    'classroom':data.classroom,
                    'car_no':data.license_plate,
                    'camera_id':data.camera_id
                })
            }
        }
     }
}

LaneTwo.template = 'plate_recognizer.LaneTwo'
whenReady(()=>{
    const element = document.querySelector('#lane_two_plate')
    if (element){
        mount(LaneTwo,element,{templates})
    }
})