import os
import inflection


class Meal:

    def __init__(self, meal_name: str, prep_time: int, taste_preference: float) -> None:
        self.meal_name = meal_name
        self.prep_time = prep_time
        self.taste_preference = taste_preference
        self.is_snack = False
        self.ingredients = {}
        self.quantities = {}
        self.instructions = None
        self.calories = 0
        self.fat = 0
        self.carbs = 0
        self.fiber = 0
        self.protein = 0
        self.vitamin_a = 0
        self.vitamin_b = 0
        self.vitamin_c = 0
        self.vitamin_d = 0
        self.vitamin_k = 0
        self.potassium = 0
        self.sodium = 0
        self.cholesterol = 0


    def write_meal_instructions(self):
        folder_directory = "C:/Users/18327/PycharmProjects/csci127-su22/Personal Projects/CSCI-127 Final/meal_instructions/"
        instruction_directory = os.path.join(folder_directory, inflection.underscore(self.meal_name) + "_instructions.txt")
        with open(instruction_directory, "r", encoding="utf-8") as meal_instructions_txt:
            self.instructions = meal_instructions_txt.read()
            print("The current instructions for \'" + self.meal_name + "\' are:")
            print("\"" + self.instructions + "\"\n")
            meal_instructions_txt.close()
        user_input = input("Append(1) existing instructions, Overwrite(2) existing instructions, or Exit(3)?\n-> ")
        getting_input = True
        while getting_input is True:
            if user_input == "1":
                with open(instruction_directory, "a", encoding="utf-8") as meal_instructions_txt:
                    instructions = input("Enter meal instructions:\n-> ")
                    meal_instructions_txt.write(instructions)
                    meal_instructions_txt.close()
                    getting_input = False
            elif user_input == "2":
                with open(instruction_directory, "w", encoding="utf-8") as meal_instructions_txt:
                    instructions = input("Enter meal instructions:\n-> ")
                    meal_instructions_txt.write(instructions)
                    meal_instructions_txt.close()
                    getting_input = False
            elif user_input == "3":
                getting_input = False
            else:
                user_input = ("Unrecognized input. Append(1) existing instructions, Overwrite(2) existing "
                              "instructions, or Exit(3)?\n-> ")

    def remove_ingredient(self):
        ingredient = input("Which ingredient would you like to remove from the meal?\n-> ").lower()
        if ingredient in self.ingredients.keys():
            del self.ingredients[ingredient]
            print("\'" + ingredient + "\' successfully removed from \'" + self.meal_name + ".\'")
        else:
            print("Invalid input. Ingredient not found in meal.")

    def print_meal_nutrition(self):
        print("\n///////////////////////////////////////")
        print("Displaying nutrition facts for " + self.meal_name + "...\n")
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

