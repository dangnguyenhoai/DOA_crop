from algorithm.untils import find_crop_id
from algorithm.untils import valid_individual
from algorithm.Data import crop_list
from algorithm.Fitness import fitness_individual
total_month = 15
import random
import numpy as np

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
        if(valid_individual(individual) and fitness_individual(individual) > fitness_individual(individual_change)):
            return individual
    else:
        return individual_change

# if __name__ == "__main__":
#     individual = [[17, 19, 5, 18], [16, 4, 3, 15], [13, 2, 12, 9, 4, 18, 14], [7, 8, 7, 13]]
#     print("Cá thể hợp lệ: ",valid_condition(individual))