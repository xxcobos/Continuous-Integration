"""Este módulo maneja la gestión de membresías en un gimnasio."""

class GymMembership:
    """Representa un plan de membresía de gimnasio con características adicionales."""

    def __init__(self, name, base_cost, additional_features=None):
        """
        Inicializa una membresía de gimnasio.

        :param name: Nombre del plan de membresía
        :param base_cost: Costo base de la membresía
        :param additional_features: Diccionario de características adicionales con sus costos
        """
        self.name = name
        self.base_cost = base_cost
        self.additional_features = additional_features if additional_features else {}
        self.selected_features = []

    def add_feature(self, feature_name):
        """
        Agrega una característica adicional a la membresía.

        :param feature_name: Nombre de la característica a agregar
        :raises ValueError: Si la característica no está disponible
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
        Calcula el costo total de la membresía incluyendo las características seleccionadas.

        :return: Costo total
        """
        total_cost = self.base_cost
        for feature in self.selected_features:
            total_cost += self.additional_features[feature]
        return total_cost


class Gym:
    """Representa un gimnasio con múltiples planes de membresía."""

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
        Agrega un plan de membresía al gimnasio.

        :param membership: Instancia de GymMembership
        """
        self.memberships[membership.name] = membership

    def display_memberships(self):
        """Muestra todos los planes de membresía con sus costos base y características adicionales."""
        for membership in self.memberships.values():
            print(f"Membership: {membership.name}, Base Cost: ${membership.base_cost}")
            for feature, cost in membership.additional_features.items():
                print(f"  - Feature: {feature}, Cost: ${cost}")

    def select_membership(self, membership_name):
        """
        Selecciona un plan de membresía por nombre.

        :param membership_name: Nombre del plan de membresía
        :return: Instancia de GymMembership
        :raises ValueError: Si el plan de membresía no existe
        """
        if membership_name in self.memberships:
            return self.memberships[membership_name]
        raise ValueError(f"Membership {membership_name} is not available.")

    def calculate_total_cost(self, membership, num_members=1):
        """
        Calcula el costo total para una membresía dada y un número de miembros.

        :param membership: Instancia de GymMembership
        :param num_members: Número de miembros
        :return: Costo total después de aplicar descuentos
        """
        base_cost = membership.calculate_cost()
        total_cost = base_cost * num_members

        if membership.name == "Premium" and len(membership.selected_features) >= 1:
            surcharge = total_cost * self.premium_surcharge
            total_cost += surcharge
            print(f"15% surcharge applied for being a Premium plan with at least 1 feature: ${surcharge}")

        if num_members >= 2:
            total_cost -= total_cost * self.group_discount
            print(f"Group discount applied: {self.group_discount * 100}%")

        sorted_special_discounts = sorted(self.special_discounts, key=lambda x: x[0], reverse=True)
        for threshold, discount in sorted_special_discounts:
            if total_cost > threshold:
                total_cost -= discount
                print(f"Special discount of ${discount} applied for total cost over ${threshold}")
                break

        return total_cost

    def confirm_membership(self, membership, num_members=1):
        """
        Confirma la membresía y calcula el costo total.

        :param membership: Instancia de GymMembership
        :param num_members: Número de miembros
        :return: Costo total si se confirma, -1 en caso contrario
        """
        try:
            total_cost = self.calculate_total_cost(membership, num_members)
            print(f"Membership: {membership.name}")
            print(f"Base Cost: ${membership.base_cost}")
            print(f"Additional Feature(s): {' - '.join([f'{feature} (Cost ${membership.additional_features[feature]})' for feature in membership.selected_features])}")
            print(f"\nTotal Cost: ${total_cost}\n")
            confirmation = input("Do you want to confirm this membership? (yes/no): ").lower()
            if confirmation == 'yes':
                return total_cost
            return -1
        except ValueError as e:
            print(f"Error: {e}")
            return -1


def main():
    """Función principal para ejecutar el sistema de membresía de gimnasio."""
    gym = Gym()
    basic_features = {"Group Classes": 25, "Crossfit Sessions": 10}
    premium_features = {"Personal Trainer": 40, "Sauna": 10, "Nutrition Plan": 20}
    family_features = {"Tennis Court": 10, "Group Classes": 15}

    basic_membership = GymMembership("Basic", 60, basic_features)
    premium_membership = GymMembership("Premium", 80, premium_features)
    family_membership = GymMembership("Family", 100, family_features)

    gym.add_membership(basic_membership)
    gym.add_membership(premium_membership)
    gym.add_membership(family_membership)

    continue_in_system = True
    while continue_in_system:
        print("\n -----------------WELCOME TO YOUR FAVOURITE GYM-------------------\n" +
              "\nAvailable Memberships:")
        memberships_list = list(gym.memberships.values())
        for i, membership in enumerate(memberships_list, start=1):
            print(f"{i}.  {membership.name} - Base Cost: ${membership.base_cost}")

        print("\n ------------------------ATTENTION!!------------------------------------\n" +
              "\n If two or more members sign up for the same membership plan together, \n apply a 10 percent discount on the total membership cost\n" +
              "\n ------------------------------------------------------------------------\n")

        try:
            membership_selection = int(input("Select a membership plan: ")) - 1
            if membership_selection < 0 or membership_selection >= len(memberships_list):
                raise ValueError("Invalid selection. Please select a valid number.")
            membership = memberships_list[membership_selection]
            print(f"\nYou have chosen {membership.name} Plan for your membership.")
            num_members = int(input("\nEnter the number of members to subscribe: "))

            while True:
                print("\nAvailable Features:")
                features_list = [
                    feature for feature in membership.additional_features.keys()
                    if feature not in membership.selected_features
                ]
                for i, feature in enumerate(features_list, start=1):
                    print(f"{i}. {feature}: ${membership.additional_features[feature]}")

                feature_selection = input("\nSelect a feature to add (or 'done' to finish): ")
                print("\n")
                if feature_selection.lower() == 'done':
                    break
                try:
                    feature_selection = int(feature_selection) - 1
                    if feature_selection < 0 or feature_selection >= len(features_list):
                        raise ValueError("Invalid selection. Please select a valid number.")
                    feature_name = features_list[feature_selection]
                    membership.selected_features.append(feature_name)
                    print(f"Adding {feature_name} feature to your membership.")
                except ValueError as e:
                    print(e)

            total_cost = gym.confirm_membership(membership, num_members)
            if total_cost != -1:
                print(f"Membership confirmed. Total cost: ${total_cost}")
            else:
                print("Membership not confirmed.")

            membership.selected_features.clear()

            continue_response = input("\nDo you want to continue in the system? (yes/no): ").lower()
            continue_in_system = continue_response == 'yes'
            if not continue_in_system:
                print("Goodbye!")

        except ValueError as e:
            print(e)
            return -1


if __name__ == "__main__":
    main()