from flask import Flask, render_template_string, jsonify
import board
import adafruit_dht
import time

app = Flask(__name__)

# DHT11 센서 초기화 (GPIO 27번 핀 지정)
# adafruit_dht 라이브러리는 board.D27 형태로 GPIO 번호를 인식합니다.
dht_device = adafruit_dht.DHT11(board.D27)

# HTML 템플릿 (웹 브라우저에 보여질 화면)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>라즈베리파이 온습도 모니터링</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .data { font-size: 24px; font-weight: bold; margin: 20px 0; color: #007BFF; }
        .error { color: red; font-size: 16px; }
        .refresh-btn { padding: 10px 20px; font-size: 16px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .refresh-btn:hover { background-color: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Raspberry Pi 4 온습도 모니터</h1>
        {% if error %}
            <p class="error">센서 읽기 실패: {{ error }} <br>(잠시 후 다시 시도해 주세요)</p>
        {% else %}
            <div class="data">
                온도: {{ temperature }}°C <br>
                습도: {{ humidity }}%
            </div>
        {% endif %}
        <button class="refresh-btn" onclick="location.reload()">새로고침</button>
    </div>
</body>
</html>
"""

def get_environmental_data():
    """DHT11 센서로부터 값을 읽어오는 함수"""
    try:
        # DHT11 센서는 읽기 타이밍이 민감하여 간혹 실패하므로 예외처리가 필수입니다.
        temp = dht_device.temperature
        hum = dht_device.humidity
        
        if temp is not None and hum is not None:
            return {"temperature": temp, "humidity": hum, "error": None}
    except RuntimeError as error:
        # 센서 읽기 통신 에러 처리 (일시적 오류인 경우가 많음)
        return {"temperature": None, "humidity": None, "error": error.args[0]}
    except Exception as e:
        return {"temperature": None, "humidity": None, "error": str(e)}
    
    return {"temperature": None, "humidity": None, "error": "데이터를 읽을 수 없습니다."}

@app.route('/')
def index():
    # 웹 페이지 접속 시 센서 데이터를 읽어 HTML에 전달
    data = get_environmental_data()
    return render_template_string(HTML_TEMPLATE, **data)

@app.route('/api/data')
def api_data():
    # 추후 자바스크립트(Ajax)나 외부 연동을 위해 JSON 형태로 데이터를 주는 API 엔드포인트
    data = get_environmental_data()
    return jsonify(data)

if __name__ == '__main__':
    # 0.0.0.0으로 설정해야 같은 와이파이/네트워크에 있는 다른 컴퓨터나 스마트폰에서 접속 가능합니다.
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        # 프로그램 종료 시 센서 객체 해제
        dht_device.exit()