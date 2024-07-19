class GymMembership:
    """Class representing a gym membership plan with additional features."""
    
    def __init__(self, name, base_cost, additional_features=None):
        """
        Initialize a gym membership.

        :param name: Name of the membership plan
        :param base_cost: Base cost of the membership
        :param additional_features: Dictionary of additional features with their costs
        """
        self.name = name
        self.base_cost = base_cost
        self.additional_features = additional_features if additional_features else {}
        self.selected_features = []

    def add_feature(self, feature_name):
        """
        Add an additional feature to the membership.

        :param feature_name: Name of the feature to add
        :raises ValueError: If the feature is not available
        """
        if feature_name in self.additional_features:
            self.selected_features.append(feature_name)
            print("\n-----------------------------------------------------\n" +
                f"Adding {feature_name} feature to your membership...\n" +
                "-----------------------------------------------------\n ")
        else:
            raise ValueError(f"Feature {feature_name} is not available for {self.name} membership.")

    def calculate_cost(self):
        """
        Calculate the total cost of the membership including selected features.

        :return: Total cost
        """
        total_cost = self.base_cost
        for feature in self.selected_features:
            total_cost += self.additional_features[feature]
        return total_cost
    
class Gym:
    """Class representing a gym with multiple membership plans."""
    
    def __init__(self):
        self.memberships = {}
        self.group_discount = 0.10
        self.special_discounts = [
            (400, 50),
            (200, 20)
        ]
        self.premium_surcharge = 0.15

    def add_membership(self, membership):
        """
        Add a membership plan to the gym.

        :param membership: GymMembership instance
        """
        self.memberships[membership.name] = membership

    def select_membership(self, name):
        """
        Select a membership plan by name.

        :param name: Name of the membership plan
        :return: GymMembership instance
        :raises ValueError: If the membership plan does not exist
        """
        if name in self.memberships:
            return self.memberships[name]
        else:
            raise ValueError(f"Membership plan {name} does not exist.")

    def calculate_total_cost(self, membership, members):
        """
        Calculate the total cost for a given membership and number of members.

        :param membership: GymMembership instance
        :param members: Number of members
        :return: Total cost after applying any discounts
        """
        total_cost = membership.calculate_cost() * members

        for threshold, discount in self.special_discounts:
            if total_cost >= threshold:
                total_cost -= discount

        if membership.name == "Premium":
            total_cost += total_cost * self.premium_surcharge

        if members > 1:
            total_cost -= total_cost * self.group_discount

        return total_cost
