from policyengine_us.model_api import *


class aca_ptc(Variable):
    value_type = float
    entity = TaxUnit
    label = "ACA premium tax credit for tax unit"
    unit = USD
    definition_period = YEAR
    reference = "https://www.law.cornell.edu/uscode/text/26/36B"
    defined_for = "is_aca_ptc_eligible"

    def formula(tax_unit, period, parameters):
        plan_cost = tax_unit("slcsp", period)
        income = tax_unit("aca_magi", period)
        applicable_figure = tax_unit(
            "aca_required_contribution_percentage", period
        )
        takes_up_aca_if_eligible = tax_unit("takes_up_aca_if_eligible", period)
        # Get minimum monthly premium contribution and convert to yearly
        min_monthly_contribution = parameters(
            period
        ).gov.aca.minimum_monthly_premium_contribution
        min_yearly_contribution = min_monthly_contribution * MONTHS_IN_YEAR
        # Calculate required contribution with minimum floor
        required_contribution = max_(
            min_yearly_contribution, income * applicable_figure
        )
        return (
            max_(0, plan_cost - required_contribution)
            * takes_up_aca_if_eligible
        )
