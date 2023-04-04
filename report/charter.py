import seaborn as sns
from matplotlib.ticker import StrMethodFormatter
import matplotlib.pyplot as plt

column_names = {
        'ServePercentage': 'Aufschlag',
        'ReceptionPercentage': 'Annahme',
        'Attack2Percentage': 'Angriff 2',
        'Attack3Percentage': 'Angriff 3',
        'Attack4Percentage': 'Angriff 4',
        'AttackBackrowPercentage': 'Angriff HF'
    }

column_names_condensed = {
        'ServePercentage': 'Aufschlag',
        'ReceptionPercentage': 'Annahme',
        'AttackPercentage': 'Angriff',
    }


def set_heatmap(df, path, ylabel='Satz', figsize=(12, 4), title='Satzanalyse', drop_match=True, clear_graph=False):
    if clear_graph:
        plt.clf()
    # Make heatmap beautiful
    if drop_match:
        df = df.drop('match', axis=1)
    df = df[column_names.keys()]
    df = df.rename(index={'set': 'Satz'}, columns=column_names)
    # set_statistics = set_statistics.rename()
    df = df.mul(100).round()
    sns.set(rc={'figure.figsize': figsize})
    heatmap = sns.heatmap(df, center=0, vmin=-100, vmax=100,
                          linewidths=.5, annot=True, cbar_kws={'format': '%.0f%%'}, fmt='g',
                          cmap="RdBu")
    heatmap.set(xlabel='Quote', ylabel=ylabel)
    heatmap.set_title(title, fontsize=20)
    for t in heatmap.texts:
        t.set_text(t.get_text() + '%')
    fig = heatmap.get_figure()
    fig.savefig(path, bbox_inches='tight')


def season_lineplot(df, path, xlabels):
    plt.clf()
    legend_entries = list(column_names_condensed.keys())
    legend_entries.reverse()
    df = df[legend_entries]
    df = df.rename(index={'match': 'Spiel'}, columns=column_names_condensed)
    df = df.mul(100).round()
    sns.set(rc={'figure.figsize': (12, 4)})
    palette = ['r', 'b', 'g']
    lineplot = sns.lineplot(df, markers=True, dashes=False, palette=palette)
    # heatmap = sns.heatmap(match_statistics, center=0, vmin=-100, vmax=100,
    #                  linewidths=.5, annot=True, cbar_kws={'format': '%.0f%%'}, fmt='g',
    #                  cmap="PiYG")
    lineplot.set(xlabel='Spiel', ylabel='Quote')
    lineplot.set_title('Saisonverlauf', fontsize=15)
    # for t in lineplot.texts: t.set_text(t.get_text() + '%')
    # control x and y limits
    #plt.ylim(0, 20)
    lineplot.set(xticks=list(df.index), xticklabels=xlabels)
    lineplot.set_xticklabels(lineplot.get_xticklabels(), rotation=30)
    yticks = StrMethodFormatter('{x: .0f}%')
    lineplot.yaxis.set_major_formatter(yticks)
    fig = lineplot.get_figure()
    fig.savefig(path, bbox_inches='tight')
