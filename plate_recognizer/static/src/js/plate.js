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
            });

           var dchannel =pusher.subscribe('out');
           dchannel.bind('departure',function(data){
                self.departureData(data.message)
           })
        })
        
    }
    departureData(data){
       if(data !== undefined){
            this.state.forEach((d,index)=>{
                if (d.raw_carno === data.plate){
                    this.state.splice(index)
                }
            })
       }
    }

    updateData(data){
        console.log("Update data is working ",this.state)
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
        console.log("Main data ->",data)
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
  @extension_plate template area@
  
*/
class ExtensionPlate extends Component{
    setup(){
        this.state =useState([])
        onWillStart(async ()=>{
            await loadJS('https://js.pusher.com/7.0/pusher.min.js')
        })

        onMounted(()=>{
            var pusher = new Pusher('318074f4614f41479a6c', {
                cluster: 'us2',
            });

            var channel = pusher.subscribe('extension');
            var self = this; // Store reference to 'this'
            channel.bind('display-1',function(data) {
                self.updateData(data.message)
            });
            pusher.subscribe('out').bind('departure',function(data){
                self.departureData(data.message)
           })

        })  
    }
    departureData(data){
        if(data !== undefined){
             this.state.forEach((d,index)=>{
                 if (d.raw_carno === data.plate){
                     this.state.splice(index)
                 }
             })
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
        console.log("Extension data ->",data)
     }
}

ExtensionPlate.template = 'plate_recognizer.Extension'
whenReady(()=>{
    const element = document.querySelector('#extension_plate')
    if (element){
        mount(ExtensionPlate,element,{templates})
    }
})


/**
  *@waiting_plate template area
*/
class WaitingPlate extends Component{
    setup(){
        this.state =useState([])
        onWillStart(async ()=>{
            await loadJS('https://js.pusher.com/7.0/pusher.min.js')
        })

        onMounted(()=>{
            var pusher = new Pusher('318074f4614f41479a6c', {
                cluster: 'us2',
            });

            var channel = pusher.subscribe('waiting');
            var self = this; // Store reference to 'this'
            channel.bind('display-2',function(data) {
                self.updateData(data.message)
            });
            pusher.subscribe('out').bind('departure',function(data){
                self.departureData(data.message)
            })
        })
        
    }
    departureData(data){
        if(data !== undefined){
             this.state.forEach((d,index)=>{
                 if (d.raw_carno === data.plate){
                     this.state.splice(index)
                 }
             })
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
        console.log("Waiting data ->",data)
     }
    
}

WaitingPlate.template = 'plate_recognizer.Waiting'
whenReady(()=>{
    const element = document.querySelector('#waiting_plate')
    if (element){
        mount(WaitingPlate,element,{templates})
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
            this.state.student_type= data.student_type
            this.state.sibling_academic = data.sibling_academic
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

