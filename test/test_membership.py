import unittest
from src.main import GymMembership, Gym

class TestGymMembership(unittest.TestCase):
    def test_add_feature(self):
        membership = GymMembership("Basic", 100, {"Feature1": 20})
        membership.add_feature("Feature1")
        self.assertIn("Feature1", membership.selected_features)

    def test_calculate_cost(self):
        membership = GymMembership("Basic", 100, {"Feature1": 20})
        membership.add_feature("Feature1")
        self.assertEqual(membership.calculate_cost(), 120)

class TestGym(unittest.TestCase):
    def test_add_membership(self):
        gym = Gym()
        membership = GymMembership("Basic", 100)
        gym.add_membership(membership)
        self.assertIn("Basic", gym.memberships)

    def test_calculate_total_cost(self):
        gym = Gym()
        membership = GymMembership("Basic", 100, {"Feature1": 20})
        gym.add_membership(membership)
        membership.add_feature("Feature1")
        self.assertEqual(gym.calculate_total_cost("Basic", num_members=1, apply_premium=False), 120)
        self.assertEqual(gym.calculate_total_cost("Basic", num_members=2, apply_premium=False), 108)  # 10% discount for group
        self.assertEqual(gym.calculate_total_cost("Basic", num_members=1, apply_premium=True), 138)  # 15% surcharge for premium

if __name__ == "__main__":
    unittest.main()
