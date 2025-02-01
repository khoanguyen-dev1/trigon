from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
@app.route('/trigon', methods=['GET'])
def trigon():
    url = request.args.get('link')  
    
    if not url:
        return jsonify({'error': 'Missing parameter: link'}), 400

    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        

        button = soup.find('div', class_='glass-light')
        
        if not button:
            return jsonify({"error": "Không tìm thấy phần tử với class 'glass-light'."}), 400
        

        onclick_attr = button.get('onclick', '')
        

        match = re.search(r"window\.location\.href=['\"](https?://[^\s'\";]+)['\"]", onclick_attr)
        
        if match:
            redirect_url = match.group(1)
            

            api_url = f"https://iwoozie.baby/api/free/bypass?url={redirect_url}"
            api_response = requests.get(api_url)

            if api_response.status_code == 200:
                api_data = api_response.json()  
                result = api_data.get('result') 

                if result:
                    return jsonify({"result": result}), 200
                else:
                    return jsonify({"error": "Không tìm thấy trường 'result' trong phản hồi API."}), 400
            else:
                return jsonify({"error": "Không thể truy cập API hoặc nhận phản hồi hợp lệ."}), 400

        else:
            return jsonify({"error": "Không tìm thấy URL trong onclick."}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Đã xảy ra lỗi khi tải trang: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port,debug=False) 
