import pandas as pd


def analyze_category(name, match, scores, cat):
    assessments = list()
    scores = str(scores).split('|')
    set_number = 1
    for set_scores in scores:
        if set_scores != 'nan':
            assessment = dict()
            assessment['player'] = name
            assessment['match'] = match
            assessment['set'] = set_number
            assessment[cat+'_+'] = 0
            assessment[cat+'_0'] = 0
            assessment[cat+'_-'] = 0
            for value in set(set_scores):
                if value not in ['+', '0', '-', 'E', 'A']:
                    print(f'Wrong character in match {match} and category {cat}')
                assessment[cat + '_' + value] = set_scores.count(value)

            assessments.append(assessment)
        set_number += 1
    return assessments


def analyze_player(player):
    assessments = list()
    name = player.Spieler
    match = player.Spiel

    assessments.extend(analyze_category(name, match, player.Annahme, 'Reception'))
    assessments.extend(analyze_category(name, match, player.Aufschlag, 'Serve'))
    assessments.extend(analyze_category(name, match, player.Angriff2, 'Attack2'))
    assessments.extend(analyze_category(name, match, player.Angriff3, 'Attack3'))
    assessments.extend(analyze_category(name, match, player.Angriff4, 'Attack4'))
    assessments.extend(analyze_category(name, match, player.AngriffHinterfeld, 'AttackBackrow'))

    return assessments


def analyze_match(df):
    assessments = list()
    for player in df.itertuples():
        assessments.extend(analyze_player(player))
    aggregated_assessment = pd.DataFrame(assessments)
    aggregated_assessment = pd.pivot_table(data=aggregated_assessment, index=['match', 'player', 'set'])
    return aggregated_assessment
