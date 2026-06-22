from odoo import models, fields, tools
from odoo.addons.base.models.res_partner import _tz_get


class T4GateKeeperEmployee(models.Model):
    _name = "t4.gate_keeper.employee"
    _describe = "Employee"

    name = fields.Char(
        string="Employee name",
    )

    emp_id = fields.Char(
        string="Employee ID",
    )