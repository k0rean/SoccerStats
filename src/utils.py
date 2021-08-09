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

    return pd.read_csv(url)


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
    points = _df_points.loc[favor] * 3 + _df_points.loc['D'] * 1
    # Points HT
    _df_ht_points = games.groupby('HTR').size()
    points_1t = _df_ht_points.loc[favor] * 3 + _df_ht_points.loc['D'] * 1
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
    team_name = team_h_games.iloc[0].HomeTeam
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
    _df_homeGames = games.groupby('HomeTeam')
    _df_awayGames = games.groupby('AwayTeam')

    res = [calculate_team_stats(_df_homeGames.get_group(team), _df_awayGames.get_group(team)) for team in teams]
    df = pd.concat(res).reset_index(drop=True)
    df.columns = ['Team',  'W', 'D', 'L',
                  'HGames', 'HPoints', 'HPoints1H', 'HPoints2H', 'HScored1H', 'HScored2H', 'HConceded1H', 'HConceded2H',
                  'HShotsFavor', 'HShotsAgainst', 'HShotsTFavor', 'HShotsTAgainst', 'HFoulsCommited', 'HFoulsSuffered',
                  'HCornersFavor', 'HCornersAgainst', 'HYellowFavor', 'HYellowAgainst', 'HRedFavor', 'HRedAgainst',
                  'AGames', 'APoints', 'APoints1H', 'APoints2H', 'AScored1H', 'AScored2H', 'AConceded1H', 'AConceded2H',
                  'AShotsFavor', 'AShotsAgainst', 'AShotsTFavor', 'AShotsTAgainst', 'AFoulsCommited', 'AFoulsSuffered',
                  'ACornersFavor', 'ACornersAgainst', 'AYellowFavor', 'AYellowAgainst', 'ARedFavor', 'ARedAgainst']
    league_stats = df.iloc[(df.HPoints + df.APoints).sort_values(ascending=False).index].reset_index(drop=True)

    return league_stats
