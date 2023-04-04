import numpy as np
import seaborn as sns
from ingest import sheetreader, transformation
from report import charter, reporter
import environmentvariables
import analyzer

environmentvariables.store_envs()

heatmap_path = 'output/setheatmap.png'
season_path = 'output/seasongraph.png'
all_players_path = 'output/allplayers.png'
each_player_path = 'output/individual/'

reload = False
df_match_details = sheetreader.read_sheet('Spiele', reload)
df_statistics = sheetreader.read_sheet('StatistikSaison', reload)


def filter_match(df, match):
    return df[df['Spiel'] == match]


def match_info(df, matches):
    details = list()
    for match in matches:
        details.append(
            df[df.Spiel == match].iloc[0]['Gegner'] + ' (' + df[df.Spiel == match].iloc[0]['Ergebnis'] + ')')
    return details


def single_match_info(df, match):
    return df[df.Spiel == match].iloc[0]['Gegner'] + ' ' + df[df.Spiel == match].iloc[0]['Ergebnis'] + '\n(' + df[df.Spiel == match].iloc[0]['Satzergebnis'] + ')'


def create_set_statistics(df, path, match):
    df = filter_match(df, match)

    # Remove 2nd ball from setter
    df.loc[df['Spieler'] == 'Timi', 'Angriff2'] = np.nan
    df = transformation.analyze_match(df).reset_index()

    df = df.groupby(['set']).sum()
    df = analyzer.compute_quota(df)
    # set_statistics = analyzer.clean(set_statistics)
    df = analyzer.count_filter(df, min_frequency=2)

    charter.set_heatmap(df, path)


def attack_distribution(df, match):
    df = filter_match(df, match)
    df = transformation.analyze_match(df).reset_index()
    df = df.groupby(['match']).sum()
    return analyzer.attack_distribution(df)


def highlights(df, match):
    df = filter_match(df, match)
    df = transformation.analyze_match(df).reset_index()
    df = df.groupby(['player']).sum()
    return analyzer.highlights(df)


def create_season_overview(df, path):
    df = transformation.analyze_match(df).reset_index()
    df = df.groupby(['match']).sum()
    df = analyzer.compute_quota(df, aggregate_attack=True)
    xlabels = match_info(df_match_details, list(df.index))
    charter.season_lineplot(df, path, xlabels)


def analyze_match(match):
    create_set_statistics(df_statistics, heatmap_path, match)
    create_season_overview(df_statistics, season_path)
    reporter.create_report(
        single_match_info(df_match_details, match),
        heatmap_path, season_path,
        attack_distribution(df_statistics, match),
        highlights(df_statistics, match))


def analyze_all_players():
    df = transformation.analyze_match(df_statistics).reset_index()
    df = df.groupby(['player']).sum()
    analyzer.compute_pos_neut_neg_attack_quota(df)

    df = analyzer.compute_quota(df)
    # set_statistics = analyzer.clean(set_statistics)
    df = analyzer.count_filter(df, min_frequency=5)

    charter.set_heatmap(df, all_players_path, ylabel='Spieler', figsize=(12, 6), title='Spieleranalyse')


def analyze_each_player():
    df = transformation.analyze_match(df_statistics).reset_index()
    for player in set(df['player']):
        single_df = df[df['player'] == player]
        single_df = single_df.groupby(['match']).sum()
        single_df = analyzer.compute_quota(single_df)
        single_df = analyzer.count_filter(single_df, min_frequency=4)
        # single_df = analyzer.clean(single_df, remove_set=True)
        charter.set_heatmap(
            single_df,
            each_player_path+player+'.png',
            ylabel='Match', figsize=(12, 6), title=player, drop_match=False, clear_graph=True)


def count_serve_errors():
    df = transformation.analyze_match(df_statistics).reset_index()
    df = df.groupby(['match']).sum()
    print(df[['Serve_A', 'Serve_E']])


analyze_match(16)
# analyze_all_players()
# count_serve_errors()
# analyze_each_player()

