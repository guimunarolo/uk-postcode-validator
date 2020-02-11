import re

from .exceptions import InvalidPostcode


class PostcodeRule:
    attr_applied = None
    applied_areas_regex = None
    rule_regex = None

    def __init__(self, postcode):
        self.postcode = postcode

    def validate(self):
        postcode_attr_value = getattr(self.postcode, self.attr_applied, None)
        if not postcode_attr_value:
            raise AttributeError(f"This entity has not attr {self.attr_applied}")

        if not self.applied_areas_regex.match(postcode_attr_value):
            return

        if not self.rule_regex.match(postcode_attr_value):
            raise InvalidPostcode


class SingleDigitDistrict(PostcodeRule):
    """
    Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE
    (although WC is always subdivided by a further letter, e.g. WC1A)
    """

    attr_applied = "outward"
    applied_areas_regex = re.compile(r"^(BR|FY|HA|HD|HG|HR|HS|HX|JE|LD|SM|SR|WC|WN|ZE)")
    rule_regex = re.compile(r"^(?!WC)[A-Z]{2}[0-9]$|^WC[0-9][A-Z]$")


class DoubleDigitDistrict(PostcodeRule):
    """Areas with only double-digit districts: AB, LL, SO"""

    attr_applied = "outward"
    applied_areas_regex = re.compile(r"^(AB|LL|SO)")
    rule_regex = re.compile(r"^[A-Z]{2}[0-9]{2}$")


class ZeroOrTenDistrict(PostcodeRule):
    """
    Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS
    (BS is the only area to have both a district 0 and a district 10)
    """

    attr_applied = "outward"
    applied_areas_regex = re.compile(r"^(BL|BS|CM|CR|FY|HA|PR|SL|SS)")
    rule_regex = re.compile(r"^[A-Z]{2}0$|^BS10$")


class CentralLondonDistrict(PostcodeRule):
    """
    The following central London single-digit districts have been further divided by inserting a letter after
    the digit and before the space: EC1–EC4 (but not EC50), SW1, W1, WC1, WC2 and parts of E1 (E1W),
    N1 (N1C and N1P), NW1 (NW1W) and SE1 (SE1P).
    """

    attr_applied = "outward"
    applied_areas_regex = re.compile(r"^(EC|E1|N1|NW1|SE1|SW1|W1|WC1|WC2)")
    rule_regex = re.compile(
        r"^EC[1-4][A-Z]$|^E1W$|^N1[C|P]$|^NW1W$|^SE1P$|^SW1[A-Z]$|^W1[A-Z]$|^WC[1-2][A-Z]$"
    )
