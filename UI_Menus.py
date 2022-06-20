class UI_Menu:

    def __init__(self):
        pass

    def print_main_menu(self) -> None:
        """Prints the main menu"""
        print("\n======== MAIN MENU ========")
        print("'1' - User")
        print("'2' - Ingredients")
        print("'3' - Meals")
        print("'4' - Meal Planning")
        print("'5' - Sync from Google Sheets")
        print("'?' - Print this menu again")
        print("'X' - Save and quit")

    def print_user_menu(self) -> None:
        "Prints the user menu"
        print("\n======= USER ========")
        print("'1' - View username")
        print("'2' - About this program")
        print("'?' - Print this menu again")
        print("'X' - Return to the main menu")

    def print_ingredients_menu(self) -> None:
        """Prints the ingredients menu"""
        print("\n======= INGREDIENTS ========")
        print("'1' - Add an ingredient to the database")
        print("'2' - Remove an ingredient from the database")
        print("'3' - Sync ingredients from Google Sheets")
        print("'4' - Sync ingredients from CSV")
        print("'5' - Sync ingredients to CSV")
        print("'6' - Print the nutrition facts of an ingredient")
        print("'7' - Print all ingredients in the database")
        print("'8' - Print the current inventory")
        print("'?' - Print this menu again")
        print("'X' - Return to the main menu")

    def print_meals_menu(self) -> None:
        """Prints the meals menu"""
        print("\n======== MEALS ========")
        print("'1'  - Add a meal to the database")
        print("'2'  - Remove a meal from the database")
        print("'3'  - Assign an ingredient to a meal")
        print("'4'  - Remove an ingredient from a meal")
        print("'5'  - Change preparation time of a meal")
        print("'6'  - Change cost of a meal")
        print("'7'  - Edit meal instructions")
        print("'8'  - Print all meals in the database")
        print("'9'  - Print all ingredients in a meal")
        print("'10' - Print nutrition facts for a meal")
        print("'11' - Sync meals from Google Sheets")
        print("'12' - Sync meals from CSV")
        print("'13' - Sync meals to CSV")
        print("'?'  - Print this menu again")
        print("'X'  - Return to the main menu")

    def print_meal_planning_menu(self) -> None:
        """Prints the meal planning menu"""
        print("\n======== MEAL PLANNING ========")
        print("'1' - Generate meal plans")
        print("'2' - Select and export plan")
        print("'?' - Print this menu again")
        print("'X' - Return to the main menu")