from policyengine_us.model_api import *


class StateGroup(Enum):
    CONTIGUOUS_US = "Contiguous US"
    AK = "Alaska"
    HI = "Hawaii"
    GU = "Guam"
    PR = "Puerto Rico"
    VI = "Virgin Islands"
    # Omit other territories for now.


class state_group(Variable):
    value_type = Enum
    possible_values = StateGroup
    default_value = StateGroup.CONTIGUOUS_US
    entity = Household
    label = "State group"
    definition_period = YEAR

    def formula(household, period, parameters):
        NON_CONTIGUOUS_STATES = ("AK", "HI", "GU", "PR", "VI")
        state_code = household("state_code", period).decode_to_str()
        # `StateGroup.encode` raises on invalid values. Since we pass a full
        # vector to numpy `where` (which evaluates both branches), we normalize
        # contiguous states to `CONTIGUOUS_US` first so encoding is safe.
        non_contiguous_mask = np.isin(state_code, NON_CONTIGUOUS_STATES)
        normalized_state_code = np.where(
            non_contiguous_mask,
            state_code,
            "CONTIGUOUS_US",
        )
        return StateGroup.encode(normalized_state_code).decode()
