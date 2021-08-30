# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields, _
from odoo.exceptions import UserError

import socket
import time


class Scale(models.Model):
    _name = 'scale.scale'
    _description = "Scale"

    name = fields.Char(required=True)
    ip = fields.Char(required=True)
    port = fields.Integer(required=True)
    command_ask = fields.Char(required=True)
    answer_prefix = fields.Char()
    answer_time = fields.Integer(default=0, required=True, help='Time in ms')
    attempt_number = fields.Integer(default=0, required=True)
    time_between_attempt = fields.Integer(
        default=0,
        required=True,
        help='Time in ms'
    )
    uom_id = fields.Many2one(
        'uom.uom',
        required=True,
        domain="[('measure_type','=','weight')]",
    )
    last_weight = fields.Integer(readonly=True)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company,
    )

    def get_last_weight(self):
        last_weight = self.get_weight()
        self.last_weight = last_weight['value']
        return self.last_weight

    def get_weight(self):
        # TODO refactor exception handling (too returns)

        self.ensure_one()
        socket.setdefaulttimeout(self.answer_time / 1000)
        server_address = (self.ip, self.port)

        error_socket = False
        for attempt in range(self.attempt_number):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if error_socket:
                time.sleep(self.time_between_attempt / 1000)
            try:
                sock.connect(server_address)
                error_socket = False
                break
            except socket.error as error:
                error_socket = error

        if error_socket:
            return {
                "value": "----",
                "err": "%s after %d attempt(s)" % (
                    error_socket, self.attempt_number
                )
            }

        try:
            sock.settimeout(self.answer_time / 1000)
            command_ask = self.command_ask.encode()
            sock.sendall(command_ask)

            data = sock.recv(16)
            strdata = data.decode()
            if self.answer_prefix:
                if self.answer_prefix != strdata[:len(self.answer_prefix)]:
                    return {
                        "value": "----",
                        "err": _(
                            "Unexpected frame format received (%s)."
                            " Expected: '%s12345'"
                        ) % (strdata, self.answer_prefix)
                    }
                strdata = strdata[len(self.answer_prefix):]

                try:
                    data = int(strdata)
                except ValueError:
                    return {
                        "value": "----",
                        "err": _(
                            "Unexpected received number format (%s)"
                        ) % strdata
                    }

            return {
                "value": data,
                "err": False
            }

        except socket.timeout:
            return {
                "value": "----",
                "err": _("Timed out on weighing scale")
            }

        finally:
            sock.close()

    def test_get_weight(self):
        self.ensure_one()
        ret = self.get_weight()
        msg = (
            ret.get("err", False)
            or
            _("Success!! Weight read: %d") % ret["value"]
        )
        raise UserError(msg)
