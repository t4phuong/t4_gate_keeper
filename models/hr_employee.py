from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_id = fields.Char(
        string="Mã số nhân viên",
        default=False
    )
    lasted_update = fields.Datetime(
        string="Ngày cập nhật",
        default=False
    )

    _sql_constraints = [
        (
            'employee_id_custom_unique',
            'UNIQUE(emp_id)',
            'employee id must be unique'
        )
    ]

    @api.model
    def write(self, vals):
        vals['lasted_update'] = fields.Datetime.now()
        return super(HrEmployee, self).write(vals)


