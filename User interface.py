from Database import Database
import jsonpickle
import os
from os import path
from UI_Menus import UI_Menu
from VirtualShoppingCart import VirtualShoppingCart


def autosave(database, load_name) -> None:
    output_file = jsonpickle.encode(db)
    current_directory = os.getcwd()
    save_file = "{0}.txt".format(load_name)
    cat_path = os.path.join(current_directory, save_file)
    file = open(cat_path, 'w+')
    file.write(output_file)
    file.close()


def print_about_info() -> None:
    print("\nThis is a meal-planner that"
          "\nallows you to input ingredients,"
          "\nmeals, and snacks. It will"
          "\ngenerate meal plans closest"
          "\nto your budget and nutritional"
          "\nneeds based on what you input.")


"""Loads the database"""
print("This is a text-based meal planner.")
loading = True
while loading is True:
    entering_username = True
    while entering_username is True:
        load_name = input("Enter your name:\n-> ").title()
        if len(load_name) != 0:
            symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "+", "/", "|", "?", "<",
                       ">", ".", "{", "}", "[", "]", ":", ";", ",", "'"]
            no_symbols = True
            for symbol in symbols:
                if symbol in load_name:
                    no_symbols = False
            if no_symbols is True:
                if not path.exists(load_name + ".txt"):
                    load_input = input("User not found. Create new user(1) or try again(2):\n-> ").title()
                    if load_input == "1":
                        db = Database()
                        db.user = load_name
                        entering_username = False
                        loading = False
                    elif load_input == 2:
                        pass
                else:
                    current_directory = os.getcwd()
                    cat_path = os.path.join(current_directory, load_name + ".txt")
                    file = open(cat_path, 'r')
                    pickled_database = file.read()
                    db = jsonpickle.decode(pickled_database)
                    file.close()
                    db.user = load_name
                    entering_username = False
                    loading = False
            else:
                print("Username cannot contain symbols.")
        else:
            print("Username cannot be blank.")

"""Prints welcome message"""
db.user_log_count += 1
print("\n===========================")
print("Welcome, " + db.user + ".")
if db.user_log_count > 1:
    print("You've logged on " + str(db.user_log_count) + " times.")
else:
    print_about_info()
print("===========================")

"""Main functionality"""
vs = VirtualShoppingCart()
ui = UI_Menu()
ui.print_main_menu()
user_input = input("\nWhat would you like to do?\n-> ").upper()
while user_input != "X":
    if user_input == "1":
        # TODO Users Menu
        ui.print_user_menu()
        user_user_input = input("\nWhat would you like to do?\n-> ").upper()
        while user_user_input != "X":
            if user_user_input == "1":
                """Print username"""
                print("Your username is " + db.user + ".")
                if db.user_log_count > 1:
                    print("You've logged on " + str(db.user_log_count) + " times.")
                else:
                    print("You've logged on 1 time.")
            elif user_user_input == "2":
                """Change user target preferences"""
                ui.print_targets_menu()
            elif user_user_input == "3":
                print_about_info()
            elif user_user_input == "?":
                """Print the ingredients menu"""
                ui.print_user_menu()
            else:
                print("Invalid input. Press \'?\' to display menu or try again.")
            autosave(db, load_name)
            ui.print_user_menu()
            user_user_input = input("\nWhat would you like to do?\n-> ").upper()
    elif user_input == "2":
        # TODO Ingredients Menu
        ui.print_ingredients_menu()
        user_ingredients_input = input("\nWhat would you like to do?\n-> ").upper()
        while user_ingredients_input != "X":
            if user_ingredients_input == "1":
                """Adds ingredient to the database"""
                db.add_ingredient()
            elif user_ingredients_input == "2":
                """Remove an ingredient from the database"""
                db.remove_ingredient()
            elif user_ingredients_input == "3":
                db.sync_ingredients_from_google_sheets()
            elif user_ingredients_input == "4":
                """Sync ingredients from CSV"""
                db.sync_ingredients_from_csv()
                db.reload_meals()
            elif user_ingredients_input == "5":
                """Sync ingredients to CSV"""
                db.sync_ingredients_to_csv()
            elif user_ingredients_input == "6":
                """Print the nutrition facts of an ingredient"""
                db.print_ingredient_nutrients()
            elif user_ingredients_input == "7":
                """Print all ingredients in the database"""
                db.print_all_ingredients_in_database()
            elif user_ingredients_input == "8":
                """Print current ingredient inventory"""
                db.print_ingredient_inventory()
            elif user_ingredients_input == "?":
                """Print the ingredients menu"""
                ui.print_ingredients_menu()
            else:
                print("Invalid input. Press \'?\' to display menu or try again.")
            autosave(db, load_name)
            ui.print_ingredients_menu()
            user_ingredients_input = input("\nWhat would you like to do?\n-> ").upper()
    elif user_input == "3":
        # TODO Meals Menu
        ui.print_meals_menu()
        user_meals_input = input("\nWhat would you like to do?\n-> ").upper()
        while user_meals_input != "X":
            if user_meals_input == "1":
                """Adds meal to the database"""
                db.add_meal()
            elif user_meals_input == "2":
                """Remove a meal from the database"""
                db.remove_meal()
            elif user_meals_input == "3":
                """Assign an ingredient to a meal"""
                db.assign_ingredient_to_meal()
            elif user_meals_input == "4":
                """Remove an ingredient from a meal"""
                db.remove_ingredient_from_meal()
            elif user_meals_input == "5":
                """Change prep time of a meal"""
                db.change_prep_time_of_meal()
            elif user_meals_input == "6":
                """Change cost of a meal"""
                db.change_cost_of_meal()
            elif user_meals_input == "7":
                """Edit meal instructions"""
                meal_name = input("For which meal would you like to edit the instructions?\n-> ").lower()
                if meal_name not in db.meals.keys():
                    print("\'" + meal_name + "\' not in database.")
                else:
                    db.meals[meal_name].write_meal_instructions()
            elif user_meals_input == "8":
                """Print all meals in the database"""
                db.print_all_meals_in_database()
            elif user_meals_input == "9":
                """Print all ingredients in a meal"""
                db.print_ingredients_in_meal()
            elif user_meals_input == "10":
                """Print nutrition facts for a meal"""
                db.print_meal_nutrients()
            elif user_meals_input == "11":
                """Mark meal as snack"""
                db.change_meal_to_snack()
            elif user_meals_input == "12":
                """Print all snacks in the database"""
                db.print_all_snacks_in_database()
            elif user_meals_input == "13":
                """Sync meals from Google Sheets"""
                db.sync_meals_from_google_sheets()
            elif user_meals_input == "14":
                """Sync meals from CSV"""
                db.sync_meals_from_csv()
            elif user_meals_input == "15":
                """Sync meals to CSV"""
                db.sync_meals_to_csv()
            elif user_meals_input == "?":
                """Print the meals menu"""
                ui.print_meals_menu()
            else:
                print("Invalid input. Press \'?\' to display menu or try again.")
            autosave(db, load_name)
            ui.print_meals_menu()
            user_meals_input = input("\nWhat would you like to do?\n-> ").upper()
    elif user_input == "4":
        # TODO Planning Menu
        ui.print_meal_planning_menu()
        user_plans_input = input("\nWhat would you like to do?\n-> ").upper()
        while user_plans_input != "X":
            if user_plans_input == "1":
                """Generates new plans at random"""
                db.generate_new_plans()
                db.print_all_plans()
            elif user_plans_input == "2":
                """Generate new plans around meal"""
                pass
            elif user_plans_input == "3":
                """Select and export plan"""
                db.select_and_export_plan()
            autosave(db, load_name)
            ui.print_meal_planning_menu()
            user_plans_input = input("\nWhat would you like to do?\n-> ").upper()
    elif user_input == "5":
        print("Syncing ingredients...")
        db.sync_ingredients_from_google_sheets()
        print("Syncing meals...")
        db.sync_meals_from_google_sheets()
    elif user_input == "?":
        """Prints Main Menu Again"""
        ui.print_main_menu()
    else:
        print("Invalid input. Press \'?\' to display menu or try again.")
    autosave(db, load_name)
    ui.print_main_menu()
    user_input = input("\nWhat would you like to do?\n-> ").upper()

autosave(db, load_name)
print("Save successful.")
