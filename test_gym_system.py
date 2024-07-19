import unittest
from main import GymMembership,Gym

class TestGymSystem(unittest.TestCase):

    def setUp(self):
        self.basic_features = {"Group Classes": 25, "Crossfit Sessions": 10}
        self.premium_features = {"Personal Trainer": 40, "Sauna": 10, "Nutrition Plan": 20}
        self.family_features = {"Tennis Court": 10, "Group Classes": 15}

        self.basic_membership = GymMembership("Basic", 60, self.basic_features)
        self.premium_membership = GymMembership("Premium", 80, self.premium_features)
        self.family_membership = GymMembership("Family", 100, self.family_features)

        self.gym = Gym()
        self.gym.add_membership(self.basic_membership)
        self.gym.add_membership(self.premium_membership)
        self.gym.add_membership(self.family_membership)

    def test_membership_plan_selection(self):
        self.assertIsNotNone(self.gym.select_membership("Basic"))
        self.assertIsNotNone(self.gym.select_membership("Premium"))
        self.assertIsNotNone(self.gym.select_membership("Family"))
        with self.assertRaises(ValueError):
            self.gym.select_membership("Nonexistent")

    def test_additional_features_selection(self):
        self.basic_membership.add_feature("Group Classes")
        self.assertIn("Group Classes", self.basic_membership.selected_features)

        with self.assertRaises(ValueError):
            self.basic_membership.add_feature("Nonexistent Feature")

        self.premium_membership.add_feature("Personal Trainer")
        self.premium_membership.add_feature("Sauna")
        self.assertIn("Personal Trainer", self.premium_membership.selected_features)
        self.assertIn("Sauna", self.premium_membership.selected_features)

    def test_cost_calculation(self):
        self.assertEqual(self.basic_membership.calculate_cost(), 60)

        self.basic_membership.add_feature("Group Classes")
        self.assertEqual(self.basic_membership.calculate_cost(), 85)

        self.premium_membership.add_feature("Personal Trainer")
        self.premium_membership.add_feature("Sauna")
        self.assertEqual(self.premium_membership.calculate_cost(), 130)

    def test_discounts_for_group_memberships(self):
        self.basic_membership.add_feature("Group Classes")
        total_cost = self.gym.calculate_total_cost(self.basic_membership, 2)
        self.assertAlmostEqual(total_cost, 153, places=0)

        total_cost = self.gym.calculate_total_cost(self.basic_membership, 1)
        self.assertEqual(total_cost, 85)

    def test_special_offer_discounts(self):
        self.premium_membership.add_feature("Personal Trainer")
        self.premium_membership.add_feature("Sauna")
        total_cost = self.gym.calculate_total_cost(self.premium_membership, 5)
        self.assertAlmostEqual(total_cost, 622.75, places=0)

        self.basic_membership.add_feature("Group Classes")
        total_cost = self.gym.calculate_total_cost(self.basic_membership, 4)
        self.assertAlmostEqual(total_cost, 286, places=0)

    def test_premium_membership_features(self):
        self.premium_membership.add_feature("Personal Trainer")
        total_cost = self.gym.calculate_total_cost(self.premium_membership, 1)
        self.assertEqual(total_cost, 138)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.basic_membership.add_feature("Nonexistent Feature")

if __name__ == "__main__":
    unittest.main()