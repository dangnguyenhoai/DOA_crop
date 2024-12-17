from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from models.crop import Crop, Region, CropScheduler
from algorithm.Fitness import DOA_Fuction

app = Flask(__name__)

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

crop_list = []

# Trang để hiển thị kế hoạch trồng cây
@app.route("/ke-hoach-trong-cay", methods=["POST"])
def show_schedule():
    global crop_list
    total_months = request.form.get("total_months", type=int)

    if not total_months:
        return "Vui lòng nhập số tháng hợp lệ.", 400

    # Tạo lịch trình dựa trên crop_list và kết quả
    try:
        result = DOA_Fuction(crop_list, total_months)
        crop_schedule = CropScheduler(crop_list, result, total_months=total_months)
        schedule = crop_schedule.generate_crop_schedule()

        # Chuyển dữ liệu thành DataFrame để hiển thị dưới dạng bảng
        df = pd.DataFrame.from_dict(schedule, orient="index").transpose()
        table_html = df.to_html(classes="table table-bordered", border=0, justify="center")

        return render_template("schedule.html", table=table_html)

    except Exception as e:
        return f"Error generating schedule: {str(e)}", 500

# Route để tải file CSV và nhập số tháng
@app.route("/", methods=["GET", "POST"])
def upload_file():
    global crop_list  # Để cập nhật biến toàn cục
    table_html = ""

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file and file.filename != "":
            filename = os.path.join("uploads", file.filename)
            file.save(filename)

            try:
                # Đọc file CSV và chuyển đổi dữ liệu thành danh sách dictionary
                df = pd.read_csv(filename)
                os.remove(filename)  # Xóa file tạm thời

                # Kiểm tra các cột cần thiết
                required_columns = {"crop_id", "crop_name", "crop_month", "crop_profit", "crop_land_score", "crop_viability_score"}
                if not required_columns.issubset(df.columns):
                    return "CSV file is missing required columns", 400

                # Cập nhật crop_list
                crop_list = df.to_dict(orient="records")

                # Hiển thị dữ liệu tải lên trong bảng HTML
                table_html = df.to_html(classes="table table-bordered", border=0, justify="center")

            except Exception as e:
                return f"Error processing file: {str(e)}", 500

    return render_template("upload.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)
