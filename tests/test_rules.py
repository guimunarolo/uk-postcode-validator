import re
import string
from unittest import mock

import pytest
from postcode_validator_uk.exceptions import InvalidPostcode
from postcode_validator_uk.rules import (
    CentralLondonDistrict,
    DoubleDigitDistrict,
    FirstLetter,
    FourthLetter,
    LastTwoLetter,
    PostcodeRule,
    SecondLetter,
    SingleDigitDistrict,
    ThirdLetter,
    ZeroDistrict,
)

SINGLE_DIGIT_DISTRICTS_AREAS = (
    "BR",
    "FY",
    "HA",
    "HD",
    "HG",
    "HR",
    "HS",
    "HX",
    "JE",
    "LD",
    "SM",
    "SR",
    "WC",
    "WN",
    "ZE",
)
DOUBLE_DIGIT_DISTRICTS_AREAS = ("AB", "LL", "SO")
ZERO_DISTRICTS_AREAS = ("BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS")


class TestPostcodeRule:
    def test_validation_raises_attr_error_without_required_attr(self):
        PostcodeRule.attr_applied = "outward"

        postcode = mock.Mock(outward=None)

        with pytest.raises(AttributeError):
            rule = PostcodeRule(postcode)
            rule.validate()

    def test_validation_returns_none_without_match_any_case(self):
        PostcodeRule.attr_applied = "outward"
        PostcodeRule.applied_areas_regex = re.compile(r"BR|FY")

        postcode = mock.Mock(outward="HA1")
        rule = PostcodeRule(postcode)

        assert rule.validate() is None

    def test_validation_returns_false_with_invalid_postcode(self):
        PostcodeRule.attr_applied = "outward"
        PostcodeRule.applied_areas_regex = re.compile(r"BR|FY")
        PostcodeRule.rule_regex = re.compile(r"^[A-Z]{2}[0-9]$")

        postcode = mock.Mock(outward="BRA")
        rule = PostcodeRule(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()


class TestSingleDigitDistrict:
    @pytest.mark.parametrize("area", SINGLE_DIGIT_DISTRICTS_AREAS)
    def test_validating_valid_postcodes(self, area):
        outward = f"{area}1" if area != "WC" else f"{area}1A"
        postcode = mock.Mock(outward=outward)
        rule = SingleDigitDistrict(postcode)

        assert rule.validate() is None

    @pytest.mark.parametrize("area", SINGLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_when_has_double_digits(self, area):
        postcode = mock.Mock(outward=f"{area}11")
        rule = SingleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()

    @pytest.mark.parametrize("area", SINGLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_when_has_alphanumeric(self, area):
        postcode = mock.Mock(outward=f"{area}A")
        rule = SingleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()

    @pytest.mark.parametrize("area", SINGLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_when_has_no_digit(self, area):
        postcode = mock.Mock(outward=f"{area}")
        rule = SingleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()


class TestDoubleDigitDistrict:
    @pytest.mark.parametrize("area", DOUBLE_DIGIT_DISTRICTS_AREAS)
    def test_validating_valid_postcode(self, area):
        postcode = mock.Mock(outward=f"{area}11")
        rule = DoubleDigitDistrict(postcode)

        assert rule.validate() is None

    @pytest.mark.parametrize("area", DOUBLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_when_has_only_one_digit(self, area):
        postcode = mock.Mock(outward=f"{area}1")
        rule = DoubleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()

    @pytest.mark.parametrize("area", DOUBLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_when_has_alphanumeric(self, area):
        postcode = mock.Mock(outward=f"{area}A1")
        rule = DoubleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()

    @pytest.mark.parametrize("area", DOUBLE_DIGIT_DISTRICTS_AREAS)
    def test_invalidating_has_no_digit(self, area):
        postcode = mock.Mock(outward=f"{area}")
        rule = DoubleDigitDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()


class TestZeroDistrict:
    @pytest.mark.parametrize("area", ZERO_DISTRICTS_AREAS)
    def test_validating_valid_postcode_with_district_zero(self, area):
        postcode = mock.Mock(outward=f"{area}0")
        rule = ZeroDistrict(postcode)

        assert rule.validate() is None


    @pytest.mark.parametrize("area", ZERO_DISTRICTS_AREAS)
    def test_invalidating_when_not_valid_area_has_zero(self, area):
        postcode = mock.Mock(outward=f"AA0")
        rule = ZeroDistrict(postcode)

        with pytest.raises(InvalidPostcode):
            rule.validate()


class TestCentralLondonDistrict:
    @pytest.mark.parametrize("digit", range(1, 10))
    def test_validating_EC_only_between_one_and_four(self, digit):
        postcode = mock.Mock(outward=f"EC{digit}A")
        rule = CentralLondonDistrict(postcode)

        if digit < 5:
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()

    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_validating_E1_only_with_W(self, letter):
        postcode = mock.Mock(outward=f"E1{letter}")
        rule = CentralLondonDistrict(postcode)

        if letter == "W":
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()

    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_validating_N1_only_with_C_or_P(self, letter):
        postcode = mock.Mock(outward=f"N1{letter}")
        rule = CentralLondonDistrict(postcode)

        if letter in ("C", "P"):
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()

    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_validating_NW1_only_with_W(self, letter):
        postcode = mock.Mock(outward=f"NW1{letter}")
        rule = CentralLondonDistrict(postcode)

        if letter == "W":
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()


class TestFirstLetters:
    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_first_letter_is_invalid(self, letter):
        postcode = mock.Mock(outward=f"{letter}1")
        rule = FirstLetter(postcode)

        if letter in ("Q", "V", "X"):
            with pytest.raises(InvalidPostcode):
                rule.validate()
        else:
            assert rule.validate() is None


class TestSecondLetters:
    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_second_letter_is_invalid(self, letter):
        postcode = mock.Mock(outward=f"A{letter}")
        rule = SecondLetter(postcode)

        if letter in ("I", "J", "Z"):
            with pytest.raises(InvalidPostcode):
                rule.validate()
        else:
            assert rule.validate() is None


class TestThirdLetter:
    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_third_letter_is_invalid(self, letter):
        postcode = mock.Mock(outward=f"A9{letter}")
        rule = ThirdLetter(postcode)

        if letter in ("A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "P", "S", "T", "U", "W"):
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()


class TestFourthLetter:
    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_fourth_letter_is_invalid(self, letter):
        postcode = mock.Mock(outward=f"AA9{letter}")
        rule = FourthLetter(postcode)

        if letter in ("A", "B", "E", "H", "M", "N", "P", "R", "V", "W", "X", "Y"):
            assert rule.validate() is None
        else:
            with pytest.raises(InvalidPostcode):
                rule.validate()


class TestLastTwoLetter:
    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_last_letter_is_invalid(self, letter):
        postcode = mock.Mock(inward=f"9A{letter}")
        rule = LastTwoLetter(postcode)

        if letter in ("C", "I", "K", "M", "O", "V"):
            with pytest.raises(InvalidPostcode):
                rule.validate()
        else:
            assert rule.validate() is None

    @pytest.mark.parametrize("letter", string.ascii_uppercase)
    def test_invalidating_when_penultimate_letter_is_invalid(self, letter):
        postcode = mock.Mock(inward=f"9{letter}A")
        rule = LastTwoLetter(postcode)

        if letter in ("C", "I", "K", "M", "O", "V"):
            with pytest.raises(InvalidPostcode):
                rule.validate()
        else:
            assert rule.validate() is None
