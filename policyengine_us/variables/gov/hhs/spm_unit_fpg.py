from policyengine_us.model_api import *


class spm_unit_fpg(Variable):
    value_type = float
    entity = SPMUnit
    label = "SPM unit's federal poverty guideline"
    definition_period = YEAR
    unit = USD

    def formula(spm_unit, period, parameters):
        n = spm_unit("spm_unit_size", period)
        # Use the computed enum `state_group` rather than `state_group_str`.
        # Some datasets include a raw `state_group_str` input with state codes
        # (e.g. "CA"), which then fails parameter indexing for `gov.hhs.fpg`
        # (expects StateGroup values like "CONTIGUOUS_US", "AK", "HI", etc.).
        state_group = spm_unit.household("state_group", period).decode_to_str()
        p_fpg = parameters(period).gov.hhs.fpg
        p1 = p_fpg.first_person[state_group]
        pn = p_fpg.additional_person[state_group]
        return p1 + pn * (n - 1)
