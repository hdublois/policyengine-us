from policyengine_us.model_api import *


class slcsp_family_tier_applies(Variable):
    value_type = bool
    entity = TaxUnit
    label = "ACA family tier applies, rather than age curves"
    definition_period = MONTH

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.aca
        # Use state_code_str to avoid StateGroup enum validation bug
        state_code_str = tax_unit.household("state_code_str", period)
        # Use bracket notation for array indexing instead of getattr
        return p.family_tier_states[state_code_str]
