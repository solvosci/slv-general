# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import api, models, fields, registry, tools, _
from odoo.exceptions import UserError

import socket
import time

import logging
_logger = logging.getLogger(__name__)


class Scale(models.Model):
    _name = 'scale.scale'
    _description = "Scale"

    name = fields.Char(required=True)
    ip = fields.Char(required=True)
    port = fields.Integer(required=True)

    # TODO safe removal of these fields
    command_ask = fields.Char(readonly=True)
    answer_prefix = fields.Char(readonly=True)
    answer_suffix = fields.Char(readonly=True)

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
    last_weight_dt = fields.Datetime(
        readonly=True,
        string="Last Weight Datetime"
    )
    last_weight_ok = fields.Char(readonly=True)
    last_weight_error = fields.Char(readonly=True)
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

        # command_ask = (
        #     self.command_ask and
        #     self.command_ask.encode() + b'\r'
        #     or False
        # )

        frame_length = 2*8
        error_socket = False
        for attempt in range(self.attempt_number):
            if error_socket:
                time.sleep(self.time_between_attempt / 1000)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.answer_time / 1000)
                    t_ini = fields.datetime.now()
                    sock.connect(server_address)
                    # if command_ask:
                    #     sock.send(command_ask)
                    try:
                        data = b''
                        not_finished = True
                        while not_finished:
                            # We ensure at least 1 complete frame => 2 end of
                            #  frames captured
                            data += sock.recv(frame_length)
                            strdata_tmp = data.decode()
                            if len(strdata_tmp.split("\r")) >= 3:
                                not_finished = False
                        # Connection accepted and answer received
                        #  => we've finished with TCP connection and attempts
                        error_socket = False
                        ts = fields.datetime.now() - t_ini
                    except socket.timeout as st:
                        # Connection accepted, but not answer not received
                        error_socket = st
                        continue

                    try:
                        # With two end of frames captured, this split action
                        #  guarantees a complete frame
                        _logger.info("Accepted extended frame: [%s]" % data)
                        strdata = data.decode().split("\r")[1]
                        i_data = self._get_weight_process(strdata)
                        error_socket = False
                    except UserError as err:
                        # Bad format
                        _logger.error(
                            "Solved frame %s (extended [%s]) with error"
                            %
                            (strdata, data)
                        )
                        error_socket = _(
                            "Unexpected frame format received (%s): %s."
                            " Expected: '%s+ 12345\r%s'"
                        ) % (
                            str(err),
                            strdata,
                            self.answer_prefix or "",
                            self.answer_suffix or ""
                        )
                    if not error_socket:
                        success_msg = _("Attempt #%d completed in %d ms") % (
                            attempt + 1, int(1000*ts.total_seconds())
                        )
                        return {
                            "value": i_data,
                            "err": False,
                            "ok": success_msg,
                        }

            except socket.error as error:
                # Connection refused
                error_socket = error
                continue

        # If for loop is finished and return is not performed,
        #  we've reached total attempts and last error message obtained is shown
        return {
            "value": "----",
            "err": _("%s after %d attempt(s)") % (
                error_socket, self.attempt_number
            )
        }

    def _get_weight_process(self, data):
        """
        Process the frame
        """
        if len(data) != 7:
            raise UserError(_("unexpected frame lenght"))
        if data[0] not in ["+", "-"]:
            raise UserError(_("missing sign (+/-)"))
        i_sign = 1 if data[0] == "+" else -1
        try:
            idata = i_sign*int(data[1:])
        except ValueError:
            raise UserError(_("bad number format"))
        return idata

    def test_get_weight(self):
        self.ensure_one()
        ret = self.get_weight()
        msg = (
            ret.get("err", False)
            or
            _("Success!! %s\n\nWeight read: %d") % (ret["ok"], ret["value"])
        )
        raise UserError(msg)

    @api.model
    def _run_scheduler_once(self, scale_id):
        with api.Environment.manage():
            # NOT SURE OF THIS
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            scheduler_cron = self.sudo().env.ref("scale.ir_cron_scale_action")
            # Avoid to run the scheduler multiple times in the same time
            try:
                with tools.mute_logger('odoo.sql_db'):
                    self._cr.execute("SELECT id FROM ir_cron WHERE id = %s FOR UPDATE NOWAIT", (scheduler_cron.id,))
            except Exception:
                _logger.info('Attempt to run scale scheduler aborted, as already running')
                ret = {
                    "last_weight": scale_id.last_weight,
                    "last_weight_dt": scale_id.last_weight_dt,
                    "last_weight_ok": scale_id.last_weight_ok,
                    "last_weight_error": scale_id.last_weight_error,
                }
                self._cr.rollback()
                self._cr.close()
                return ret

            ret = self.sudo().run_scheduler(
                use_new_cursor=self._cr.dbname,
                scale_id=scale_id.id,
            )
            new_cr.close()
            return ret

    @api.model
    def run_scheduler(self, use_new_cursor=False, scale_id=False):
        ret = {}
        try:
            if scale_id:
                if use_new_cursor:
                    cr = registry(self._cr.dbname).cursor()
                    self = self.with_env(self.env(cr=cr))  # TDE FIXME
                scale_id = self.env["scale.scale"].sudo().browse(scale_id)
                ret = scale_id.get_weight()
                if not ret.get("err", False):
                    ret = {
                        "last_weight": ret["value"],
                        "last_weight_dt": fields.Datetime.now(),
                        "last_weight_ok": ret["ok"],
                        "last_weight_error": False,
                    }
                else:
                    ret = {
                        "last_weight_ok": False,
                        "last_weight_error": ret["err"]
                    }
                scale_id.write(ret)
                if use_new_cursor:
                    self._cr.commit()
        finally:
            if use_new_cursor and scale_id:
                try:
                    self._cr.close()
                except Exception:
                    pass
        return ret
