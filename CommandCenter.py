from flask import Flask, render_template, request, jsonify, redirect, session, flash, make_response
import os
import json
import requests

app = Flask(__name__)

AUTH_API_URL = 'http://lilbite.org:9000'

def validate_session(token):
    """
    Sends token to auth server to validate, should recieve
    associated team number if it is valid

    :param token: the session token to validate

    :return team_id: the id of the team the token is attached to
    """
    post_data = dict()
    post_data['token'] = token
    resp = requests.post("{}/validate-session".format(AUTH_API_URL, data=post_data))
    if resp.status_code != 200:
        raise Exception("Bad status code")

    if 'success' not in resp.json():
        raise Exception(resp.json()['error'])

    team_id = resp['success']
    return team_id

@app.route('/')
def home():
    if session.get('token'):
        token = session.get('token')
        try:
            validate_session(token)
        except:
            redirect('/login')

        # Ship Data
        ship_data = getShips(1).data
        ship_json = json.loads(ship_data.decode('utf8').replace("'", '"'))
        ship1_count = ship_json['ship1_count']
        ship2_count = ship_json['ship2_count']
        ship3_count = ship_json['ship3_count']

        # Credit Data
        credit_data = getCredits(1).data
        credit_json = json.loads(credit_data.decode('utf8').replace("'", '"'))
        credits = credit_json['credits']

        # Stats Data
        stats_data = getStats(1).data
        stats_json = json.loads(stats_data.decode('utf8').replace("'", '"'))
        damage = stats_json['damage']
        damage_color = 'white'
        if damage[0] == '+':
            damage_color = 'green'
        elif damage[0] == '-':
            damage_color = 'red'
        health = stats_json['health']
        health_color = 'white'
        if health[0] == '+':
            health_color = 'green'
        elif health[0] == '-':
            health_color = 'red'
        speed = stats_json['speed']
        speed_color = 'white'
        if speed[0] == '+':
            speed_color = 'green'
        elif speed[0] == '-':
            speed_color = 'red'

        return render_template('index.html', ship1_count=ship1_count, ship2_count=ship2_count, ship3_count=ship3_count,
                               credits=credits, damage=damage, health=health, speed=speed, damage_color=damage_color,
                               health_color=health_color, speed_color=speed_color)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    username = request.form['username']
    data = {'username': username, 'password': password}
    url = 'http://lilbite.org:9000/login'
    r = requests.post(url, data)
    if r.status_code != 200:
        # error
        pass
    elif 'error' in r.json():
        # error
        pass
    else:
        token = r.json()['token']
        team_id = r.json()['team_id']
        session['token'] = token
        session['team_id'] = team_id
        response = make_response(redirect('/'))
        response.set_cookie('token', token)
        return response
    #print(r.json())

    return home()


"""
        Ansible
"""
@app.route('/ansible_playbook1', methods=['POST'])
def ansible_playbook1():
    command = 'ping -n 3 google.com'
    os.system(command)
    return redirect('/')


@app.route('/ansible_playbook2', methods=['POST'])
def ansible_playbook2():
    command = ''
    os.system(command)
    return redirect('/')


@app.route('/ansible_playbook3', methods=['POST'])
def ansible_playbook3():
    command = ''
    os.system(command)
    return redirect('/')


@app.route('/ansible_playbook4', methods=['POST'])
def ansible_playbook4():
    command = ''
    os.system(command)
    return redirect('/')


"""
    Statuses
"""
@app.route("/status/alerts")
def alerts():
    return jsonify({'status': 200, 'alerts': ['Perk5 will be unavailable for 10 minutes', 'Alert 2']})


@app.route('/status/koth')
def koth():
    return jsonify({'status': 200, 'planets': {'planet1': 'team4', 'planet2': 'team1'}})


"""
        Team Functions
"""
@app.route('/credits/<teamID>')
def getCredits(teamID):
    if not validateteamID(teamID):
        return jsonify({'status': 404})
    return jsonify({'status': 200, 'credits': 50000})


@app.route('/stats/<teamID>')
def getStats(teamID):
    if not validateteamID(teamID):
        return jsonify({'status': 404})
    return jsonify({'status': 200, 'health': '-50%', 'damage': '100%', 'speed': '+100%'})


@app.route('/ships/<teamID>')
def getShips(teamID):
    if not validateteamID(teamID):
        return jsonify({'status': 404})
    return jsonify({'status': 200, 'ship1_count': 50, 'ship2_count': 0, 'ship3_count': 1000})


"""
        Helpers
"""
def validateteamID(team_id):
    if team_id is None:
        return False
    return True


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
