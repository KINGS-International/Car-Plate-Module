from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
import datetime
from datetime import date,timedelta

class VehicleInOut(models.Model):
    _name = "kis.vehicle.in.out"
    _description = "Vehicle Attendance Check In/Out"

    # name = fields.Char()
    car_no = fields.Char()
    check_in_out_time = fields.Datetime(string="Check In/Out Time")
    check_in_out = fields.Selection([('check_in','Check In'),('check_out','Check Out')])
    status = fields.Selection([('register','Register'),('unregister','Unregister')],compute='compute_state', store=True)
    duration = fields.Float(string="Duration",compute='_compute_duration')
    check_in = fields.Datetime()
    check_out = fields.Datetime()


    _order = 'check_in desc'

    def name_get(self):
        result = []

        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.car_no, rec.status)))
        return result

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        if self:
            for rec in self:
                rec.duration = 0.0
                if rec.check_in and rec.check_out:
                    diff_time = rec.check_out - rec.check_in
                    duration = float(diff_time.days) * 24 + \
                               (float(diff_time.seconds) / 3600)
                    rec.duration = round(duration, 2)

    @api.depends('car_no')
    def compute_state(self):
        for rec in self:
            vehicle_obj = self.env['vehicle.control'].search([('car_no','=',rec.car_no)])
            if vehicle_obj:
                rec.status = 'register'
            else:
                rec.status = 'unregister'
