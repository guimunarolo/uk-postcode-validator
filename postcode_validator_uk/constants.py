import re

from .rules import (
    CentralLondonDistrict,
    DoubleDigitDistrict,
    FirstLetter,
    FourthLetter,
    LastTwoLetter,
    SecondLetter,
    SingleDigitDistrict,
    ThirdLetter,
    ZeroDistrict,
)

UK_POSTCODE_VALIDATION_REGEX = re.compile(r"^([A-Z]{1,2}[0-9][A-Z0-9]?) *([0-9][A-Z]{2})$")
UK_POSTCODE_AREA_REGEX = re.compile(r"^[A-Z]{1,2}")
UK_POSTCODE_DISTRICT_REGEX = re.compile(r"[0-9]{1,2}[A-Z]?$")
UK_POSTCODE_SECTOR_REGEX = re.compile(r"^[0-9]")
UK_POSTCODE_UNIT_REGEX = re.compile(r"[A-Z0-9]{2}$")
UK_POSTCODE_RULES_LIST = (
    CentralLondonDistrict,
    DoubleDigitDistrict,
    FirstLetter,
    FourthLetter,
    LastTwoLetter,
    SecondLetter,
    SingleDigitDistrict,
    ThirdLetter,
    ZeroDistrict,
)
