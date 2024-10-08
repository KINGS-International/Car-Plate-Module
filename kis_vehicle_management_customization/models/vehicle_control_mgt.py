from odoo import fields, models, api


class PlateRecognizer(models.Model):
    _name = 'kis.vehicle.control'
    _description = 'Vehicle Control'

    student_id_code = fields.Char(string="Student ID")
    name = fields.Char(string="Name")
    student_academic = fields.Selection(
        [('preschool', 'Preschool'), ('y1', 'Year-1'), ('y2', 'Year-2'), ('y3', 'Year-3'), ('y4', 'Year-4'),
        ('y5', 'Year-5'), ('y6', 'Year-6'), ('y7', 'Year-7'), ('y8', 'Year-8'), ('y9', 'Year-9'),
        ('y10','Year-10'),('y11','Year-11'),('training', 'Training'),], string='Student Type')
    classroom = fields.Char(string='Classroom')
    car_no = fields.Char("Car No.", compute="get_stu_info", store=True)
    lane = fields.Selection([('l1','Lane-one'),('l2','Lane-Two'),('l3','Lane-Three'),('l4','Lane-Four')],compute="_compute_lane",store=True)
    real_car_no = fields.Char("Real Car No.")
    is_sibling = fields.Boolean("Is Sibling")
    sibling_academic = fields.Selection(
        [('preschool', 'Preschool'), ('lower_pri', 'Lower Primary'), ('upper_pri', 'Upper Primary'), ('lower_sec', 'Lower Secondary'), ('upper_sec', 'Upper Secondary'),
        ('ncuk', 'NCUK'), ('oversea_agency', 'Oversea Agency'), ('higher_edu', 'Higher Education'), ('advisory', 'Advisory'),
        ('training', 'Training'), ('others', 'Others')], string="Sibling's Student Type")
    vehicle_type = fields.Selection([('ferry', 'Ferry'),('car','Car')],default='car',string="Vehicle Type", required=True)

    @api.depends('student_academic','is_sibling')
    def _compute_lane(self):
        for rec in self:
            if rec.is_sibling:
                rec.lane = 'l4'
            elif rec.student_academic in ['y3','y4','y6','y8','y9']:
                rec.lane = 'l1'
            elif rec.student_academic in ['y1','y2','y5','y7','preschool']:
                rec.lane = 'l2'
            elif rec.student_academic in ['y10','y11']:
                rec.lane = 'l3'

    @api.depends('name', 'real_car_no')
    def get_stu_info(self):
        for stu in self:
            split_char = ''
            if stu.real_car_no:
                car_no = stu.real_car_no
                lower_case = car_no.lower()
                split_char = lower_case.split('-')
                split_char1 = lower_case.split('–')
                if split_char:
                    str_carno = split_char[0] + split_char[1]
                elif split_char1:
                    str_carno = split_char1[0] + split_char1[1]
                stu.car_no = str_carno

            #     # split_char1 = lower_case[:2]
            #     # split_char2 = upper_case[2:]
            #     # print(',,,,,',split_char)
            #
            #     #***Can't read Car No. Q condition***
            #     str_carno = split_char[0] + split_char[1]
            #     list_carno = list(str_carno)
            #
            #     if list_carno[1] == 'q' or list_carno[1] == 'Q':
            #         list_carno[1] = '0'
            #         update_carno = ''.join(list_carno)
            #         result_no = update_carno
            #
            #     else:
            #         result_no = str_carno
            #
            #     stu.car_no = result_no

    # def get_car_no(self):
    #     car_no_obj = self.env['vehicle.control'].search([])
    #     for car in car_no_obj:
    #         car.tag_id = car.name.tag_ids.id
    #         if car.real_car_no:
    #             car_no = car.real_car_no
    #             lower_case = car_no.lower()
    #             split_char = lower_case.split('-')
    #
    #             # split_char1 = lower_case[:2]
    #             # split_char2 = upper_case[2:]
    #             # print(',,,,,',split_char)
    #
    #             #***Can't read Car No. Q condition***
    #             str_carno = split_char[0] + split_char[1]
    #             list_carno = list(str_carno)
    #
    #             if list_carno[1] == 'q' or list_carno[1] == 'Q':
    #                 list_carno[1] = '0'
    #                 update_carno = ''.join(list_carno)
    #                 result_no = update_carno
    #
    #             else:
    #                 result_no = str_carno
    #
    #             car.car_no = result_no
