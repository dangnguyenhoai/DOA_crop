from Data import crop_list
total_month = 15
from Generate import generate_individual
from untils import valid_individual
from untils import find_crop_id
#convert score to percentage
def convert_stp(score):
    if score == 1:
        return 0
    if score == 2:
        return 10
    if score == 3:
        return 20
    if score == 4:
        return 40
    return 60
def profit_crop(crop_id, crop_list):
    crop = find_crop_id(crop_id, crop_list)
    # profit_final = crop_profit - crop_profit * percentage of (crop_land_score + crop_viabilit_score) / 100
    profit = crop["crop_profit"] - crop["crop_profit"] * (convert_stp(crop["crop_land_score"]) + convert_stp(crop["crop_viability_score"]))/100
    return profit

def profit_land(land_clist, crop_list, total_month):
    profit = 0
    month_temp = 0
    # caculate land profit
    for crop_id in land_clist:
        profit += profit_crop(crop_id, crop_list)
    # sum month of land
    for crop_id in land_clist:
        crop = find_crop_id(crop_id, crop_list)
        month_temp += crop["crop_month"]
    # Subtract the percentage of the surplus months from the profit
    profit -= (1 - month_temp/total_month) * profit
    return profit
def fitness_individual(individual, crop_list, total_month):
    profit = 0
    for land_clist in individual:
        profit += profit_land(land_clist, crop_list, total_month)
    return profit
class Result_individual:
    def __init__(self, individual=None, fitness=0):
        self.individual = individual
        self.fitness = fitness
def best_fitness(individual_list, crop_list, total_month):
    rs_list = [
        Result_individual(individual, fitness_individual(individual, crop_list, total_month))
        for individual in individual_list
    ]
    max_fitness = max(rs_list, key = lambda obj: obj.fitness)
    return max_fitness.individual

if __name__ == '__main__':
    cnt = 0
    individual_list = generate_individual(crop_list, total_month)
    for individual in individual_list:
        if valid_individual(individual) == False:
            print("\033[31m")
        print(individual)
        print(fitness_individual(individual, crop_list, total_month))
        print("\033[0m")
        if valid_individual(individual) == False:
            cnt += 1
    best_individual = best_fitness(individual_list, crop_list, total_month)
    print("\n\t \033[33m Result: \n\t", best_individual, "\n\t Profit: ",fitness_individual(best_individual, crop_list, total_month),"\033[0m")
    print(valid_individual(best_individual))
    print("count: ",cnt)