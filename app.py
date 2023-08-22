# Example: setting up Python server using Flask
import os
from flask import Flask, jsonify, request, abort, render_template, Markup

import pygsheets

import pandas as pd


app = Flask(__name__)

gc = pygsheets.authorize(service_file= 'andrabi-analytics.json')
gsheet = gc.open("xG Stats").sheet1

# Access Google Spreadsheet
sh = gc.open('xG Stats')

#print(sh)
#--Declare and initialize variables for each individual worksheet within Google Spreadsheet--#

wks = sh[0] # First worksheet: raw_xG 

wks1 = sh[1] # Second worksheet: Season_team (Seasonal Performance Stats (Team))

wks2 = sh[2] # Third worksheet: Season-player (Seasonal Performance Stats (per Player))

wks3 = sh[3] # Fourth worksheet: Game_team (per Game Performance Stats (Team))

wks4 = sh[4] # Fifth worksheet: Game_player (per Game Performance Stats (per Player))

wks5 = sh[5] # Sixth worksheet: Season_GK (Goalkeeper Performance Stats)

wks6 = sh[6]

wks7 = sh[7]

wks10 = sh[9] # Ninth worksheet: Season_opponents (Opposition Performance Stats)

wks11 = sh[10]

seasonTeam = pd.DataFrame(wks1.get_all_records())      # Returns a list of dictionaries


chartTeam = pd.DataFrame(wks11.get_all_records())


seasonPlayer = pd.DataFrame(wks2.get_all_records())

gameTeam = pd.DataFrame(wks3.get_all_records())

metricIndex = pd.DataFrame(wks7.get_all_records())

gamePlayer = pd.DataFrame(wks4.get_all_records())

gkSeason = pd.DataFrame(wks5.get_all_records())

gameOpp = pd.DataFrame(wks10.get_all_records())      # Returns a list of dictionaries

# OppxG = gameOpp.iloc[0,2]
# print(gameTeam.iloc[0, 7])
# print(gameTeam.iloc[0,8])
# print("Hello")
# print(len(gameTeam.iloc[:,1]))
# print("Points Test")
# points = gameTeam.iloc[:,7]
# print(points[0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def index1():
    return render_template('index.html')


#---Analysis Page Route---#
@app.route('/analysis')
def games():
    return render_template('analysis.html')

#---About Page Route---#
@app.route('/about')
def analysis():
    return render_template('about.html')

#---Contact Page Route---#
@app.route('/contact')
def season():
    return render_template('contact.html')

#---Analysis Home Routes---#
@app.route('/analysis-home')
def analysisHome():
    return render_template('analysis-home.html')

@app.route('/externalReference')
def externalReference():
    return render_template('externalReference.html')

@app.route('/analysis-home/metric_index')
def metric_index():
    offense = metricIndex.loc[metricIndex['ID'] == 'O']
    defense = metricIndex.loc[metricIndex['ID'] == 'D']
    overall = metricIndex.loc[metricIndex['ID'] == 'Ov']
    return render_template('metricIndex.html',tables=[overall.to_html(classes='overall'), offense.to_html(classes = 'offense'), defense.to_html(classes = 'defense')],
    titles = ['na', 'Overall Metrics', 'Offensive Metrics', 'Defensive Metrics'])   

     

@app.route('/analysis-season')
def analysisSeason():
    numGames = len(gameTeam.iloc[:,1])
    aG = seasonTeam.iloc[0,0]
    xG = seasonTeam.iloc[0,1]
    aGp90 = seasonTeam.iloc[0,2]
    xGp90 = seasonTeam.iloc[0,3]
    aGconvR = (seasonTeam.iloc[0,6])*100
    xGconvR = (seasonTeam.iloc[0,7])*100
    shots = seasonTeam.iloc[0,8]
    sot = seasonTeam.iloc[0,9]
    shotsp90 = seasonTeam.iloc[0,10]
    sotp90 = seasonTeam.iloc[0,11]
    gD = aG - (sum(gameOpp.iloc[:,1]))
    cQ = round((xG/shots)*100, 2)
    aP = sum(gameTeam.iloc[:, 7])
    xP = sum(gameTeam.iloc[:, 8])
    return render_template('analysis-season.html', title = 'Radar Chart Tester', numGames = numGames, aG = aG, xG = xG, aGp90 = aGp90, xGp90 = xGp90, aGconvR = aGconvR, xGconvR = xGconvR, shots = shots, sot = sot, shotsp90 = shotsp90, sotp90 = sotp90, gD = gD, cQ = cQ, aP = aP, xP = xP)

    return render_template('analysis-season.html')

#---Player Breakdown ROUTES---#
@app.route('/analysis-season/playerBreakdown')
def playerBreakdown():
    goalKeepers = seasonPlayer.loc[seasonPlayer['position']=='GK']
    defenders = seasonPlayer.loc[seasonPlayer['position']=='D']
    midfielders = seasonPlayer.loc[seasonPlayer['position'] == 'M']
    forwards = seasonPlayer.loc[seasonPlayer['position'] == 'F']
    return render_template('analysis-season-playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

@app.route('/analysis-season/teamBreakdown')
def teamBreakdown():

    return render_template('analysis-season-teamBreakdown.html',tables=[gameTeam.to_html(classes='game')],
    titles = ['na'])

@app.route('/analysis-season/team-SeasonBreakdown')
def teamSeasonBreakdown():

    return render_template('analysis-season-teamSeasonBreakdown.html',tables=[seasonTeam.to_html(classes='game')],
    titles = ['na'])


@app.route('/analysis-season/teamVisuals')
def teamVisuals():
    return render_template('analysis-season-teamVisuals.html')


@app.route('/analysis-season/oppBreakdown')
def oppBreakdown():

    return render_template('analysis-season-oppBreakdown.html',tables=[gameOpp.to_html(classes='game')],
    titles = ['na'])


#---p90 Evaluation Routes---#
@app.route('/analysis-game')
def analysisGame():
    OxyaG = gameTeam.iloc[0, 1]
    OppaG = gameOpp.iloc[0, 1]
    OxyxG = gameTeam.iloc[0, 2]
    OppxG = gameOpp.iloc[0,2]

    OxyaP = gameTeam.iloc[0, 7]
    OxyxP = gameTeam.iloc[0,8]
    Oxyshots = gameTeam.iloc[0, 3]
    Oxysot = gameTeam.iloc[0,4]
    OxyconvR = gameTeam.iloc[0,5]
    OxycQ = gameTeam.iloc[0,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[0, 3]
    Oppsot = gameOpp.iloc[0, 4]
    OppconvR = gameOpp.iloc[0, 5]
    OppcQ = gameOpp.iloc[0, 6]

    return render_template('analysis-game1.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)


@app.route('/analysis-game/team/playerBreakdown')
def analysisGame_Breakdown():
    seasonPlayer.set_index(['Player'], inplace=True)
    seasonPlayer.index.name=None
    goalKeepers = seasonPlayer.loc[seasonPlayer['position']=='GK']
    defenders = seasonPlayer.loc[seasonPlayer['position']=='D']
    midfielders = seasonPlayer.loc[seasonPlayer['position'] == 'M']
    forwards = seasonPlayer.loc[seasonPlayer['position'] == 'F']
    return render_template('test.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 1 Analytics Routes--#
@app.route('/analysis-game/team-game1')
def analysisGame1():
    OxyaG = gameTeam.iloc[0, 1]
    OppaG = gameOpp.iloc[0, 1]
    OxyxG = gameTeam.iloc[0, 2]
    OppxG = gameOpp.iloc[0,2]

    OxyaP = gameTeam.iloc[0, 7]
    OxyxP = gameTeam.iloc[0,8]
    Oxyshots = gameTeam.iloc[0, 3]
    Oxysot = gameTeam.iloc[0,4]
    OxyconvR = gameTeam.iloc[0,5]
    OxycQ = gameTeam.iloc[0,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[0, 3]
    Oppsot = gameOpp.iloc[0, 4]
    OppconvR = gameOpp.iloc[0, 5]
    OppcQ = gameOpp.iloc[0, 6]

    return render_template('analysis-game1.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, ap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)


@app.route('/analysis-game/team-game1-playerBreakdown')
def game1_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 1])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game1_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 2 Analytics Routes--#
@app.route('/analysis-game/team-game2')
def analysisGame2():
    OxyaG = gameTeam.iloc[1, 1]
    OppaG = gameOpp.iloc[1, 1]
    OxyxG = gameTeam.iloc[1, 2]
    OppxG = gameOpp.iloc[1,2]

    OxyaP = gameTeam.iloc[1, 7]
    OxyxP = gameTeam.iloc[1,8]
    Oxyshots = gameTeam.iloc[1, 3]
    Oxysot = gameTeam.iloc[1,4]
    OxyconvR = gameTeam.iloc[1,5]
    OxycQ = gameTeam.iloc[1,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[1, 3]
    Oppsot = gameOpp.iloc[1, 4]
    OppconvR = gameOpp.iloc[1, 5]
    OppcQ = gameOpp.iloc[1, 6]

    return render_template('analysis-game2.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)


@app.route('/analysis-game/team-game2-playerBreakdown')
def game2_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 2])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game2_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])



#--Game 3 Analytics Routes--#
@app.route('/analysis-game/team-game3')
def analysisGame3():
    OxyaG = gameTeam.iloc[2, 1]
    OppaG = gameOpp.iloc[2, 1]
    OxyxG = gameTeam.iloc[2, 2]
    OppxG = gameOpp.iloc[2,2]

    OxyaP = gameTeam.iloc[2, 7]
    OxyxP = gameTeam.iloc[2,8]
    Oxyshots = gameTeam.iloc[2, 3]
    Oxysot = gameTeam.iloc[2,4]
    OxyconvR = gameTeam.iloc[2,5]
    OxycQ = gameTeam.iloc[2,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[2, 3]
    Oppsot = gameOpp.iloc[2, 4]
    OppconvR = gameOpp.iloc[2, 5]
    OppcQ = gameOpp.iloc[2, 6]

    return render_template('analysis-game3.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game3-playerBreakdown')
def game3_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 3])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game3_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])




#--Game 4 Analytics Routes--#
@app.route('/analysis-game/team-game4')
def analysisGame4():
    OxyaG = gameTeam.iloc[3, 1]
    OppaG = gameOpp.iloc[3, 1]
    OxyxG = gameTeam.iloc[3, 2]
    OppxG = gameOpp.iloc[3,2]

    OxyaP = gameTeam.iloc[3, 7]
    OxyxP = gameTeam.iloc[3,8]
    Oxyshots = gameTeam.iloc[3, 3]
    Oxysot = gameTeam.iloc[3,4]
    OxyconvR = gameTeam.iloc[3,5]
    OxycQ = gameTeam.iloc[3,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[3, 3]
    Oppsot = gameOpp.iloc[3, 4]
    OppconvR = gameOpp.iloc[3, 5]
    OppcQ = gameOpp.iloc[3, 6]

    return render_template('analysis-game4.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game4-playerBreakdown')
def game4_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 4])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game4_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 5 Analytics Routes--#
@app.route('/analysis-game/team-game5')
def analysisGame5():
    OxyaG = gameTeam.iloc[4, 1]
    OppaG = gameOpp.iloc[4, 1]
    OxyxG = gameTeam.iloc[4, 2]
    OppxG = gameOpp.iloc[4,2]

    OxyaP = gameTeam.iloc[4, 7]
    OxyxP = gameTeam.iloc[4,8]
    Oxyshots = gameTeam.iloc[4, 3]
    Oxysot = gameTeam.iloc[4,4]
    OxyconvR = gameTeam.iloc[4,5]
    OxycQ = gameTeam.iloc[4,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[4, 3]
    Oppsot = gameOpp.iloc[4, 4]
    OppconvR = gameOpp.iloc[4, 5]
    OppcQ = gameOpp.iloc[4, 6]

    return render_template('analysis-game5.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)


@app.route('/analysis-game/team-game5-playerBreakdown')
def game5_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 5])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game5_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 6 Analytics Routes--#
@app.route('/analysis-game/team-game6')
def analysisGame6():
    OxyaG = gameTeam.iloc[5, 1]
    OppaG = gameOpp.iloc[5, 1]
    OxyxG = gameTeam.iloc[5, 2]
    OppxG = gameOpp.iloc[5,2]

    OxyaP = gameTeam.iloc[5, 7]
    OxyxP = gameTeam.iloc[5,8]
    Oxyshots = gameTeam.iloc[5, 3]
    Oxysot = gameTeam.iloc[5,4]
    OxyconvR = gameTeam.iloc[5,5]
    OxycQ = gameTeam.iloc[5,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[5, 3]
    Oppsot = gameOpp.iloc[5, 4]
    OppconvR = gameOpp.iloc[5, 5]
    OppcQ = gameOpp.iloc[5, 6]

    return render_template('analysis-game6.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)


@app.route('/analysis-game/team-game6-playerBreakdown')
def game6_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 6])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game6_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 7 Analytics Routes--#
@app.route('/analysis-game/team-game7')
def analysisGame7():
    OxyaG = gameTeam.iloc[6, 1]
    OppaG = gameOpp.iloc[6, 1]
    OxyxG = gameTeam.iloc[6, 2]
    OppxG = gameOpp.iloc[6,2]

    OxyaP = gameTeam.iloc[6, 7]
    OxyxP = gameTeam.iloc[6,8]
    Oxyshots = gameTeam.iloc[6, 3]
    Oxysot = gameTeam.iloc[6,4]
    OxyconvR = gameTeam.iloc[6,5]
    OxycQ = gameTeam.iloc[6,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[6, 3]
    Oppsot = gameOpp.iloc[6, 4]
    OppconvR = gameOpp.iloc[6, 5]
    OppcQ = gameOpp.iloc[6, 6]

    return render_template('analysis-game7.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game7-playerBreakdown')
def game7_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 7])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game7_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 8 Analytics Routes--#
@app.route('/analysis-game/team-game8')
def analysisGame8():
    OxyaG = gameTeam.iloc[7, 1]
    OppaG = gameOpp.iloc[7, 1]
    OxyxG = gameTeam.iloc[7, 2]
    OppxG = gameOpp.iloc[7,2]

    OxyaP = gameTeam.iloc[7, 7]
    OxyxP = gameTeam.iloc[7,8]
    Oxyshots = gameTeam.iloc[7, 3]
    Oxysot = gameTeam.iloc[7,4]
    OxyconvR = gameTeam.iloc[7,5]
    OxycQ = gameTeam.iloc[7,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[7, 3]
    Oppsot = gameOpp.iloc[7, 4]
    OppconvR = gameOpp.iloc[7, 5]
    OppcQ = gameOpp.iloc[7, 6]

    return render_template('analysis-game8.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game8-playerBreakdown')
def game8_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 8])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game8_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 9 Analytics Routes--#
@app.route('/analysis-game/team-game9')
def analysisGame9():
    OxyaG = gameTeam.iloc[8, 1]
    OppaG = gameOpp.iloc[8, 1]
    OxyxG = gameTeam.iloc[8, 2]
    OppxG = gameOpp.iloc[8,2]

    OxyaP = gameTeam.iloc[8, 7]
    OxyxP = gameTeam.iloc[8,8]
    Oxyshots = gameTeam.iloc[8, 3]
    Oxysot = gameTeam.iloc[8,4]
    OxyconvR = gameTeam.iloc[8,5]
    OxycQ = gameTeam.iloc[8,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[8, 3]
    Oppsot = gameOpp.iloc[8, 4]
    OppconvR = gameOpp.iloc[8, 5]
    OppcQ = gameOpp.iloc[8, 6]

    return render_template('analysis-game9.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game9-playerBreakdown')
def game9_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 9])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game9_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 10 Analytics Routes--#
@app.route('/analysis-game/team-game10')
def analysisGame10():
    OxyaG = gameTeam.iloc[9, 1]
    OppaG = gameOpp.iloc[9, 1]
    OxyxG = gameTeam.iloc[9, 2]
    OppxG = gameOpp.iloc[9,2]

    OxyaP = gameTeam.iloc[9, 7]
    OxyxP = gameTeam.iloc[9,8]
    Oxyshots = gameTeam.iloc[9, 3]
    Oxysot = gameTeam.iloc[9,4]
    OxyconvR = gameTeam.iloc[9,5]
    OxycQ = gameTeam.iloc[9,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[9, 3]
    Oppsot = gameOpp.iloc[9, 4]
    OppconvR = gameOpp.iloc[9, 5]
    OppcQ = gameOpp.iloc[9, 6]

    return render_template('analysis-game10.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game10-playerBreakdown')
def game10_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 10])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game10_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 11 Analytics Routes--#
@app.route('/analysis-game/team-game11')
def analysisGame11():
    OxyaG = gameTeam.iloc[10, 1]
    OppaG = gameOpp.iloc[10, 1]
    OxyxG = gameTeam.iloc[10, 2]
    OppxG = gameOpp.iloc[10,2]

    OxyaP = gameTeam.iloc[10, 7]
    OxyxP = gameTeam.iloc[10,8]
    Oxyshots = gameTeam.iloc[10, 3]
    Oxysot = gameTeam.iloc[10,4]
    OxyconvR = gameTeam.iloc[10,5]
    OxycQ = gameTeam.iloc[10,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[10, 3]
    Oppsot = gameOpp.iloc[10, 4]
    OppconvR = gameOpp.iloc[10, 5]
    OppcQ = gameOpp.iloc[10, 6]

    return render_template('analysis-game11.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game11-playerBreakdown')
def game11_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 11])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game11_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 12 Analytics Routes--#
@app.route('/analysis-game/team-game12')
def analysisGame12():
    OxyaG = gameTeam.iloc[11, 1]
    OppaG = gameOpp.iloc[11, 1]
    OxyxG = gameTeam.iloc[11, 2]
    OppxG = gameOpp.iloc[11,2]

    OxyaP = gameTeam.iloc[11, 7]
    OxyxP = gameTeam.iloc[11,8]
    Oxyshots = gameTeam.iloc[11, 3]
    Oxysot = gameTeam.iloc[11,4]
    OxyconvR = gameTeam.iloc[11,5]
    OxycQ = gameTeam.iloc[11,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[11, 3]
    Oppsot = gameOpp.iloc[11, 4]
    OppconvR = gameOpp.iloc[11, 5]
    OppcQ = gameOpp.iloc[11, 6]

    return render_template('analysis-game12.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game12-playerBreakdown')
def game12_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 12])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game12_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])

#--Game 13 Analytics Routes--#
@app.route('/analysis-game/team-game13')
def analysisGame13():
    OxyaG = gameTeam.iloc[12, 1]
    OppaG = gameOpp.iloc[12, 1]
    OxyxG = gameTeam.iloc[12, 2]
    OppxG = gameOpp.iloc[12,2]

    OxyaP = gameTeam.iloc[12, 7]
    OxyxP = gameTeam.iloc[12,8]
    Oxyshots = gameTeam.iloc[12, 3]
    Oxysot = gameTeam.iloc[12,4]
    OxyconvR = gameTeam.iloc[12,5]
    OxycQ = gameTeam.iloc[12,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[12, 3]
    Oppsot = gameOpp.iloc[12, 4]
    OppconvR = gameOpp.iloc[12, 5]
    OppcQ = gameOpp.iloc[12, 6]

    return render_template('analysis-game13.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game13-playerBreakdown')
def game13_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 13])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game13_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 14 Analytics Routes--#
@app.route('/analysis-game/team-game14')
def analysisGame14():
    OxyaG = gameTeam.iloc[13, 1]
    OppaG = gameOpp.iloc[13, 1]
    OxyxG = gameTeam.iloc[13, 2]
    OppxG = gameOpp.iloc[13,2]

    OxyaP = gameTeam.iloc[13, 7]
    OxyxP = gameTeam.iloc[13,8]
    Oxyshots = gameTeam.iloc[13, 3]
    Oxysot = gameTeam.iloc[13,4]
    OxyconvR = gameTeam.iloc[13,5]
    OxycQ = gameTeam.iloc[13,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[13, 3]
    Oppsot = gameOpp.iloc[13, 4]
    OppconvR = gameOpp.iloc[13, 5]
    OppcQ = gameOpp.iloc[13, 6]

    return render_template('analysis-game14.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game14-playerBreakdown')
def game14_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 14])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game14_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 15 Analytics Routes--#
@app.route('/analysis-game/team-game15')
def analysisGame15():
    OxyaG = gameTeam.iloc[14, 1]
    OppaG = gameOpp.iloc[14, 1]
    OxyxG = gameTeam.iloc[14, 2]
    OppxG = gameOpp.iloc[14,2]

    OxyaP = gameTeam.iloc[14, 7]
    OxyxP = gameTeam.iloc[14,8]
    Oxyshots = gameTeam.iloc[14, 3]
    Oxysot = gameTeam.iloc[14,4]
    OxyconvR = gameTeam.iloc[14,5]
    OxycQ = gameTeam.iloc[14,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[14, 3]
    Oppsot = gameOpp.iloc[14, 4]
    OppconvR = gameOpp.iloc[14, 5]
    OppcQ = gameOpp.iloc[14, 6]

    return render_template('analysis-game15.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game15-playerBreakdown')
def game15_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 15])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game15_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Game 16 Analytics Routes--#
@app.route('/analysis-game/team-game16')
def analysisGame16():
    OxyaG = gameTeam.iloc[15, 1]
    OppaG = gameOpp.iloc[15, 1]
    OxyxG = gameTeam.iloc[15, 2]
    OppxG = gameOpp.iloc[15,2]

    OxyaP = gameTeam.iloc[15, 7]
    OxyxP = gameTeam.iloc[15,8]
    Oxyshots = gameTeam.iloc[15, 3]
    Oxysot = gameTeam.iloc[15,4]
    OxyconvR = gameTeam.iloc[15,5]
    OxycQ = gameTeam.iloc[15,6]

    #OppaP = gameOpp.iloc[0, 3]
    #OppxP = gameOpp.iloc[]
    Oppshots = gameOpp.iloc[15, 3]
    Oppsot = gameOpp.iloc[15, 4]
    OppconvR = gameOpp.iloc[15, 5]
    OppcQ = gameOpp.iloc[15, 6]

    return render_template('analysis-game16.html', OxyaG = OxyaG, OppaG = OppaG, OxyxG = OxyxG, OppxG = OppxG, Oxyap = OxyaP, OxyxP = OxyxP, Oxyshots = Oxyshots, Oxysot = Oxysot, OxyconvR = OxyconvR, OxycQ = OxycQ, Oppshots = Oppshots, Oppsot = Oppsot, OppconvR = OppconvR, OppcQ = OppcQ)

@app.route('/analysis-game/team-game16-playerBreakdown')
def game16_playerBreakdown():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['ID'] == 16])
    goalKeepers = playerStat.loc[playerStat['position']=='GK']
    defenders = playerStat.loc[playerStat['position']=='D']
    midfielders = playerStat.loc[playerStat['position'] == 'M']
    forwards = playerStat.loc[playerStat['position'] == 'F']
    return render_template('game16_playerBreakdown.html',tables=[goalKeepers.to_html(classes='goalKeepers'), defenders.to_html(classes='defenders'), midfielders.to_html(classes='midfielders'), forwards.to_html(classes='forwards')],
    titles = ['na', 'Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'])


#--Player Stats Routes--#
# Ben Harding - GK, 00
@app.route('/analysis-home/playerBreakdown-benHarding')
def playerBreakdown_benHarding():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Ben Harding'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Ben Harding']


    return render_template('gameBreakdown_bHarding.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')], 
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

@app.route('/analysis-season/bHarding_visual')
def bHarding_visuals():
    return render_template('dataViz-bHarding.html')

# Jacob Gitin - GK, 0
@app.route('/analysis-home/playerBreakdown-jacobGitin')
def playerBreakdown_jacobGitin():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Jacob Gitin'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Jacob Gitin']


    return render_template('gameBreakdown_jGitin.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Scott Drazan - GK, 01
@app.route('/analysis-home/playerBreakdown-scottDrazan')
def playerBreakdown_scottDrazan():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Scott Drazan'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]

    return render_template('gameBreakdown_sDrazan.html',tables=[gkSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Riley Mccabe - D, 02
@app.route('/analysis-home/playerBreakdown-rileyMccabe')
def playerBreakdown_rileyMccabe():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Riley Mccabe'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Riley Mccabe']


    return render_template('gameBreakdown_rMccabe.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Spencer Shearer - M, 03
@app.route('/analysis-home/playerBreakdown-spencerShearer')
def playerBreakdown_spencerShearer():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Spencer Shearer'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Spencer Shearer']


    return render_template('gameBreakdown_sShearer.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Ryan Wilson - M, 04
@app.route('/analysis-home/playerBreakdown-ryanWilson')
def playerBreakdown_ryanWilson():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Ryan Wilson'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Ryan Wilson']


    return render_template('gameBreakdown_rWilson.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# David Paine - D, 05
@app.route('/analysis-home/playerBreakdown-davidPaine')
def playerBreakdown_davidPaine():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Daivd Paine'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'David Paine']


    return render_template('gameBreakdown_dPaine.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na','Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Nicolas Eble - M, 06
@app.route('/analysis-home/playerBreakdown-nicEble')
def playerBreakdown_nicEble():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Nicolas Eble'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Nicolas Eble']


    return render_template('gameBreakdown_nEble.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Matthew Teplitz - F, 07
@app.route('/analysis-home/playerBreakdown-mattTeplitz')
def playerBreakdown_mattTeplitz():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Matthew Teplitz'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Matthew Teplitz']


    return render_template('gameBreakdown_mTeplitz.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Ben Simon - M, 08
@app.route('/analysis-home/playerBreakdown-benSimon')
def playerBreakdown_benSimon():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Ben Simon'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Ben Simon']


    return render_template('gameBreakdown_bSimon.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Marcus Blumenfeld - F, 09
@app.route('/analysis-home/playerBreakdown-marcBlumenfeld')
def playerBreakdown_marcBlumenfeld():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Marcus Blumenfeld'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Marcus Blumenfeld']


    return render_template('gameBreakdown_mBlumenfeld.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Jasper Brannon - M, 10
@app.route('/analysis-home/playerBreakdown-jasperBrannon')
def playerBreakdown_jasperBrannon():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Jasper Brannon'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Jasper Brannon']


    return render_template('gameBreakdown_jBrannon.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Matthew Anzalone - D, 11
@app.route('/analysis-home/playerBreakdown-mattAnzalone')
def playerBreakdown_mattAnzalone():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Matthew Anzalone'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Matthew Anzalone']


    return render_template('gameBreakdown_mAnzalone.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Sean Kim - F, 12
@app.route('/analysis-home/playerBreakdown-seanKim')
def playerBreakdown_seanKim():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Sean Kim'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Sean Kim']


    return render_template('gameBreakdown_sKim.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Jack Meeker - D, 13
@app.route('/analysis-home/playerBreakdown-jackMeeker')
def playerBreakdown_jackMeeker():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Jack Meeker'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Jack Meeker']


    return render_template('gameBreakdown_jMeeker.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Adrian Paredes - M, 14
@app.route('/analysis-home/playerBreakdown-adrianParedes')
def playerBreakdown_adrianParedes():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Adrian Paredes'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game1 = game1.loc[:, ['aG', 'xG', 'Total_Shots', 'Shots_on_Target']]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game2 = game2.loc[:, ['aG', 'xG', 'Total_Shots', 'Shots_on_Target']]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game3 = game3.loc[:, ['aG', 'xG', 'Total_Shots', 'Shots_on_Target']]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Adrian Paredes']


    return render_template('gameBreakdown_aParedes.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

@app.route('/analysis-season/aParedes_visual')
def aParedes_visual():
    return render_template('dataViz-aParedes.html')


# Logan Myers - M, 16
@app.route('/analysis-home/playerBreakdown-loganMyers')
def playerBreakdown_loganMyers():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Logan Myers'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Logan Myers']


    return render_template('gameBreakdown_lMyers.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Tyler Wray - F, 17
@app.route('/analysis-home/playerBreakdown-tylerWray')
def playerBreakdown_tylerWray():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Tyler Wray'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Tyler Wray']


    return render_template('gameBreakdown_tWray.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Jake Foster - M, 18
@app.route('/analysis-home/playerBreakdown-jakeFoster')
def playerBreakdown_jakeFoster():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Jake Foster'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Jake Foster']


    return render_template('gameBreakdown_jFoster.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Joey Schwartz - M, 19
@app.route('/analysis-home/playerBreakdown-joeySchwartz')
def playerBreakdown_joeySchwartz():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Joey Schwartz'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Joey Schwartz']


    return render_template('gameBreakdown_jSchwartz.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Jazz Henry - F, 20
@app.route('/analysis-home/playerBreakdown-jazzHenry')
def playerBreakdown_jazzHenry():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Jazz Henry'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Jazz Henry']


    return render_template('gameBreakdown_jHenry.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na','Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Teagan Jarvis - F, 21
@app.route('/analysis-home/playerBreakdown-teaganJarvis')
def playerBreakdown_teaganJarvis():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Teagan Jarvis'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Teagan Jarvis']


    return render_template('gameBreakdown_tJarvis.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Tye Hernandez - M, 22
@app.route('/analysis-home/playerBreakdown-tyeHernandez')
def playerBreakdown_tyeHernandez():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Tye Hernandez'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Tye Hernandez']


    return render_template('gameBreakdown_tHernandez.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Miles Robertson - D, 23
@app.route('/analysis-home/playerBreakdown-milesRobertson')
def playerBreakdown_milesRobertson():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Miles Robertson'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Miles Robertson']


    return render_template('gameBreakdown_mRobertson.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Caleb Jordening - F, 24
@app.route('/analysis-home/playerBreakdown-calebJorden')
def playerBreakdown_calebJorden():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Caleb Jordening'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Caleb Jordening']


    return render_template('gameBreakdown_cJordening.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Neython Streitz - D, 25
@app.route('/analysis-home/playerBreakdown-neythonStreitz')
def playerBreakdown_neythonStreitz():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Neython Streitz'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Neython Streitz']


    return render_template('gameBreakdown_nStreitz.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Ben Tucker - D, 27
@app.route('/analysis-home/playerBreakdown-benTucker')
def playerBreakdown_benTucker():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Ben Tucker'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Ben Tucker']


    return render_template('gameBreakdown_bTucker.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

# Luke Haas - GK, 30
@app.route('/analysis-home/playerBreakdown-lukeHaas')
def playerBreakdown_lukeHaas():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Luke Haas'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Luke Haas']


    return render_template('gameBreakdown_lHaas.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Eric DaCosta - D, 31
@app.route('/analysis-home/playerBreakdown-ericDacosta')
def playerBreakdown_ericDacosta():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Eric Dacosta'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Eric Dacosta']


    return render_template('gameBreakdown_eDacosta.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])


# Player Selection Page
@app.route('/analysis-home/playerSelection')
def playerSelection():
    return render_template('playerSelection.html')

@app.route('/tabletest')
def tabletest():
    statName = chartTeam.iloc[:,0]
    statValues = chartTeam.iloc[:,1]
    return render_template('tabletest.html', title = 'Radar Chart Tester', labels = statName, values = statValues, tables=[seasonTeam.to_html(classes='game')],
    titles = ['na'])


@app.route('/charttest')
def charttest():
    aG = seasonTeam.iloc[0,0]
    xG = seasonTeam.iloc[0,1]
    aGp90 = seasonTeam.iloc[0,2]
    xGp90 = seasonTeam.iloc[0,3]
    aGconvR = seasonTeam.iloc[0,6]
    xGconvR = seasonTeam.iloc[0,7]
    shots = seasonTeam.iloc[0,8]
    sot = seasonTeam.iloc[0,9]
    shotsp90 = seasonTeam.iloc[0,10]
    sotp90 = seasonTeam.iloc[0,11]
    return render_template('charttest.html', title = 'Radar Chart Tester', aG = aG, xG = xG, aGp90 = aGp90, xGp90 = xGp90, aGconvR = aGconvR, xGconvR = xGconvR, shots = shots, sot = sot, shotsp90 = shotsp90, sotp90 = sotp90)

@app.route('/playerDash')
def playerDash():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Adrian Paredes'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Adrian Paredes']


    return render_template('playerDash.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])

@app.route('/')
def dashboardMain():
    return render_template('dashboardMain.html')

@app.route('/dashboard-season')
def dashboardSeason():
    numGames = len(gameTeam.iloc[:,1])

    aG = seasonTeam.iloc[0,0]
    xG = seasonTeam.iloc[0,1]
    aGp90 = seasonTeam.iloc[0,2]
    xGp90 = seasonTeam.iloc[0,3]
    aGconvR = (seasonTeam.iloc[0,6])*100
    xGconvR = (seasonTeam.iloc[0,7])*100
    shots = seasonTeam.iloc[0,8]
    sot = seasonTeam.iloc[0,9]
    shotsp90 = seasonTeam.iloc[0,10]
    sotp90 = seasonTeam.iloc[0,11]
    gD = aG - (sum(gameOpp.iloc[:,1]))
    cQ = round((xG/shots)*100, 2)
    aP = sum(gameTeam.iloc[:, 7])
    xP = sum(gameTeam.iloc[:, 8])
    OxyaG = seasonTeam.iloc[0, 1]
    #OppaG = seasonOpp.iloc[0, 1]
    OxyxG = seasonTeam.iloc[0, 2]
    #OppxG = seasonOpp.iloc[0,2]
    points = gameTeam.iloc[:, 7]
    draw = 0
    win = 0
    loss = 0

    for i in range(len(points)):
        if points[i] == 3:
            win += 1
        elif points[i] == 1:
            draw += 1
        elif points[i] ==0:
            loss += 1
    
    return render_template('dashboardSeason.html', title = 'Radar Chart Tester', numGames = numGames, aG = aG, xG = xG, aGp90 = aGp90, xGp90 = xGp90, aGconvR = aGconvR, xGconvR = xGconvR, shots = shots, sot = sot, shotsp90 = shotsp90, sotp90 = sotp90, gD = gD, cQ = cQ, aP = aP, xP = xP, win = win, draw = draw, loss = loss)

    return render_template('dashboardSeason.html')

@app.route('/dashboard-players')
def dashboardPlayers():
    return render_template('dashboardPlayers.html')

@app.route('/dashboard-gameData')
def dashboardGameData():
    return render_template('dashboardGameData.html')

@app.route('/passHome')
def passHomePage():
    return render_template('passHome.html')

# Adrian Paredes - M, 14
@app.route('/playerProfileTest')
def playerProfileTest():
    playerStat = pd.DataFrame(gamePlayer.loc[gamePlayer['Player'] == 'Adrian Paredes'])
    game1 = playerStat.loc[playerStat['ID']== 1]
    game2 = playerStat.loc[playerStat['ID']== 2]
    game3 = playerStat.loc[playerStat['ID'] == 3]
    game4 = playerStat.loc[playerStat['ID'] == 4]
    game5 = playerStat.loc[playerStat['ID'] == 5]
    game6 = playerStat.loc[playerStat['ID'] == 6]
    game7 = playerStat.loc[playerStat['ID'] == 7]
    game8 = playerStat.loc[playerStat['ID'] == 8]
    game9 = playerStat.loc[playerStat['ID'] == 9]
    game10 = playerStat.loc[playerStat['ID'] == 10]
    game11 = playerStat.loc[playerStat['ID'] == 11]
    game12 = playerStat.loc[playerStat['ID'] == 12]
    game13 = playerStat.loc[playerStat['ID'] == 13]
    game14 = playerStat.loc[playerStat['ID'] == 14]
    game15 = playerStat.loc[playerStat['ID'] == 15]
    game16 = playerStat.loc[playerStat['ID'] == 16]
    playerSeason = seasonPlayer.loc[seasonPlayer['Player'] == 'Adrian Paredes']


    return render_template('gameBreakdown_aParedes.html',tables=[playerSeason.to_html(classes = 'playerStat'), game1.to_html(classes='game1'), game2.to_html(classes='game2'), game3.to_html(classes='game3'), game4.to_html(classes='game4'), 
    game5.to_html(classes='game5'), game6.to_html(classes='game6'), game7.to_html(classes='game7'), game8.to_html(classes='game8'), game9.to_html(classes='game9'), game10.to_html(classes='game10'), 
    game11.to_html(classes='game11'), game12.to_html(classes='game12'), game13.to_html(classes='game13'), game14.to_html(classes='game14'), game15.to_html(classes='game15'), game16.to_html(classes='game16')],
    titles = ['na', 'Seasonal', 'Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7', 'Game 8', 'Game 9', 'Game 10', 'Game 11', 'Game 12', 'Game 13', 'Game 14', 'Game 15', 'Game 16'])
    
if __name__ == '__main__':
 app.run(debug=True, use_reloader=True)