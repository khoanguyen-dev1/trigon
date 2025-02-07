from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import re
import time  

app = Flask(__name__)
CORS(app)

@app.route('/trigon', methods=['GET'])
def trigon():
    url = request.args.get('link')  

    if not url:
        return jsonify({'error': 'Missing parameter: link'}), 400

    start_time = time.time()  

    try:
        response = requests.get(url, timeout=30)  
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        button = soup.find('div', class_='glass-light')
        
        if not button:
            return jsonify({"error": "no class 'glass-light'."}), 400

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
                    if result.startswith("http"):  
                        result_response = requests.get(result)
                        result_response.raise_for_status()
                        result = result_response.text
                    end_time = time.time() 
                    elapsed_time = round(end_time - start_time, 2)

                    return jsonify({"result": "Whitelist - trigon", "time": elapsed_time}), 200
                else:
                    return jsonify({"error": "sikibidi toilet"}), 400
            else:
                return jsonify({"error": "Api down"}), 400

        else:
            return jsonify({"result": "Whitelist - trigon"}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Đã xảy ra lỗi khi tải trang: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=False)
