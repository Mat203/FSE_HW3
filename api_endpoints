from flask import Flask, request, jsonify
import data_procession
from datetime import datetime

app = Flask(__name__)

@app.route('/api/stats/user', methods=['GET'])
def get_user():
    date_str = request.args.get('date')
    userId = request.args.get('userId')
    date = data_procession.datetime.fromisoformat(date_str)
    user_data = data_procession.get_user_data(date, userId)
    
    if user_data is None:
        return jsonify({'error': 'Invalid userId'}), 404

    return jsonify(user_data)

@app.route('/api/predictions/users', methods=['GET'])
def get_prediction():
    date_str = request.args.get('date')
    date = data_procession.datetime.fromisoformat(date_str)
    prediction = data_procession.predict_users(date)
    
    return jsonify(prediction)

@app.route('/api/predictions/user', methods=['GET'])
def get_user_prediction():
    date_str = request.args.get('date')
    userId = request.args.get('userId')
    tolerance = float(request.args.get('tolerance'))
    date = data_procession.datetime.fromisoformat(date_str)
    
    prediction = data_procession.predict_user(date, userId)
    
    if prediction is None:
        return jsonify({'error': 'Invalid userId'}), 404

    prediction['willBeOnline'] = prediction['onlineChance'] >= tolerance

    return jsonify(prediction)

@app.route('/api/stats/users', methods=['GET'])
def get_users():
    date_str = request.args.get('date')
    date = datetime.fromisoformat(date_str)
    users_online = data_procession.get_users_online(date)
    
    return jsonify({'date': date_str, 'usersOnline': users_online})

if __name__ == '__main__':
    app.run(debug=True)
