import pandas as pd
class Crop:
    def __init__(self, crop_id, crop_name, crop_month, crop_profit, crop_land_score, crop_viability_score):
        self.crop_id = crop_id
        self.crop_name = crop_name
        self.crop_month = crop_month
        self.crop_profit = crop_profit
        self.crop_land_score = crop_land_score
        self.crop_viability_score = crop_viability_score
    def to_dict(self):
        return {
            "crop_id": self.crop_id,
            "crop_name": self.crop_name,
            "crop_month": self.crop_month,
            "crop_profit": self.crop_profit,
            "crop_land_score": self.crop_land_score,
            "crop_viability_score": self.crop_viability_score,
        }

class Region:
    def __init__(self, region_id, crops_in_region):
        self.region_id = region_id
        self.crops_in_region = crops_in_region  # List of crop IDs


class CropScheduler:
    def __init__(self, crop_list, result, total_months=12):
        self.total_months = total_months
        self.crop_list = [
            {
                'crop_id': crop['crop_id'],
                'crop_name': crop['crop_name'],
                'crop_month': crop['crop_month']
            }
            for crop in crop_list
        ]
        self.result = result
        self.months = [f"Tháng {i + 1}" for i in range(self.total_months)]

    def generate_crop_schedule(self):
        # Tạo dict cho crop
        crop_dict = {crop['crop_id']: {'crop_name': crop['crop_name'], 'crop_month': crop['crop_month']} for crop in self.crop_list}
        # Khởi tạo lịch theo từng tháng
        schedule = {month: [] for month in self.months}

        # Xử lý từng vùng
        for region_index, crops_in_region in enumerate(self.result):
            sum_tl = 0
            region_schedule = [0] * self.total_months
            remaining_time = 0  # Thời gian dư thừa từ cây trước
            months_start = 0
            temp_name = ""

            for crop_id in crops_in_region:
                crop = crop_dict[crop_id]
                crop_name = crop['crop_name']
                crop_month = crop['crop_month']
                view_crop_month = crop_month

                # Xử lý nếu cây dưới 1 tháng
                if crop_month < 1:
                    if crop_month < remaining_time:
                        crop_name_temp = f"{temp_name}{crop_name} {crop_month:.1f}"
                        remaining_time -= crop_month
                        remaining_time = round(remaining_time, 1)
                        region_schedule[months_start - 1] = crop_name_temp
                        if remaining_time == 0:
                            temp_name = ""
                            months_start += 1
                        elif remaining_time > 0:
                            temp_name = f"{crop_name_temp}({remaining_time:.1f})"
                    else:
                        temp_name = f"{crop_name}({remaining_time:.1f})"
                        crop_month -= remaining_time
                        remaining_time = 1 - crop_month
                        temp_name += f"{crop_name}{remaining_time:.1f}"
                        region_schedule[months_start - 1] = temp_name
                        temp_name = ""
                else:
                    # Xử lý cho cây >= 1 tháng
                    crop_month -= remaining_time
                    full_months = int(crop_month)  # Số tháng đầy đủ
                    remainder = crop_month - full_months  # Phần dư
                    month_end = min(months_start + full_months, self.total_months)  # Kết thúc trong giới hạn tổng số tháng

                    for i in range(months_start - 1, month_end):
                        if temp_name and i == months_start - 1:
                            crop_name_temp = f"{temp_name}{crop_name}{remaining_time:.1f}"
                            region_schedule[i] = crop_name_temp
                            temp_name = ""
                        else:
                            region_schedule[i] = f"{crop_name}"

                    if remainder > 0:
                        temp_name = f"{crop_name}({remainder:.1f})"
                        remaining_time = 1 - remainder
                    months_start = min(months_start + full_months + 1, self.total_months)

            # Map region_schedule vào lịch tổng
            for month_index, month in enumerate(self.months):
                if region_schedule[month_index] != 0:
                    schedule[month].append(f"{region_schedule[month_index]}")

        return schedule
