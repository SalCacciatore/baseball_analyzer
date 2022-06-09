

#pip install pybaseball

import pandas as pd

import streamlit


from pybaseball import batting_stats
from pybaseball import pitching_stats


import numpy as np

import plotly.graph_objects as go

from IPython.display import display

ind_bat = batting_stats(2022)

qual_batters = ind_bat[['Name','Team','PA','AVG','OBP','SLG','HR','wRC+','O-Swing%','Z-Contact%','Z-Swing%','O-Contact%','SwStr%','Barrel%','EV','HardHit%','LD%']]

perc_rank = ind_bat.rank(pct=True)
perc_stats = perc_rank.sort_values('HardHit%',ascending=False)[['AVG','OBP','SLG','wRC+','K%','BB%','Barrel%','HardHit%','EV','SwStr%','O-Swing%','Z-Contact%','FB%','GB%','LD%']]

perc_stats = perc_stats.round(2)

col_list = []
for col in perc_stats.columns:
  x = str(col) + "_perc"
  col_list.append(x)

perc_stats.set_axis(col_list, axis=1,inplace=True)

#perc_stats

qualified_batters = qual_batters.merge(perc_stats,right_index=True,left_index=True)

chase_median = qual_batters['O-Swing%'].median()

z_contact_median = qual_batters['Z-Contact%'].median()

z_swing_median = qual_batters['Z-Swing%'].median()

o_contact_median = qual_batters['O-Contact%'].median()

swstr_median = qual_batters['SwStr%'].median()

barrel_median = qual_batters['Barrel%'].median()

EV_median = qual_batters['EV'].median()

hard_hit_median = qual_batters['HardHit%'].median()

line_drive_median = qual_batters['LD%'].median()

all_batters = batting_stats(2022, qual=1)

all_batters['O-Swing%+'] = round(all_batters['O-Swing%']/chase_median,2)*100
all_batters['O-Contact%+'] = round(all_batters['O-Contact%']/o_contact_median,2)*100
all_batters['Z-Contact%+'] = round(all_batters['Z-Contact%']/z_contact_median,2)*100
all_batters['Z-Swing%+'] = round(all_batters['Z-Swing%']/z_swing_median,2)*100
all_batters['SwStr%+'] = round(all_batters['SwStr%']/swstr_median,2)*100

all_batters['HH%+'] = round(all_batters['HardHit%']/hard_hit_median,2)*100
all_batters['EV+'] = round(all_batters['EV']/EV_median,2)*100
all_batters['Barrel%+'] = round(all_batters['Barrel%']/barrel_median,2)*100
all_batters['LD%+'] = round(all_batters['LD%']/line_drive_median,2)*100





all_batters = all_batters[['Name','Team','PA','OBP','SLG','wRC+','WAR','K%+','BB%+','ISO+','BABIP+','GB%+','LD%+','FB%+','Pull%+','EV','EV+','Barrel%+','HH%+','SwStr%+','O-Swing%+','O-Contact%+','Z-Swing%+','Z-Contact%+']]

all_batters['K%+'] = 100+(100 - all_batters['K%+'])
all_batters['O-Swing%+'] = 100+ (100 - all_batters['O-Swing%+'])
all_batters['SwStr%+'] = 100+ (100 - all_batters['SwStr%+'])

Yanks = all_batters[all_batters['Team']=='NYY'].sort_values('WAR',ascending=False).drop(['Team','Pull%+','EV'],axis=1).set_index('Name')

#Yanks

#today_lineup = pd.DataFrame()
#lineup_list = ['Luis Arraez','Byron Buxton','Jorge Polanco','Max Kepler','Gary Sanchez','Trevor Larnach','Gio Urshela','Gillberto Celestino','Jermaine Palacios']
#today_lineup['Name'] =lineup_list

#today_lineup.merge(all_batters,on='Name').drop(['Team','Pull%+','O-Contact%+','EV'],axis=1).set_index('Name')

def create_scatter(answer):
  categories = all_batters[['BB%+','K%+','SwStr%+','Z-Contact%+','O-Contact%+','O-Swing%+','Z-Swing%+','EV+','HH%+','Barrel%+','LD%+','FB%+','ISO+','BABIP+']].columns
  avg_list = []
  for cat in categories:
    avg_list.append(100)
  avg_list.append(100)

  player_chart=all_batters.loc[all_batters['Name']==answer]

  stats = []

  for x in categories:
    stats.append(player_chart[x].item())

  fig = go.Figure()

  fig.add_trace(go.Scatterpolar(
      r=stats,
      theta=categories,
      fill='toself',
      name=answer))
  fig.add_trace(go.Scatterpolar(
      r=avg_list,
      theta=categories,
      #fill='toself',
      name='MLB Average'))

  fig.update_layout(title=answer)

  streamlit.plotly_chart(fig, use_container_width=True)


def create_scatter_past(df,player,year):
  categories = df[['BB%+','K%+','SwStr%+','Z-Contact%+','O-Contact%+','O-Swing%+','Z-Swing%+','EV+','HH%+','Barrel%+','LD%+','FB%+','ISO+','BABIP+']].columns



  avg_list = []
  for cat in categories:
    avg_list.append(100)

  avg_list.append(100)

  player_chart=df

  stats = []

  for x in categories:
    stats.append(player_chart[x].item())

  fig = go.Figure()

  fig.add_trace(go.Scatterpolar(
      r=stats,
      theta=categories,
      fill='toself',
      name='{} ({})'.format(player,year)))
  fig.add_trace(go.Scatterpolar(
      r=avg_list,
      theta=categories,
      #fill='toself',
      name='MLB Average'))

  fig.update_layout(title='{} ({})'.format(player,year))

  streamlit.plotly_chart(fig, use_container_width=True)


def baseball_query(answer):
  if answer in all_batters['Name'].values:
    df_show = all_batters[all_batters['Name']==answer][['Name','PA',	'OBP', 'SLG',	'wRC+',	'WAR',	'K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']].set_index('Name')
    streamlit.write(df_show)
    create_scatter(answer)
  else:
    streamlit.text("{} has no plate appearances this season.".format(answer))

def season_definer(year):

  #load in qualified hitters
  ind_bat = batting_stats(year)
  qual_batters = ind_bat[['Name','Team','PA','AVG','OBP','SLG','HR','wRC+','O-Swing%','Z-Contact%','Z-Swing%','O-Contact%','SwStr%','Barrel%','EV','HardHit%','LD%']]

  #defining leaguewide medians for that year
  chase_median = qual_batters['O-Swing%'].median()
  z_contact_median = qual_batters['Z-Contact%'].median()
  z_swing_median = qual_batters['Z-Swing%'].median()
  o_contact_median = qual_batters['O-Contact%'].median()
  swstr_median = qual_batters['SwStr%'].median()
  barrel_median = qual_batters['Barrel%'].median()
  EV_median = qual_batters['EV'].median()
  hard_hit_median = qual_batters['HardHit%'].median()
  line_drive_median = qual_batters['LD%'].median()


  #load in all hitters
  all_batters = batting_stats(year, qual=1)
  all_batters['O-Swing%+'] = round(all_batters['O-Swing%']/chase_median,2)*100
  all_batters['O-Contact%+'] = round(all_batters['O-Contact%']/o_contact_median,2)*100
  all_batters['Z-Contact%+'] = round(all_batters['Z-Contact%']/z_contact_median,2)*100
  all_batters['Z-Swing%+'] = round(all_batters['Z-Swing%']/z_swing_median,2)*100
  all_batters['SwStr%+'] = round(all_batters['SwStr%']/swstr_median,2)*100
  all_batters['HH%+'] = round(all_batters['HardHit%']/hard_hit_median,2)*100
  all_batters['EV+'] = round(all_batters['EV']/EV_median,2)*100
  all_batters['Barrel%+'] = round(all_batters['Barrel%']/barrel_median,2)*100
  all_batters['LD%+'] = round(all_batters['LD%']/line_drive_median,2)*100

  #adjust strikeout rate, whiff rate and chase rate so higher is better (not worse)
  all_batters['K%+'] = 100+(100 - all_batters['K%+'])
  all_batters['O-Swing%+'] = 100+ (100 - all_batters['O-Swing%+'])
  all_batters['SwStr%+'] = 100+ (100 - all_batters['SwStr%+'])

  return all_batters

def player_szn_finder(player,year):
  all_batters = season_definer(year)
  if player not in all_batters['Name'].values:
    streamlit.text("{} had no plate appearances in {}.".format(player,year))
  else:
    all_batters['Season'] = year
    df = all_batters[all_batters['Name']==player].set_index('Name')
    display_df = df[['Season','Team','PA',	'OBP', 'SLG',	'wRC+',	'WAR',	'K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']]
    streamlit.write(display_df)
    create_scatter_past(df,player,year)


def player_szn(player,year):
  all_batters = season_definer(year)
  if player not in all_batters['Name'].values:
      print('{} had no recorded plate appearances in {}.'.format(player, year))
  all_batters['Season'] = year
  df = all_batters[all_batters['Name']==player].set_index('Name')
  #display(df[['Season','Team','PA',	'OBP', 'SLG',	'wRC+',	'WAR',	'K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']])
  return df

def compare_seasons(player1,player2,year1,year2):
  if int(year1) not in range (1871,2023):
      print("Invalid year.")
  else:
      if int(year2) not in range (1871,2023):
          print("Invalid year.")
      else:


          player1_szn = player_szn(player1,year1)
          player2_szn = player_szn(player2,year2)
          if player1_szn.shape[0] == 0 or player2_szn.shape[0] == 0:
              streamlit.text("One or both of these players had no plate appearances in the selected season.")
          else:
              both_players = player1_szn.append(player2_szn)
              display_df = (both_players[['Season','Team','PA',	'OBP', 'SLG',	'wRC+',	'WAR',	'K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']])
              streamlit.write(display_df)


              categories = all_batters[['BB%+','K%+','SwStr%+','Z-Contact%+','O-Contact%+','O-Swing%+','Z-Swing%+','EV+','HH%+','Barrel%+','LD%+','FB%+','ISO+','BABIP+']].columns

              avg_list = []
              for cat in categories:
                  avg_list.append(100)

              avg_list.append(100)

              player_chart1 = player1_szn

              stats1 = []

              for x in categories:
                  stats1.append(player_chart1[x].item())

              player_chart2 = player2_szn

              stats2 = []

              for x in categories:
                  stats2.append(player_chart2[x].item())



              fig = go.Figure()

              fig.add_trace(go.Scatterpolar(
                r=stats1,
                theta=categories,
                fill='toself',
                name="{} ({})".format(player1,year1)))

              fig.add_trace(go.Scatterpolar(
                r=stats2,
                theta=categories,
                fill='toself',
                name="{} ({})".format(player2,year2)))

              fig.add_trace(go.Scatterpolar(
                r=avg_list,
                theta=categories,
          #fill='toself',
                name='MLB Average'))

              fig.update_layout(title="{} ({}) vs. {} ({})".format(player1,year1,player2,year2))

              streamlit.plotly_chart(fig, use_container_width=True)


def prompt():
  answer=input("Get a player's CURRENT season stats, PAST season stats or COMPARE two seasons?" ).upper()
  if answer == 'CURRENT':
    current=input("What player from the current season?" )
    baseball_query(current)
  elif answer == 'PAST':
    player=input("What player?" )
    szn=input("What year?" )
    player_szn_finder(player,szn)
  elif answer == 'COMPARE':
    player1=input("First player:" )
    szn1=input("What year?" )
    player2=input("Second player:" )
    szn2=input("What year?" )
    compare_seasons(player1,player2,szn1,szn2)


  elif answer == 'YANKS':
    display(Yanks)
    prompt()
  elif answer == 'CANCEL':
    print("See you later.")
    return
  else:
    print('Invalid entry. Insert CANCEL to exit.')
    prompt()

header = streamlit.container()
current_szn = streamlit.container()


with header:
    streamlit.title("BASEBALL STAT ANALYZER")
    streamlit.markdown("Get current and historical baseball data from [FanGraphs](https://www.fangraphs.com).")

with current_szn:
    streamlit.header("Batter Season Analyzer")
    sel_col, disp_col = streamlit.columns(2)
    player_prompt = sel_col.selectbox("Look at a batter's stats from this season or past seasons, or compare two individual seasons.",options=["Current","Past","Compare"],index=0)
    if player_prompt == "Current":
      what_player = sel_col.text_input('What player do you want to learn about?',"Giancarlo Stanton")
      baseball_query(what_player)
    if player_prompt == "Past":
        with streamlit.form("past_selection"):
            what_past = sel_col.text_input('What player do you want to learn about?',"Bernie Williams")
            what_szn = sel_col.slider("What season?",min_value=1871,max_value=2022,value=1998)
            submitted = streamlit.form_submit_button("Submit")
            if submitted:
                streamlit.write("Player:", what_past, "Year:", str(what_szn))
                player_szn_finder(what_past,what_szn)


    if player_prompt == "Compare":
        with streamlit.form('comparison'):

            player1 = sel_col.text_input('Who is the first player you want to learn about?',"Mike Trout")
            szn1 = sel_col.slider("What season?",min_value=1871,max_value=2022,value=2013)
            player2 = sel_col.text_input('Who is the second player you want to learn about?',"Aaron Judge")
            szn2 = sel_col.slider("What season?",min_value=1871,max_value=2022,value=2017)
            submitted = streamlit.form_submit_button("Submit")
            if submitted:
                streamlit.write("Player 1: " + player1 + " ("+str(szn1)+")"+" | Player 2:",player2 +" ("+str(szn2)+")")
                compare_seasons(player1,player2,szn1,szn2)






    streamlit.header("Pitcher Season Analyzer")
    streamlit.text("Coming soon!")



    streamlit.header("Player Career Analyzer")
    streamlit.text("Coming soon")

    streamlit.header("fWAR Leaderboards")
    what_year = streamlit.slider("What season?",min_value=1871,max_value=2022,value=1961)
    hit_or_throw = streamlit.selectbox("Do you want the hitting leaders or pitching leaders?",options=["Hitters","Pitchers"],index=0)
    if hit_or_throw == 'Hitters':
        yr = batting_stats(what_year)
        disp_df = yr[['Name','Team','PA','wRC+','OBP','SLG','HR','ISO','WAR']].head(10)
        streamlit.write(disp_df)
    if hit_or_throw == 'Pitchers':
        yr = pitching_stats(what_year)
        disp_df = yr[['Name','Team','ERA','FIP','xFIP','ERA-','FIP-','xFIP-','K%','BB%','WAR']].head(10)
        streamlit.write(disp_df)





    streamlit.header("Roster Analyzer")
    if streamlit.button("Let's see those Yanks!"):
        streamlit.text("Here are the 2022 Yankees hitters. Complete roster tool coming soon.")
        streamlit.write(Yanks)

    else:
        streamlit.text("Coming soon.")




    streamlit.header("Team Stats by Season")
    streamlit.text("Coming soon!")

#prompt()
