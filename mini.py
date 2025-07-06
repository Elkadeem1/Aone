from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    # استقبل البيانات JSON من الـ request
    data = request.json
    # رجع البيانات تاني مع رسالة
    return jsonify({
        "status": "success",
        "you_sent": data
    })

if __name__ == '__main__':
    app.run(debug=True)
