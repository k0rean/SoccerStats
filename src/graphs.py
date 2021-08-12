import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['toolbar'] = 'None'
fig = ""


def graph_goals(df, txt, theme):
    if theme == 'dark':
        plt.style.use("dark_background")
    else:
        plt.style.use('default')
    teams = df.Team.to_list()
    if "Scored" in txt:
        h_goals1 = df.HScored1H.to_list()
        h_goals2 = df.HScored2H.to_list()
        a_goals1 = df.AScored1H.to_list()
        a_goals2 = df.AScored2H.to_list()
    else:
        h_goals1 = df.HConceded1H.to_list()
        h_goals2 = df.HConceded2H.to_list()
        a_goals1 = df.AConceded1H.to_list()
        a_goals2 = df.AConceded2H.to_list()

    plt.subplot(211)
    plt.bar(teams, h_goals1, label='1st Half Home')
    plt.bar(teams, h_goals2, bottom=h_goals1, label='2nd Half Home')
    plt.legend(prop={'size': 8})
    plt.title(txt)
    plt.xticks(fontsize=10, rotation=20)
    plt.ylabel('Home')

    plt.subplot(212)
    plt.bar(teams, a_goals1, label='1st Half Away')
    plt.bar(teams, a_goals2, bottom=a_goals1, label='2nd Half Away')
    plt.legend(prop={'size': 8})
    plt.xticks(fontsize=10, rotation=20)
    plt.ylabel('Away')

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close(fig)


def graph_situations(df, txt, theme):
    if theme == 'dark':
        plt.style.use("dark_background")
    else:
        plt.style.use('default')
    teams = df.Team.to_list()
    if "Corners" in txt:
        h_corners1 = df.HCornersFavor.to_list()
        h_corners2 = df.HCornersAgainst.to_list()
        a_corners1 = df.ACornersFavor.to_list()
        a_corners2 = df.ACornersAgainst.to_list()
    elif "Fouls" in txt:
        h_fouls1 = df.HFoulsCommited.to_list()
        h_fouls2 = df.HFoulsSuffered.to_list()
        a_fouls1 = df.AFoulsCommited.to_list()
        a_fouls2 = df.AFoulsSuffered.to_list()
    elif "Goal Difference" in txt:
        h_perf1 = df.HScored1H.sub(df.HConceded1H, axis=0).to_list()
        h_perf2 = df.HScored2H.sub(df.HConceded2H, axis=0).to_list()
        a_perf1 = df.AScored1H.sub(df.AConceded1H, axis=0).to_list()
        a_perf2 = df.AScored2H.sub(df.AConceded2H, axis=0).to_list()

    plt.subplot(211)
    if "Corners" in txt:
        subcategorybar(teams, [h_corners1, h_corners2])
        plt.legend(('Home Corners in favor', 'Home Corners Against'), prop={'size': 8})
    elif "Fouls" in txt:
        subcategorybar(teams, [h_fouls1, h_fouls2])
        plt.legend(('Home Fouls Commited', 'Home Fouls Suffered'), prop={'size': 8})
    elif "Goal Difference" in txt:
        subcategorybar(teams, [h_perf1, h_perf2], 0.6)
        plt.legend(('Home Performance 1Half', 'Home Performance 2Half'), prop={'size': 8})
        plt.axhline(y=0, color='black', linestyle='-')
    plt.title(txt)
    plt.xticks(fontsize=10, rotation=20)
    plt.ylabel('Home')

    plt.subplot(212)
    if "Corners" in txt:
        subcategorybar(teams, [a_corners1, a_corners2])
        plt.legend(('Away Corners in favor', 'Away Corners Against'), prop={'size': 8})
    elif "Fouls" in txt:
        subcategorybar(teams, [a_fouls1, a_fouls2])
        plt.legend(('Away Fouls Commited', 'Away Fouls Suffered'), prop={'size': 8})
    elif "Goal Difference" in txt:
        subcategorybar(teams, [a_perf1, a_perf2], 0.6)
        plt.legend(('Away Performance 1Half', 'Away Performance 2Half'), prop={'size': 8})
        plt.axhline(y=0, color='black', linestyle='-')
    plt.ylabel('Away')
    plt.xticks(fontsize=10, rotation=20)

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close(fig)


def subcategorybar(x, vals, width=0.8):
    n = len(vals)
    _x = np.arange(len(x))
    for i in range(n):
        plt.bar(_x - width / 2. + i / float(n) * width, vals[i],
                width=width / float(n), align="edge")
    plt.xticks(_x, x)


def graph_situations_stack(df, txt, theme):
    if theme == 'dark':
        plt.style.use("dark_background")
    else:
        plt.style.use('default')
    teams = df.Team.to_list()
    if "Shots" in txt:
        h_shots1 = df.HShotsFavor.to_list()
        h_shots2 = df.HShotsAgainst.to_list()
        a_shots1 = df.AShotsFavor.to_list()
        a_shots2 = df.AShotsAgainst.to_list()
        # target
        h_shots_t1 = df.HShotsTFavor.to_list()
        h_shots_t2 = df.HShotsTAgainst.to_list()
        a_shots_t1 = df.AShotsTFavor.to_list()
        a_shots_t2 = df.AShotsTAgainst.to_list()
    elif "Cards" in txt:
        h_yellow1 = df.HYellowFavor.to_list()
        h_yellow2 = df.HYellowAgainst.to_list()
        a_yellow1 = df.AYellowFavor.to_list()
        a_yellow2 = df.AYellowAgainst.to_list()
        # Red
        h_red1 = df.HRedFavor.to_list()
        h_red2 = df.HRedAgainst.to_list()
        a_red1 = df.ARedFavor.to_list()
        a_red2 = df.ARedAgainst.to_list()

    plt.subplot(211)
    if "Shots" in txt:
        subcategorybar_stack(teams, [h_shots1, h_shots2], [h_shots_t1, h_shots_t2])
        plt.legend(('Home Shots in favor', 'Home Shots on target in favor', 'Home Shots against',
                    'Home Shots on target against'), prop={'size': 8})
    elif "Cards" in txt:
        subcategorybar_stack(teams, [h_yellow1, h_yellow2], [h_red1, h_red2])
        plt.legend(('Home Yellows in favor', 'Home Reds in favor', 'Home Yellows against', 'Home Reds against'),
                   prop={'size': 8})
    plt.title(txt)
    plt.xticks(fontsize=10, rotation=20)
    plt.ylabel('Home')

    plt.subplot(212)
    if "Shots" in txt:
        subcategorybar_stack(teams, [a_shots1, a_shots2], [a_shots_t1, a_shots_t2])
        plt.legend(('Away Shots in favor', 'Away Shots on target in favor', 'Away Shots against',
                    'Away Shots on target against'), prop={'size': 8})
    elif "Cards" in txt:
        subcategorybar_stack(teams, [a_yellow1, a_yellow2], [a_red1, a_red2])
        plt.legend(('Away Yellows in favor', 'Away Reds in favor', 'Away Yellows against', 'Away Reds against'),
                   prop={'size': 8})
    plt.xticks(fontsize=10, rotation=20)
    plt.ylabel('Away')

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close(fig)


def subcategorybar_stack(x, vals1, vals2, width=0.8):
    n = len(vals1)
    _x = np.arange(len(x))
    for i in range(n):
        plt.bar(_x - width / 2. + i / float(n) * width, vals1[i],
                width=width / float(n), align="edge")
        plt.bar(_x - width / 2. + i / float(n) * width, vals2[i],
                width=width / float(n), align="edge", bottom=vals1[i])
    plt.xticks(_x, x)
