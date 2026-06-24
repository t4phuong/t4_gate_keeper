# pyrefly: ignore [missing-import]
from odoo import models, fields, _

SYNC_STATUS = [
    ('success', 'Success'),
    ('fail', 'Failed'),
    ('updating', 'Updating'),
]

VERIFICATION_TYPE = [
    ('face', 'Face'),
    ('fingerprint', 'Fingerprint'),
    ('card', 'Card'),
    ('password', 'Password'),
    ('other', 'Other'),
]

DIRECTION = [
    ('in', 'Check-in'),
    ('out', 'Check-out'),
]

class GateKeeperAccessLog(models.Model):
    _name = "t4.gate_keeper.access_log"
    _description = "Gate Keeper Access Log"
    _order = "access_time desc"

    controller_id = fields.Many2one(
        comodel_name="t4.gate_keeper.controller",
        string="Controller",
        required=True,
        index=True,
    )
    
    device_id = fields.Many2one(
        comodel_name="t4.gate_keeper.device",
        string="Device",
        index=True,
    )
    
    employee_id = fields.Many2one(
        comodel_name="t4.gate_keeper.employee",
        string="Employee",
        index=True,
    )
    
    access_time = fields.Datetime(
        string="Access Time",
        required=True,
        default=fields.Datetime.now,
    )
    
    direction = fields.Selection(
        selection=DIRECTION,
        string="Direction",
    )
    
    verification_type = fields.Selection(
        selection=VERIFICATION_TYPE,
        string="Verification Type",
    )
    
    sync_status = fields.Selection(
        selection=SYNC_STATUS,
        string="Sync Status",
        default="updating",
        tracking=True,
    )
    
    branch_id = fields.Many2one(
        related="controller_id.branch_id",
        string="Branch",
        store=True,
        readonly=True,
    )
