import logging

from odoo import _, fields, models
from odoo.addons.t4_coreapi.utils import endpoint, get_body, set_response
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


CONTROLLER_STATUS = [
    ("online", "Online"),
    ("offline", "Offline"),
    ("maintenance", "Maintenance"),
    ("disabled", "Disabled"),
]


class T4GateKeeperController(models.Model):
    _name = "t4.gate_keeper.controller"
    _description = "Gate Keeper Controller"
    _order = "last_heartbeat_at desc, id desc"

    name = fields.Char(
        string="Controller Name",
        required=True,
        help="Human-readable name used to identify this controller.",
    )

    serial_number = fields.Char(
        string="Serial Number",
        required=True,
        copy=False,
        index=True,
        help="Physical serial number used for maintenance and hardware replacement checks.",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    device_ids = fields.One2many(
        "t4.gate_keeper.device",
        "controller_id",
        string="Devices",
    )

    hardware_model = fields.Char(
        string="Hardware Model",
        help="Controller model or product line.",
    )

    firmware_version = fields.Char(
        string="Firmware Version",
        help="Firmware version installed on the controller.",
    )

    ip_address = fields.Char(
        string="IP Address",
        help="Connection address when the controller uses TCP/IP.",
    )

    mac_address = fields.Char(
        string="MAC Address",
        help="Hardware identifier useful when DHCP changes the IP address.",
    )

    connection_type = fields.Selection(
        selection=[
            ("tcp_ip", "TCP/IP"),
            ("rs485", "RS485"),
            ("wiegand", "Wiegand"),
        ],
        string="Connection Type",
        required=True,
        default="tcp_ip",
        help="Communication method used by this controller.",
    )

    status = fields.Selection(
        selection=CONTROLLER_STATUS,
        string="Status",
        default="offline",
        tracking=True,
    )

    last_heartbeat_at = fields.Datetime(
        string="Last Heartbeat",
        readonly=True,
        help="Last time this controller reported that it was online.",
    )

    last_sync_at = fields.Datetime(
        string="Last Sync",
        readonly=True,
        help="Last successful permission or template synchronization.",
    )

    installed_at = fields.Date(
        string="Installed On",
        help="Installation date used for maintenance planning.",
    )

    _sql_constraints = [
        (
            "serial_number_unique",
            "UNIQUE(serial_number)",
            _("Controller serial number must be unique."),
        ),
    ]

    ################################## ENDPOINT ###############################################
    @endpoint(name="ControllerHeartbeat")
    def controller_heartbeat(self):
        body = get_body()
        serial_number = body.get("serial_number", False)

        controller = self._find_heartbeat_controller(serial_number)
        if not controller:
            raise ValidationError(f"Can not find controller with serial {serial_number}")

        heartbeat_at = fields.Datetime.now()
        controller.write({
            "last_heartbeat_at": heartbeat_at,
            "status": "online",
        })


    def _find_heartbeat_controller(self, serial_number):
        return self.search([
            ("serial_number", "=", serial_number),
        ], limit=1)
