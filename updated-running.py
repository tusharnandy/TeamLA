def knn(dataframe, k, history, gross_history):

    avg_coordinates = []
    for dim in space:
        avg = 0
        for p in history:
            avg += dataframe.loc[dataframe["Song Name"] == p, dim].values[0]
        avg /= len(history)
        avg_coordinates.append(avg)

    list = dataframe["Song Name"].values.tolist()
    for now in gross_history:
      list.remove(now)
    if song1 and command != "skip-next":
      list.remove(song1)

    upcoming = []

    for j in range(k):

        nextsong = ''
        min = 10**8

        for next in list:
            dist = 0

            for dim in range(len(space)):
                dist += (dataframe.loc[dataframe["Song Name"] == next, space[dim]].values[0] - avg_coordinates[dim]) ** 2

            dist = np.sqrt(dist)
            if dist < min:
                min = dist
                nextsong = next

        list.remove(nextsong)
        upcoming.append(nextsong)

    return upcoming

def farthest(dataframe, k, history):

    avg_coordinates = []
    for dim in space:
        avg = 0
        for p in history:
            avg += dataframe.loc[dataframe["Song Name"] == p, dim].values[0]
        avg /= len(history)
        avg_coordinates.append(avg)

    list = dataframe["Song Name"].values.tolist()
    for now in gross_history:
      list.remove(now)
    if song1:
      list.remove(song1)

    nextsong = ''
    max = 0

    for next in list:
        dist = 0
        for dim in range(len(space)):
            dist += (dataframe.loc[dataframe["Song Name"] == next, space[dim]].values[0] - avg_coordinates[dim]) ** 2
        dist = np.sqrt(dist)
        if dist >max :
            min = dist
            nextsong = next

    return nextsong






def mood_of_user(dataframe,history):

    avg_mood = []
    for dim in df.columns.tolist()[2:5]:
        avg = 0
        for p in history:
            avg += dataframe.loc[dataframe["Song Name"] == p, dim].values[0]
        avg /= len(history)
        avg_mood.append(avg)


    moods = df.columns.tolist()[2:5]
    mood = moods[0]
    for i in range(1, 3):
        if avg_mood[0] < avg_mood[i]:
            mood = moods[i]
    return mood

def wrong_recom(df,song_num, mood,rejection_score):
    if rejection_score[song_num] == 0 and df[mood][song_num] != 0:
            df[mood][song_num] -= 0.5
    elif df[mood][song_num] != 0:
        rejection_score[song_num] += 1
        p= rejection_score[song_num]
        if p < 2 :
            df[mood][song_num] -= (p*0.5)**(1/3)
        else:
            df[mood][song_num] -= (p*0.5)**(1.5)



import pandas as pd
import numpy as np

path = "Songs_LA - Sheet1.csv"
database = pd.read_csv(path)


space = database.columns.tolist()[2:]
space.pop(3)

df = database

print('''WElCOME...!!!''')

current_song = input("\nPlease type your first song: ")


rejection_score = [0]*60
recent_history = [current_song]
gross_history = [current_song]
wrong_predictions = 0
total_predictions=2
dislikes=0

song1 = ''
song2 = ''
song1, song2 = knn(df, 2, recent_history, gross_history)

while True:

    print(f'''\nCurrently playing: {current_song}
            Upcoming song:{song1}, {song2}\n''')

    command = input("Type command here: ").lower()

    if command == "next":
        dislikes=0
        total_predictions+=1
        current_song = song1
        song1 = song2

        if len(recent_history) < 15:
            recent_history.append(current_song)
        else:
            recent_history.remove(recent_history[0])
            recent_history.append(current_song)

        if len(gross_history) < 60:
            gross_history.append(current_song)
        else:
            gross_history = [current_song]

        song2 = knn(df, 1, recent_history, gross_history)[0]

    elif command == "skip-next":
        dislikes+=1
        total_predictions+=1
        wrong_predictions+=1
        current_song = song2

        if len(recent_history) < 15:
            recent_history.append(current_song)
        else:
            recent_history.remove(recent_history[0])
            recent_history.append(current_song)

        if len(gross_history) < 60:
            gross_history.append(current_song)
            gross_history.append(song1)
        else:
            gross_history = [current_song]

        for song_num in range (60):
            if current_song == df['Song Name'][song_num]:
                break

        for song1_num in range (60):
            if song1 == df['Song Name'][song1_num]:
                break

        mood= mood_of_user(df, recent_history)
        wrong_recom(df,song1_num,mood,rejection_score)

        song1, song2 = knn(df, 2, recent_history, gross_history)

        if dislikes > 2:
            current_song=farthest(df,1,recent_history, gross_history)
            recent_history = [current_song]
            song1, song2 = knn(df,2,recent_history, gross_history)


    elif command == "search":
        dislikes=0
        total_predictions+=2
        wrong_predictions+=2
        print('Choose the song you wish to play: ')
        print(df['Song Name'])
        current_song = input("What would you like to hear? ")

        # code for negative marking
        for song_num in range (60):
            if current_song == df['Song Name'][song_num]:
                break

        for song1_num in range (60):
            if song1 == df['Song Name'][song1_num]:
                break

        for song2_num in range (60):
            if song2 == df['Song Name'][song2_num]:
                break

        mood = mood_of_user(df, recent_history)
        wrong_recom(df,song1_num,mood,rejection_score)
        wrong_recom(df,song2_num,mood,rejection_score)

        gross_history = recent_history
        for now in recent_history:
            recent_history.remove(now)

        recent_history.append(current_song)
        song1, song2 = knn(df,2,recent_history, gross_history)


    elif command == "exit":
        accuracy= 1- (wrong_predictions/total_predictions)
        accuracy= accuracy*100
        print(accuracy)
        break
