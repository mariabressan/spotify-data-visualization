import pandas as pd
import pickle
import time
import glob

minSecs = 5 # min number of miliseconds to be considered a play
FileDir = "extended_data"

start = time.perf_counter()
outName = 'out_'+str(minSecs)
StreamingHistoryFileNames = glob.glob(FileDir+"/Streaming_History_Audio_*.json")
dfs = [pd.read_json(x) for x in StreamingHistoryFileNames]

out = {"artists":[],"aN":[],"aT":[],"songs":[],"sN":[],"sT":[],"artists_all":[],"songs_all":[],"sN_all":[],"sT_all":[]}
keyArtistName = "master_metadata_album_artist_name"
keySongName = "master_metadata_track_name"
keyMsPlayed = "ms_played"
minT = minSecs*1000
for df in dfs:
    for i,a in enumerate(df[keyArtistName]):   
        T = df[keyMsPlayed][i]
        if T > minT and a != None:
            s = df[keySongName][i]
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

file = open(outName, 'wb')
pickle.dump(out, file)
file.close()

end = time.perf_counter()
print("saved "+outName)
print('pickle_dict.py took',end-start,"s")