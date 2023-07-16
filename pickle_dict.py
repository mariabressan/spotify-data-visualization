import pandas as pd
import pickle

# Keys: Index(['endTime', 'artistName', 'trackName', 'msPlayed'], dtype='object')

StreamingHistoryFileNames = ['StreamingHistory0.json','StreamingHistory1.json','StreamingHistory2.json','StreamingHistory3.json']

dfs = [pd.read_json(x) for x in StreamingHistoryFileNames]
out = {"artists":[],"aN":[],"aT":[],"songs":[],"sN":[],"sT":[],"artists_all":[],"songs_all":[],"sN_all":[],"sT_all":[]}

for df in dfs:
    for i,a in enumerate(df["artistName"]):   
        s = df["trackName"][i]
        T = df["msPlayed"][i]
        if a not in out["artists"]:
            out["artists"].append(a)
            out["aT"].append(T)
            out["aN"].append(1)
            out["songs"].append([s])
            out["sN"].append([1])
            out["sT"].append([T])
        elif s not in out["songs"][out["artists"].index(a)]:
            out["songs"][out["artists"].index(a)].append(s)
            out["sN"][out["artists"].index(a)].append(1)
            out["sT"][out["artists"].index(a)].append(T)
            out["aN"][out["artists"].index(a)]+=1
            out["aT"][out["artists"].index(a)]+=T
        else:
            out["sN"][out["artists"].index(a)][out["songs"][out["artists"].index(a)].index(s)]+=1
            out["sT"][out["artists"].index(a)][out["songs"][out["artists"].index(a)].index(s)]+=T
            out["aN"][out["artists"].index(a)]+=1
            out["aT"][out["artists"].index(a)]+=T
        if s not in out["songs_all"]:
            out["songs_all"].append(s)
            out["artists_all"].append(a)
            out["sN_all"].append(1)
            out["sT_all"].append(T)
        else:
            out["sN_all"][out["songs_all"].index(s)]+=1
            out["sT_all"][out["songs_all"].index(s)]+=T

for i in range(len(out["artists"])):
    out["sN"][i], out["sT"][i], out["songs"][i] = zip(*sorted(zip(out["sN"][i], out["sT"][i], out["songs"][i])))
out["aN"], out["aT"], out["artists"], out["sN"], out["sT"], out["songs"] = zip(*sorted(zip(out["aN"], out["aT"], out["artists"], out["sN"], out["sT"], out["songs"])))
out["sN_all"], out["sT_all"], out["songs_all"], out["artists_all"] = zip(*sorted(zip(out["sN_all"], out["sT_all"], out["songs_all"], out["artists_all"])))

file = open('out', 'wb')
pickle.dump(out, file)
file.close()

