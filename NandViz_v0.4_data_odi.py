import pandas as pd

team_names = ['England','Australia','New Zealand','West Indies','India','Pakistan','South Africa','Sri Lanka','Bangladesh','Zimbabwe','Afghanistan']

filter = 'filter=advanced'
size = 'size=50'
start = 'spanmin1=01+Jan+2017'
end = 'spanval1=span'
template = 'template=results'
format = 'class=2' #ODI
opposition_dict = {'England': 'opposition=1', 'Australia': 'opposition=2', 'South Africa': 'opposition=3', 'West Indies': 'opposition=4', 'New Zealand': 'opposition=5', 'India': 'opposition=6', 'Pakistan': 'opposition=7', 'Sri Lanka': 'opposition=8', 'Zimbabwe': 'opposition=9', 'Bangladesh': 'opposition=25', 'Afghanistan': 'opposition=40'}
oppositions = ';'.join([opposition_dict.get(i) for i in team_names])

od_inningss = ['innings_number=1', 'innings_number=2']
innings_names = ['1st Innings', '2nd Innings']
team_dict = {'England': 'team=1', 'Australia': 'team=2', 'South Africa': 'team=3', 'West Indies': 'team=4', 'New Zealand': 'team=5', 'India': 'team=6', 'Pakistan': 'team=7', 'Sri Lanka': 'team=8', 'Zimbabwe': 'team=9', 'Bangladesh': 'team=25', 'Afghanistan': 'team=40'}
teams = [team_dict.get(i) for i in team_names]


batting_data = pd.DataFrame(columns=['Innings', 'Team', 'Player', 'Span', 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s', '6s'])
for tm in range(len(teams)):
    team = teams[tm]
    for inns in range(len(od_inningss)):
        batting_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?'+format+';'+filter+';'+oppositions+';'+od_inningss[inns]+';orderby=runs;'+size+';'+start+';'+end+';'+str(team)+';'+template+';type=batting'
        batting_table = pd.read_html(batting_url)[2]
        batting_table.insert(loc=0, column='Team', value=team_names[tm])
        batting_table.insert(loc=0, column='Innings', value=innings_names[inns])
        batting_data = batting_data.append(batting_table, ignore_index=True, sort=False)
batting_data = batting_data.drop(columns=['Unnamed: 15'])
batting_data = batting_data.fillna(0).replace('-',0)
batting_data = batting_data.astype({'BF': 'int32', 'Inns': 'int32', 'NO': 'int32', 'SR': 'float64'})
batting_data = batting_data[[(j-k) > 0 for j,k in zip(batting_data['Inns'],batting_data['NO'])]]
batting_data['BallAve'] = [i/(j-k) for i,j,k in zip(batting_data['BF'],batting_data['Inns'],batting_data['NO'])]
batting_data['BallSR'] = [i/100 for i in batting_data['SR']]
batting_data.insert(loc=0, column='Lookup', value=[i+'_'+j for i,j in zip(batting_data['Player'], batting_data['Innings'])])


bowling_data = pd.DataFrame(columns=['Innings', 'Team', 'Player', 'Span', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Ave', 'Econ', 'SR', '4', '5'])
for tm in range(len(teams)):
    team = teams[tm]
    for inns in range(len(od_inningss)):
        bowling_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?' + format + ';' + filter + ';' + od_inningss[inns] + ';orderby=wickets;' + size + ';' + start + ';' + end + ';' + team + ';' + template + ';type=bowling'
        bowling_table = pd.read_html(bowling_url)[2]
        bowling_table.insert(loc=0, column='Team', value=team_names[tm])
        bowling_table.insert(loc=0, column='Innings', value=innings_names[inns])
        bowling_data = bowling_data.append(bowling_table, ignore_index=True, sort=False)
bowling_data = bowling_data.drop(columns=['Unnamed: 14'])
bowling_data = bowling_data.fillna(0).replace('-',0)
bowling_data = bowling_data.astype({'Inns': 'int32','Econ': 'float64'})
bowling_data = bowling_data[[i > 0 for i in bowling_data['Inns']]]
bowling_data['BallEcon'] = [i/6 for i in bowling_data['Econ']]
bowling_data.insert(loc=0, column='Lookup', value=[i+'_'+j for i,j in zip(bowling_data['Player'], bowling_data['Innings'])])


batting_data.to_csv('batting_data.csv', index=False)
bowling_data.to_csv('bowling_data.csv', index=False)