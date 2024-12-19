from untils import find_crop_id
from untils import valid_individual
from Fitness import fitness_individual
import random

def remaining_month(crop_list, land_clist, total_month):
    month_temp = 0
    for crop_id in land_clist:
        crop = find_crop_id(crop_list, crop_id)
        month_temp += crop["crop_month"]
    return total_month - month_temp

def make_new_crop(crop_list, crop_id, leftover_month):
    temp = find_crop_id(crop_list, crop_id)
    random.shuffle(crop_list)
    for newc in crop_list:
        # find new valid crop about month
        if newc["crop_month"] <= temp["crop_month"] + leftover_month:
            return newc["crop_id"]
    else:
        return -1

def update_individual(crop_list, total_month, best_individual, individual_change):
    for _ in range(1):
        individual = [a.copy() for a in best_individual]
        # make random number of crops must change
        num_change_crop = random.randint(2,4)
        for _ in range(num_change_crop):
            # make random land to change
            land = random.randint(0,3)
            # random crop
            value = random.choice(individual[land])
            index_value = individual[land].index(value)
            new = make_new_crop(crop_list, value, remaining_month(crop_list, individual[land],total_month))
            if(new != -1):
                individual[land][index_value] = new
        if(valid_individual(crop_list, individual) and fitness_individual(individual, crop_list, total_month) > fitness_individual(individual_change, crop_list, total_month)):
            return individual
    else:
        return individual_change