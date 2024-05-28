# -*- coding: utf-8 -*-

from . import models


import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.base_multi_company import hooks
except ImportError:
    _logger.info("Cannot find `base_multi_company` module in addons path.")


def post_init_hook(env):
    try:
        hooks.post_init_hook(
            env,
            "product.product_comp_rule",
            "product.template",
        )
    except NameError:
        _logger.exception("Hooks is not defined")


def uninstall_hook(env):
    try:
        hooks.uninstall_hook(
            env,
            "product.product_comp_rule",
        )
    except NameError:
        _logger.exception("Hooks is not defined")
