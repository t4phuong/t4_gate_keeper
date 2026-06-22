from odoo import fields, models

class GateKeeperBranch(models.Model):
    _name = "t4.gate_keeper.branch"
    _description = "Gate Keeper Branch"
    _order = "name"

    name = fields.Char(
        string="Branch Name",
        required=True,
        help="Name of the branch.",
    )
    
    code = fields.Char(
        string="Branch Code",
        help="Short code for the branch.",
    )
    
    address = fields.Text(
        string="Address",
    )
    
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    
    controller_ids = fields.One2many(
        "t4.gate_keeper.controller",
        "branch_id",
        string="Controllers",
    )
