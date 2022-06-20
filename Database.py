import csv
from Ingredient import Ingredient
from Meal import Meal
from Plan import Plan
import os
import inflection
import random
import urllib.request
import codecs
import datetime



class Database:

    def __init__(self):
        """Keeps track of all ingredients, meals, and meal plans."""
        self.user = None
        self.user_log_count = 0
        self.user_preferences = {"Budget per week": 50, "Calories": 2000, "Fat": 87, "Carbs": 263, "Fiber": 38,
                                 "Protein": 100, "Vitamin C": 100, "Vitamin D": 100, "Vitamin A": 100, "Vitamin K": 100,
                                 "Potassium": 100, "Sodium": 100, "Cholesterol": 100, "Prep time per week": 120}
        self.ingredients = {}
        self.meals = {}
        self.plans = {}
        self.top_five_plans = {}
        self.ingredients_in_cart = {}
        self.ingredients_on_hand = {}
        self.ingredients_to_purchase = {}
        self.cheapest_plan = None

    def add_ingredient(self) -> None:
        """Adds an ingredient to the database."""
        getting_input = "Y"
        while getting_input != "N":
            ingredient_name = input("Enter ingredient name:\n-> ").lower()
            if ingredient_name not in self.ingredients.keys():
                measurement = input("Enter a scale of measurement (ex. \'one cup\' or \'one medium\'):\n-> ").lower()
                calories = float(input("Enter calories:\n-> "))
                fat = float(input("Enter fat in grams:\n-> "))
                carbs = float(input("Enter carbs in grams:\n-> "))
                fiber = float(input("Enter fiber in grams:\n-> "))
                protein = float(input("Enter protein in grams:\n-> "))
                vitamin_c = float(input("Enter vitamin C as percentage of daily value:\n-> "))
                vitamin_d = float(input("Enter vitamin D as percentage of daily value:\n-> "))
                vitamin_a = float(input("Enter vitamin A as percentage of daily value:\n-> "))
                vitamin_k = float(input("Enter vitamin K as percentage of daily value:\n-> "))
                potassium = float(input("Enter potassium as percentage of daily value:\n-> "))
                sodium = float(input("Enter sodium as percentage of daily value:\n-> "))
                cholesterol = float(input("Enter cholesterol as percentage of daily value:\n-> "))
                purchase_price = float(input("Enter purchase price:\n-> "))
                purchase_quantity = float(input("Enter purchase quantity:\n-> "))
                quantity_on_hand = float(input("Enter quantity you current have on hand:\n-> "))
                self.ingredients[ingredient_name] = Ingredient(ingredient_name, measurement, calories, fat, carbs,
                                                               fiber, protein, vitamin_a, vitamin_c, vitamin_d,
                                                               vitamin_k, potassium, sodium, cholesterol,
                                                               purchase_price, purchase_quantity, quantity_on_hand)
                print("\'" + ingredient_name.title() + "\' added to database.")
                getting_input = "N"
            else:
                getting_input = input("Ingredient already in database. Would you like to enter a new ingredient? "
                                      "\'Y\'/\'N\'\n-> ").upper()
                if getting_input != 'Y' or getting_input != 'N':
                    getting_input = input("Unrecognized command. Would you like to enter a new ingredient? Type "
                                          "\'Y\' for yes, \'N\' for no.\n-> ").upper()

    def sync_ingredients_from_google_sheets(self) -> None:
        """Deletes the ingredients in the database and recreates the ingredients from the URL. Reloads all meals with
        the new ingredients to solve possible memory address issues."""
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjS3n1KA5odkbCOf60D6CQ_SZkSZFZDgH8JVoxPzDCCDSx1zd8KXJWGWpUgSV9Cfg3y3iKftxKFamQ/pub?gid=1532887167&single=true&output=csv"
        ftpstream = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
        self.ingredients = {}
        for line in csvfile:
            if line[0] == "ingredient_name":
                pass
            else:
                ingredient_name = line[0]
                quantity_on_hand = float(str(line[1]))
                purchase_price = float(str(line[2]))
                purchase_quantity = float(str(line[3]))
                measurement = str(line[4])
                calories = float(str(line[5]))
                fat = float(line[6])
                carbs = float(line[7])
                fiber = float(line[8])
                protein = float(line[9])
                vitamin_a = float(line[10])
                vitamin_c = float(line[11])
                vitamin_d = float(line[12])
                vitamin_k = float(line[13])
                potassium = float(line[14])
                sodium = float(line[15])
                cholesterol = float(line[16])
                self.ingredients[ingredient_name] = Ingredient(ingredient_name=ingredient_name, measurement=measurement,
                                                               quantity_on_hand=quantity_on_hand, purchase_price=purchase_price,
                                                               purchase_quantity=purchase_quantity, calories=calories,
                                                               fat=fat, carbs=carbs, fiber=fiber, protein=protein, vitamin_a=vitamin_a,
                                                               vitamin_c=vitamin_c, vitamin_d=vitamin_d, vitamin_k=vitamin_k,
                                                               potassium=potassium, sodium=sodium, cholesterol=cholesterol)
        self.reload_meals()
        print("Google Sheets ingredient sync successful.")

    def sync_ingredients_from_csv(self) -> None:
        """Deletes the ingredients in the database and recreates the ingredients from the CSV."""
        folder_directory = "ingredients/"
        try:
            instruction_directory = os.path.join(folder_directory,
                                                 inflection.underscore(self.user) + "_ingredients.csv")
            with open(instruction_directory, "r", newline="", encoding="utf-8") as user_ingredients:
                field_names = ["ingredient_name", "measurement", "calories", "fat", "carbs", "fiber", "protein",
                               "vitamin_a", "vitamin_c", "vitamin_d", "vitamin_k", "potassium", "sodium", "cholesterol",
                               "purchase_price", "purchase_quantity", "quantity_on_hand"]
                csvreader = csv.DictReader(user_ingredients, fieldnames=field_names)
                self.ingredients = {}
                for row in csvreader:
                    if row["ingredient_name"] == "ingredient_name":
                        pass
                    else:
                        self.ingredients[row["ingredient_name"]] = Ingredient(str(row["ingredient_name"]),
                                                                              str(row["measurement"]),
                                                                              float(row["calories"]), float(row["fat"]),
                                                                              float(row["carbs"]),
                                                                              float(row["fiber"]),
                                                                              float(row["protein"]),
                                                                              float(row["vitamin_a"]),
                                                                              float(row["vitamin_c"]),
                                                                              float(row["vitamin_d"]),
                                                                              float(row["vitamin_k"]),
                                                                              float(row["potassium"]),
                                                                              float(row["sodium"]),
                                                                              float(row["cholesterol"]),
                                                                              float(row["purchase_price"]),
                                                                              float(row["purchase_quantity"]),
                                                                              float(row["quantity_on_hand"]))
                print("CSV sync successful.")
        except FileNotFoundError:
            instruction_directory = os.path.join(folder_directory, "default_ingredients.csv")
            with open(instruction_directory, "r", newline="", encoding="utf-8") as user_ingredients:
                field_names = ["ingredient_name", "measurement", "calories", "fat", "carbs", "fiber", "protein",
                               "vitamin_a", "vitamin_c", "vitamin_d", "vitamin_k", "potassium", "sodium", "cholesterol",
                               "purchase_price", "purchase_quantity", "quantity_on_hand"]
                csvreader = csv.DictReader(user_ingredients, fieldnames=field_names)
                self.ingredients = {}
                for row in csvreader:
                    if row["ingredient_name"] == "ingredient_name":
                        pass
                    else:
                        self.ingredients[row["ingredient_name"]] = Ingredient(str(row["ingredient_name"]),
                                                                              str(row["measurement"]),
                                                                              float(row["calories"]), float(row["fat"]),
                                                                              float(row["carbs"]),
                                                                              float(row["fiber"]),
                                                                              float(row["protein"]),
                                                                              float(row["vitamin_a"]),
                                                                              float(row["vitamin_c"]),
                                                                              float(row["vitamin_d"]),
                                                                              float(row["vitamin_k"]),
                                                                              float(row["potassium"]),
                                                                              float(row["sodium"]),
                                                                              float(row["cholesterol"]),
                                                                              float(row["purchase_price"]),
                                                                              float(row["purchase_quantity"]),
                                                                              float(row["quantity_on_hand"]))
                print("CSV sync successful.")

    def sync_ingredients_to_csv(self) -> None:
        """Saves the ingredients in the database as a CSV."""
        folder_directory = "ingredients/"
        instruction_directory = os.path.join(folder_directory,
                                             inflection.underscore(self.user) + "_ingredients.csv")
        with open(instruction_directory, "w+", newline="", encoding="utf-8") as user_ingredients:
            field_names = ["ingredient_name", "measurement", "calories", "fat", "carbs", "fiber", "protein",
                           "vitamin_a", "vitamin_c", "vitamin_d", "vitamin_k", "potassium", "sodium", "cholesterol",
                           "purchase_price", "purchase_quantity", "quantity_on_hand"]
            csvwriter = csv.DictWriter(user_ingredients, fieldnames=field_names)
            csvwriter.writeheader()
            for ingredient in self.ingredients:
                this_ingredient = self.ingredients[ingredient]
                csvwriter.writerow({"ingredient_name": this_ingredient.ingredient_name,
                                    "measurement": this_ingredient.measurement,
                                    "calories": this_ingredient.calories, "fat": this_ingredient.fat,
                                    "carbs": this_ingredient.carbs, "fiber": this_ingredient.fiber,
                                    "protein": this_ingredient.protein, "vitamin_a": this_ingredient.vitamin_a,
                                    "vitamin_c": this_ingredient.vitamin_c, "vitamin_d": this_ingredient.vitamin_d,
                                    "vitamin_k": this_ingredient.vitamin_k, "potassium": this_ingredient.potassium,
                                    "sodium": this_ingredient.sodium, "cholesterol": this_ingredient.cholesterol,
                                    "purchase_price": this_ingredient.purchase_price,
                                    "purchase_quantity": this_ingredient.purchase_quantity,
                                    "quantity_on_hand": this_ingredient.quantity_on_hand})
            print("CSV sync successful.")

    def sync_meals_to_csv(self) -> None:
        """Saves meals in the database as a CSV."""
        folder_directory = "meals/"
        instruction_directory = os.path.join(folder_directory,
                                             inflection.underscore(self.user) + "_meals.csv")
        with open(instruction_directory, "w+", newline="", encoding="utf-8") as user_meals:
            field_names = ["meal_name", "prep_time", "ingredient_1_name", "ingredient_1_quantity",
                           "ingredient_2_name", "ingredient_2_quantity", "ingredient_3_name",
                           "ingredient_3_quantity", "ingredient_4_name", "ingredient_4_quantity",
                           "ingredient_5_name", "ingredient_5_quantity", "ingredient_6_name",
                           "ingredient_6_quantity", "ingredient_7_name", "ingredient_7_quantity",
                           "ingredient_8_name", "ingredient_8_quantity", "ingredient_9_name", "ingredient_9_quantity",
                           "ingredient_10_name", "ingredient_10_quantity", "ingredient_11_name", "ingredient_11_quantity",
                           "ingredient_12_name", "ingredient_12_quantity", "taste_preference"]
            csvwriter = csv.DictWriter(user_meals, fieldnames=field_names)
            csvwriter.writeheader()
            for meal in self.meals:
                this_meal = self.meals[meal]
                this_meal_ingredients = []
                for ingredient in this_meal.ingredients:
                    this_ingredient = this_meal.ingredients[ingredient]
                    this_meal_ingredients.append(this_ingredient.ingredient_name)
                    this_ingredient_quantity = this_meal.quantities[ingredient]
                    this_meal_ingredients.append(this_ingredient_quantity)
                for index in range(16-len(this_meal_ingredients)):
                    this_meal_ingredients.append("")
                csvwriter.writerow({"meal_name": this_meal.meal_name, "prep_time": this_meal.prep_time,
                                    "ingredient_1_name": this_meal_ingredients[0],
                                    "ingredient_1_quantity": this_meal_ingredients[1],
                                    "ingredient_2_name": this_meal_ingredients[2],
                                    "ingredient_2_quantity": this_meal_ingredients[3],
                                    "ingredient_3_name": this_meal_ingredients[4],
                                    "ingredient_3_quantity": this_meal_ingredients[5],
                                    "ingredient_4_name": this_meal_ingredients[6],
                                    "ingredient_4_quantity": this_meal_ingredients[7],
                                    "ingredient_5_name": this_meal_ingredients[8],
                                    "ingredient_5_quantity": this_meal_ingredients[9],
                                    "ingredient_6_name": this_meal_ingredients[10],
                                    "ingredient_6_quantity": this_meal_ingredients[11],
                                    "ingredient_7_name": this_meal_ingredients[12],
                                    "ingredient_7_quantity": this_meal_ingredients[13],
                                    "ingredient_8_name": this_meal_ingredients[14],
                                    "ingredient_8_quantity": this_meal_ingredients[15],
                                    "ingredient_9_name": this_meal_ingredients[16],
                                    "ingredient_9_quantity": this_meal_ingredients[17],
                                    "ingredient_10_name": this_meal_ingredients[18],
                                    "ingredient_10_quantity": this_meal_ingredients[19],
                                    "ingredient_11_name": this_meal_ingredients[20],
                                    "ingredient_11_quantity": this_meal_ingredients[21],
                                    "ingredient_12_name": this_meal_ingredients[22],
                                    "ingredient_12_quantity": this_meal_ingredients[23],
                                    "taste_preference": this_meal_ingredients[24]})
            print("CSV sync successful.")

    def sync_meals_from_csv(self) -> None:
        """Deletes the meals currently contained in the database and recreates the meals from the CSV."""
        folder_directory = "meals/"
        try:
            instruction_directory = os.path.join(folder_directory,
                                                 inflection.underscore(self.user) + "_meals.csv")
            with open(instruction_directory, "r", newline="", encoding="utf-8") as user_ingredients:
                field_names = ["meal_name", "prep_time", "ingredient_1_name", "ingredient_1_quantity",
                               "ingredient_2_name", "ingredient_2_quantity", "ingredient_3_name",
                               "ingredient_3_quantity", "ingredient_4_name", "ingredient_4_quantity",
                               "ingredient_5_name", "ingredient_5_quantity", "ingredient_6_name",
                               "ingredient_6_quantity", "ingredient_7_name", "ingredient_7_quantity",
                               "ingredient_8_name", "ingredient_8_quantity", "ingredient_9_name", "ingredient_9_quantity",
                               "ingredient_10_name", "ingredient_10_quantity", "ingredient_11_name", "ingredient_11_quantity",
                               "ingredient_12_name", "ingredient_12_quantity", "taste_preference"]
                csvreader = csv.DictReader(user_ingredients, fieldnames=field_names)
                self.meals = {}
                for row in csvreader:
                    if row["meal_name"] == "meal_name":
                        pass
                    else:
                        self.meals[row["meal_name"]] = Meal(str(row["meal_name"]), row["prep_time"],
                                                            float(row["taste_preference"]))
                        meal_name = row["meal_name"]
                        ingredients_to_add = {}
                        if len(row["ingredient_1_name"]) != 0:
                            ingredients_to_add[row["ingredient_1_name"]] = row["ingredient_1_quantity"]
                        if len(row["ingredient_2_name"]) != 0:
                            ingredients_to_add[row["ingredient_2_name"]] = row["ingredient_2_quantity"]
                        if len(row["ingredient_3_name"]) != 0:
                            ingredients_to_add[row["ingredient_3_name"]] = row["ingredient_3_quantity"]
                        if len(row["ingredient_4_name"]) != 0:
                            ingredients_to_add[row["ingredient_4_name"]] = row["ingredient_4_quantity"]
                        if len(row["ingredient_5_name"]) != 0:
                            ingredients_to_add[row["ingredient_5_name"]] = row["ingredient_5_quantity"]
                        if len(row["ingredient_6_name"]) != 0:
                            ingredients_to_add[row["ingredient_6_name"]] = row["ingredient_6_quantity"]
                        if len(row["ingredient_7_name"]) != 0:
                            ingredients_to_add[row["ingredient_7_name"]] = row["ingredient_7_quantity"]
                        if len(row["ingredient_8_name"]) != 0:
                            ingredients_to_add[row["ingredient_8_name"]] = row["ingredient_8_quantity"]
                        if len(row["ingredient_9_name"]) != 0:
                            ingredients_to_add[row["ingredient_9_name"]] = row["ingredient_9_quantity"]
                        if len(row["ingredient_10_name"]) != 0:
                            ingredients_to_add[row["ingredient_10_name"]] = row["ingredient_10_quantity"]
                        if len(row["ingredient_11_name"]) != 0:
                            ingredients_to_add[row["ingredient_11_name"]] = row["ingredient_11_quantity"]
                        if len(row["ingredient_12_name"]) != 0:
                            ingredients_to_add[row["ingredient_12_name"]] = row["ingredient_12_quantity"]
                        for new_ingredient in ingredients_to_add.keys():
                            for ingredient in self.ingredients:
                                this_ingredient = self.ingredients[ingredient]
                                if this_ingredient.ingredient_name == new_ingredient:
                                    this_meal = self.meals[row["meal_name"]]
                                    quantity = ingredients_to_add[new_ingredient]
                                    this_meal.ingredients[this_ingredient] = this_ingredient
                                    this_meal.quantities[this_ingredient] = quantity
                                    this_meal.calories += float(this_ingredient.calories) * float(quantity)
                                    this_meal.fat += float(this_ingredient.fat) * float(quantity)
                                    this_meal.carbs += float(this_ingredient.carbs) * float(quantity)
                                    this_meal.fiber += (float(this_ingredient.fiber) * float(quantity))
                                    this_meal.protein += (float(this_ingredient.protein) * float(quantity))
                                    this_meal.vitamin_a += (float(this_ingredient.vitamin_a) * float(quantity))
                                    this_meal.vitamin_c += (float(this_ingredient.vitamin_c) * float(quantity))
                                    this_meal.vitamin_d += (float(this_ingredient.vitamin_d) * float(quantity))
                                    this_meal.vitamin_k += (float(this_ingredient.vitamin_k) * float(quantity))
                                    this_meal.potassium += (float(this_ingredient.potassium) * float(quantity))
                                    this_meal.sodium += (float(this_ingredient.sodium) * float(quantity))
                                    this_meal.cholesterol += (float(this_ingredient.cholesterol) * float(quantity))
                                else:
                                    pass
                        folder_directory = "meal_instructions/"
                        instruction_directory = os.path.join(folder_directory,
                                                             inflection.underscore(meal_name) + "_instructions.txt")
                        try:
                            with open(instruction_directory, "r", encoding="utf-8") as meal_instructions_txt:
                                meal_instructions_txt.close()
                        except FileNotFoundError:
                            with open(instruction_directory, "w+", encoding="utf-8") as meal_instructions_txt:
                                meal_instructions_txt.write("No Instructions")
                                meal_instructions_txt.close()
                print("CSV sync successful.")
        except FileNotFoundError:
            instruction_directory = os.path.join(folder_directory, "default_meals.csv")
            with open(instruction_directory, "r", newline="", encoding="utf-8") as user_ingredients:
                field_names = ["meal_name", "prep_time", "ingredient_1_name", "ingredient_1_quantity",
                               "ingredient_2_name", "ingredient_2_quantity", "ingredient_3_name",
                               "ingredient_3_quantity", "ingredient_4_name", "ingredient_4_quantity",
                               "ingredient_5_name", "ingredient_5_quantity", "ingredient_6_name",
                               "ingredient_6_quantity", "ingredient_7_name", "ingredient_7_quantity",
                               "ingredient_8_name", "ingredient_8_quantity"]
                csvreader = csv.DictReader(user_ingredients, fieldnames=field_names)
                self.meals = {}
                for row in csvreader:
                    if row["meal_name"] == "meal_name":
                        pass
                    else:
                        self.meals[row["meal_name"]] = Meal(str(row["meal_name"]), row["prep_time"],
                                                            float(row["taste_preference"]))
                        meal_name = row["meal_name"]
                        ingredients_to_add = {}
                        if len(row["ingredient_1_name"]) != 0:
                            ingredients_to_add[row["ingredient_1_name"]] = row["ingredient_1_quantity"]
                        if len(row["ingredient_2_name"]) != 0:
                            ingredients_to_add[row["ingredient_2_name"]] = row["ingredient_2_quantity"]
                        if len(row["ingredient_3_name"]) != 0:
                            ingredients_to_add[row["ingredient_3_name"]] = row["ingredient_3_quantity"]
                        if len(row["ingredient_4_name"]) != 0:
                            ingredients_to_add[row["ingredient_4_name"]] = row["ingredient_4_quantity"]
                        if len(row["ingredient_5_name"]) != 0:
                            ingredients_to_add[row["ingredient_5_name"]] = row["ingredient_5_quantity"]
                        if len(row["ingredient_6_name"]) != 0:
                            ingredients_to_add[row["ingredient_6_name"]] = row["ingredient_6_quantity"]
                        if len(row["ingredient_7_name"]) != 0:
                            ingredients_to_add[row["ingredient_7_name"]] = row["ingredient_7_quantity"]
                        if len(row["ingredient_8_name"]) != 0:
                            ingredients_to_add[row["ingredient_8_name"]] = row["ingredient_8_quantity"]
                        if len(row["ingredient_9_name"]) != 0:
                            ingredients_to_add[row["ingredient_9_name"]] = row["ingredient_9_quantity"]
                        if len(row["ingredient_10_name"]) != 0:
                            ingredients_to_add[row["ingredient_10_name"]] = row["ingredient_10_quantity"]
                        if len(row["ingredient_11_name"]) != 0:
                            ingredients_to_add[row["ingredient_11_name"]] = row["ingredient_11_quantity"]
                        if len(row["ingredient_12_name"]) != 0:
                            ingredients_to_add[row["ingredient_12_name"]] = row["ingredient_12_quantity"]
                        for new_ingredient in ingredients_to_add.keys():
                            for ingredient in self.ingredients:
                                this_ingredient = self.ingredients[ingredient]
                                if this_ingredient.ingredient_name == new_ingredient:
                                    this_meal = self.meals[row["meal_name"]]
                                    quantity = ingredients_to_add[new_ingredient]
                                    this_meal.ingredients[this_ingredient] = this_ingredient
                                    this_meal.quantities[this_ingredient] = quantity
                                    this_meal.calories += float(this_ingredient.calories) * float(quantity)
                                    this_meal.fat += float(this_ingredient.fat) * float(quantity)
                                    this_meal.carbs += float(this_ingredient.carbs) * float(quantity)
                                    this_meal.fiber += (float(this_ingredient.fiber) * float(quantity))
                                    this_meal.protein += (float(this_ingredient.protein) * float(quantity))
                                    this_meal.vitamin_a += (float(this_ingredient.vitamin_a) * float(quantity))
                                    this_meal.vitamin_c += (float(this_ingredient.vitamin_c) * float(quantity))
                                    this_meal.vitamin_d += (float(this_ingredient.vitamin_d) * float(quantity))
                                    this_meal.vitamin_k += (float(this_ingredient.vitamin_k) * float(quantity))
                                    this_meal.potassium += (float(this_ingredient.potassium) * float(quantity))
                                    this_meal.sodium += (float(this_ingredient.sodium) * float(quantity))
                                    this_meal.cholesterol += (float(this_ingredient.cholesterol) * float(quantity))
                                else:
                                    pass
                        folder_directory = "meal_instructions/"
                        instruction_directory = os.path.join(folder_directory,
                                                             inflection.underscore(meal_name) + "_instructions.txt")
                        try:
                            with open(instruction_directory, "r", encoding="utf-8") as meal_instructions_txt:
                                meal_instructions_txt.close()
                        except FileNotFoundError:
                            with open(instruction_directory, "w+", encoding="utf-8") as meal_instructions_txt:
                                meal_instructions_txt.write("No Instructions")
                                meal_instructions_txt.close()
                print("CSV sync successful.")

    def sync_meals_from_google_sheets(self) -> None:
        """Deletes the meals currently contained in the database and recreates the meals from the URL."""
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjS3n1KA5odkbCOf60D6CQ_SZkSZFZDgH8JVoxPzDCCDSx1zd8KXJWGWpUgSV9Cfg3y3iKftxKFamQ/pub?gid=776826678&single=true&output=csv"
        ftpstream = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
        self.meals = {}
        for line in csvfile:
            if line[0] == "meal_name":
                pass
            else:
                if len(line[0]) != 0:
                    meal_name = line[0]
                else:
                    meal_name = ""
                if len(line[1]) != 0:
                    prep_time = line[1]
                else:
                    prep_time = ""
                if len(line[2]) != 0:
                    ingredient_1_name = line[2]
                else:
                    ingredient_1_name = ""
                if len(line[3]) != 0:
                    ingredient_1_quantity = line[3]
                else:
                    ingredient_1_quantity = ""
                if len(line[4]) != 0:
                    ingredient_2_name = line[4]
                else:
                    ingredient_2_name = ""
                if len(line[5]) != 0:
                    ingredient_2_quantity = line[5]
                else:
                    ingredient_2_quantity = ""
                if len(line[6]) != 0:
                    ingredient_3_name = line[6]
                else:
                    ingredient_3_name = ""
                if len(line[7]) != 0:
                    ingredient_3_quantity = line[7]
                else:
                    ingredient_3_quantity = ""
                if len(line[8]) != 0:
                    ingredient_4_name = line[8]
                else:
                    ingredient_4_name = ""
                if len(line[9]) != 0:
                    ingredient_4_quantity = line[9]
                else:
                    ingredient_4_quantity = ""
                if len(line[10]) != 0:
                    ingredient_5_name = line[10]
                else:
                    ingredient_5_name = ""
                if len(line[11]) != 0:
                    ingredient_5_quantity = line[11]
                else:
                    ingredient_5_quantity = ""
                if len(line[12]) != 0:
                    ingredient_6_name = line[12]
                else:
                    ingredient_6_name = ""
                if len(line[13]) != 0:
                    ingredient_6_quantity = line[13]
                else:
                    ingredient_6_quantity = ""
                if len(line[14]) != 0:
                    ingredient_7_name = line[14]
                else:
                    ingredient_7_name = ""
                if len(line[15]) != 0:
                    ingredient_7_quantity = line[15]
                else:
                    ingredient_7_quantity = ""
                if len(line[16]) != 0:
                    ingredient_8_name = line[16]
                else:
                    ingredient_8_name = ""
                if len(line[17]) != 0:
                    ingredient_8_quantity = line[17]
                else:
                    ingredient_8_quantity = ""
                if len(line[18]) != 0:
                    ingredient_9_name = line[18]
                else:
                    ingredient_9_name = ""
                if len(line[19]) != 0:
                    ingredient_9_quantity = line[19]
                else:
                    ingredient_9_quantity = ""
                if len(line[20]) != 0:
                    ingredient_10_name = line[20]
                else:
                    ingredient_10_name = ""
                if len(line[21]) != 0:
                    ingredient_10_quantity = line[21]
                else:
                    ingredient_10_quantity = ""
                if len(line[22]) != 0:
                    ingredient_11_name = line[22]
                else:
                    ingredient_11_name = ""
                if len(line[23]) != 0:
                    ingredient_11_quantity = line[23]
                else:
                    ingredient_11_quantity = ""
                if len(line[24]) != 0:
                    ingredient_12_name = line[24]
                else:
                    ingredient_12_name = ""
                if len(line[25]) != 0:
                    ingredient_12_quantity = line[25]
                else:
                    ingredient_12_quantity = ""
                if len(line[26]) != 0:
                    taste_preference = line[26]
                else:
                    taste_preference = 0
                self.meals[meal_name] = Meal(meal_name=meal_name, prep_time=int(prep_time), taste_preference=float(taste_preference))
                this_meal = self.meals[meal_name]
                ingredients_to_add = {}
                if len(ingredient_1_name) != 0 and len(ingredient_1_quantity) != 0:
                    ingredients_to_add[ingredient_1_name] = float(ingredient_1_quantity)
                if len(ingredient_2_name) != 0 and len(ingredient_2_quantity) != 0:
                    ingredients_to_add[ingredient_2_name] = float(ingredient_2_quantity)
                if len(ingredient_3_name) != 0 and len(ingredient_3_quantity) != 0:
                    ingredients_to_add[ingredient_3_name] = float(ingredient_3_quantity)
                if len(ingredient_4_name) != 0 and len(ingredient_4_quantity) != 0:
                    ingredients_to_add[ingredient_4_name] = float(ingredient_4_quantity)
                if len(ingredient_5_name) != 0 and len(ingredient_5_quantity) != 0:
                    ingredients_to_add[ingredient_5_name] = float(ingredient_5_quantity)
                if len(ingredient_6_name) != 0 and len(ingredient_6_quantity) != 0:
                    ingredients_to_add[ingredient_6_name] = float(ingredient_6_quantity)
                if len(ingredient_7_name) != 0 and len(ingredient_7_quantity) != 0:
                    ingredients_to_add[ingredient_7_name] = float(ingredient_7_quantity)
                if len(ingredient_8_name) != 0 and len(ingredient_8_quantity) != 0:
                    ingredients_to_add[ingredient_8_name] = float(ingredient_8_quantity)
                if len(ingredient_9_name) != 0 and len(ingredient_9_quantity) != 0:
                    ingredients_to_add[ingredient_9_name] = float(ingredient_9_quantity)
                if len(ingredient_10_name) != 0 and len(ingredient_10_quantity) != 0:
                    ingredients_to_add[ingredient_10_name] = float(ingredient_10_quantity)
                if len(ingredient_11_name) != 0 and len(ingredient_11_quantity) != 0:
                    ingredients_to_add[ingredient_11_name] = float(ingredient_11_quantity)
                if len(ingredient_12_name) != 0 and len(ingredient_12_quantity) != 0:
                    ingredients_to_add[ingredient_12_name] = float(ingredient_12_quantity)
                for new_ingredient in ingredients_to_add.keys():
                    for ingredient in self.ingredients:
                        this_ingredient = self.ingredients[ingredient]
                        if this_ingredient.ingredient_name == new_ingredient:
                            quantity = ingredients_to_add[new_ingredient]
                            this_meal.ingredients[this_ingredient] = this_ingredient
                            this_meal.quantities[this_ingredient] = quantity
                            this_meal.calories += float(this_ingredient.calories) * float(quantity)
                            this_meal.fat += float(this_ingredient.fat) * float(quantity)
                            this_meal.carbs += float(this_ingredient.carbs) * float(quantity)
                            this_meal.fiber += (float(this_ingredient.fiber) * float(quantity))
                            this_meal.protein += (float(this_ingredient.protein) * float(quantity))
                            this_meal.vitamin_a += (float(this_ingredient.vitamin_a) * float(quantity))
                            this_meal.vitamin_c += (float(this_ingredient.vitamin_c) * float(quantity))
                            this_meal.vitamin_d += (float(this_ingredient.vitamin_d) * float(quantity))
                            this_meal.vitamin_k += (float(this_ingredient.vitamin_k) * float(quantity))
                            this_meal.potassium += (float(this_ingredient.potassium) * float(quantity))
                            this_meal.sodium += (float(this_ingredient.sodium) * float(quantity))
                            this_meal.cholesterol += (float(this_ingredient.cholesterol) * float(quantity))
                        else:
                            pass
                folder_directory = "meal_instructions/"
                instruction_directory = os.path.join(folder_directory,
                                                     inflection.underscore(meal_name) + "_instructions.txt")
                try:
                    with open(instruction_directory, "r", encoding="utf-8") as meal_instructions_txt:
                        meal_instructions_txt.close()
                except FileNotFoundError:
                    with open(instruction_directory, "w+", encoding="utf-8") as meal_instructions_txt:
                        meal_instructions_txt.write("No Instructions")
                        meal_instructions_txt.close()
        print("Google Sheets meal sync complete.\nIf an ingredient wasn't previously defined, it wasn't added to the meal.")
        self.reload_meals()

    def remove_ingredient(self) -> None:
        """Removes an ingredient from the database."""
        ingredient = input("Which ingredient would you like to remove from the database?\n-> ").lower()
        if ingredient in self.ingredients.keys():
            del self.ingredients[ingredient]
        else:
            print("Ingredient not found in database.")

    def print_ingredient_nutrients(self) -> None:
        """Prints the nutrition facts of an ingredient."""
        printing_nutrition = True
        checking_error = True
        while printing_nutrition is True:
            ingredient_to_check = input("Enter ingredient to print nutrition facts:\n-> ").lower()
            if ingredient_to_check in self.ingredients.keys():
                ingredient = self.ingredients[ingredient_to_check]
                ingredient.print_ing_nutrition()
                printing_nutrition = False
            else:
                while checking_error is True:
                    error_message = input("\'" + ingredient_to_check + "\' not in database. Try again(1) or cancel(2).")
                    if error_message == "1":
                        checking_error = False
                    elif error_message == "2":
                        checking_error = False
                        printing_nutrition = False
                    else:
                        print("Invalid input.")

    def print_meal_nutrients(self) -> None:
        """Prints the nutrition facts of a meal."""
        printing_nutrition = True
        checking_error = True
        while printing_nutrition is True:
            meal_to_check = input("Enter meal to print nutrition facts:\n-> ").lower()
            if meal_to_check in self.meals.keys():
                meal = self.meals[meal_to_check]
                meal.print_meal_nutrition()
                printing_nutrition = False
            else:
                while checking_error is True:
                    error_message = input("\'" + meal_to_check + "\' not in database. Try again(1) or cancel(2).")
                    if error_message == "1":
                        checking_error = False
                    elif error_message == "2":
                        checking_error = False
                        printing_nutrition = False
                    else:
                        print("Invalid input.")

    def print_all_ingredients_in_database(self) -> None:
        """Prints all ingredients contained in the database."""
        count_ingredients = 0
        for ingredient in self.ingredients.keys():
            count_ingredients += 1
            if count_ingredients == 0:
                print("There are no ingredients in the database.")
            else:
                this_ingredient = self.ingredients[ingredient]
                print(inflection.titleize(this_ingredient.ingredient_name))

    def print_ingredient_inventory(self) -> None:
        """Prints the quantity of each ingredient you currently have on hand."""
        print("================== CURRENT INVENTORY ==================\n")
        for ingredient in self.ingredients.keys():
            this_ingredient = self.ingredients[ingredient]
            if this_ingredient.quantity_on_hand > 0:
                print(str(round(this_ingredient.quantity_on_hand, 2)) + " x " + str(this_ingredient.measurement) + " " +
                      str(inflection.titleize(this_ingredient.ingredient_name)))
        print("\n=======================================================")

    def print_all_meals_in_database(self) -> None:
        """Prints all the meals in the database."""
        count_meals = 0
        for meal in self.meals.keys():
            count_meals += 1
            if count_meals == 0:
                print("There are no meals in the database.")
            else:
                this_meal = self.meals[meal]
                if this_meal.is_snack is False:
                    print(inflection.titleize(this_meal.meal_name))

    def add_meal(self) -> None:
        """Adds a meal to the database and creates an instruction.txt file."""
        getting_input = "Y"
        while getting_input != "N":
            meal_name = input("Enter meal name:\n-> ").lower()
            if meal_name not in self.meals.keys():
                folder_directory = "C:/Users/18327/PycharmProjects/csci127-su22/Personal Projects/CSCI-127 Final/meal_instructions/"
                instruction_directory = os.path.join(folder_directory,
                                                     inflection.underscore(meal_name) + "_instructions.txt")
                with open(instruction_directory, "w", encoding="utf-8") as meal_instructions_txt:
                    instructions = "< No Instructions >"
                    meal_instructions_txt.write(instructions)
                    meal_instructions_txt.close()
                prep_time = int(input("Enter meal preparation time in minutes:\n-> "))
                taste_preference = float(input("On a scale of 1-5 (5 being best), how does it taste?\n-> "))
                self.meals[meal_name] = Meal(meal_name, prep_time, taste_preference)
                print("\'" + meal_name.title() + "\' added to database.")
                getting_input = "N"
            else:
                getting_input = input("Meal already in database. Would you like to enter a new meal? "
                                      "\'Y\'/\'N\'\n-> ").upper()
                if getting_input != 'Y' or getting_input != 'N':
                    getting_input = input("Unrecognized command. Would you like to enter a new meal? Type "
                                          "\'Y\' for yes, \'N\' for no.\n-> ").upper()

    def remove_meal(self) -> None:
        """Removes a meal from the database."""
        meal = input("Which meal would you like to remove from the database?\n-> ").lower()
        if meal in self.meals.keys():
            del self.meals[meal]
        else:
            print("Meal not found in database.")

    def print_ingredients_in_meal(self) -> None:
        """Prints ingredient objects contained in a meal object."""
        meal = input("For which meal would you like to print the ingredients?\n-> ").lower()
        if meal not in self.meals.keys():
            print("\'" + meal + "\' not found in database.")
        else:
            this_meal = self.meals[meal]
            print(this_meal.meal_name.title() + " contains:")
            for ingredient in this_meal.ingredients.keys():
                this_ingredient = this_meal.ingredients[ingredient]
                print(str(this_meal.quantities[ingredient]) + " x " + str(this_ingredient.measurement) + " "
                      + inflection.titleize(this_ingredient.ingredient_name))

    def reload_meals(self) -> None:
        """Deletes and recreates meals currently in the database. Solves the problem of a possible changed memory
        address after syncing from CSV or Google Sheets."""
        for meal in self.meals:
            this_meal = self.meals[meal]
            meal_name = this_meal.meal_name
            meal_prep_time = this_meal.prep_time
            meal_taste_preference = this_meal.taste_preference
            ingredients_to_add = {}
            for ingredient in this_meal.ingredients.keys():
                this_ingredient = this_meal.ingredients[ingredient]
                ingredients_to_add[this_ingredient.ingredient_name] = this_meal.quantities[ingredient]
            del meal
            self.meals[meal_name] = Meal(meal_name, meal_prep_time, meal_taste_preference)
            for new_ingredient in ingredients_to_add.keys():
                this_meal = self.meals[meal_name]
                this_ingredient = self.ingredients[new_ingredient]
                quantity = ingredients_to_add[new_ingredient]
                this_meal.ingredients[this_ingredient] = this_ingredient
                this_meal.quantities[this_ingredient] = quantity
                this_meal.calories += float(this_ingredient.calories) * float(quantity)
                this_meal.fat += float(this_ingredient.fat) * float(quantity)
                this_meal.carbs += float(this_ingredient.carbs) * float(quantity)
                this_meal.fiber += (float(this_ingredient.fiber) * float(quantity))
                this_meal.protein += (float(this_ingredient.protein) * float(quantity))
                this_meal.vitamin_a += (float(this_ingredient.vitamin_a) * float(quantity))
                this_meal.vitamin_c += (float(this_ingredient.vitamin_c) * float(quantity))
                this_meal.vitamin_d += (float(this_ingredient.vitamin_d) * float(quantity))
                this_meal.vitamin_k += (float(this_ingredient.vitamin_k) * float(quantity))
                this_meal.potassium += (float(this_ingredient.potassium) * float(quantity))
                this_meal.sodium += (float(this_ingredient.sodium) * float(quantity))
                this_meal.cholesterol += (float(this_ingredient.cholesterol) * float(quantity))

    def assign_ingredient_to_meal(self) -> None:
        """Assigns an ingredient object to a meal object."""
        meal = input("Which meal do you want to assign an ingredient to?\n-> ").lower()
        if meal not in self.meals.keys():
            getting_input = input("\'" + meal + "\' not in database. Would you like to enter a new meal? "
                                                "\'Y\'/\'N\'\n-> ").upper()
            if getting_input == 'Y':
                self.add_meal()
            elif getting_input == 'N':
                pass
            else:
                print("Unrecognized command.")
        else:
            ingredient = input("Which ingredient do you want to assign?\n-> ").lower()
            if ingredient not in self.ingredients.keys():
                getting_input = input(
                    "\'" + ingredient + "\' not in database. Would you like to enter a new ingredient? "
                                        "\'Y\'/\'N\'\n-> ").upper()
                if getting_input == 'Y':
                    self.add_ingredient()
                elif getting_input == 'N':
                    pass
                else:
                    print("Unrecognized command.")
            else:
                this_meal = self.meals[meal]
                this_ingredient = self.ingredients[ingredient]
                quantity = input(
                    "Enter quantity of " + ingredient + ", measured in " + this_ingredient.measurement + ":\n-> ")
                this_meal.ingredients[this_ingredient] = this_ingredient
                this_meal.quantities[this_ingredient] = quantity
                this_meal.calories += float(this_ingredient.calories) * float(quantity)
                this_meal.fat += float(this_ingredient.fat) * float(quantity)
                this_meal.carbs += float(this_ingredient.carbs) * float(quantity)
                this_meal.fiber += (float(this_ingredient.fiber) * float(quantity))
                this_meal.protein += (float(this_ingredient.protein) * float(quantity))
                this_meal.vitamin_a += (float(this_ingredient.vitamin_a) * float(quantity))
                this_meal.vitamin_c += (float(this_ingredient.vitamin_c) * float(quantity))
                this_meal.vitamin_d += (float(this_ingredient.vitamin_d) * float(quantity))
                this_meal.vitamin_k += (float(this_ingredient.vitamin_k) * float(quantity))
                this_meal.potassium += (float(this_ingredient.potassium) * float(quantity))
                this_meal.sodium += (float(this_ingredient.sodium) * float(quantity))
                this_meal.cholesterol += (float(this_ingredient.cholesterol) * float(quantity))
                print("\'" + inflection.titleize(ingredient) + "\'" + " added to " + inflection.titleize(meal) + ".\n")
                print(this_meal.meal_name.title() + " contains:")
                for ingredient in this_meal.ingredients.keys():
                    this_ingredient = this_meal.ingredients[ingredient]
                    print(this_meal.quantities[ingredient] + " x " + this_ingredient.measurement + " "
                          + inflection.titleize(this_ingredient.ingredient_name))

    def remove_ingredient_from_meal(self) -> None:
        """Removes an ingredient from a meal."""
        meal = input("Which meal would you like to remove an ingredient from?\n-> ").lower()
        if meal not in self.meals.keys():
            print("\'" + inflection.titleize(meal) + "\' not found in database.")
        else:
            ingredient_to_remove = input("Which ingredient would you like to remove?\n-> ").lower()
            this_meal = self.meals[meal]
            for ingredient in this_meal.ingredients:
                this_ingredient = this_meal.ingredients[ingredient]
                if ingredient_to_remove == this_ingredient.ingredient_name:
                    del ingredient
                    print(inflection.titleize(ingredient_to_remove) + " removed from " + inflection.titleize(meal) + ".")

    def change_prep_time_of_meal(self) -> None:
        """Changes a meal's prep time."""
        meal = input("Which meal would you like to change the prep time of?\n-> ").lower()
        if meal not in self.meals.keys():
            print("\'" + meal + "\' not found in database.")
        else:
            this_meal = self.meals[meal]
            this_meal.prep_time = round(float(input("Enter the prep time of \'" + this_meal.meal_name + ":\n-> ")), 2)

    def assign_meal_to_plan(self, plan: Plan, meal_to_assign: Meal) -> None:
        """Assigns a meal object to a plan object. Keeps track of quantities of meals contained in the plan."""
        this_plan = self.plans[plan]
        this_meal = meal_to_assign
        this_plan.meals[this_meal] = this_meal
        try:
            this_plan.quantities[this_meal] += 1
        except KeyError:
            this_plan.quantities[this_meal] = 1
        this_plan.prep_time += this_meal.prep_time
        this_plan.calories += this_meal.calories
        this_plan.fat += this_meal.fat
        this_plan.carbs += this_meal.carbs
        this_plan.fiber += this_meal.fiber
        this_plan.protein += this_meal.protein
        this_plan.vitamin_a += this_meal.vitamin_a
        this_plan.vitamin_b += this_meal.vitamin_b
        this_plan.vitamin_c += this_meal.vitamin_c
        this_plan.vitamin_d += this_meal.vitamin_d
        this_plan.vitamin_k += this_meal.vitamin_k
        this_plan.potassium += this_meal.potassium
        this_plan.sodium += this_meal.sodium
        this_plan.cholesterol += this_meal.cholesterol
        this_plan.taste_preference += this_meal.taste_preference

    def generate_new_plans(self) -> None:
        """Generates a large number of potential plans by randomly assigning meals based on criteria a user inputs.
        Vast majority of plans will be duplicates but everything but the top five will be removed later when user goes
        to display plans generated."""
        generating_new_plans = True
        while generating_new_plans is True:
            number_of_meals = 0
            while number_of_meals == 0:
                try:
                    number_of_days = int(float(input("How many days would you like to plan? (Generates lunch and dinner.)\n-> ")))
                    number_of_meals = number_of_days * 2
                except ValueError:
                    print("Invalid input. Input should be a whole number.")
            meal_frequency = 0
            while meal_frequency == 0:
                try:
                    meal_frequency = int(float(input("How many times maximum are you willing to eat the same meal?\n-> ")))
                except ValueError:
                    print("Invalid input. Input should be a whole number.")
            budget = 0
            while budget == 0:
                try:
                    budget = float(input("What's your budget?\n-> "))
                except ValueError:
                    print("Invalid input. (Note: do not use $ or other symbols.)")
            print("Generating plans...")
            if number_of_meals > 0:
                meal_list = list(self.meals.values())
                self.plans = {}
                plan_number = 0
                for new_plan_index in range(15000):  # Generates a large number of plans
                    plan_number += 1
                    new_plan_index = Plan()
                    new_plan_index.budget = budget
                    new_plan_index.index = plan_number
                    self.plans[new_plan_index] = new_plan_index
                    for meal in range(number_of_meals):
                        meal_selected = False
                        while meal_selected is False:
                            random_meal = random.choice(meal_list)
                            if random_meal in new_plan_index.meals:
                                if new_plan_index.quantities[random_meal] < meal_frequency:
                                    self.assign_meal_to_plan(new_plan_index, random_meal)
                                    meal_selected = True
                                else:
                                    pass
                            elif random_meal not in new_plan_index.meals:
                                self.assign_meal_to_plan(new_plan_index, random_meal)
                                meal_selected = True
                            else:
                                pass
                    new_plan_index.overall_score = round(
                        new_plan_index.single_metric_score(number_of_meals, self.user_preferences["Calories"],
                                                           self.user_preferences["Fat"], self.user_preferences["Carbs"],
                                                           self.user_preferences["Fiber"],
                                                           self.user_preferences["Protein"],
                                                           self.user_preferences["Prep time per week"]), 2)
                print("Plans generated successfully.")
                generating_new_plans = False
            else:
                print("Please input a number greater than 0.")

    def get_top_five_plans(self) -> None:
        """If there are five or more plans that fit your criteria, this method narrows the generated plans down to
        a top five based on score (with some further refinement if calories are way outside 2000/day)"""
        sorted_by_score_list = []
        top_five_list = []
        self.top_five_plans = {}
        for plan in self.plans:
            this_plan = self.plans[plan]
            if this_plan.cost > this_plan.budget:
                del this_plan
            else:
                if this_plan.calories_score < 80:
                    del this_plan
                else:
                    if this_plan.calories_score > 120:
                        del this_plan
                    else:
                        score_entry = [this_plan.overall_score, this_plan.index]
                        sorted_by_score_list.append(score_entry)
        sorted_by_score_list.sort(reverse=True)
        for score_entry in sorted_by_score_list:
            this_score = score_entry[0]
            if sorted_by_score_list.count(this_score) > 1:
                del score_entry
            else:
                pass
        if len(sorted_by_score_list) >= 5:
            for score in range(5):
                top_five_list.append(sorted_by_score_list[score])
        else:
            for score in range(len(sorted_by_score_list)):
                top_five_list.append(sorted_by_score_list[score])
        for score in top_five_list:
            plan_to_add_index = score[1]
            for plan in self.plans:
                this_plan = self.plans[plan]
                if this_plan.index == plan_to_add_index:
                    self.top_five_plans[this_plan] = this_plan

    def print_all_plans(self) -> None:
        """For each plan previously generated, assigns a price/plan cost through a virtual shopping trip.
        Considers current inventory in assigning price. Then calls get_top_five_plans and displays those."""
        for plan in self.plans:
            self.get_ingredients_in_cart(plan)
            self.get_ingredients_to_purchase()
            self.virtual_shopping_trip(plan)
        self.get_top_five_plans()
        self.plans = {}
        for plan in self.top_five_plans:
            this_plan = self.top_five_plans[plan]
            print("\n======================== PLAN " + str(this_plan.index) + " ========================")
            print("Total cost is: $" + str(round(this_plan.cost, 2)))
            print("Meals contained:")
            for meal in this_plan.meals:
                this_meal = this_plan.meals[meal]
                print("\t" + str(this_plan.quantities[this_meal]) + " x " + inflection.titleize(this_meal.meal_name))
            this_plan.print_score()

    def select_and_export_plan(self) -> None:
        """Allows user to select a top five plan and export it."""
        selected_plan = None
        plan_id = int(input("Please input the number of the plan you want to export."))
        plan_found = False
        for plan in self.top_five_plans:
            test_plan = self.top_five_plans[plan]
            if test_plan.index == plan_id:
                selected_plan = test_plan
                print("Plan " + str(test_plan.index) + " selected.")
                plan_found = True
        if plan_found is True:
            # Write instructions
            print("Exporting plan...")
            plan_folder_directory = "plan_instructions/"
            plan_instruction_directory = os.path.join(plan_folder_directory,
                                                      "meal_plan_instructions.txt")
            with open(plan_instruction_directory, "w+", encoding="utf-8") as plan_instructions_txt:
                intro_str = "======================== PLAN " + str(selected_plan.index) + " ========================\n"
                plan_instructions_txt.write(intro_str)
                current_time = datetime.datetime.now()
                plan_instructions_txt.write("Plan generated " + str(current_time) + "\n")
                total_cost_str = "\nTOTAL COST: $" + str(round(selected_plan.cost, 2))
                plan_instructions_txt.write(total_cost_str + "\n")
                plan_instructions_txt.write("\nMEALS CONTAINED:\n")
                for meal in selected_plan.meals:
                    this_meal = selected_plan.meals[meal]
                    plan_instructions_txt.write(
                        "\t" + str(selected_plan.quantities[this_meal]) + " x " + inflection.titleize(
                            this_meal.meal_name) + "\n")
                plan_instructions_txt.write("\nYOU WILL NEED:\n")
                for item in selected_plan.ingredients_to_purchase:
                    plan_instructions_txt.write("\t" + item + "\n")
                plan_instructions_txt.write("\n")
                for meal in selected_plan.meals:
                    this_meal = selected_plan.meals[meal]
                    # plan_instructions_txt.write("\n============================================================\n")
                    plan_instructions_txt.write("\n\n" + this_meal.meal_name.upper())
                    plan_instructions_txt.write("\n============================================================\n")
                    plan_instructions_txt.write("INGREDIENTS:")
                    for ingredient in this_meal.ingredients.keys():
                        this_ingredient = this_meal.ingredients[ingredient]
                        ing_quantities_str = "\n\t" + str(this_meal.quantities[ingredient]) + " x " + \
                                             str(this_ingredient.measurement) + " " + \
                                             inflection.titleize(this_ingredient.ingredient_name)
                        plan_instructions_txt.write(ing_quantities_str)
                    meal_folder_directory = "meal_instructions/"
                    meal_instruction_directory = os.path.join(meal_folder_directory,
                                                         inflection.underscore(this_meal.meal_name) + "_instructions.txt")
                    with open(meal_instruction_directory, "r", encoding="utf-8") as meal_instructions_txt:
                        this_meal.instructions = meal_instructions_txt.read()
                        plan_instructions_txt.write("\n\nINSTRUCTIONS:\n" + this_meal.instructions + "\n")
                        meal_instructions_txt.close()
                    plan_instructions_txt.write("\nNUTRITION FACTS")
                    plan_instructions_txt.write("\n\tCalories " + "\t\t" + str(this_meal.calories))
                    plan_instructions_txt.write("\n\tFat " + "\t\t\t" + str(this_meal.fat) + " grams")
                    plan_instructions_txt.write("\n\tCarbs " + "\t\t\t" + str(this_meal.carbs) + " grams")
                    plan_instructions_txt.write("\n\tFiber " + "\t\t\t" + str(this_meal.fiber) + " grams")
                    plan_instructions_txt.write("\n\tProtein " + "\t\t" + str(this_meal.protein) + " grams")
                    plan_instructions_txt.write("\n\tVitamin A " + "\t\t" + str(this_meal.vitamin_a) + "% daily value")
                    plan_instructions_txt.write("\n\tVitamin C " + "\t\t" + str(this_meal.vitamin_c) + "% daily value")
                    plan_instructions_txt.write("\n\tVitamin D " + "\t\t" + str(this_meal.vitamin_d) + "% daily value")
                    plan_instructions_txt.write("\n\tVitamin K " + "\t\t" + str(this_meal.vitamin_k) + "% daily value")
                    plan_instructions_txt.write("\n\tPotassium " + "\t\t" + str(this_meal.potassium) + "% daily value")
                    plan_instructions_txt.write("\n\tSodium " + "\t\t\t" + str(this_meal.sodium) + "% daily value")
                    plan_instructions_txt.write("\n\tCholesterol " + "\t" + str(this_meal.cholesterol) + "% daily value")
                    plan_instructions_txt.write("\n\n")
                print("\'meal_plan_instructions.txt\' saved in /plan_instructions/.")
                plan_instructions_txt.close()
        else:
            print("Plan not found. Please select from the top five plans or the cheapest plan.")

    def get_ingredients_in_cart(self, plan: Plan) -> None:
        """Loops through meals in a plan and adds the ingredients contained to a shopping cart dictionary."""
        self.ingredients_in_cart = {}
        for meal in plan.meals:
            for ingredient in meal.ingredients.keys():
                this_ingredient = meal.ingredients[ingredient]
                try:
                    self.ingredients_in_cart[this_ingredient.ingredient_name] += meal.quantities[ingredient] * plan.quantities[meal]
                except KeyError:
                    self.ingredients_in_cart[this_ingredient.ingredient_name] = meal.quantities[ingredient] * plan.quantities[meal]

    def get_ingredients_to_purchase(self) -> None:
        """Takes the shopping cart dictionary from get_ingredients_in_cart and considers whether each item is already in
        inventory. If so, removes the item from the shopping cart."""
        self.ingredients_to_purchase = {}
        self.ingredients_to_purchase = self.ingredients_in_cart.copy()
        for ingredient_name in self.ingredients_to_purchase.keys():
            for ingredient_object in self.ingredients:
                test_ingredient = self.ingredients[ingredient_object]
                if ingredient_name == test_ingredient.ingredient_name:
                    self.ingredients_to_purchase[ingredient_name] -= test_ingredient.quantity_on_hand
                    if self.ingredients_to_purchase[ingredient_name] < 0:
                        self.ingredients_to_purchase[ingredient_name] = 0

    def virtual_shopping_trip(self, plan: Plan) -> None:
        """Method created to solve the problem of per serving cost vs actual cost. Seeks to generate an actual cost
        for a meal plan rather than how people will claim their recipes are cheap if you plan to eat 10 servings,
        for example. Takes a virtual grocery store trip for each meal plan with a previously generated list of
        ingredients to purchase and returns the total cost of the plan."""
        for ingredient_name in self.ingredients_to_purchase.keys():
            number_to_buy = self.ingredients_to_purchase[ingredient_name]
            for ingredient_object in self.ingredients:
                test_ingredient = self.ingredients[ingredient_object]
                if ingredient_name == test_ingredient.ingredient_name:
                    this_ingredient = test_ingredient
                    purchase_quantity = this_ingredient.purchase_quantity
                    purchase_price = this_ingredient.purchase_price
                    if number_to_buy == 0:
                        pass
                    elif number_to_buy <= purchase_quantity:
                        plan.cost += purchase_price
                        plan.ingredients_to_purchase.append(
                            "1x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity < number_to_buy <= purchase_quantity * 2:
                        plan.cost += purchase_price * 2
                        plan.ingredients_to_purchase.append(
                            "2x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 2 < number_to_buy <= purchase_quantity * 3:
                        plan.cost += purchase_price * 3
                        plan.ingredients_to_purchase.append(
                            "3x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 3 < number_to_buy <= purchase_quantity * 4:
                        plan.cost += purchase_price * 4
                        plan.ingredients_to_purchase.append(
                            "4x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 4 < number_to_buy <= purchase_quantity * 5:
                        plan.cost += purchase_price * 5
                        plan.ingredients_to_purchase.append(
                            "5x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 5 < number_to_buy <= purchase_quantity * 6:
                        plan.cost += purchase_price * 6
                        plan.ingredients_to_purchase.append(
                            "6x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 6 < number_to_buy <= purchase_quantity * 7:
                        plan.cost += purchase_price * 7
                        plan.ingredients_to_purchase.append(
                            "7x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 7 < number_to_buy <= purchase_quantity * 8:
                        plan.cost += purchase_price * 8
                        plan.ingredients_to_purchase.append(
                            "8x" + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 8 < number_to_buy <= purchase_quantity * 9:
                        plan.cost += purchase_price * 9
                        plan.ingredients_to_purchase.append(
                            "9x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 9 < number_to_buy <= purchase_quantity * 10:
                        plan.cost += purchase_price * 10
                        plan.ingredients_to_purchase.append(
                            "10x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 10 < number_to_buy <= purchase_quantity * 11:
                        plan.cost += purchase_price * 11
                        plan.ingredients_to_purchase.append(
                            "11x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 11 < number_to_buy <= purchase_quantity * 12:
                        plan.cost += purchase_price * 12
                        plan.ingredients_to_purchase.append(
                            "12x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 12 < number_to_buy <= purchase_quantity * 13:
                        plan.cost += purchase_price * 13
                        plan.ingredients_to_purchase.append(
                            "13x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    elif purchase_quantity * 13 < number_to_buy <= purchase_quantity * 14:
                        plan.cost += purchase_price * 14
                        plan.ingredients_to_purchase.append(
                            "14x " + this_ingredient.ingredient_name + " at $" + str(purchase_price))
                    else:
                        plan.cost = 10000
                else:
                    pass

