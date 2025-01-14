from flask import Flask, request, jsonify
import joblib

# โหลดโมเดล
model = joblib.load("linear_regression_model.pkl")

# สร้าง Flask API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # รับข้อมูล JSON
    input_features = [data['feature']]  # ดึงค่า feature
    prediction = model.predict([input_features])  # ทำนาย
    return jsonify({'prediction': prediction[0]})  # ส่งผลลัพธ์กลับ

if __name__ == '__main__':
    app.run(debug=True)
