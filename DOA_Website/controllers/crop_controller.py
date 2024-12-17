from models.crop import Crop

class CropController:
    def __init__(self):
        self.crop_list = [
            Crop(1, "Mè", 3.7, 15000, 2, 3),
            Crop(2, "Ngô", 3.7, 20000, 1, 1),
            Crop(3, "Khoai", 5.5, 35000, 2, 2),
            Crop(4, "Đậu", 2.4, 12000, 1, 1),
            Crop(14, "Rau muống", 1.3, 8000, 1, 1),
            Crop(15, "Cà chua", 3.9, 45000, 1, 1),
            Crop(18, "Xà lách", 0.9, 10000, 1, 1),
            Crop(10, "Cà rốt", 3.0, 25000, 2, 2),
            Crop(7, "Ớt", 5.6, 80000, 1, 1),
            Crop(13, "Hành lá", 0.8, 12000, 1, 1),
            Crop(17, "Măng tây", 6.6, 60000, 3, 3),
            Crop(19, "Dâu tây", 4.0, 90000, 3, 3),
            Crop(8, "Su hào", 2.2, 15000, 1, 1),
            Crop(12, "Cải bắp", 2.1, 18000, 1, 1),
            Crop(16, "Bắp cải", 2.9, 22000, 1, 1),
        ]
        # Tạo dictionary tra cứu nhanh bằng crop_id
        self.crop_dict = {crop.crop_id: crop for crop in self.crop_list}

    def get_crops_by_output(self, output):
        """
        Lấy dữ liệu cây trồng từ danh sách output (id).
        Trả về thông tin cây trồng theo từng vùng.
        
        :param output: Danh sách chứa các vùng, mỗi vùng là danh sách id cây trồng.
        :return: Danh sách thông tin cây trồng dạng bảng.
        """
        result = []
        for region_index, region in enumerate(output):
            region_data = []
            for crop_id in region:
                # Tra cứu thông tin cây trồng
                crop = self.crop_dict.get(crop_id)
                if crop:
                    region_data.append({
                        "crop_id": crop.crop_id,
                        "crop_name": crop.crop_name,
                        "crop_month": crop.crop_month,
                        "crop_profit": crop.crop_profit
                    })
                else:
                    region_data.append({
                        "crop_id": crop_id,
                        "crop_name": "N/A",
                        "crop_month": 0,
                        "crop_profit": 0
                    })
            result.append(region_data)
        return result

    def display_table(self, output):
        """
        Hiển thị thông tin dạng bảng với các vùng và cây trồng theo tháng.

        :param output: Danh sách chứa các vùng (list các crop_id).
        """
        from tabulate import tabulate

        # Lấy thông tin theo output
        table_data = []
        region_data = self.get_crops_by_output(output)

        # Xây dựng dữ liệu bảng
        for month in range(1, len(region_data[0]) + 1):  # Số tháng tương ứng với cột
            row = [f"Tháng {month}"]
            for region in region_data:
                if month <= len(region):
                    crop = region[month - 1]
                    row.append(f"{crop['crop_name']} ({crop['crop_month']})")
                else:
                    row.append("N/A")
            table_data.append(row)

        # Hiển thị bảng
        headers = ["Tháng"] + [f"Vùng {i+1}" for i in range(len(region_data))]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    def get_crops_by_output(self, output):
        """
        Lấy dữ liệu cây trồng từ output (id) và trả về thông tin theo vùng.
        """
        result = []
        for region in output:
            region_data = []
            for crop_id in region:
                crop = self.crop_dict.get(crop_id)
                if crop:
                    region_data.append(crop)  # Thêm đối tượng Crop vào vùng
            result.append(region_data)
        return result
    