import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value

def test_repair_quote_branches():
    # 1. Budget screen, no warranty, no express (Hits budget tier, screen labour=600, under_warranty False, express False)
    assert repair_quote("screen", "budget", False, False) == 4600
    
    # 2. Flagship camera, under warranty=True, express=True (Hits flagship tier cost*2=5000, labour=300, under_warranty=True & part != screen -> cost=0, express=True -> +500)
    assert repair_quote("camera", "flagship", True, True) == 800

    # 3. Test exceptions for unknown part and unknown brand tier
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("unknown_part", "budget", False, False)
        
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("battery", "invalid_tier", False, False)


def test_repair_days_branches():
    # 1. Technicians free == 0, part not in stock & part == "screen"
    assert repair_days("screen", False, 0) == 8
    
    # 2. Technicians free != 0 (e.g., 2), part in stock & part != "screen" (e.g., charging_port)
    assert repair_days("charging_port", True, 2) == 1
    
    # 3. Technicians free != 0, part not in stock & part != "screen" (e.g., battery)
    assert repair_days("battery", False, 1) == 3


def test_trade_in_value_branches():
    # 1. Invalid input exceptions (price <= 0 or age < 0)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 10, False)
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(10000, -1, False)
        
    # 2. Age > 48 months boundary (returns 0)
    assert trade_in_value(10000, 49, False) == 0
    
    # 3. Age <= 12 months, screen_cracked = True
    assert trade_in_value(10000, 10, True) == 3000
    
    # 4. Age between 13 and 24 months, screen_cracked = False
    assert trade_in_value(10000, 20, False) == 4000
    
    # 5. Age between 25 and 48 months, screen_cracked = False
    assert trade_in_value(10000, 36, False) == 2000