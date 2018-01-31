from flask import Flask, render_template, request, jsonify, redirect
import os
import json
import requests

app = Flask(__name__)


@app.route('/')
def index():
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


@app.route('/login')
def login():
    return render_template('login.html')


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
    app.run(debug=True)