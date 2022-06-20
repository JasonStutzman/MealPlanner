class Plan:

    def __init__(self) -> None:
        self.index = 0
        self.overall_score = 0
        self.cost = 0
        self.budget = 0
        self.prep_time = 0
        self.meals = {}
        self.virtual_shopping_cart = {}
        self.quantities = {}
        self.ingredients_to_purchase = []
        self.taste_preference = 0
        self.taste_score = 0
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
        self.calories_score = 0
        self.fat_score = 0
        self.carbs_score = 0
        self.fiber_score = 0
        self.protein_score = 0
        self.vitamin_a_score = 0
        self.vitamin_b_score = 0
        self.vitamin_c_score = 0
        self.vitamin_d_score = 0
        self.vitamin_k_score = 0
        self.vitamin_score = 0
        self.potassium_score = 0
        self.sodium_score = 0
        self.cholesterol_score = 0
        self.prep_time_score = 0

    def score_meal_plan(self, number_of_meals: int, calorie_target: int, fat_target: float, carbs_target: float, fiber_target: float,
                        protein_target: float, prep_time_target: float) -> None:
        self.calories_score = int((self.calories / (calorie_target * number_of_meals)) * 100)
        self.fat_score = int((self.fat / (fat_target * number_of_meals)) * 100)
        self.carbs_score = int((self.carbs / (carbs_target * number_of_meals)) * 100)
        self.fiber_score = int((self.fiber / (fiber_target * number_of_meals)) * 100)
        self.protein_score = int((self.protein / (protein_target * number_of_meals)) * 100)
        self.vitamin_a_score = int((self.vitamin_a / (100 * number_of_meals)) * 100)
        self.vitamin_b_score = int((self.vitamin_b / (100 * number_of_meals)) * 100)
        self.vitamin_c_score = int((self.vitamin_c / (100 * number_of_meals)) * 100)
        self.vitamin_d_score = int((self.vitamin_d / (100 * number_of_meals)) * 100)
        self.vitamin_k_score = int((self.vitamin_k / (100 * number_of_meals)) * 100)
        self.vitamin_score = int((
                                         self.vitamin_a_score + self.vitamin_b_score + self.vitamin_c_score + self.vitamin_d_score + self.vitamin_k_score) / 5)
        self.potassium_score = int((self.potassium / (100 * number_of_meals)) * 100)
        self.sodium_score = int((self.vitamin_a / (100 * number_of_meals)) * 100)
        self.cholesterol_score = int((self.vitamin_a / (100 * number_of_meals)) * 100)
        self.prep_time_score = int((self.prep_time / prep_time_target) * 100)

    def single_metric_score(self, number_of_meals: int, calorie_target: int, fat_target: float, carbs_target: float, fiber_target: float,
                            protein_target: float, prep_time_target: float) -> float:
        fat_score_weight = 2.0
        general_nutrition_score_weight = 1.0
        protein_score_weight = 2.5
        prep_time_score_weight = 0.0
        vitamin_score_weight = 3.0
        cholesterol_score_weight = 2.0
        taste_score_weight = 0.75
        self.calories_score = (self.calories / (calorie_target * number_of_meals / 2)) * 100
        self.fat_score = (1 - abs((fat_target * number_of_meals / 2) - self.fat)/(fat_target * number_of_meals / 2)) * 100
        self.carbs_score = (1 - abs((carbs_target * number_of_meals / 2) - self.carbs)/(carbs_target * number_of_meals / 2)) * 100
        self.fiber_score = (1 - abs((fiber_target * number_of_meals / 2) - self.fiber)/(fat_target * number_of_meals / 2)) * 100
        self.protein_score = (1 - abs((protein_target * number_of_meals / 2) - self.protein)/(protein_target * number_of_meals / 2)) * 100
        if self.vitamin_a / number_of_meals / 2 >= 100:
            self.vitamin_a_score = 100
        else:
            self.vitamin_a_score = self.vitamin_a / number_of_meals / 2
        if self.vitamin_c / number_of_meals / 2 >= 100:
            self.vitamin_c_score = 100
        else:
            self.vitamin_c_score = self.vitamin_c / number_of_meals / 2
        if self.vitamin_d / number_of_meals / 2 >= 100:
            self.vitamin_d_score = 100
        else:
            self.vitamin_d_score = self.vitamin_d / number_of_meals / 2
        if self.vitamin_k / number_of_meals / 2 >= 100:
            self.vitamin_k_score = 100
        else:
            self.vitamin_k_score = self.vitamin_k / number_of_meals / 2
        self.vitamin_score = (self.vitamin_a_score + self.vitamin_c_score + self.vitamin_d_score
                              + self.vitamin_k_score) / 4
        self.potassium_score = (1 - abs((100 * number_of_meals / 2) - self.potassium)/(100 * number_of_meals / 2)) * 100
        self.sodium_score = (1 - abs((100 * number_of_meals / 2) - self.potassium)/(100 * number_of_meals / 2)) * 100
        self.cholesterol_score = (1 - abs((100 * number_of_meals / 2) - self.potassium)/(100 * number_of_meals / 2)) * 100
        self.prep_time_score = (1 - (self.prep_time - prep_time_target) / prep_time_target) * 100
        self.taste_score = self.taste_preference * 10
        return round(self.fat_score * fat_score_weight + self.carbs_score * general_nutrition_score_weight +
                     self.fiber_score * general_nutrition_score_weight + self.protein_score * protein_score_weight +
                     self.vitamin_score * vitamin_score_weight + self.potassium_score * general_nutrition_score_weight +
                     self.cholesterol_score * cholesterol_score_weight + self.prep_time_score * prep_time_score_weight +
                     self.taste_score * taste_score_weight, 2)

    def print_score(self) -> None:
        print("Overall score: " + str(round(self.overall_score, 2)))
        print("Calories: " + str(round(self.calories_score, 2)) + "%")
        print("\n\tFat score \t\t\t\t" + str(round(self.fat_score, 2)))
        print("\tFiber score \t\t\t" + str(round(self.fiber_score, 2)))
        print("\tProtein score \t\t\t" + str(round(self.protein_score, 2)))
        print("\tVitamin A score \t\t" + str(round(self.vitamin_a_score, 2)))
        print("\tVitamin C score \t\t" + str(round(self.vitamin_c_score, 2)))
        print("\tVitamin D score \t\t" + str(round(self.vitamin_d_score, 2)))
        print("\tVitamin K score \t\t" + str(round(self.vitamin_k_score, 2)))
        print("\tPotassium score \t\t" + str(round(self.potassium_score, 2)))
        print("\tSodium score \t\t\t" + str(round(self.sodium_score, 2)))
        print("\tCholesterol score \t\t" + str(round(self.cholesterol_score, 2)))
        print("\tPrep time score \t\t" + str(round(self.prep_time_score, 2)))
        print("\tTaste score \t\t\t" + str(round(self.taste_score, 2)))

