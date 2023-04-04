import pandas as pd
import numpy as np
import math

metric_pairs = dict()
metric_pairs['ReceptionCount'] = 'ReceptionPercentage'
metric_pairs['ServeCount'] = 'ServePercentage'
metric_pairs['Attack2Count'] = 'Attack2Percentage'
metric_pairs['Attack3Count'] = 'Attack3Percentage'
metric_pairs['Attack4Count'] = 'Attack4Percentage'
metric_pairs['AttackCount'] = 'AttackPercentage'
metric_pairs['AttackBackrowCount'] = 'AttackBackrowPercentage'


def compute_quota(df, aggregate_attack=False):
    df['ServePercentage'] = (df['Serve_A']+0.5*df['Serve_+']+0.25*df['Serve_0']-0.5*df['Serve_E']) /\
                            (df['Serve_A']+df['Serve_+']+df['Serve_0']+df['Serve_-'])
    df['ServeCount'] = df['Serve_A']+df['Serve_+']+df['Serve_0']+df['Serve_-']

    df['ReceptionPercentage'] = (df['Reception_+'] - 0.5 * df['Reception_-'] - df['Reception_E']) / \
                            (df['Reception_+']+df['Reception_0']+df['Reception_-']+df['Reception_E'])
    df['ReceptionCount'] = df['Reception_+']+df['Reception_0']+df['Reception_-']+df['Reception_E']

    if aggregate_attack:
        df['AttackPercentage'] = (df['Attack2_+'] + df['Attack3_+'] + df['Attack4_+'] + df['AttackBackrow_+']
                                  - df['Attack2_-'] - df['Attack3_-'] - df['Attack4_-'] - df['AttackBackrow_-']
                                  ) / \
                                 (df['Attack2_+'] + df['Attack2_0'] + df['Attack2_-'] +
                                  df['Attack3_+'] + df['Attack3_0'] + df['Attack3_-'] +
                                  df['Attack4_+'] + df['Attack4_0'] + df['Attack4_-'] +
                                  df['AttackBackrow_+'] + df['AttackBackrow_0'] + df['AttackBackrow_-'])
        df['AttackCount'] = (df['Attack2_+'] + df['Attack2_0'] + df['Attack2_-'] +
                             df['Attack3_+'] + df['Attack3_0'] + df['Attack3_-'] +
                             df['Attack4_+'] + df['Attack4_0'] + df['Attack4_-'] +
                             df['AttackBackrow_+'] + df['AttackBackrow_0'] + df['AttackBackrow_-'])
    else:
        for attack in ['Attack2', 'Attack3', 'Attack4', 'AttackBackrow']:
            df[attack + 'Percentage'] = (df[attack + '_+']-df[attack + '_-']) /\
                                        (df[attack + '_+']+df[attack + '_0']+df[attack + '_-'])
            df[attack + 'Count'] = df[attack + '_+']+df[attack + '_0']+df[attack + '_-']
    return df


def compute_pos_neut_neg_attack_quota(df):
    df['AttackPosCount'] = df['Attack2_+'] + df['Attack3_+'] + df['Attack4_+'] + df['AttackBackrow_+']
    df['AttackNeutCount'] = df['Attack2_0'] + df['Attack3_0'] + df['Attack4_0'] + df['AttackBackrow_0']
    df['AttackNegCount'] = df['Attack2_-'] + df['Attack3_-'] + df['Attack4_-'] + df['AttackBackrow_-']
    print(df[['AttackPosCount', 'AttackNeutCount', 'AttackNegCount']])
    df[['AttackPosCount', 'AttackNeutCount', 'AttackNegCount']].to_csv('posnegquota.csv')


def count_filter(df, min_frequency=0):
    for count_name in metric_pairs.keys():
        if count_name in df.columns:
            df.loc[df[count_name] < min_frequency, metric_pairs[count_name]] = np.nan
    return df


def clean(df,):
    return df.drop(labels=['Attack2_+', 'Attack2_-', 'Attack2_0',
                           'Attack3_+', 'Attack3_-', 'Attack3_0',
                           'Attack4_+', 'Attack4_-', 'Attack4_0',
                           'AttackBackrow_+', 'AttackBackrow_0', 'AttackBackrow_-',
                           'Reception_+', 'Reception_-', 'Reception_0', 'Reception_E',
                           'Serve_+', 'Serve_-', 'Serve_0', 'Serve_A', 'Serve_E'],
                   errors='ignore',
                   axis=1)


def attack_distribution(df):
    distribution = dict()
    distribution['Attack2'] = df['Attack2_+'].sum() + df['Attack2_0'].sum() + df['Attack2_-'].sum()
    distribution['Attack3'] = df['Attack3_+'].sum() + df['Attack3_0'].sum() + df['Attack3_-'].sum()
    distribution['Attack4'] = df['Attack4_+'].sum() + df['Attack4_0'].sum() + df['Attack4_-'].sum()
    distribution['AttackBackrow'] = df['AttackBackrow_+'].sum() + df['AttackBackrow_0'].sum() + df['AttackBackrow_-'].sum()
    factor = 1 / sum(distribution.values())
    return {key: value * factor for key, value in distribution.items()}


def highlight(df, column, percent=False):
    value = df[column].max()
    if percent:
        return [', '.join(list(df[df[column] == value].index)), "{0:.0%}".format(value)]
    else:
        return [', '.join(list(df[df[column] == value].index)), int(value)]


def highlights(df):
    df['Attacks'] = df['Attack2_+'] + df['Attack2_0'] + df['Attack2_-'] \
                    + df['Attack3_+'] + df['Attack3_0']\
                    + df['Attack3_-'] +df['Attack4_+'] + df['Attack4_0'] + df['Attack4_-']\
                    + df['AttackBackrow_+'] + df['AttackBackrow_0'] + df['AttackBackrow_-']
    df['Receptions'] = df['Reception_+'] + df['Reception_0'] + df['Reception_-'] + df['Reception_E']
    df['Serves'] = df['Serve_+'] + df['Serve_0'] + df['Serve_-'] + df['Serve_A'] + df['Serve_E']
    df['Points'] = df['Attack2_+'] + df['Attack3_+'] + df['Serve_A'] + df['Attack4_+'] + df['AttackBackrow_+']
    # print(df[['Attacks', 'Receptions']])
    df = compute_quota(df, aggregate_attack=True)
    df = count_filter(df, min_frequency=6)

    distribution = dict()
    distribution['Punkte'] = highlight(df, 'Points')
    distribution['Aufschlagsquote'] = highlight(df, 'ServePercentage', percent=True)
    distribution['Annahmequote'] = highlight(df, 'ReceptionPercentage', percent=True)
    distribution['Angriffsquote'] = highlight(df, 'AttackPercentage', percent=True)

    return distribution
