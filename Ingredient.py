class Ingredient:

    def __init__(self, ingredient_name: str, measurement: str, calories: float, fat: float, carbs: float, fiber: float,
                 protein: float, vitamin_a: float, vitamin_c: float, vitamin_d: float, vitamin_k: float, potassium: float,
                 sodium: float, cholesterol: float, purchase_price: float, purchase_quantity: float, quantity_on_hand: float):
        """Defines food with various attributes"""
        self.ingredient_name = ingredient_name
        self.measurement = measurement
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.fiber = fiber
        self.protein = protein
        self.vitamin_a = vitamin_a
        self.vitamin_c = vitamin_c
        self.vitamin_d = vitamin_d
        self.vitamin_k = vitamin_k
        self.potassium = potassium
        self.sodium = sodium
        self.cholesterol = cholesterol
        self.purchase_price = purchase_price
        self.purchase_quantity = purchase_quantity
        self.quantity_on_hand = quantity_on_hand

    def print_ing_nutrition(self) -> None:
        print("\n///////////////////////////////////////")
        print("Displaying nutrition facts per " + self.measurement + " " + self.ingredient_name + "...\n")
        print("\tCalories " + "\t\t" + str(self.calories))
        print("\tFat " + "\t\t\t" + str(self.fat) + " grams")
        print("\tCarbs " + "\t\t\t" + str(self.carbs) + " grams")
        print("\tFiber " + "\t\t\t" + str(self.fiber) + " grams")
        print("\tProtein " + "\t\t" + str(self.protein) + " grams")
        print("\tVitamin A " + "\t\t" + str(self.vitamin_a) + "% daily value")
        print("\tVitamin C " + "\t\t" + str(self.vitamin_c) + "% daily value")
        print("\tVitamin D " + "\t\t" + str(self.vitamin_d) + "% daily value")
        print("\tVitamin K " + "\t\t" + str(self.vitamin_k) + "% daily value")
        print("\tPotassium " + "\t\t" + str(self.potassium) + "% daily value")
        print("\tSodium " + "\t\t\t" + str(self.sodium) + "% daily value")
        print("\tCholesterol " + "\t" + str(self.cholesterol) + "% daily value")
        print("\n///////////////////////////////////////")


    def modify_vitamin_a(self) -> None:
        print("\nVitamin A per " + self.measurement + " " + self.ingredient_name + " currently set to " +
              str(self.vitamin_a) + "% daily value.")
        while True:
            user_input = (input("Input a new percentage of Vitamin A per " + self.measurement + " " +
                                self.ingredient_name + " or press \'x\' to cancel:\n-> "))
            try:
                if user_input != "x":
                    if int(user_input) < 0:
                        print("INVALID INPUT - Input must be greater than or equal to 0.\n")
                        pass
                    else:
                        self.vitamin_a = int(user_input)
                        print("Vitamin A per " + self.measurement + " " + self.ingredient_name + " set to " +
                              str(self.vitamin_a) + "% daily value.")
                        break
                else:
                    break
            except ValueError:
                print("INVALID INPUT - Input must be a whole number.\n")



    # Ability to modify any quantity above

if __name__ == "__main__":
    banana = Ingredient("banana", "one medium 7\"-8\"", 105, 1, 27, 3, 1, 3, 11, 0, 0, 12, 0, 0)
    banana.print_ing_nutrition()
    banana.modify_vitamin_a()
    banana.print_ing_nutrition()