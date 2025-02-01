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
        # Setting a timeout of 60 seconds for the initial request
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        button = soup.find('div', class_='glass-light')
        
        if not button:
            return jsonify({"error": "Không tìm thấy phần tử với class 'glass-light'."}), 400
        
        onclick_attr = button.get('onclick', '')
        
        match = re.search(r"window\.location\.href=['\"](https?://[^\s'\";]+)['\"]", onclick_attr)
        
        if match:
            redirect_url = match.group(1)
            
            # Setting a timeout of 60 seconds for the API request
            api_url = f"https://iwoozie.baby/api/free/bypass?url={redirect_url}"
            api_response = requests.get(api_url, timeout=60)

            if api_response.status_code == 200:
                api_data = api_response.json()  
                result = api_data.get('result') 

                if result:
                    return jsonify({"result": result , "owner" : "UwU"}), 200
                else:
                    return jsonify({"error": "result error"}), 400
            else:
                return jsonify({"error": "Api down"}), 400

        else:
            return jsonify({"error": "url not found"}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"{str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

