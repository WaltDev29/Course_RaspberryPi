from flask import Flask, render_template_string, jsonify, request
import board
import adafruit_dht
import smbus2
import time

app = Flask(__name__)

# 1. DHT11 온도 센서 설정 (GPIO 27)
dht_device = adafruit_dht.DHT11(board.D27)

# 2. PCF8574 I2C 설정 (주소: 0x20, 버스 번호: 1)
I2C_BUS = 1
PCF8574_ADDRESS = 0x20
bus = smbus2.SMBus(I2C_BUS)

# LED 핀 마스크 설정 (P0, P1, P2)
# PCF8574는 출력을 LOW(0)로 만들 때 LED가 켜지는 씽크(Sink) 방식인 경우가 많으나,
# 여기서는 하이(1)일 때 켜지는 일반적인 소스(Source) 방식으로 가정하고 작성했습니다.
# 만약 LED가 반대로 작동하면 코멘트를 참고하여 0과 1을 뒤집어주세요.
LED_PINS = {
    "red": 0b00000001,    # P0
    "green": 0b00000010,  # P1
    "blue": 0b00000100   # P2
}

# 현재 LED 상태 저장 변수 (초기값: 모두 꺼짐 0x00)
current_led_state = 0x00

def update_pcf8574(state_byte):
    """PCF8574 칩에 I2C 데이터 쓰기"""
    global current_led_state
    try:
        bus.write_byte(PCF8574_ADDRESS, state_byte)
        current_led_state = state_byte
    except Exception as e:
        print(f"I2C 통신 오류: {e}")

# 시작할 때 모든 LED 끄기
update_pcf8574(0x00)


# 3. HTML 및 JavaScript 웹 페이지 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>라즈베리파이 IoT 모니터 및 제어</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; text-align: center; background-color: #f4f4f9; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .chart-container { width: 100%; height: 350px; margin-top: 20px; }
        .control-panel { margin-top: 30px; padding: 20px; border-top: 2px solid #eee; }
        .btn { padding: 12px 24px; font-size: 16px; margin: 10px; border: none; border-radius: 5px; cursor: pointer; color: white; font-weight: bold; }
        .btn-red { background-color: #dc3545; }
        .btn-green { background-color: #28a745; }
        .btn-blue { background-color: #007bff; }
        .btn-off { background-color: #6c757d; }
        .btn:hover { opacity: 0.9; }
        .status-text { font-size: 18px; margin: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Raspberry Pi 4 IoT 대시보드</h1>
        
        <div class="status-text" id="live-data">데이터를 불러오는 중...</div>
        
        <div class="chart-container">
            <canvas id="climateChart"></canvas>
        </div>

        <div class="control-panel">
            <h3>PCF8574 LED 제어 (I2C: 0x20)</h3>
            <button class="btn btn-red" onclick="controlLED('red')">RED 켜기</button>
            <button class="btn btn-green" onclick="controlLED('green')">GREEN 켜기</button>
            <button class="btn btn-blue" onclick="controlLED('blue')">BLUE 켜기</button>
            <button class="btn btn-off" onclick="controlLED('off')">모두 끄기</button>
        </div>
    </div>

    <script>
        // --- 1. 실시간 Chart.js 환경 설정 ---
        const ctx = document.getElementById('climateChart').getContext('2d');
        const climateChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [], // 시간 라벨이 들어갈 배열
                datasets: [
                    {
                        label: '온도 (°C)',
                        data: [],
                        borderColor: '#ff4d4d',
                        backgroundColor: 'rgba(255, 77, 77, 0.1)',
                        yAxisID: 'y-temp',
                        tension: 0.3
                    },
                    {
                        label: '습도 (%)',
                        data: [],
                        borderColor: '#3399ff',
                        backgroundColor: 'rgba(51, 153, 255, 0.1)',
                        yAxisID: 'y-hum',
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    'y-temp': { type: 'linear', position: 'left', title: { display: true, text: '온도 (°C)' } },
                    'y-hum': { type: 'linear', position: 'right', title: { display: true, text: '습도 (%)' }, grid: { drawOnChartArea: false } }
                }
            }
        });

        // --- 2. 3초마다 웹서버에서 센서 데이터 가져오기 (AJAX) ---
        function updateDashboard() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    const statusTextEl = document.getElementById('live-data');
                    
                    if (data.error) {
                        statusTextEl.innerText = "센서 읽기 일시적 통신 오류 (재시도 중...)";
                        return; // 에러 발생 시 차트 업데이트는 건너뜀
                    }

                    // 텍스트 업데이트
                    statusTextEl.innerText = `현재 상태 - 온도: ${data.temperature}°C | 습도: ${data.humidity}%`;

                    // 차트에 데이터 추가 (최대 20개까지만 유지하고 오래된 데이터는 삭제)
                    const now = new Date().toLocaleTimeString();
                    
                    climateChart.data.labels.push(now);
                    climateChart.data.datasets[0].data.push(data.temperature);
                    climateChart.data.datasets[1].data.push(data.humidity);

                    if (climateChart.data.labels.length > 20) {
                        climateChart.data.labels.shift();
                        climateChart.data.datasets[0].data.shift();
                        climateChart.data.datasets[1].data.shift();
                    }
                    climateChart.update();
                });
        }

        // 3초 간격으로 주기적 실행
        setInterval(updateDashboard, 3000);
        updateDashboard(); // 페이지 로드 시 즉시 1회 실행

        // --- 3. LED 제어 신호 전송 함수 ---
        function controlLED(color) {
            fetch('/api/led', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ color: color })
            })
            .then(response => response.json())
            .then(data => {
                console.log("LED 변경 결과:", data);
            });
        }
    </script>
</body>
</html>
"""

# 4. 웹 에러 대비 DHT11 안전 리딩 함수
def get_sensor_data():
    try:
        temp = dht_device.temperature
        hum = dht_device.humidity
        if temp is not None and hum is not None:
            return {"temperature": temp, "humidity": hum, "error": None}
    except RuntimeError as e:
        return {"temperature": None, "humidity": None, "error": str(e)}
    except Exception as e:
        return {"temperature": None, "humidity": None, "error": str(e)}
    return {"temperature": None, "humidity": None, "error": "데이터 없음"}


# 5. Flask 라우팅 엔드포인트 정의
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def api_data():
    """자바스크립트가 주기적으로 요청하는 온습도 데이터 API"""
    return jsonify(get_sensor_data())

@app.route('/api/led', methods=['POST'])
def api_led():
    """웹 버튼을 클릭했을 때 LED를 제어하는 API"""
    global current_led_state
    req_data = request.get_json()
    color = req_data.get('color')
    
    if color == 'off':
        new_state = 0x00  # 모든 비트 클리어 (모두 끄기)
    elif color in LED_PINS:
        # 다른 LED는 유지하고 클릭한 색상만 토글하고 싶다면: new_state = current_led_state ^ LED_PINS[color]
        # 여기서는 단일 색상 한 개만 켜지도록 비트마스크를 지정합니다.
        new_state = LED_PINS[color]
    else:
        return jsonify({"status": "error", "message": "잘못된 색상"}), 400
        
    # PCF8574 I2C 전송
    # 만약 LED 하드웨어 결선이 'Active Low'(0일때 켜짐) 방식이라면 아래 주석을 풀고 변전해 주세요.
    # new_state = ~new_state & 0xFF 
    
    update_pcf8574(new_state)
    return jsonify({"status": "success", "current_state": bin(current_led_state)})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        # 종료 시 센서 해제 및 LED 소등
        dht_device.exit()
        update_pcf8574(0x00)
        bus.close()