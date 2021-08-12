import pandas as pd

league_codes = {'Premier League': 'E0',
                'La Liga': 'SP1',
                'Bundesliga': 'D1',
                'Serie A': 'I1',
                'Ligue 1': 'F1',
                'Liga NOS': 'P1',
                'Eredivisie': 'N1',
                'Jupiler': 'B1',
                'Turkey': 'T1',
                'Greece': 'G1',
                'Premiership': 'SC0',
                'Championship': 'E1',
                'La Liga2': 'SP2',
                'Bundesliga2': 'D2',
                'Serie B': 'I2',
                'Ligue 2': 'F2'}


def download_league(league, year):
    """
    Download league-year games from football-data.co.uk
    :param league: button league
    :param year: button year
    :return: pandas dataframe league_games
    """
    if type(league) is str:
        filename = league_codes[league] + ".csv"
    else:
        filename = league_codes[league.get()] + ".csv"
    if type(year) is str:
        url = 'http://www.football-data.co.uk/mmz4281/{}/{}'.format(year.replace('/', ''), filename)
    else:
        url = 'http://www.football-data.co.uk/mmz4281/{}/{}'.format(year.get().replace('/', ''), filename)
    try:
        _df = pd.read_csv(url)
        return _df
    except UnicodeDecodeError:
        return pd.DataFrame()


def calculate_side_stats(games, side):
    # side selection
    if side == 'home':
        favor = 'H'
        against = 'A'
    else:
        favor = 'A'
        against = 'H'

    n_games = len(games)
    # Points FT
    _df_points = games.groupby('FTR').size()
    points = 0
    if favor in _df_points.index:
        points += _df_points.loc[favor] * 3
    if 'D' in _df_points.index:
        points += _df_points.loc['D'] * 1
    # Points HT
    _df_ht_points = games.groupby('HTR').size()
    points_1t = 0
    if favor in _df_ht_points.index:
        points_1t += _df_ht_points.loc[favor] * 3
    if 'D' in _df_ht_points.index:
        points_1t += _df_ht_points.loc['D'] * 1
    # Points 2nd half
    wins = len(games[(games['FT{}G'.format(favor)] - games['HT{}G'.format(favor)]) >
                     (games['FT{}G'.format(against)] - games['HT{}G'.format(against)])])
    draws = len(games[(games['FTHG'] - games['HTHG']) == (games['FTAG'] - games['HTAG'])])
    points_2t = wins * 3 + draws * 1
    # Goals
    scored_1t = games['HT{}G'.format(favor)].mean()
    scored_2t = games['FT{}G'.format(favor)].sub(games['HT{}G'.format(favor)], axis=0).mean()
    conceded_1t = games['HT{}G'.format(against)].mean()
    conceded_2t = games['FT{}G'.format(against)].sub(games['HT{}G'.format(against)], axis=0).mean()
    # Shots
    shots_favor = games['{}S'.format(favor)].mean()
    shots_against = games['{}S'.format(against)].mean()
    shots_target_favor = games['{}ST'.format(favor)].mean()
    shots_target_against = games['{}ST'.format(against)].mean()
    # Fouls
    fouls_commited = games['{}F'.format(favor)].mean()
    fouls_suffered = games['{}F'.format(against)].mean()
    corners_favor = games['{}C'.format(favor)].mean()
    corners_against = games['{}C'.format(against)].mean()
    yellow_favor = games['{}Y'.format(favor)].mean()
    yellow_against = games['{}Y'.format(against)].mean()
    red_favor = games['{}R'.format(favor)].mean()
    red_against = games['{}R'.format(against)].mean()

    return [n_games, points, points_1t, points_2t, scored_1t, scored_2t, conceded_1t, conceded_2t,
            shots_favor, shots_against, shots_target_favor, shots_target_against, fouls_commited, fouls_suffered,
            corners_favor, corners_against, yellow_favor, yellow_against, red_favor, red_against]


def calculate_team_stats(team_h_games, team_a_games):
    """
    Calculate stats for a team
    :param team_h_games: pandas dataframe home games
    :param team_a_games: pandas dataframe away games
    :return: pandas dataframe team stats
    """
    if len(team_h_games) > 0:
        team_name = team_h_games.iloc[0].HomeTeam
    else:
        team_name = team_a_games.iloc[0].AwayTeam
    wins = len(team_h_games[team_h_games.FTR == 'H']) + len(team_a_games[team_a_games['FTR'] == 'A'])
    draws = len(team_h_games[team_h_games.FTR == 'D']) + len(team_a_games[team_a_games['FTR'] == 'D'])
    losses = len(team_h_games[team_h_games.FTR == 'A']) + len(team_a_games[team_a_games['FTR'] == 'H'])

    _df = pd.DataFrame(
        [team_name, wins, draws, losses] + calculate_side_stats(team_h_games, 'home')
        + calculate_side_stats(team_a_games, 'away'))

    return _df.transpose()


def calculate_league_stats(games):
    """
    Calculate stats for every team in the league
    :param games: pandas dataframe league games
    :return: pandas dataframe stats
    """
    teams = list({*games.HomeTeam, *games.AwayTeam})
    # _df_homeGames = games.groupby('HomeTeam')
    # _df_awayGames = games.groupby('AwayTeam')
    # res = [calculate_team_stats(_df_homeGames.get_group(team), _df_awayGames.get_group(team)) for team in teams]
    res = [calculate_team_stats(games[games.HomeTeam == team], games[games.AwayTeam == team]) for team in teams]
    df = pd.concat(res).reset_index(drop=True)
    df.columns = ['Team', 'W', 'D', 'L',
                  'HGames', 'HPoints', 'HPoints1H', 'HPoints2H', 'HScored1H', 'HScored2H', 'HConceded1H', 'HConceded2H',
                  'HShotsFavor', 'HShotsAgainst', 'HShotsTFavor', 'HShotsTAgainst', 'HFoulsCommited', 'HFoulsSuffered',
                  'HCornersFavor', 'HCornersAgainst', 'HYellowFavor', 'HYellowAgainst', 'HRedFavor', 'HRedAgainst',
                  'AGames', 'APoints', 'APoints1H', 'APoints2H', 'AScored1H', 'AScored2H', 'AConceded1H', 'AConceded2H',
                  'AShotsFavor', 'AShotsAgainst', 'AShotsTFavor', 'AShotsTAgainst', 'AFoulsCommited', 'AFoulsSuffered',
                  'ACornersFavor', 'ACornersAgainst', 'AYellowFavor', 'AYellowAgainst', 'ARedFavor', 'ARedAgainst']
    league_stats = df.iloc[(df.HPoints + df.APoints).sort_values(ascending=False).index].reset_index(drop=True)

    return league_stats


def get_table_sorted(league_stats, sortBy):
    """
    Get Table sorted by sortBy
    :param league_stats: pandas dataframe
    :param sortBy: str
    :return: pandas dataframe sorted
    """
    _df = league_stats.copy(deep=True)
    _df['Scored'] = (_df.HScored1H + _df.HScored2H) * _df.HGames + (_df.AScored1H + _df.AScored2H) * _df.AGames
    _df['Conceded'] = (_df.HConceded1H + _df.HConceded2H) * _df.HGames + (
            _df.AConceded1H + _df.AConceded2H) * _df.AGames
    _df['Points'] = _df.HPoints + _df.APoints
    _df['Shots'] = ((_df.HShotsFavor * _df.HGames + _df.AShotsFavor * _df.AGames) / (_df.HGames + _df.AGames))
    _df['Corners'] = ((_df.HCornersFavor * _df.HGames + _df.ACornersFavor * _df.AGames) / (_df.HGames + _df.AGames))
    _df['OEff'] = get_offensive_efficiency(_df)
    _df['DEff'] = get_defensive_efficiency(_df)

    for col in ['Shots', 'Corners', 'OEff', 'DEff']:  # round to two decimal places
        _df[col] = (_df[col] * 100).fillna(0).astype(int) / 100.0

    sort_order = False
    if sortBy.get() == 'Conceded' or sortBy.get() == 'DEff':
        sort_order = True

    _df = _df[['Team', sortBy.get()]]
    _df = _df.sort_values(sortBy.get(), ascending=sort_order).reset_index(drop=True)
    _df.index = _df.index + 1

    return _df


def get_offensive_efficiency(_df, side='all'):
    """
    Get offensive efficiency
    :param _df: league_stats
    :param side: 'home', 'away' or 'all'
    :return:
    """
    try:
        home_eff = 100 * ((_df.HScored1H + _df.HScored2H) / _df.HGames) / (
                    _df.HShotsFavor + _df.HShotsTFavor + _df.HCornersFavor)
    except ZeroDivisionError:
        home_eff = 0
    try:
        away_eff = 100 * ((_df.AScored1H + _df.AScored2H) / _df.AGames) / (
                    _df.AShotsFavor + _df.AShotsTFavor + _df.ACornersFavor)
    except ZeroDivisionError:
        away_eff = 0
    if side == 'home':
        return home_eff
    elif side == 'away':
        return away_eff
    else:
        return (home_eff * _df.HGames + away_eff * _df.AGames) / (_df.HGames + _df.AGames)


def get_defensive_efficiency(_df, side='all'):
    """
    Get defensive efficiency
    :param _df: league_stats
    :param side: 'home', 'away' or 'all'
    :return:
    """
    try:
        home_eff = 100 * ((_df.HConceded1H + _df.HConceded2H) / _df.HGames) / (
                    _df.HShotsAgainst + _df.HShotsTAgainst + _df.HCornersAgainst)
    except ZeroDivisionError:
        home_eff = 0
    try:
        away_eff = 100 * ((_df.AConceded1H + _df.AConceded2H) / _df.AGames) / (
                    _df.AShotsAgainst + _df.AShotsTAgainst + _df.ACornersAgainst)
    except ZeroDivisionError:
        away_eff = 0
    if side == 'home':
        return home_eff
    elif side == 'away':
        return away_eff
    else:
        return (home_eff * _df.HGames + away_eff * _df.AGames) / (_df.HGames + _df.AGames)


def get_team_metrics(league_stats, team, side_name):
    """
    Get team metrics
    :param league_stats:
    :param team:
    :param side_name:
    """
    if side_name == 'home':
        side = 'H'
    else:
        side = 'A'
    _df = league_stats.copy(deep=True).set_index('Team', drop=True)
    dic = dict()
    # League rank
    _df['aux'] = (_df.HPoints + _df.APoints)
    dic['Rank'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}Points'.format(side)])
    dic['{}Rank'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Goals
    # Scored
    _df['aux'] = (_df.HScored1H + _df.HScored2H + _df.AScored1H + _df.AScored2H)
    dic['Scored'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}Scored1H'.format(side)] + _df['{}Scored2H'.format(side)])
    dic['{}Scored'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # # 1 Half
    _df['aux'] = (_df.HScored1H + _df.AScored1H)
    dic['Scored_1H'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}Scored1H'.format(side)])
    dic['{}Scored_1H'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # # 2 Half
    _df['aux'] = (_df.HScored2H + _df.AScored2H)
    dic['Scored_2H'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}Scored2H'.format(side)])
    dic['{}Scored_2H'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Conceded
    _df['aux'] = (_df.HConceded1H + _df.HConceded2H + _df.AConceded1H + _df.AConceded2H)
    dic['Conceded'] = _df.sort_values('aux').index.get_loc(team) + 1
    _df['aux'] = (_df['{}Conceded1H'.format(side)] + _df['{}Conceded2H'.format(side)])
    dic['{}Conceded'.format(side)] = _df.sort_values('aux').index.get_loc(team) + 1
    # # 1 Half
    _df['aux'] = (_df.HConceded1H + _df.AConceded1H)
    dic['Conceded_1H'] = _df.sort_values('aux').index.get_loc(team) + 1
    _df['aux'] = (_df['{}Conceded1H'.format(side)])
    dic['{}Conceded_1H'.format(side)] = _df.sort_values('aux').index.get_loc(team) + 1
    # # 2 Half
    _df['aux'] = (_df.HConceded2H + _df.AConceded2H)
    dic['Conceded_2H'] = _df.sort_values('aux').index.get_loc(team) + 1
    _df['aux'] = (_df['{}Conceded2H'.format(side)])
    dic['{}Conceded_2H'.format(side)] = _df.sort_values('aux').index.get_loc(team) + 1
    # Shots
    _df['aux'] = (_df.HShotsFavor + _df.AShotsFavor)
    dic['Shots'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}ShotsFavor'.format(side)])
    dic['{}Shots'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Shots on target
    _df['aux'] = (_df.HShotsTFavor + _df.AShotsTFavor)
    dic['ShotsT'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}ShotsTFavor'.format(side)])
    dic['{}ShotsT'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Corners
    _df['aux'] = (_df.HCornersFavor + _df.ACornersFavor)
    dic['Corners'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}CornersFavor'.format(side)])
    dic['{}Corners'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Efficiency
    _df['OEff'] = get_offensive_efficiency(_df)
    _df['{}OEff'.format(side)] = get_offensive_efficiency(_df, side_name)
    _df['DEff'] = get_defensive_efficiency(_df)
    _df['{}DEff'.format(side)] = get_defensive_efficiency(_df, side_name)
    # Offensive
    _df['aux'] = _df.OEff
    dic['OEff'] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    _df['aux'] = (_df['{}OEff'.format(side)])
    dic['{}OEff'.format(side)] = _df.sort_values('aux', ascending=False).index.get_loc(team) + 1
    # Defensive
    _df['aux'] = _df.DEff
    dic['DEff'] = _df.sort_values('aux').index.get_loc(team) + 1
    _df['aux'] = (_df['{}DEff'.format(side)])
    dic['{}DEff'.format(side)] = _df.sort_values('aux').index.get_loc(team) + 1

    return dic


def get_match(league_stats, h_team, a_team):
    """
    Get Match metrics
    :param league_stats: pandas dataframe
    :param h_team: str
    :param a_team: str
    :return:
    """
    home = get_team_metrics(league_stats, h_team, 'home')
    away = get_team_metrics(league_stats, a_team, 'away')

    return home, away
