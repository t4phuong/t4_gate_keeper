from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    gate_keeper_controller_ids = fields.One2many(
        "t4.gate_keeper.controller",
        "company_id",
        string="Gate Keeper Controllers",
    )
