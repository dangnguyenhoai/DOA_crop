from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from models.crop import Crop, Region, CropScheduler
from algorithm.DOA_Main import DOA_main

app = Flask(__name__)

# Ensure the 'uploads' directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

crop_list = []

def generate_crop_schedule(result, crop_list, total_months):
    crop_dict = {
        crop['crop_id']: {
            'crop_name': crop['crop_name'],
            'crop_month': round(crop['crop_month'], 1)
        }
        for crop in crop_list
    }

    months = [f"Tháng {i + 1}" for i in range(total_months)]
    schedule = {month: [] for month in months}

    for region_index, crops_in_region in enumerate(result):
        remaining_time = 0
        temp_name = ""
        month_index = 0

        for crop_id in crops_in_region:
            if month_index >= total_months:
                break

            crop = crop_dict.get(crop_id, {})
            crop_name = crop.get('crop_name', 'Unknown')
            crop_month = round(crop.get('crop_month', 0), 1)

            while crop_month > 0 and month_index < total_months:
                remaining_time = round(remaining_time, 1)

                if remaining_time > 0:
                    if crop_month <= remaining_time:
                        temp_name += f" + {crop_name} ({crop_month})"
                        schedule[months[month_index]].append(temp_name.strip('+ '))
                        remaining_time = round(remaining_time - crop_month, 1)
                        crop_month = 0
                        temp_name = ""
                        month_index += 1
                    else:
                        temp_name += f" + {crop_name} ({remaining_time})"
                        schedule[months[month_index]].append(temp_name.strip('+ '))
                        crop_month = round(crop_month - remaining_time, 1)
                        remaining_time = 0
                        month_index += 1
                        temp_name = ""
                else:
                    if crop_month >= 1:
                        schedule[months[month_index]].append(f"{crop_name} (1.0)")
                        month_index += 1
                        crop_month = round(crop_month - 1, 1)
                    else:
                        temp_name = f"{crop_name} ({crop_month})"
                        remaining_time = round(1 - crop_month, 1)
                        crop_month = 0

        if remaining_time > 0 and month_index < total_months:
            schedule[months[month_index]].append(f"{temp_name.strip('+ ')}")

    for month in months:
        if not schedule[month]:
            del schedule[month]

    df = pd.DataFrame.from_dict(schedule, orient='index')
    df = df.transpose()
    return df

@app.route("/ke-hoach-trong-cay", methods=["POST"])
def show_schedule():
    global crop_list
    total_months = request.form.get("total_months", type=int)

    if not total_months:
        return "Vui lòng nhập số tháng hợp lệ.", 400

    try:
        result = DOA_main(crop_list, total_months)
        schedule_df = generate_crop_schedule(result, crop_list, total_months)

        # Thay đổi tiêu đề cột "Tháng" thành "Vùng" và điều chỉnh chỉ số bắt đầu từ 1
        schedule_df.index = schedule_df.index + 1  # Chỉ số bắt đầu từ 1
        schedule_df.index.name = "Vùng"  # Đổi tên cột thành "Vùng"

        # Đặt lại tên cột "index" thành "Vùng" khi xuất bảng
        schedule_df = schedule_df.rename_axis("Vùng").reset_index()

        table_html = schedule_df.to_html(
            classes="table table-bordered", border=0, escape=False, index=False, justify="center"
        )

        return render_template("schedule.html", table=table_html)

    except Exception as e:
        return f"Error generating schedule: {str(e)}", 500

@app.route("/", methods=["GET", "POST"])
def upload_file():
    global crop_list
    table_html = ""

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file and file.filename != "":
            filename = os.path.join("uploads", file.filename)
            file.save(filename)

            try:
                df = pd.read_csv(filename)
                os.remove(filename)

                required_columns = {"crop_id", "crop_name", "crop_month", "crop_profit", "crop_land_score", "crop_viability_score"}
                if not required_columns.issubset(df.columns):
                    return "CSV file is missing required columns", 400

                crop_list = df.to_dict(orient="records")

                df_rename = df.rename(columns={
                    "crop_id": "Mã cây",
                    "crop_name": "Tên cây",
                    "crop_month": "Số tháng trồng",
                    "crop_profit": "Lợi nhuận / m²",
                    "crop_land_score": "Độ thích hợp đất",
                    "crop_viability_score": "Điểm khả năng sống sót"
                })

                table_html = df_rename.to_html(classes="table table-bordered", border=0, justify="center", index=False)

            except Exception as e:
                return f"Error processing file: {str(e)}", 500

    return render_template("upload.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)
