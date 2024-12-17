from flask import Flask, render_template
from controllers.crop_controller import CropController

app = Flask(__name__)

# Khởi tạo controller
crop_controller = CropController()

@app.route("/")
def home():
    crops = crop_controller.get_all_crops()
    return render_template("crops.html", crops=crops)

output = [
    [4, 14, 15, 18, 2, 14, 18],
    [10, 7, 18, 13, 15, 13],
    [14, 18, 13, 18, 17, 19],
    [8, 2, 12, 16, 12, 13]
]

@app.route("/crop_table")
def crop_table():
    crops_data = crop_controller.get_crops_by_output(output)
    return render_template("crop_table.html", crops_data=crops_data)

if __name__ == "__main__":
    app.run(debug=True)
