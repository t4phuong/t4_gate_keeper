# pyrefly: ignore [missing-import]
from odoo import _, fields, models

# DEVICE_ROLES = [
#     ("input", "Input"),
#     ("output", "Output"),
# ]

DEVICE_STATUS = [
    ("online", "Online"),
    ("offline", "Offline"),
    ("controller_offline", "Controller Offline"),
]


class GateKeeperDevice(models.Model):
    _name = "t4.gate_keeper.device"
    _description = "Gate Keeper Device"
    _order = "controller_id, id"

    name = fields.Char(
        string="Device Name",
        required=True,
        help="Human-readable name used to identify this device.",
    )

    controller_id = fields.Many2one(
        comodel_name="t4.gate_keeper.controller",
        string="Controller",
        required=True,
        ondelete="cascade",
        index=True,
        help="Controller that manages this device.",
    )

    branch_id = fields.Many2one(
        comodel_name="t4.gate_keeper.branch",
        related="controller_id.branch_id",
        string="Branch",
        store=True,
        readonly=True,
    )

    timezone = fields.Selection(
        related="controller_id.branch_id.timezone",
        string="Timezone",
        readonly=True,
        store=True,
    )



    area_id = fields.Many2one(
        comodel_name="t4.gate_keeper.area",
        string="Area",
        domain="[('branch_id', '=', branch_id)]",
        help="Area within the branch where this device is located.",
    )

    # device_role = fields.Selection(
    #     selection=DEVICE_ROLES,
    #     string="Device Role",
    #     required=True,
    #     help="Defines whether the device reads data or receives output commands.",
    # )

    vendor = fields.Char(
        string="Vendor",
        help="Device manufacturer, for example ZKTeco, Hikvision, or Suprema.",
    )

    device_model_id = fields.Many2one(
        comodel_name="t4.gate_keeper.device_model",
        string="Device Model",
        help="Specific model name or number of the hardware device.",
    )

    serial_number = fields.Char(
        string="Serial Number",
        copy=False,
        index=True,
        help="Physical serial number of the device.",
    )

    port_or_channel = fields.Char(
        string="Port / Channel",
        help="Physical port or channel on the controller, for example relay 1 or input 2.",
    )

    firmware_version = fields.Char(
        string="Firmware Version",
        help="Firmware version installed on the device.",
    )

    system_version = fields.Char(
        string="System Version",
        help="Operating system or embedded application version installed on the device.",
    )

    algorithm_ids = fields.Many2many(
        related="device_model_id.algorithm_ids",
        readonly=True,
        string="Supported Algorithms",
        help="Face, fingerprint, or other recognition algorithms supported by this device.",
    )

    status = fields.Selection(
        selection=DEVICE_STATUS,
        string="Status",
        default="offline",
        tracking=True,
    )

    last_seen_at = fields.Datetime(
        string="Last Seen",
        readonly=True,
        help="Last time the controller received a response from this device.",
    )

    installed_at = fields.Date(
        string="Installed On",
    )

    last_sync_at = fields.Datetime(
        string="Last Sync",
        readonly=True,
        help="Last successful permission or template synchronization.",
    )

    employee_sync_status = fields.Selection(
        selection=[
            ("synced", "Synced"),
            ("out_of_sync", "Out of Sync"),
        ],
        string="Employee Sync Status",
        compute="_compute_employee_sync_status",
        help="Indicates whether the device has synchronized the latest employee updates.",
    )

    def _compute_employee_sync_status(self):
        # Placeholder logic: Currently unhandled API, just return out_of_sync if not set
        for device in self:
            if device.last_sync_at:
                device.employee_sync_status = "synced"
            else:
                device.employee_sync_status = "out_of_sync"

    _controller_port_unique = models.Constraint(
        "UNIQUE(controller_id, port_or_channel)",
        _("Device port or channel must be unique per controller.")
    )