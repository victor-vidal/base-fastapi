from enum import Enum, auto


# WE STILL NEED TO CHANGE ENUMS IN DJANGO
# TODO Redefine to a django-like TextChoices because we need a displayable version of the enum value
class BaseEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def get_choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TransactionStatus(BaseEnum):
    PROCESSING = auto()
    CANCELLED = auto()
    REVIEW = auto()
    APPROVED = auto()
    REJECTED = auto()
    FRAUD = auto()
    FRIENDLY_FRAUD = auto()
    TRADE_DISAGREEMENT = auto()
    AUTOFRAUD = auto()


class DeviceType(BaseEnum):
    MOBILE = auto()
    DESKTOP = auto()


class ScreenOrientation(str, Enum):
    PORTRAIT_PRIMARY = "portrait-primary"
    PORTRAIT_SECONDARY = "portrait-secondary"
    LANDSCAPE_PRIMARY = "landscape-primary"
    LANDSCAPE_SECONDARY = "landscape-secondary"


class DecisorAgent(BaseEnum):
    MANUAL = auto()
    ALGORITHM = auto()
    RULE = auto()
    THIRD_PARTY = auto()
    UNKNOW = auto()
    CUSTOMER = auto()
