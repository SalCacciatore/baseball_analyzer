

#pip install pybaseball

import pandas as pd

import streamlit

import random

from pybaseball import batting_stats,pitching_stats,team_batting,team_pitching

import numpy as np

from plotly import graph_objects as go

from IPython.display import display

ind_bat = batting_stats(2022)

qual_batters = ind_bat[['Name','Team','PA','K%','BB%','ISO','BABIP','AVG','OBP','SLG','HR','wRC+','O-Swing%','Z-Contact%','Z-Swing%','O-Contact%','SwStr%','Barrel%','EV','HardHit%','LD%']]

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


k_median = qual_batters['K%'].median()

bb_median = qual_batters['BB%'].median()

iso_median = qual_batters['ISO'].median()

babip_median = qual_batters['BABIP'].median()

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

all_batters['WAR/600'] = round(all_batters['WAR']/all_batters['PA']*600,1)


Yanks = all_batters[all_batters['Team']=='NYY'].sort_values('WAR',ascending=False).drop(['Team','Pull%+','EV'],axis=1).set_index('Name')

#Yanks

#today_lineup = pd.DataFrame()
#lineup_list = ['Luis Arraez','Byron Buxton','Jorge Polanco','Max Kepler','Gary Sanchez','Trevor Larnach','Gio Urshela','Gillberto Celestino','Jermaine Palacios']
#today_lineup['Name'] =lineup_list

#today_lineup.merge(all_batters,on='Name').drop(['Team','Pull%+','O-Contact%+','EV'],axis=1).set_index('Name')


hitter_proj = pd.read_csv('Steamer_hitters.csv')

hitter_proj['K%'] = hitter_proj['SO']/hitter_proj['PA']
hitter_proj['BB%'] = hitter_proj['BB']/hitter_proj['PA']
hitter_proj['ISO'] = hitter_proj['SLG'] - hitter_proj['AVG']
hitter_proj['BABIP'] = (hitter_proj['H'] - hitter_proj['HR'])/(hitter_proj['AB']-hitter_proj['SO']-hitter_proj['HR'])
hitter_proj['WAR/600'] = round(hitter_proj['WAR']/hitter_proj['PA']*600,1)
hitter_proj['K%+'] = round(hitter_proj['K%']/k_median,2)*100
hitter_proj['K%+'] = 100+(100 - hitter_proj['K%+'])
hitter_proj['BB%+'] = round(hitter_proj['BB%']/bb_median,2)*100
hitter_proj['BABIP+'] = round(hitter_proj['BABIP']/babip_median,2)*100
hitter_proj['ISO+'] = round(hitter_proj['ISO']/iso_median,2)*100





hitter_proj = hitter_proj[['Name','Team','PA','OBP','SLG','wRC+','WAR','WAR/600','K%+','BB%+','ISO+','BABIP+']]
hitter_proj['Name']=hitter_proj['Name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')





def create_scatter(answer):
  categories = all_batters[['BB%+','K%+','SwStr%+','Z-Contact%+','O-Contact%+','O-Swing%+','Z-Swing%+','EV+','HH%+','Barrel%+','LD%+','FB%+','ISO+','BABIP+']].columns
  avg_list = []
  for cat in categories:
    avg_list.append(100)
  avg_list.append(100)

  player_chart=all_batters.loc[all_batters['Name']==answer]

  gran_chart = player_chart[['Name','SwStr%+','Z-Contact%+','O-Contact%+','O-Swing%+','Z-Swing%+','EV+','HH%+','Barrel%+','LD%+','FB%+']]

  projected_chart=hitter_proj[hitter_proj['Name']==answer]
  #projected_chart = projected_chart.merge(gran_chart,on='Name')
  p_categories = ['K%+','BB%+','ISO+','BABIP+']


  stats = []
  p_stats = []
  for x in categories:
    stats.append(player_chart[x].item())

  for x in p_categories:
    p_stats.append(projected_chart[x].item())



  fig = go.Figure()

  fig.add_trace(go.Scatterpolar(
      r=stats,
      theta=categories,
      fill='toself',
      name=answer+" (YTD)"))

  fig.add_trace(go.Scatterpolar(
      r=avg_list,
      theta=categories,
      #fill='toself',
      name='MLB Average'))

  fig.add_trace(go.Scatterpolar(
      r=p_stats,
      theta=p_categories,
      fill='toself',
      name='Steamer Projection'))

      # + YTD Swing/BB Data'))


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
    df_show = all_batters[all_batters['Name']==answer][['Name','Team','PA',	'OBP', 'SLG',	'wRC+',	'WAR','WAR/600','K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']].set_index('Name')
    #df_show.rename(index={answer: 'Year-to-date'},inplace=True)
    streamlit.write("Year-to-date stats")
    streamlit.write(df_show)
    proj_show = hitter_proj[hitter_proj['Name']==answer].set_index('Name')
    proj_show.rename(index={answer: 'Steamer'},inplace=True)
    streamlit.write("Rest-of-season projections")
    streamlit.write(proj_show)
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
  all_batters['WAR/600'] = round(all_batters['WAR']/all_batters['PA']*600,1)
  return all_batters

def player_szn_finder(player,year):
  all_batters = season_definer(year)
  if player not in all_batters['Name'].values:
    streamlit.text("{} had no plate appearances in {}.".format(player,year))
  else:
    all_batters['Season'] = year
    df = all_batters[all_batters['Name']==player].set_index('Name')
    display_df = df[['Season','Team','PA',	'OBP', 'SLG',	'wRC+',	'WAR', 'WAR/600', 'K%+',	'BB%+',	'ISO+',	'BABIP+',	'GB%+',	'LD%+',	'FB%+', 'Barrel%+']]
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


all_pitchers = pitching_stats(2022,qual=1)
qual_pitch = pitching_stats(2022)

K_9_median = (all_pitchers['SO'].sum()/all_pitchers['IP'].sum())*9

BB_9_median = (all_pitchers['BB'].sum()/all_pitchers['IP'].sum())*9

p_chase_median = qual_pitch['O-Swing%'].median()

p_z_contact_median = qual_pitch['Z-Contact%'].median()

p_z_swing_median = qual_pitch['Z-Swing%'].median()

p_o_contact_median = qual_pitch['O-Contact%'].median()

p_swstr_median = qual_pitch['SwStr%'].median()

p_barrel_median = qual_pitch['Barrel%'].median()

p_EV_median = qual_pitch['EV'].median()

p_hard_hit_median = qual_pitch['HardHit%'].median()




all_pitchers['O-Swing%+'] = round(all_pitchers['O-Swing%']/p_chase_median,2)*100
all_pitchers['O-Contact%+'] = (1 - round(all_pitchers['O-Contact%']/p_o_contact_median,2))*100 + 100
all_pitchers['Z-Contact%+'] = (1 - round(all_pitchers['Z-Contact%']/p_z_contact_median,2))*100 + 100
all_pitchers['Z-Swing%+'] = (1 - round(all_pitchers['Z-Swing%']/p_z_swing_median,2))*100 + 100
all_pitchers['SwStr%+'] = round(all_pitchers['SwStr%']/p_swstr_median,2)*100

all_pitchers['HH%+'] = (1 - round(all_pitchers['HardHit%']/p_hard_hit_median,2))*100 +100
all_pitchers['EV+'] = (1 - round(all_pitchers['EV']/p_EV_median,2))*100+100
all_pitchers['Barrel%+'] = (1-round(all_pitchers['Barrel%']/p_barrel_median,2))*100+100

all_pitchers['ERA+'] = 100 - all_pitchers['ERA-'] + 100
all_pitchers['FIP+'] = 100 - all_pitchers['FIP-'] + 100
all_pitchers['xFIP+'] = 100 - all_pitchers['xFIP-'] + 100
all_pitchers['BB%+'] = 100 - all_pitchers['BB%+'] + 100
all_pitchers['BABIP+'] = 100 - all_pitchers['BABIP+'] + 100
all_pitchers['HR/FB%+'] = 100 - all_pitchers['HR/FB%+'] + 100
all_pitchers['WAR/150'] = all_pitchers['WAR']/all_pitchers['IP']*150


pitcher_proj = pd.read_csv('Steamer_pitchers.csv')



pitcher_proj['K/9+'] = round(pitcher_proj['K/9']/K_9_median,2)*100
pitcher_proj['BB/9+'] = round(pitcher_proj['BB/9']/BB_9_median,2)*100
pitcher_proj['BB/9+'] = 100+(100 - pitcher_proj['BB/9+'])

pitcher_proj['WAR/150'] = pitcher_proj['WAR']/pitcher_proj['IP']*150

pitcher_proj = pitcher_proj[['Name','Team','G','GS','IP','WAR','WAR/150','ERA','K/9+','BB/9+']]




#Team Ranks

def team_stats(year,team):
    df = team_batting(year)[['Team','WAR','wRC+','R','OBP','SLG','ISO','K%','BB%','BABIP','FB%','LD%','Barrel%','EV','HardHit%','Def']]
    df['K%'] = df['K%'] * -1
    for x in df.columns[1:]:
        df[x] = df[x].rank(ascending=0)
        df[x] = df[x].astype(int)
    df = df[df['Team']==team]
    df['Team'] = 'Hitters'
    df.set_index('Team',inplace=True)
    return df

def squad_pitching(year,team):
    low_is_good = ['ERA-','FIP-','xFIP-','BB%','HR%','HR/FB','BABIP','Barrel%']
    df = team_pitching(year)
    df['HR%'] = df['HR']/df['TBF']
    df = df[['Team','WAR','Starting','Relieving','Start-IP','ERA-','FIP-','xFIP-','K-BB%','K%','BB%','GB%','HR%','HR/FB','LOB%','BABIP','Barrel%']]
    for stat in low_is_good:
        df[stat] = df[stat]*-1
    for x in df.columns[1:]:
        df[x] = df[x].rank(ascending=0)
        df[x] = df[x].astype(int)
    df = df[df['Team']==team]
    df['Team'] = 'Pitchers'
    df.set_index('Team',inplace=True)
    return df



def pitcher_query(answer):
  if answer in all_pitchers['Name'].values:
    displ_df = all_pitchers[all_pitchers['Name']==answer][['Name','Team','G','GS','IP','WAR','WAR/150','ERA','ERA+','FIP+','xFIP+','K%+','BB%+','GB%+','BABIP+','HR/FB%+','LOB%+','O-Swing%+','O-Contact%+','Z-Contact%+','Z-Swing%+','SwStr%+','HH%+','EV+','Barrel%+']].set_index('Name')
    streamlit.write("Year-to-date stats")
    streamlit.write(displ_df)
    displ_proj = pitcher_proj[pitcher_proj['Name']==answer]
    displ_proj['Name'] = 'Steamer'
    displ_proj = displ_proj.set_index('Name')
    streamlit.write('Rest-of-season projections')
    streamlit.write(displ_proj)
    pitcher_spider(answer)
  else:
    streamlit.write("{} has not piched this season.".format(answer))

def pitcher_spider(answer):
  categories = all_pitchers[['LOB%+','BABIP+','HR/FB%+','EV+','HH%+','Barrel%+','GB%+','Z-Swing%+','O-Swing%+','Z-Contact%+','O-Contact%+','SwStr%+','K%+','BB%+']].columns

  avg_list = []
  for cat in categories:
    avg_list.append(100)

  avg_list.append(100)

  player_chart=all_pitchers.loc[all_pitchers['Name']==answer]

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

  #fig.show()



header = streamlit.container()
current_szn = streamlit.container()
pitcher_szn = streamlit.container()
roster_szn = streamlit.container()


with header:
    streamlit.title("BASEBALL STAT ANALYZER")
    streamlit.markdown("Get current and historical baseball data from [FanGraphs](https://www.fangraphs.com).")

with current_szn:
    streamlit.header("Batter Season Analyzer")
    sel_col, disp_col = streamlit.columns(2)
    player_prompt = sel_col.selectbox("Look at a batter's stats from this season or past seasons, or compare two individual seasons.",options=["Current","Past","Compare"],index=0)

    if player_prompt == "Current":
        current_form = streamlit.form(key='current_selection')
        what_player = current_form.text_input('What player do you want to learn about?',"Giancarlo Stanton")
        p_submitted = current_form.form_submit_button("Submit")
        if p_submitted:
            baseball_query(what_player)
        with streamlit.form("random"):
            r_submit = streamlit.form_submit_button("Random Player")
            if r_submit:
                random_player = random.choices(all_batters['Name'], k=1)[0]
                baseball_query(random_player)




    if player_prompt == "Past":
        form = streamlit.form(key = "past_selection")
        what_past = form.text_input('What batter do you want to learn about?',"Bernie Williams")
        what_szn = form.text_input("What season?",1998)
            #what_szn = sel_col.slider("What season?",min_value=1871,max_value=2022,value=1998)
        submitted = form.form_submit_button("Submit")
        if submitted:
            if what_szn.isnumeric() == False:
                streamlit.write('Please insert an integer next time.')
            elif int(what_szn) not in range (1871,2023):
                streamlit.write('Invalid year. Please select a year between 1871 and 2022.')
            else:
                streamlit.write("Player: " + str(what_past) + ", " + str(what_szn))
                player_szn_finder(what_past,what_szn)


    if player_prompt == "Compare":
        c_form = streamlit.form(key = 'comparison')
        player1 = c_form.text_input('Who is the first player you want to learn about?',"Mike Trout")
        szn1 = c_form.text_input("What season?",2013)
        player2 = c_form.text_input('Who is the second player you want to learn about?',"Aaron Judge")
        szn2 = c_form.text_input("What season?",2017)
        c_submitted = c_form.form_submit_button("Submit")
        if c_submitted:
            if szn1.isnumeric() == False or szn2.isnumeric() == False:
                streamlit.write('Please insert an integer next time.')
            elif int(szn1) not in range (1871,2023) or int(szn2) not in range (1871,2023):
                streamlit.write('Invalid year. Please select a year between 1871 and 2022.')
            else:
                streamlit.write("Player 1: " + player1 + " ("+str(szn1)+")"+" | Player 2:",player2 +" ("+str(szn2)+")")
                compare_seasons(player1,player2,szn1,szn2)

with current_szn:
    streamlit.header("Pitcher Season Analyzer")
    sel_col, disp_col = streamlit.columns(2)
    pitcher_prompt = sel_col.selectbox("Look at a pitcher's stats from this season or past seasons, or compare two individual seasons.",options=["Current","Past","Compare"],index=0)
    if pitcher_prompt == "Compare":
        streamlit.write('Feature coming soon.')
    if pitcher_prompt == "Past":
                streamlit.write('Feature coming soon.')
    if pitcher_prompt == "Current":
        pitch_form = streamlit.form(key = "pitcher_selection")
        what_pitcher = pitch_form.text_input('What pitcher do you want to learn about?',"Nestor Cortes")
        pi_submitted = pitch_form.form_submit_button("Submit")
        if pi_submitted:
            pitcher_query(what_pitcher)
        with streamlit.form("random_pitcher"):
            rp_submit = streamlit.form_submit_button("Random Pitcher")
            if rp_submit:
                random_pitcher = random.choices(all_pitchers['Name'], k=1)[0]
                pitcher_query(random_pitcher)









    streamlit.header("Player Career Analyzer")
    streamlit.text("Coming soon")

    streamlit.header("fWAR Leaderboards")
    war_form = streamlit.form(key = 'fWAR')
    what_year = war_form.slider("What season?",min_value=1871,max_value=2022,value=2022)
    hit_or_throw = war_form.selectbox("Do you want the hitting leaders or pitching leaders?",options=["Hitters","Pitchers"],index=0)
    war_submitted = war_form.form_submit_button("Submit")
    if war_submitted:
        if hit_or_throw == 'Hitters':
            yr = batting_stats(what_year)
            disp_df = yr[['Name','Team','PA','wRC+','OBP','SLG','HR','ISO','WAR']].head(10)
            streamlit.write("Hitters,",str(what_year))
            streamlit.write(disp_df)
        if hit_or_throw == 'Pitchers':
            yr = pitching_stats(what_year)
            disp_df = yr[['Name','Team','ERA','FIP','xFIP','ERA-','FIP-','xFIP-','K%','BB%','WAR']].head(10)
            streamlit.write("Pitchers,",str(what_year))
            streamlit.write(disp_df)


team_list = all_batters['Team'].unique()

all_pitchers['WAR/150'] = all_pitchers['WAR']/all_pitchers['IP']*150




all_pitchers_show = all_pitchers[['Name','Team','G','GS','IP','WAR','WAR/150','ERA','ERA+','FIP+','xFIP+','K%+','BB%+','GB%+','BABIP+','HR/FB%+','LOB%+','O-Swing%+','O-Contact%+','Z-Contact%+','Z-Swing%+','SwStr%+','HH%+','EV+','Barrel%+']]




with roster_szn:
    streamlit.header("Roster Analyzer")
    with streamlit.form("roster_picker"):
        what_roster = streamlit.selectbox("What roster do you want to look at?",options=team_list,index=0)
        team_submit = streamlit.form_submit_button("Submit")
        if team_submit:
            streamlit.write(team_stats(2022,what_roster))
            streamlit.write(squad_pitching(2022,what_roster))
            df_hitters = all_batters[all_batters['Team']==what_roster].sort_values('WAR',ascending=False).set_index('Name')
            df_pitchers = all_pitchers_show[all_pitchers_show['Team']==what_roster].sort_values('WAR',ascending=False).set_index('Name')
            streamlit.write('Hitters:')
            streamlit.write(df_hitters)
            streamlit.write("Pitchers")
            streamlit.write(df_pitchers)








    streamlit.header("Team Stats by Season")
    streamlit.text("Coming soon!")

#prompt()
