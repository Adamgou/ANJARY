from odoo import api, fields, models


class MultiCompanyAbstract(models.AbstractModel):

    _name = "multi.company.abstract"
    _description = "Multi-Company Abstract"

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        compute="_compute_company_id",
        search="_search_company_id",
        inverse="_inverse_company_id",
    )
    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        default=lambda self: self._default_company_ids(),
    )
    # TODO: Remove it following https://github.com/odoo/odoo/pull/81344
    no_company_ids = fields.Boolean(
        string="No Companies",
        compute="_compute_no_company_ids",
        compute_sudo=True,
        store=True,
        index=True,
    )

    @api.depends("company_ids")
    def _compute_no_company_ids(self):
        for record in self:
            if record.company_ids:
                record.no_company_ids = False
            else:
                record.no_company_ids = True

    def _default_company_ids(self):
        return self.browse(self.env.company.ids)

    @api.depends("company_ids")
    @api.depends_context("company")
    def _compute_company_id(self):
        for record in self:
            # Give the priority of the current company of the user to avoid
            # multi company incompatibility errors.
            company_id = self.env.context.get("force_company") or self.env.company.id
            if company_id in record.company_ids.ids:
                record.company_id = company_id
            else:
                record.company_id = record.company_ids[:1].id

    def _inverse_company_id(self):
        # To allow modifying allowed companies by non-aware base_multi_company
        # through company_id field we:
        # - Remove all companies, then add the provided one
        for record in self:
            record.company_ids = [(6, 0, record.company_id.ids)]

    def _search_company_id(self, operator, value):
        return [("company_ids", operator, value)]

    @api.model_create_multi
    def create(self, vals_list):
        """Discard changes in company_id field if company_ids has been given."""
        for vals in vals_list:
            if "company_ids" in vals and "company_id" in vals:
                del vals["company_id"]
        return super().create(vals_list)

    def write(self, vals):
        """Discard changes in company_id field if company_ids has been given."""
        if "company_ids" in vals and "company_id" in vals:
            del vals["company_id"]
        return super().write(vals)
