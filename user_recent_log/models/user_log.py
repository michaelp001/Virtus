# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from werkzeug.urls import url_encode
import logging

_logger = logging.getLogger(__name__)



class UserRecentLog(models.Model):
    _name = "user.recent.log"
    _description = "User Recent Log"
    _order = "last_visited_on desc"

    def get_record_name(self):
        for activity in self:
            if activity.model and activity.res_id:
                record = self.env[activity.model].browse(activity.res_id)
                activity.name = record.name_get()[0][1]

    name = fields.Char("Record", compute="get_record_name")
    model = fields.Char("Model")
    res_id = fields.Integer("Res ID")
    last_visited_on = fields.Datetime("Last Visited On")
    user_id = fields.Many2one("res.users", "User")
    activity = fields.Text("Activity")

    @api.model
    def get_record(self, model, res_id):
        return self.env[model].sudo().browse(res_id)

    @api.model
    def get_recent_log(self, model, res_id, changes=False):
        record = self.get_record(model, res_id)
        current_time = datetime.now()
        user = self.env.user.id
        if not changes and model != "user.recent.log":
            self.sudo().create(
                {
                    "model": model,
                    "res_id": res_id,
                    "user_id": user,
                    "last_visited_on": current_time,
                }
            )
        if changes and model != "user.recent.log":
            recent_record = self.sudo().create(
                {
                    "model": model,
                    "res_id": res_id,
                    "user_id": user,
                    "last_visited_on": current_time,
                }
            )
            response_text = "Please find following User Activities: \n"
            for key, value in changes.items():
                key_value = "=".join([str(key), str(value)])
                response_text += key_value + "\n"
            if response_text and recent_record:
                recent_record.activity = response_text

    def redirect_on_record(self):
        for activity in self:
            if activity.model and activity.res_id:
                params = {
                    "model": activity.model,
                    "res_id": activity.res_id,
                }
                record = self.env[activity.model].browse(activity.res_id)
                return {
                    "type": "ir.actions.act_url",
                    "url": "/mail/view?" + url_encode(params),
                    "target": "self",
                    "target_type": "public",
                    "res_id": record.id,
                }

    @api.model
    def cron_autovacuum_user_recent_log(self, days=120):
        """ Crone Job: autovacuum user recent log.

        Auto-vacuume user recent logs after 120 days on sheduler run.

        :return: None
        """

        deadline = datetime.now() - timedelta(days=days)
        # for data_model in data_models:
        records = self.env['user.recent.log'].search(
            [("create_date", "<=", deadline)]
        )
        records.unlink()
        _logger.info("AUTOVACUUM - %d 'User Recent Log' records deleted", len(records))
        return True

