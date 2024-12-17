from Fitness import find_crop_id
from Data import crop_list
from Fitness import fitness_individual
total_month = 15
import random
import numpy as np
def valid_condition(individual):
    numbers_of_land = len(individual)
    individual_t = [a.copy() for a in individual]
    # generate 1 variable for check id crop 
    individual_id = [] * numbers_of_land
    # generate 1 variable for check remaining month crop 
    individual_rm = [] * numbers_of_land
    land_info = [{"land_id": 0, "remaining_month": 0} for _ in range(numbers_of_land)]
    # Process
    for i in individual_t:
        land_info[i]
    
    
    return True
def remaining_month(individual):
    month_temp = 0
    for land_clist in individual:
        for crop_id in land_clist:
            crop = find_crop_id(crop_id)
            month_temp += crop["crop_month"]
    return total_month - month_temp
def make_new_crop(crop_id, leftover_month):
    temp = find_crop_id(crop_id)
    random.shuffle(crop_list)
    for newc in crop_list:
        # find new valid crop about month
        if newc["crop_month"] <= temp["crop_month"] + leftover_month:
            return newc["crop_id"]
    else:
        return -1

def update_individual(best_individual, individual_change):
    for _ in range(200):
        individual = [a.copy() for a in best_individual]
        # make random number of crops must change
        num_change_crop = random.randint(2,4)
        for _ in range(num_change_crop):
            # make random land to change
            land = random.randint(0,3)
            # random crop
            value = random.choice(individual[land])
            index = individual[land].index(value)
            new = make_new_crop(value, remaining_month(individual))
            if(new != -1):
                individual[land][index] = new
        if(valid_condition(individual) and fitness_individual(individual) > fitness_individual(best_individual)):
            return individual
    else:
        return individual_change
if __name__ == "__main__":
    print("Ok")