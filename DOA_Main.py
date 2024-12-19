from Data import crop_list
from Fitness import fitness_individual
from Fitness import find_best_individual
from Fitness import find_worst_individual
from Generate import generate_individual
from Update import update_individual
import random
def DOA_process_eaten_moved_poisoned(crop_list, total_month, target_individual, process_individual):
    # random eat percentage
    new_individual = None
    if random.random() >= 0.25:   # not eat
        # random move percentage
        if random.random() < 0.5: # move
            # update new location by individual_process
            new_individual = update_individual(crop_list, total_month, process_individual, process_individual)
    # update new individual by target_individual if eat or not move
    if new_individual is None:
        new_individual = update_individual(crop_list, total_month, target_individual, process_individual)

    # random percentage poisoned
    if random.random() >= 0.1: # not poisened
        new_individual = update_individual(crop_list, total_month, new_individual, new_individual)
    else:# poisened
        if fitness_individual(new_individual, crop_list, total_month) > fitness_individual(target_individual, crop_list, total_month):
            new_individual = update_individual(crop_list, total_month, new_individual, new_individual)
        else:
            new_individual = update_individual(crop_list, total_month, target_individual, new_individual)
    return new_individual

def DOA_main(crop_list, total_month):
    # Init populations
    individual_list = generate_individual(crop_list, total_month)
    best_individual = find_best_individual(individual_list, crop_list, total_month)
    for i in range(1000):
        print("\033[31mVong lap thu: \033[0m", i+1)
        # process individual
        for individual in individual_list:  
            target_individual = find_best_individual(individual_list, crop_list, total_month)
            individual_temp = DOA_process_eaten_moved_poisoned(crop_list, total_month, target_individual, individual)
            # find worst individual
            worst_individual = find_worst_individual(individual_list, crop_list, total_month)
            
            if fitness_individual(individual_temp,crop_list, total_month) > fitness_individual(worst_individual,crop_list, total_month):
                idx = individual_list.index(worst_individual)
                individual_list[idx] = individual_temp

        # find best_individual after process individual list
        best_individual_now = find_best_individual(individual_list, crop_list, total_month)
        # compare fitness
        if fitness_individual(best_individual_now, crop_list, total_month) > fitness_individual(best_individual, crop_list, total_month):
            best_individual = best_individual_now
        
    return best_individual
if __name__ == '__main__':
    DOA_main(crop_list,15)
