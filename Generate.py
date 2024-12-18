import random
import numpy as np
from untils import valid_individual
def generate_individual(crop_list, total_month):
    result = []
    while len(result) < 50:
        individual = [[] for _ in range(4)]  # Khởi tạo danh sách chứa cây cho từng vùng
        valid_crop_list = [crop for crop in crop_list if crop["crop_month"] <= total_month]
        land_clist = [{"crop_id": c["crop_id"], "remaining_month_crop": c["crop_month"], "remaining_month_land": total_month - c["crop_month"]} for c in random.sample(valid_crop_list, 4)]
        
        # Ghi nhận cây ban đầu vào danh sách kết quả
        for i, v in enumerate(land_clist):
            individual[i].append(v["crop_id"])
        
        for t in np.arange(0.1, total_month + 0.1, 0.1):
            min_crop_month = min([v["remaining_month_crop"] for v in land_clist if v["crop_id"] != 0], default=0)
            round(min_crop_month, 1)
            t += min_crop_month
            round(t, 1)
            for i, v in enumerate(land_clist):
                    if v["crop_id"] == 0:
                        continue
                    
                    v["remaining_month_crop"] -= min_crop_month
                    round(v["remaining_month_crop"], 1)
                    if v["remaining_month_crop"] <= 0:
                        # Cập nhật danh sách cây trồng còn lại
                        valid_crop_list = [c for c in valid_crop_list if c["crop_month"] <= v["remaining_month_land"]]
                        random.shuffle(valid_crop_list)
                        
                        for new_crop in valid_crop_list:
                            if new_crop["crop_id"] not in [p["crop_id"] for p in land_clist]:
                                # Thay thế cây trồng mới
                                v["crop_id"] = new_crop["crop_id"]
                                v["remaining_month_crop"] = new_crop["crop_month"]
                                v["remaining_month_land"] -= new_crop["crop_month"]
                                round(v["remaining_month_crop"], 1)
                                round(v["remaining_month_land"], 1)
                                individual[i].append(new_crop["crop_id"])
                                break
                        else:
                            v["crop_id"] = 0
                            v["remaining_month_crop"] = 0
                            v["remaining_month_land"] = 0
            
        if valid_individual(crop_list, individual) == False:
            continue
        result.append(individual)
    return result
