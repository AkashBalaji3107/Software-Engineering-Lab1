import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

def test_repair_quote_flagship_screen_warranty_express():
    # Flagship screen, warranty=True (screen warranty doesn't zero cost), express=True
    # cost = 4000 * 2 = 8000, labour = 600, express = 500 -> total = 9100
    assert repair_quote("screen", "flagship", True, True) == 9100

def test_repair_quote_battery_warranty():
    # Budget battery, warranty=True (zeros cost), labour = 300, express=False -> total = 300
    assert repair_quote("battery", "budget", True, False) == 300

def test_repair_quote_exceptions():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("battery", "midrange", False, False)

def test_repair_days_zero_technicians_out_of_stock():
    # 0 technicians -> days = 3; out of stock camera -> days += 5 -> total 8
    assert repair_days("camera", False, 0) == 8

def test_repair_days_normal_out_of_stock():
    # technicians = 1 -> days = 1; out of stock battery -> days += 2 -> total 3
    assert repair_days("battery", False, 1) == 3

def test_trade_in_value_brackets():
    # Age <= 12 months (60%), cracked screen (//2)
    assert trade_in_value(10000, 6, True) == 3000
    # Age 13-24 months (40%)
    assert trade_in_value(10000, 18, False) == 4000
    # Age 25-48 months (20%)
    assert trade_in_value(10000, 30, False) == 2000
    # Age > 48 months -> 0
    assert trade_in_value(10000, 50, False) == 0

def test_trade_in_value_exceptions():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 5, False)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(1000, -1, False)