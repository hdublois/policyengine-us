from policyengine_us.model_api import *
from policyengine_core.simulations import Simulation


class slcsp_age_0(Variable):
    value_type = float
    entity = Household
    label = "Second-lowest ACA silver-plan for a person aged 0"
    unit = USD
    definition_period = MONTH

    def formula(household, period, parameters):
        # Get state code as string and rating area
        # Use state_code_str (string variable) to avoid StateGroup enum validation bug
        state_code_str = household("state_code_str", period)
        rating_area = household("slcsp_rating_area", period)

        # Access the baseline costs from parameters
        p = parameters(period).gov.aca
        state_rating_param = p.state_rating_area_cost

        # Access parameter using bracket notation with state code string array
        # PolicyEngine parameter nodes support array indexing
        state_node = state_rating_param[state_code_str]
        return state_node[rating_area]
