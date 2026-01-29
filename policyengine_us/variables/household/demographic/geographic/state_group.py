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
        # Map state codes to StateGroup enum names (strings)
        # Contiguous states -> "CONTIGUOUS_US", non-contiguous -> their state code (which matches enum name)
        enum_names = np.where(
            np.isin(state_code, NON_CONTIGUOUS_STATES),
            state_code,  # "AK", "HI", etc. - these match StateGroup enum names
            "CONTIGUOUS_US"  # Contiguous states map to CONTIGUOUS_US enum name
        )
        # Now encode - all values in enum_names are valid StateGroup enum names
        return StateGroup.encode(enum_names).decode()
