from Data import crop_list
from Fitness import fitness_individual
from Fitness import find_best_individual
from Fitness import find_worst_individual
from Generate import generate_individual
from Update import update_individual
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import random

def DOA_process_eaten_moved_poisoned(crop_list, total_month, target_individual, process_individual):
    # Random eat percentage
    new_individual = None
    if random.random() >= 0.25:  # not eat
        # Random move percentage
        if random.random() < 0.5:  # move
            # Update new location by individual_process
            new_individual = update_individual(crop_list, total_month, process_individual, process_individual)
    # Update new individual by target_individual if eat or not move
    if new_individual is None:
        new_individual = update_individual(crop_list, total_month, target_individual, process_individual)

    # Random percentage poisoned
    if random.random() >= 0.1:  # not poisoned
        new_individual = update_individual(crop_list, total_month, new_individual, new_individual)
    else:  # poisoned
        if fitness_individual(new_individual, crop_list, total_month) > fitness_individual(target_individual, crop_list, total_month):
            new_individual = update_individual(crop_list, total_month, new_individual, new_individual)
        else:
            new_individual = update_individual(crop_list, total_month, target_individual, new_individual)
    return new_individual

def DOA_main(crop_list, total_month):
    # Init populations
    individual_list = generate_individual(crop_list, total_month)
    best_individual = find_best_individual(individual_list, crop_list, total_month)
    best_fitness_values = [fitness_individual(best_individual, crop_list, total_month)]  # Lưu giá trị fitness ban đầu

    for i in range(1000):
        print("\033[31mVòng lặp thứ: \033[0m", i + 1)
        # Process individual
        for individual in individual_list:  
            target_individual = find_best_individual(individual_list, crop_list, total_month)
            individual_temp = DOA_process_eaten_moved_poisoned(crop_list, total_month, target_individual, individual)
            # Find worst individual
            worst_individual = find_worst_individual(individual_list, crop_list, total_month)
            
            if fitness_individual(individual_temp, crop_list, total_month) > fitness_individual(worst_individual, crop_list, total_month):
                idx = individual_list.index(worst_individual)
                individual_list[idx] = individual_temp

        # Find best_individual after process individual list
        best_individual_now = find_best_individual(individual_list, crop_list, total_month)
        # Compare fitness
        if fitness_individual(best_individual_now, crop_list, total_month) > fitness_individual(best_individual, crop_list, total_month):
            best_individual = best_individual_now

        # Lưu fitness của best_individual
        best_fitness_values.append(fitness_individual(best_individual, crop_list, total_month))
    
    return best_individual, best_fitness_values

def plot_fitness_chart(fitness_values):
    """
    Vẽ biểu đồ biểu diễn giá trị fitness tốt nhất qua từng vòng lặp.

    Args:
        fitness_values (list): Danh sách giá trị fitness tốt nhất ở mỗi vòng lặp.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_values, color='blue', linewidth=2)
    
    # Title in đậm và đặt cao hơn
    #plt.title("Lợi nhuận / m$^2$ khi áp dụng thuật toán DOA vào phân hoạch", fontweight='bold', pad=20)

    # Định dạng số trên trục Y chia cho 1000
    def format_y(value, _):
        return f'{value / 1000:.0f}'  # Chia cho 1000 và hiển thị số nguyên

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(format_y))

    # Loại bỏ gridlines
    plt.grid(False)

    # Loại bỏ khung viền trên và bên phải
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Giữ lại khung viền dưới và bên trái
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Thêm đơn vị "Nghìn đồng" ở phía trên trục Y
    plt.text(-0.1, 1.02, "Nghìn đồng", transform=ax.transAxes, fontsize=10, va='bottom', ha='left')

    #plt.legend(["Fitness"])
    plt.show()

if __name__ == '__main__':
    best_individual, best_fitness_values = DOA_main(crop_list, 15)
    # Gọi hàm vẽ biểu đồ
    plot_fitness_chart(best_fitness_values)
