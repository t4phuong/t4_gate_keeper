from odoo import _, fields, models

DEVICE_ROLES = [
    ("input", "Input"),
    ("output", "Output"),
]

DEVICE_STATUS = [
    ("active", "Active"),
    ("faulty", "Faulty"),
    ("disabled", "Disabled"),
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
        related="controller_id.branch_id",
        string="Branch",
        store=True,
        readonly=True,
    )

    device_role = fields.Selection(
        selection=DEVICE_ROLES,
        string="Device Role",
        required=True,
        help="Defines whether the device reads data or receives output commands.",
    )

    vendor = fields.Char(
        string="Vendor",
        help="Device manufacturer, for example ZKTeco, Hikvision, or Suprema.",
    )

    device_model = fields.Char(
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
        "t4.gate_keeper.algorithm",
        "t4_gate_keeper_device_algorithm_rel",
        "device_id",
        "algorithm_id",
        string="Supported Algorithms",
        help="Face, fingerprint, or other recognition algorithms supported by this device.",
    )

    status = fields.Selection(
        selection=DEVICE_STATUS,
        string="Status",
        default="active",
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

    _sql_constraints = [
        (
            "controller_port_unique",
            "UNIQUE(controller_id, port_or_channel)",
            _("Device port or channel must be unique per controller."),
        ),
    ]


