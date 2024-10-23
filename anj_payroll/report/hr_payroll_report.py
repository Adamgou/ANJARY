# -*- coding: utf-8 -*-

from odoo import fields, models


class HrPayrollReport(models.Model):
    _inherit = "hr.payroll.report"

    idemnlog_wage = fields.Float("Indemnités transport", readonly=True)
    idemnrepas_wage = fields.Float("Indemnités repas", readonly=True)
    out_wage = fields.Float("Retenues pour absence", readonly=True)
    absmal2_wage = fields.Float("Congés maternité", readonly=True)
    primqu01_wage = fields.Float("Prime conditionnelle", readonly=True)
    primeass01_wage = fields.Float("Prime trimestrielle", readonly=True)
    primeperf01_wage = fields.Float("Prime exceptionnelle", readonly=True)
    preav01_wage = fields.Float("Préavis", readonly=True)
    idemn01_wage = fields.Float("Licenciement", readonly=True)
    indemn02_wage = fields.Float(
        "Indemnité compensatrice de congé non prise", readonly=True
    )

    compcong01_wage = fields.Float("Compensatrice de Congés payés", readonly=True)
    cnaps_ps_wage = fields.Float("CNAPS (part salariale)", readonly=True)
    cnaps_pp_wage = fields.Float("CNaPS (part patronale)", readonly=True)
    ostie_ps_wage = fields.Float("OSTIE (part salariale)", readonly=True)
    ostie_pp_wage = fields.Float("OSTIE (part patronale)", readonly=True)
    fmfp_wage = fields.Float("FMFP", readonly=True)
    simpo_wage = fields.Float("SALAIRE IMPOSABLE", readonly=True)
    childnum_wage = fields.Float("Nombre enfant", readonly=True)
    irsa01_wage = fields.Float("IRSA", readonly=True)
    irsa03_wage = fields.Float("IRSA intermediaire", readonly=True)

    irsa02_wage = fields.Float("IRSA à payer", readonly=True)
    fraisbanc_wage = fields.Float("Frais bancaire", readonly=True)
    paid_sick_leave_total = fields.Float("Congés maladie payé (Total)", readonly=True)
    alloc_wage = fields.Float("Allocation familiale", readonly=True)
    alloc_wage_base = fields.Float("Allocation familiale (Base)", readonly=True)
    ava15_wage = fields.Float("Avance sur salaire du 15", readonly=True)
    avansp_wage = fields.Float("Avance spéciale", readonly=True)
    rbstcnaps_wage = fields.Float("Remboursement CNAPS", readonly=True)
    totpopcom_wage = fields.Float("Total opérations complémentaires", readonly=True)
    ajustnet_wage = fields.Float("Ajustement de salaire net", readonly=True)
    gross_gross_wage = fields.Float("Salaire brut réel", readonly=True)
    allocp_wage = fields.Float("Allocation des Congés payés", readonly=True)
    abs_wage = fields.Float("Absences", readonly=True)
    tnh30_wage = fields.Float("TNH à 30%", readonly=True)
    tnh50_wage = fields.Float("TNH à 50%", readonly=True)
    tdim40_wage = fields.Float("Travail de Dimanche 40%", readonly=True)
    hsupp100_wage = fields.Float("T.jours férié à 100%", readonly=True)
    hsupp130_wage = fields.Float("HS à 130%", readonly=True)
    hsupp150_wage = fields.Float("HS à 150%", readonly=True)
    hsuppexo30_wage = fields.Float("HS à 130% (20h éxonéré)", readonly=True)
    hsuppexo50_wage = fields.Float("HS à 150% (20h éxonéré)", readonly=True)
    totalhsexo_wage = fields.Float("TOTAL avec HS éxonéré de IRSA (20h)", readonly=True)
    net_net_wage = fields.Float("SALAIRE NET", readonly=True)
    net_salary = fields.Float("SALAIRE NET À PAYER", readonly=True)
    # base
    allocp_wage_base = fields.Float("Allocation des Congés payés (Base)", readonly=True)
    absmal3_wage_base = fields.Float("Congés maternité CNaPs (Base)", readonly=True)
    basic_wage_base = fields.Float("Salaire de Base (Base)", readonly=True)
    abs_wage_base = fields.Float("Absences (Base)", readonly=True)
    tnh30_wage_base = fields.Float("TNH à 30% (Base)", readonly=True)
    tnh50_wage_base = fields.Float("TNH à 50% (Base)", readonly=True)
    tdim40_wage_base = fields.Float("Travail de Dimanche 40% (Base)", readonly=True)
    hsupp100_wage_base = fields.Float("T.jours férié à 100% (Base)", readonly=True)
    hsupp130_wage_base = fields.Float("HS à 130% (Base)", readonly=True)
    hsupp150_wage_base = fields.Float("HS à 150% (Base)", readonly=True)
    hsuppexo30_wage_base = fields.Float("HS à 130% (20h éxonéré) (Base)", readonly=True)
    hsuppexo50_wage_base = fields.Float("HS à 150% (20h éxonéré) (Base)", readonly=True)
    totalhsexo_wage_base = fields.Float(
        "TOTAL avec HS éxonéré de IRSA (20h) (Base)", readonly=True
    )
    cnaps_ps_wage_base = fields.Float("CNAPS (part salariale) (Base)", readonly=True)
    cnaps_pp_wage_base = fields.Float("CNaPS (part patronale) (Base)", readonly=True)
    ostie_ps_wage_base = fields.Float("OSTIE (part salariale) (Base)", readonly=True)
    ostie_pp_wage_base = fields.Float("OSTIE (part patronale) (Base)", readonly=True)
    fmfp_wage_base = fields.Float("FMFP (Base)", readonly=True)
    simpo_wage_base = fields.Float("SALAIRE IMPOSABLE (Base)", readonly=True)
    childnum_wage = fields.Float("Déduction impot (Base)", readonly=True)
    irsa01_wage_base = fields.Float("IRSA (Base)", readonly=True)
    irsa03_wage_base = fields.Float("IRSA intermediaire (Base)", readonly=True)

    irsa02_wage_base = fields.Float("IRSA à payer (Base)", readonly=True)
    net_wage_base = fields.Float("NET A PAYER (Base)", readonly=True)
    net_net_wage_base = fields.Float("SALAIRE NET (Base)", readonly=True)
    paid_sick_leave_base = fields.Float("Congés maladie payés (Base)", readonly=True)

    # nombre
    allocp_wage_number = fields.Float(
        "Allocation des Congés payés (Nombre)", readonly=True
    )
    absmal3_number = fields.Float("Congés maternité CNaPs (Nombre)", readonly=True)
    abs_wage_number = fields.Float("Absences (Nombre)", readonly=True)
    paid_sick_number = fields.Float("Congés maladie payés (Nombre)", readonly=True)
    public_holidays_not_worked_and_paid = fields.Float(
        "Jours fériés non travaillés et payés", readonly=True
    )
    public_holidays_not_worked_and_paid_number = fields.Float(
        "Jours fériés non travaillés et payés(Nombre)", readonly=True
    )
    public_holidays_not_worked_and_paid_base = fields.Float(
        "Jours fériés non travaillés et payés(Base)", readonly=True
    )

    def _select(self, additional_rules):
        return (
            super()._select(additional_rules)
            + """,
                CASE WHEN wd.id = min_id.min_line THEN idemnlog.total ELSE 0 END as idemnlog_wage,
                CASE WHEN wd.id = min_id.min_line THEN idemnrepas.total ELSE 0 END as idemnrepas_wage,
                CASE WHEN wd.id = min_id.min_line THEN out.total ELSE 0 END as out_wage,
                CASE WHEN wd.id = min_id.min_line THEN absmal2.total ELSE 0 END as absmal2_wage,
                CASE WHEN wd.id = min_id.min_line THEN primqu01.total ELSE 0 END as primqu01_wage,
                CASE WHEN wd.id = min_id.min_line THEN primeass01.total ELSE 0 END as primeass01_wage,
                CASE WHEN wd.id = min_id.min_line THEN primeperf01.total ELSE 0 END as primeperf01_wage,
                CASE WHEN wd.id = min_id.min_line THEN preav01.total ELSE 0 END as preav01_wage,
                CASE WHEN wd.id = min_id.min_line THEN idemn01.total ELSE 0 END as idemn01_wage,
                CASE WHEN wd.id = min_id.min_line THEN indemn02.total ELSE 0 END as indemn02_wage,
                CASE WHEN wd.id = min_id.min_line THEN compcong01.total ELSE 0 END as compcong01_wage,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_ps.total ELSE 0 END as cnaps_ps_wage,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_pp.total ELSE 0 END as cnaps_pp_wage,
                CASE WHEN wd.id = min_id.min_line THEN ostie_ps.total ELSE 0 END as ostie_ps_wage,
                CASE WHEN wd.id = min_id.min_line THEN ostie_pp.total ELSE 0 END as ostie_pp_wage,
                CASE WHEN wd.id = min_id.min_line THEN fmfp.total ELSE 0 END as fmfp_wage,
                CASE WHEN wd.id = min_id.min_line THEN fmfpbase.base ELSE 0 END as fmfp_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN simpo.total ELSE 0 END as simpo_wage,
                CASE WHEN wd.id = min_id.min_line THEN simpobase.base ELSE 0 END as simpo_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN childnum.total ELSE 0 END as childnum_wage,
                CASE WHEN wd.id = min_id.min_line THEN childnumbase.base ELSE 0 END as childnum_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN irsa01.total ELSE 0 END as irsa01_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa03.total ELSE 0 END as irsa03_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa02.total ELSE 0 END as irsa02_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa01base.base ELSE 0 END as irsa01_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN irsa03base.base ELSE 0 END as irsa03_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN irsa02base.base ELSE 0 END as irsa02_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN fraisbanc.total ELSE 0 END as fraisbanc_wage,
                CASE WHEN wd.id = min_id.min_line THEN paidsickleavetotal.total ELSE 0 END as paid_sick_leave_total,
                CASE WHEN wd.id = min_id.min_line THEN alloc.total ELSE 0 END as alloc_wage,
                CASE WHEN wd.id = min_id.min_line THEN allocbase.base ELSE 0 END as alloc_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN ava15.total ELSE 0 END as ava15_wage,
                CASE WHEN wd.id = min_id.min_line THEN avansp.total ELSE 0 END as avansp_wage,
                CASE WHEN wd.id = min_id.min_line THEN rbstcnaps.total ELSE 0 END as rbstcnaps_wage,
                CASE WHEN wd.id = min_id.min_line THEN totpopcom.total ELSE 0 END as totpopcom_wage,
                CASE WHEN wd.id = min_id.min_line THEN ajustnet.total ELSE 0 END as ajustnet_wage,
                CASE WHEN wd.id = min_id.min_line THEN gross.total ELSE 0 END as gross_gross_wage,
                CASE WHEN wd.id = min_id.min_line THEN allocp.total ELSE 0 END as allocp_wage,
                CASE WHEN wd.id = min_id.min_line THEN allocpnbr.nombre ELSE 0 END as allocp_wage_number,
                CASE WHEN wd.id = min_id.min_line THEN absmal3nbr.nombre ELSE 0 END as absmal3_number,
                CASE WHEN wd.id = min_id.min_line THEN allocpbase.base ELSE 0 END as allocp_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN absmal3base.base ELSE 0 END as absmal3_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN basicbase.base ELSE 0 END as basic_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN abs.total ELSE 0 END as abs_wage,
                CASE WHEN wd.id = min_id.min_line THEN absbase.base ELSE 0 END as abs_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN absnbr.nombre ELSE 0 END as abs_wage_number,
                CASE WHEN wd.id = min_id.min_line THEN paidsicknbr.nombre ELSE 0 END as paid_sick_number,
                CASE WHEN wd.id = min_id.min_line THEN tnh30.total ELSE 0 END as tnh30_wage,
                CASE WHEN wd.id = min_id.min_line THEN tnh30base.base ELSE 0 END as tnh30_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN tnh50.total ELSE 0 END as tnh50_wage,
                CASE WHEN wd.id = min_id.min_line THEN tnh50base.base ELSE 0 END as tnh50_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN tdim40.total ELSE 0 END as tdim40_wage,
                CASE WHEN wd.id = min_id.min_line THEN tdim40base.base ELSE 0 END as tdim40_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN hsupp100.total ELSE 0 END as hsupp100_wage,
                CASE WHEN wd.id = min_id.min_line THEN hsupp100base.base ELSE 0 END as hsupp100_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN hsupp130.total ELSE 0 END as hsupp130_wage,
                CASE WHEN wd.id = min_id.min_line THEN hsupp130base.base ELSE 0 END as hsupp130_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN hsupp150.total ELSE 0 END as hsupp150_wage,
                CASE WHEN wd.id = min_id.min_line THEN hsupp150base.base ELSE 0 END as hsupp150_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN hsuppexo30.total ELSE 0 END as hsuppexo30_wage,
                CASE WHEN wd.id = min_id.min_line THEN hsuppexo30base.base ELSE 0 END as hsuppexo30_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN hsuppexo50.total ELSE 0 END as hsuppexo50_wage,
                CASE WHEN wd.id = min_id.min_line THEN hsuppexo50base.base ELSE 0 END as hsuppexo50_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN totalhsexo.total ELSE 0 END as totalhsexo_wage,
                CASE WHEN wd.id = min_id.min_line THEN totalhsexobase.base ELSE 0 END as totalhsexo_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_psbase.base ELSE 0 END as cnaps_ps_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_ppbase.base ELSE 0 END as cnaps_pp_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN ostie_psbase.base ELSE 0 END as ostie_ps_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN ostie_ppbase.base ELSE 0 END as ostie_pp_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN netbase.base ELSE 0 END as net_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN netnet.total ELSE 0 END as net_net_wage,
                CASE WHEN wd.id = min_id.min_line THEN netnetbase.base ELSE 0 END as net_net_wage_base,
                CASE WHEN wd.id = min_id.min_line THEN netsalary.total ELSE 0 END as net_salary,
                CASE WHEN wd.id = min_id.min_line THEN paidsickbase.base ELSE 0 END as paid_sick_leave_base,
                CASE WHEN wd.id = min_id.min_line THEN publicholidaysnotworked.total ELSE 0 END as public_holidays_not_worked_and_paid,
                CASE WHEN wd.id = min_id.min_line THEN publicholidaysnotworkednumber.nombre ELSE 0 END as public_holidays_not_worked_and_paid_number,
                CASE WHEN wd.id = min_id.min_line THEN publicholidaysnotworkedbase.base ELSE 0 END as public_holidays_not_worked_and_paid_base
                """
        )

    def _from(self, additional_rules):
        return (
            super()._from(additional_rules)
            + """
                left join hr_payslip_line idemnlog on (idemnlog.slip_id = p.id and idemnlog.code = 'INDEMNLOG')
                left join hr_payslip_line idemnrepas on (idemnrepas.slip_id = p.id and idemnrepas.code = 'INDEMNREPAS')
                left join hr_payslip_line out on (out.slip_id = p.id and out.code = 'OUT')
                left join hr_payslip_line absmal2 on (absmal2.slip_id = p.id and absmal2.code = 'ABSMAL2')
                left join hr_payslip_line primqu01 on (primqu01.slip_id = p.id and primqu01.code = 'PRIMQU01')
                left join hr_payslip_line primeass01 on (primeass01.slip_id = p.id and primeass01.code = 'PRIMEASS01')
                left join hr_payslip_line primeperf01 on (primeperf01.slip_id = p.id and primeperf01.code = 'PRIMEPERF01')
                left join hr_payslip_line preav01 on (preav01.slip_id = p.id and preav01.code = 'PREAV01')
                left join hr_payslip_line idemn01 on (idemn01.slip_id = p.id and idemn01.code = 'INDEMN01')
                left join hr_payslip_line indemn02 on (indemn02.slip_id = p.id and indemn02.code = 'INDEMN02')
                left join hr_payslip_line compcong01 on (compcong01.slip_id = p.id and compcong01.code = 'COMPCONG01')
                left join hr_payslip_line cnaps_ps on (cnaps_ps.slip_id = p.id and cnaps_ps.code = 'CNaPS - PS')
                left join hr_payslip_line cnaps_pp on (cnaps_pp.slip_id = p.id and cnaps_pp.code = 'CNaPS - PP')
                left join hr_payslip_line ostie_ps on (ostie_ps.slip_id = p.id and ostie_ps.code = 'OSTIE - PS')
                left join hr_payslip_line ostie_pp on (ostie_pp.slip_id = p.id and ostie_pp.code = 'OSTIE - PP')
                left join hr_payslip_line fmfp on (fmfp.slip_id = p.id and fmfp.code = 'FMFP')
                left join hr_payslip_line fmfpbase on (fmfpbase.slip_id = p.id and fmfpbase.code = 'FMFP')
                left join hr_payslip_line simpo on (simpo.slip_id = p.id and simpo.code = 'SIMPO')
                left join hr_payslip_line simpobase on (simpobase.slip_id = p.id and simpobase.code = 'SIMPO')
                left join hr_payslip_line childnum on (childnum.slip_id = p.id and childnum.code = 'CHILDNUM')
                left join hr_payslip_line childnumbase on (childnumbase.slip_id = p.id and childnumbase.code = 'CHILDNUM')
                left join hr_payslip_line irsa01 on (irsa01.slip_id = p.id and irsa01.code = 'IRSA01')
                left join hr_payslip_line irsa03 on (irsa03.slip_id = p.id and irsa03.code = 'IRSA03')
                left join hr_payslip_line irsa02 on (irsa02.slip_id = p.id and irsa02.code = 'IRSA02')
                left join hr_payslip_line irsa01base on (irsa01base.slip_id = p.id and irsa01base.code = 'IRSA01')
                left join hr_payslip_line irsa03base on (irsa03base.slip_id = p.id and irsa03base.code = 'IRSA03')
                left join hr_payslip_line irsa02base on (irsa02base.slip_id = p.id and irsa02base.code = 'IRSA02')
                left join hr_payslip_line fraisbanc on (fraisbanc.slip_id = p.id and fraisbanc.code = 'FRAISBANC')
                left join hr_payslip_line paidsickleavetotal on (paidsickleavetotal.slip_id = p.id and paidsickleavetotal.code = 'MALA')
                left join hr_payslip_line alloc on (alloc.slip_id = p.id and alloc.code = 'ALLOC')
                left join hr_payslip_line allocbase on (allocbase.slip_id = p.id and allocbase.code = 'ALLOC')
                left join hr_payslip_line ava15 on (ava15.slip_id = p.id and ava15.code = 'AVA15')
                left join hr_payslip_line avansp on (avansp.slip_id = p.id and avansp.code = 'AVANSP')
                left join hr_payslip_line rbstcnaps on (rbstcnaps.slip_id = p.id and rbstcnaps.code = 'RBSTCNAPS')
                left join hr_payslip_line totpopcom on (totpopcom.slip_id = p.id and totpopcom.code = 'TOTPOPCOM')
                left join hr_payslip_line ajustnet on (ajustnet.slip_id = p.id and ajustnet.code = 'AJUSTNET')
                left join hr_payslip_line gross on (gross.slip_id = p.id and gross.code = 'SBRUT')
                left join hr_payslip_line allocp on (allocp.slip_id = p.id and allocp.code = 'ALLOCP')
                left join hr_payslip_line allocpbase on (allocpbase.slip_id = p.id and allocpbase.code = 'ALLOCP')
                left join hr_payslip_line absmal3base on (absmal3base.slip_id = p.id and absmal3base.code = 'ABSMAL3')
                left join hr_payslip_line allocpnbr on (allocpnbr.slip_id = p.id and allocpnbr.code = 'ALLOCP')
                left join hr_payslip_line absmal3nbr on (absmal3nbr.slip_id = p.id and absmal3nbr.code = 'ABSMAL3')
                left join hr_payslip_line basicbase on (basicbase.slip_id = p.id and basicbase.code = 'BASIC')
                left join hr_payslip_line abs on (abs.slip_id = p.id and abs.code = 'ABSC')
                left join hr_payslip_line absbase on (absbase.slip_id = p.id and absbase.code = 'ABSC')
                left join hr_payslip_line absnbr on (absnbr.slip_id = p.id and absnbr.code = 'ABSC')
                left join hr_payslip_line paidsicknbr on (paidsicknbr.slip_id = p.id and paidsicknbr.code = 'MALA')
                left join hr_payslip_line tnh30 on (tnh30.slip_id = p.id and tnh30.code = 'TNH30')
                left join hr_payslip_line tnh30base on (tnh30base.slip_id = p.id and tnh30base.code = 'TNH30')
                left join hr_payslip_line tnh50 on (tnh50.slip_id = p.id and tnh50.code = 'TNH50')
                left join hr_payslip_line tnh50base on (tnh50base.slip_id = p.id and tnh50base.code = 'TNH50')
                left join hr_payslip_line tdim40 on (tdim40.slip_id = p.id and tdim40.code = 'TDIM40')
                left join hr_payslip_line tdim40base on (tdim40base.slip_id = p.id and tdim40base.code = 'TDIM40')
                left join hr_payslip_line hsupp100 on (hsupp100.slip_id = p.id and hsupp100.code = 'HSUPP100')
                left join hr_payslip_line hsupp100base on (hsupp100base.slip_id = p.id and hsupp100base.code = 'HSUPP100')
                left join hr_payslip_line hsupp130 on (hsupp130.slip_id = p.id and hsupp130.code = 'HSUPP130')
                left join hr_payslip_line hsupp130base on (hsupp130base.slip_id = p.id and hsupp130base.code = 'HSUPP130')
                left join hr_payslip_line hsupp150 on (hsupp150.slip_id = p.id and hsupp150.code = 'HSUPP150')
                left join hr_payslip_line hsupp150base on (hsupp150base.slip_id = p.id and hsupp150base.code = 'HSUPP150')
                left join hr_payslip_line hsuppexo30 on (hsuppexo30.slip_id = p.id and hsuppexo30.code = 'HSUPPEXO30')
                left join hr_payslip_line hsuppexo30base on (hsuppexo30base.slip_id = p.id and hsuppexo30base.code = 'HSUPPEXO30')
                left join hr_payslip_line hsuppexo50 on (hsuppexo50.slip_id = p.id and hsuppexo50.code = 'HSUPPEXO50')
                left join hr_payslip_line hsuppexo50base on (hsuppexo50base.slip_id = p.id and hsuppexo50base.code = 'HSUPPEXO50')
                left join hr_payslip_line totalhsexo on (totalhsexo.slip_id = p.id and totalhsexo.code = 'TOTALHSEXO')
                left join hr_payslip_line totalhsexobase on (totalhsexobase.slip_id = p.id and totalhsexobase.code = 'TOTALHSEXO')
                left join hr_payslip_line cnaps_psbase on (cnaps_psbase.slip_id = p.id and cnaps_psbase.code = 'CNaPS - PS')
                left join hr_payslip_line cnaps_ppbase on (cnaps_ppbase.slip_id = p.id and cnaps_ppbase.code = 'CNaPS - PP')
                left join hr_payslip_line ostie_psbase on (ostie_psbase.slip_id = p.id and ostie_psbase.code = 'OSTIE - PS')
                left join hr_payslip_line ostie_ppbase on (ostie_ppbase.slip_id = p.id and ostie_ppbase.code = 'OSTIE - PP')
                left join hr_payslip_line netbase on (netbase.slip_id = p.id and netbase.code = 'NET')
                left join hr_payslip_line netnet on (netnet.slip_id = p.id and netnet.code = 'SALNET')
                left join hr_payslip_line netnetbase on (netnetbase.slip_id = p.id and netnetbase.code = 'SALNET')
                left join hr_payslip_line netsalary on (netsalary.slip_id = p.id and netsalary.code = 'SALNETAP')
                left join hr_payslip_line paidsickbase on (paidsickbase.slip_id = p.id and paidsickbase.code = 'MALA')
                left join hr_payslip_line publicholidaysnotworked on (publicholidaysnotworked.slip_id = p.id and publicholidaysnotworked.code = 'FERIE')
                left join hr_payslip_line publicholidaysnotworkednumber on (publicholidaysnotworkednumber.slip_id = p.id and publicholidaysnotworkednumber.code = 'FERIE')
                left join hr_payslip_line publicholidaysnotworkedbase on (publicholidaysnotworkedbase.slip_id = p.id and publicholidaysnotworkedbase.code = 'FERIE')
                """
        )

    def _group_by(self, additional_rules):
        return (
            super()._group_by(additional_rules)
            + """,
                idemnlog.total,
                idemnrepas.total,
                out.total,
                absmal2.total,
                primqu01.total,
                primeass01.total,
                primeperf01.total,
                preav01.total,
                idemn01.total,
                indemn02.total,
                compcong01.total,
                cnaps_ps.total,
                cnaps_pp.total,
                ostie_ps.total,
                ostie_pp.total,
                fmfp.total,
                fmfpbase.base,
                simpo.total,
                simpobase.base,
                childnum.total,
                childnumbase.base,
                irsa01.total,
                irsa03.total,
                irsa02.total,
                irsa01base.base,
                irsa03base.base,
                irsa02base.base,
                fraisbanc.total,
                paidsickleavetotal.total,
                alloc.total,
                allocbase.base,
                ava15.total,
                avansp.total,
                rbstcnaps.total,
                totpopcom.total,
                ajustnet.total,
                gross.total,
                allocp.total,
                allocpbase.base,
                absmal3base.base,
                allocpnbr.nombre,
                absmal3nbr.nombre,
                basicbase.base,
                abs.total,
                absbase.base,
                absnbr.nombre,
                paidsicknbr.nombre,
                tnh30.total,
                tnh30base.base,
                tnh50.total,
                tnh50base.base,
                tdim40.total,
                tdim40base.base,
                hsupp100.total,
                hsupp100base.base,
                hsupp130.total,
                hsupp130base.base,
                hsupp150.total,
                hsupp150base.base,
                hsuppexo30.total,
                hsuppexo30base.base,
                hsuppexo50.total,
                hsuppexo50base.base,
                totalhsexo.total,
                totalhsexobase.base,
                cnaps_psbase.base,
                cnaps_ppbase.base,
                ostie_psbase.base,
                ostie_ppbase.base,
                netbase.base,
                netnet.total,
                netnetbase.base,
                netsalary.total,
                paidsickbase.base,
                publicholidaysnotworked.total,
                publicholidaysnotworkednumber.nombre,
                publicholidaysnotworkedbase.base
                """
        )
