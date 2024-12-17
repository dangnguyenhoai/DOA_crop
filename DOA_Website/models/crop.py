class Crop:
    def __init__(self, crop_id, crop_name, crop_month, crop_profit, crop_land_score, crop_viability_score):
        if crop_month <= 0:
            raise ValueError("Số tháng trồng (crop_month) phải lớn hơn 0.")
        if crop_profit < 0:
            raise ValueError("Lợi nhuận (crop_profit) không thể âm.")

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
            "crop_viability_score": self.crop_viability_score
        }

    def __str__(self):
        return f"Crop({self.crop_id}: {self.crop_name}, Months: {self.crop_month}, Profit: {self.crop_profit}, " \
               f"Land Score: {self.crop_land_score}, Viability Score: {self.crop_viability_score})"

    def __repr__(self):
        return self.__str__()
    
    def get_full_months(self):
        # Trả về số tháng trồng, làm tròn xuống (số nguyên)
        return int(self.crop_month)

    def get_fractional_month(self):
        # Trả về phần thập phân của số tháng
        return self.crop_month - int(self.crop_month)
