# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
# Aktiv Software:
# - Yusuf Kapasi
# - Helly Kapatel
# - Harshil Soni
{
    "name": "User Activity Log",
    "summary": """
        The module will show the recent activity of users""",
    "description": """
        The module will show the recent activity of users""",
    "author": "Aktiv Software",
    "website": "http://www.aktivsoftware.com",
    "category": "Extra Tools",
    "version": "14.0.1.0.2",
    "license": "OPL-1",
    "price": 10.00,
    "currency": "EUR",
    # any module necessary for this one to work correctly
    "depends": ["base", "web"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/user_log_security.xml",
        "data/ir_cron.xml",
        "views/user_activity_view.xml",
        "views/custom_xml.xml",
    ],
    "qweb": ["static/src/xml/user_menu_template.xml"],
    "images": [
        "static/description/banner.jpg",
    ],
    "installable": True,
    "application": True,
}
