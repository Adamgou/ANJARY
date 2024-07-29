# coding: utf-8

from odoo import models, api

from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @staticmethod
    def _prepare_and_domain(domain):
        """
        Prepares and transforms a given domain to handle the 'or' operator.
        This method takes a domain, which is a list of criteria, and transforms it
        to properly handle the logical 'or' (|) operators if present. If the domain
        contains one or more 'or' operators without any 'and' (&) operators, the method
        attempts to simplify the domain by grouping criteria with identical values.

        :param domain: A list of tuples or lists representing the domain to be processed.
        :type domain: list
        :return: A transformed domain with the 'or' operators properly handled if necessary, otherwise returns the original unmodified domain.
        :rtype: list
        """
        if domain.count("|") >= 1 and "&" not in domain:
            # TODO: manage 'or' operator between domains
            value = None
            domain_list = list(
                filter(
                    lambda param: isinstance(param, list) or isinstance(param, tuple),
                    domain,
                )
            )
            for param in domain_list:
                value = param[-1]
                break
            if (
                value
                and len(value.split(" ")) == 2
                and all((param[-1] == value for param in domain_list))
            ):
                # processing domain
                value1, value2 = value.split(" ")
                return (
                    ["&"]
                    + ["|"] * (len(domain_list) - 1)
                    + list(map(lambda param: [param[0], param[1], value1], domain_list))
                    + ["|"] * (len(domain_list) - 1)
                    + list(map(lambda param: [param[0], param[1], value2], domain_list))
                )

            return domain
        return domain

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        domain = ProductTemplate._prepare_and_domain(domain)
        return super()._search(domain, offset, limit, order, access_rights_uid)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _prepare_and_domain_name_search(self, name):
        domain = expression.OR(
            [[("default_code", "ilike", name)], [("name", "ilike", name)]]
        )
        return ProductTemplate._prepare_and_domain(domain)

    @api.model
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        domain = domain or []
        if name:
            domain2 = self._prepare_and_domain_name_search(name)
            domain = expression.AND([domain, domain2])
            product_ids = list(self._search(domain, limit=limit, order=order))
        else:
            product_ids = self._search(domain, limit=limit, order=order)
        return product_ids
