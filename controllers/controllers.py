# from odoo import http, fields
# from odoo.http import request


# class GateKeeperAPI(http.Controller):

#     @http.route('/api/heartbeat', type='http', auth='public', methods=['POST'], csrf=False)
#     def heartbeat(self, **kwargs):

#         controller_id = kwargs.get('controller_id')

#         # 1. Validate input
#         if not controller_id:
#             return request.make_json_response({
#                 'status': 'error',
#                 'message': 'missing controller_id'
#             }, status=400)

#         # 2. Find controller
#         controller = request.env['t4.gate_keeper.controller'].sudo().search([
#             ('uid', '=', controller_id)
#         ], limit=1)

#         if not controller:
#             return request.make_json_response({
#                 'status': 'error',
#                 'message': 'controller not found'
#             }, status=404)

#         # 3. Update heartbeat
#         controller._heart_bump()

#         # 4. Response
#         return request.make_json_response({
#             'status': 'ok',
#             'controller': controller.name,
#             'last_heartbeat': fields.Datetime.to_string(controller.last_heartbeat)
#         })