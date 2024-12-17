from Data import crop_list
total_month = 15
from Generate import generate_individual
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
def find_crop_id(crop_id):
    return next((cay for cay in crop_list if cay["crop_id"] == crop_id),None)
def profit_crop(crop_id):
    crop = find_crop_id(crop_id)
    # profit_final = crop_profit - crop_profit * percentage of (crop_land_score + crop_viabilit_score) / 100
    profit = crop["crop_profit"] - crop["crop_profit"] * (convert_stp(crop["crop_land_score"]) + convert_stp(crop["crop_viability_score"]))/100
    return profit
    
def profit_land(land_clist):
    profit = 0
    month_temp = 0
    # caculate land profit
    for crop_id in land_clist:
        profit += profit_crop(crop_id)
    # sum month of land
    for crop_id in land_clist:
        crop = find_crop_id(crop_id)
        month_temp += crop["crop_month"]
    # Subtract the percentage of the surplus months from the profit
    profit -= (1 - month_temp/total_month) * profit
    return profit
def fitness_individual(individual):
    profit = 0
    for land_clist in individual:
        profit += profit_land(land_clist)
    return profit
class Result_individual:
    def __init__(self, individual=None, fitness=0):
        self.individual = individual
        self.fitness = fitness
def best_fitness(individual_list):
    rs_list = [
        Result_individual(individual, fitness_individual(individual))
        for individual in individual_list
    ]
    max_fitness = max(rs_list, key = lambda obj: obj.fitness)
    return max_fitness


if __name__ == '__main__':
    individual_list = generate_individual(crop_list, total_month)
    for individual in individual_list:
        print(individual)
        print(fitness_individual(individual))
    best_individual = best_fitness(individual_list)
    print("\n\t \033[33m Result: \n\t", best_individual.individual, "\n\t Profit: ",best_individual.fitness,"\033[0m")