"""
Unit tests for the Gym Membership Management System
"""

import pytest
from src.main import GymMembership, Gym

def test_add_feature():
    """Test adding a feature to a membership."""
    membership = GymMembership("Basic", 100, {"Feature1": 20})
    membership.add_feature("Feature1")
    assert "Feature1" in membership.selected_features

def test_calculate_cost():
    """Test calculating the total cost of a membership."""
    membership = GymMembership("Basic", 100, {"Feature1": 20})
    membership.add_feature("Feature1")
    assert membership.calculate_cost() == 120

def test_add_membership():
    """Test adding a membership to the gym."""
    gym = Gym()
    membership = GymMembership("Basic", 100)
    gym.add_membership(membership)
    assert "Basic" in gym.memberships

def test_calculate_total_cost():
    """Test calculating the total cost with discounts and surcharges."""
    gym = Gym()
    membership = GymMembership("Basic", 100, {"Feature1": 20})
    gym.add_membership(membership)
    membership.add_feature("Feature1")
    assert gym.calculate_total_cost("Basic", num_members=1, apply_premium=False) == 120
    assert gym.calculate_total_cost("Basic", num_members=2, apply_premium=False) == 108  # 10% discount for group
    assert gym.calculate_total_cost("Basic", num_members=1, apply_premium=True) == 138  # 15% surcharge for premium
