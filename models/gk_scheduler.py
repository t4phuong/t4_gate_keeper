from odoo import models, fields, api
from datetime import timedelta

WAITING_TIME = 5

class T4GateKeeperScheduler(models.Model):
    _name = 't4.gate_keeper.scheduler'
    _description = 'Gate Keeper Scheduler'

    @api.model
    def cron_update_controller_status(self):
        timeout = fields.Datetime.now() - timedelta(minutes=5)

        controllers = self.env['t4.gate_keeper.controller']

        online = controllers.search([
            ('last_heartbeat_at', '>=', timeout)
        ])
        online.write({'status': 'online'})

        offline = controllers.search([
            '|',
            ('last_heartbeat_at', '=', False),
            ('last_heartbeat_at', '<', timeout)
        ])
        offline.write({'status': 'offline'})
