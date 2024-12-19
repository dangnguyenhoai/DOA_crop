import random
from Generate import generate_individual
from Fitness import fitness_individual, find_best_individual
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Hàm lựa chọn (Selection)
def select_individuals(individual_list, crop_list, total_month):
    fitness_scores = [fitness_individual(ind, crop_list, total_month) for ind in individual_list]
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]
    selected = random.choices(individual_list, weights=probabilities, k=2)
    return selected

# Hàm lai ghép (Crossover)
def crossover(parent1, parent2):
    child = []
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# Hàm đột biến (Mutation)
def mutate(individual, crop_list, total_month, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            valid_crops = [crop for crop in crop_list if crop["crop_month"] <= total_month]
            new_crop = random.choice(valid_crops)
            individual[i] = [new_crop["crop_id"]]
    return individual

# Hàm chính của GA
def GA_main(crop_list, total_month, population_size=50, generations=10, mutation_rate=0.1):
    # Khởi tạo quần thể
    population = generate_individual(crop_list, total_month)
    best_individual = find_best_individual(population, crop_list, total_month)
    best_fitness_values = [fitness_individual(best_individual, crop_list, total_month)]

    for generation in range(generations):
        print(f"\033[34mGeneration {generation + 1}:\033[0m")
        new_population = []

        # Tạo thế hệ mới
        for _ in range(population_size // 2):
            parent1, parent2 = select_individuals(population, crop_list, total_month)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            child1 = mutate(child1, crop_list, total_month, mutation_rate)
            child2 = mutate(child2, crop_list, total_month, mutation_rate)
            new_population.extend([child1, child2])

        # Cập nhật quần thể
        population = new_population

        # Tìm cá thể tốt nhất
        best_individual_now = find_best_individual(population, crop_list, total_month)
        if fitness_individual(best_individual_now, crop_list, total_month) > fitness_individual(best_individual, crop_list, total_month):
            best_individual = best_individual_now

        # Ghi lại giá trị fitness tốt nhất
        best_fitness_values.append(fitness_individual(best_individual, crop_list, total_month))

    return best_individual, best_fitness_values

# Hàm vẽ biểu đồ so sánh
def plot_comparison_chart(doa_fitness, ga_fitness):
    """
    Vẽ biểu đồ so sánh giữa DOA và GA.

    Args:
        doa_fitness (list): Giá trị fitness của DOA qua các vòng lặp.
        ga_fitness (list): Giá trị fitness của GA qua các thế hệ.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(doa_fitness, label="DOA", color='blue', linewidth=2)
    plt.plot(ga_fitness, label="GA", color='green', linewidth=2)
    
    # Đặt tiêu đề dưới biểu đồ
    plt.title("", pad=20)
    #plt.figtext(0.5, -0.05, "So sánh hiệu quả thuật toán DOA và GA", ha="center", fontsize=12, fontweight="bold")

    # Định dạng trục Y chia cho 1000
    def format_y(value, _):
        return f'{value / 1000:.0f}'

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(format_y))
    plt.text(-0.1, 1.02, "Nghìn đồng", transform=ax.transAxes, fontsize=10, va='bottom', ha='left')

    # Đặt legend trực tiếp trên đường biểu đồ với phông chữ đẹp hơn
    plt.text(len(doa_fitness) - 1, doa_fitness[-1], ' DOA', color='blue', fontsize=14, fontweight='bold', va='center', ha='left')
    plt.text(len(ga_fitness) - 1, ga_fitness[-1], ' GA', color='green', fontsize=14, fontweight='bold', va='center', ha='left')

    plt.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

# Ví dụ sử dụng
if __name__ == '__main__':
    from Data import crop_list
    from DOA_Chart import DOA_main

    # Chạy thuật toán DOA
    best_individual_doa, best_fitness_values_doa = DOA_main(crop_list, total_month=12)

    # Chạy thuật toán GA
    best_individual_ga, best_fitness_values_ga = GA_main(crop_list, total_month=12, generations=1000)

    # Vẽ biểu đồ so sánh
    plot_comparison_chart(best_fitness_values_doa, best_fitness_values_ga)
