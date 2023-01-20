import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv').set_index('date')

# Clean data
df = df[(df['value'] <= df['value'].quantile(0.975))
        & (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():
  # Draw line plot
  x_axis = pd.to_datetime(df.index)
  y_axis = df.loc[:, 'value']

  fig = plt.figure(figsize=(12, 6))
  plt.plot(x_axis, y_axis)
  plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  plt.xlabel('Date')
  plt.ylabel('Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()
  df_bar['year'] = pd.to_datetime(df.index).year
  df_bar['month'] = pd.to_datetime(df.index).month

  df_bar = df_bar.groupby([df_bar['year'], df_bar['month']])['value'].mean().reset_index()

  figure = sns.catplot(data=df_bar, x='year', y='value', kind='bar', hue='month', legend=False)
  
  handles, labels = figure.ax.get_legend_handles_labels()
  labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  
  figure.ax.legend(handles, labels, title='Months')
  figure.set_axis_labels('Years', 'Average Page Views')

  fig = figure.fig

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = pd.to_datetime(df.index).year
  df_box['month'] = [d.strftime('%b') for d in pd.to_datetime(df.index)]
  df_box.sort_values(by=['year','date'],ascending=[False, True], inplace=True)
  print(df_box)
  
  # Draw box plots (using Seaborn)
  fig, (figure1,figure2) = plt.subplots(1,2)
  fig.set_figwidth(20)
  fig.set_figheight(10)

  figure1.set_title('Year-wise Box Plot (Trend)')
  figure1 = sns.boxplot(data=df_box, x='year', y='value', ax=figure1)
  figure1.set_xlabel('Year')
  figure1.set_ylabel('Page Views')

  figure2.set_title('Month-wise Box Plot (Seasonality)')
  figure2 = sns.boxplot(data = df_box, x='month', y='value', ax=figure2)
  figure2.set_xlabel('Month')
  figure2.set_ylabel('Page Views')
  
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
