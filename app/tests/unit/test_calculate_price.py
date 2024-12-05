import pytest
from app.utils.pricing import calculate_price


@pytest.mark.parametrize(
    "symbol, quantity, expected_price",
    [
        ("EURUSD", 10, 12.0),
        ("GBPUSD", 5, 6.75),
        ("PLNUSD", 20, 5.0),
    ]
)
def test_calculate_price_valid_symbols(symbol, quantity, expected_price):
    result = calculate_price(symbol, quantity)
    assert result == pytest.approx(expected_price), f"Failed for symbol: {symbol}"


@pytest.mark.parametrize(
    "symbol, quantity, expected_price",
    [
        ("INVALID", 10, 10.0),
        ("XYZ", 20, 20.0),
        ("", 5, 5.0),
    ]
)
def test_calculate_price_invalid_symbols(symbol, quantity, expected_price):
    result = calculate_price(symbol, quantity)
    assert result == pytest.approx(expected_price), f"Failed for invalid symbol: {symbol}"
