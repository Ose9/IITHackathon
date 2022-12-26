### Custom definitions and classes if any ###

def predictRuns(testInput):
    prediction = 0
    
    import pandas as pd
    test=pd.read_csv(testInput)
    batting_team  = test['batting_team']
    bowling_team  = test['bowling_team']
    print("bat :", batting_team)
    import os
    cwd = os.getcwd()
    iplsub = os.path.join(cwd,r"all_matches.csv")
    df = pd.read_csv(iplsub)
    df['total_runs'] = df['runs_off_bat'] + df['extras']
    df1 = df
    df1 = df[df['ball'] < 6.0]
    df1 = df1.groupby(['season','start_date','venue', 'innings', 'batting_team', 'bowling_team']).agg(total_runs = ('total_runs','sum'), wickets = ('wicket_type', 'count'),).reset_index()
    df = df[df['innings'] < 3]
    

    def past(batting_team, bowling_team):
      df2 = df1[df1['batting_team'].isin(batting_team)]
      df2 = df2[df2['bowling_team'].isin(bowling_team)]
      df2 = df2.tail(5)
      avg1 = (df2['total_runs'].sum())/5
      print ("Average score of 6 overs in past five matches : ",avg1)
      return avg1
    
    
    def batsman(batting_team):      
      df6 = df[df['season'] == '2021']
      df6 = df6[df6['batting_team'].isin(batting_team)]
      striker = df6['striker'] 
      striker = list(set(striker))
      runs = { }
      for st in striker:
        runs[st] = 0
      a = 0
      for st in striker:
        df7 = df6[df6['striker'] == st]
        balls = df7['ball'].count()
        runs[st] = df7['runs_off_bat'].sum()
        runs[st] /= balls      
        a += runs[st] 
      return (a*36/len(striker))

    def bowling(bowling_team):      
      df6 = df[df['season'] == '2021']
      df6 = df6[df6['bowling_team'].isin(bowling_team)]
      bowler = df6['bowler'] 
      bowler = list(set(bowler))   
      runs = { }
      for st in bowler:
        runs[st] = 0
      a = 0
      for st in bowler:
        df7 = df6[df6['bowler'] == st]
        balls = df7['ball'].count()
        runs[st] = df7['total_runs'].sum()
        runs[st] /= balls      
        a += runs[st] 
      return (a*36/len(bowler))           
           
      #bat = df6.groupby(['striker','runs_off_bat'])
      #ball = df6.groupby(['ball'])
      #print(bat)
      #strike rate (100 balls run) = striker 1
      #mean(player.strikerate)
      #120.45 for 100 balls 
      #mean/100 * 6

    stadium = test['venue']
    df4 = df1[df1['venue'].isin(stadium)]
    df5 = df4.tail(5)
    avg2 = df5['total_runs'].sum()/5
    print ("Average of past matches for ", stadium ," is: ", avg2)
 
   
    print ("\nFirst Innings : \nBatting team : ", batting_team, "\nBowling team :", bowling_team,"\n")
    prediction = int((past(batting_team, bowling_team) + avg2 + batsman(batting_team) + bowling(bowling_team))/4) 
    
    return prediction