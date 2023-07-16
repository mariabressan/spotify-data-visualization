import matplotlib.pyplot as plt
import numpy as np
import pickle
from scipy.optimize import curve_fit

file = open('out', 'rb')
out = pickle.load(file)
file.close()

# Plots artists with number of listend over N
def artistsOverN(N):
    x=[]
    y=[]
    for n,a in enumerate(out["aN"]):
        if a > N:
            x.append(out["artists"][n])
            y.append(out["aN"][n])
    plt.bar(x,y)
    plt.subplots_adjust(bottom=0.4)
    plt.ylabel("Number of times played")
    plt.title("Top artists with over "+str(N)+" plays")
    plt.xticks(rotation = 90)
    plt.show()

# Define the exponential decay function
def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

# Plots all artists. You can ask for a poly fit (poly = degree) and/or an exponential fit (exp=True)
def allArtists(poly=0,exp=False):
    y = [elem for index, elem in enumerate(out["aN"]) if (index + 1) % 10 == 0]
    x = range(len(y))
    y.reverse()
    if exp:
        popt, pcov = curve_fit(exponential_decay, x, y)
        a_opt, b_opt, c_opt = popt
        y_fit = exponential_decay(x, a_opt, b_opt, c_opt)
        plt.plot(x, y_fit, label='Exp Fit', color="Green")
    if poly: 
        degree = poly
        coeffs = np.polyfit(x, y, degree)
        y_poly = np.polyval(coeffs, x)
        plt.plot(x, y_poly, label='Poly Fit ('+str(degree)+' deg)', color="Red")
    plt.title("All top artists")
    plt.bar(x,y, label="Data")
    plt.ylabel("Number of times played")
    plt.xticks(np.linspace(1, len(y)+1, 10),np.linspace(0, len(y)*10+10, 10).astype(int))
    plt.legend()
    plt.show()

# Plots top N artists with each song a different color 
def topNArtists(N):
    artists = out["artists"][-N:]
    times_played = out["sN"][-N:]
    colors = []
    for i in range(len(artists)):
        num_songs = len(times_played[i])
        color_range = np.random.rand(num_songs, 3)  # Generate random RGB values
        colors.extend(color_range)
    # Plotting the stacked bar graph
    fig, ax = plt.subplots()
    # Iterate over each artist
    for i in range(len(artists)):
        # Determine the position for the current artist
        x = [i] * len(times_played[i])
        B = []
        for n in range(len(times_played[i])):
            B.append(sum(times_played[i][:n]))
        # Plot the bars for each song of the artist with corresponding colors
        ax.bar(x, times_played[i], bottom=B, color=colors[:len(times_played[i])])
        colors = colors[len(times_played[i]):]  # Remove used colors
    plt.title("Top "+str(N)+" artists, each song is a different color")
    ax.set_ylabel('Number of Times Played')
    ax.set_xticks(range(len(artists)))
    ax.set_xticklabels(artists, rotation=90)
    plt.subplots_adjust(bottom=0.4,left=0.05, right=0.99)
    plt.show()

# Plots top N songs, color-coded by artist
def topNSongs(N):
    col_dict = {}
    for a in set(out["artists_all"][-N:]):
        col_dict[a]= np.random.rand(1,3)
    colors = []
    for a in out["artists_all"][-N:]:
        colors.append(col_dict[a])
    plt.title("Top "+str(N)+" songs, color coded by artist")
    plt.bar(out["songs_all"][-N:],out["sN_all"][-N:],color=colors)
    plt.ylabel("Number of times played")
    plt.xticks(rotation = 90)
    plt.subplots_adjust(bottom=0.4,left=0.05, right=0.99)
    plt.show()

# Top N songs for artist. If N=0 or N>num songs for artist, shows all songs for artist
def topNSongsPerArtist(a,N=0):
    if N==0:
        N = len(out["songs"][out["artists"].index(a)])
        plt.title("All songs by "+a)
    elif N>len(out["songs"][out["artists"].index(a)]):
        print("N too large! showing all songs by artist")
        N = len(out["songs"][out["artists"].index(a)])
        plt.title("All songs by "+a)
    else:
        plt.title("Top "+str(N)+" songs by "+a)
    x = out["songs"][out["artists"].index(a)][-N:]
    y = out["sN"][out["artists"].index(a)][-N:]
    plt.bar(x,y)
    plt.ylabel("Number of times played")
    plt.xticks(rotation = 90)
    plt.subplots_adjust(bottom=0.4)
    plt.show()

#  N top songs, sorted by time
def topNSongsT(N):
    out_tmp = {}
    for key in out.keys():
        out_tmp[key] = list(out[key])
    out_tmp["sT_all"], out_tmp["songs_all"], out_tmp["artists_all"]= zip(*sorted(zip(out_tmp["sT_all"], out_tmp["songs_all"], out_tmp["artists_all"])))
    col_dict = {}
    for a in set(out_tmp["artists_all"][-N:]):
        col_dict[a]= np.random.rand(1,3)
    colors = []
    for a in out_tmp["artists_all"][-N:]:
        colors.append(col_dict[a])
    x = out_tmp["songs_all"][-N:]
    y = np.array(out_tmp["sT_all"][-N:])/3600000
    plt.bar(x,y,color=colors)
    plt.ylabel("Hours listened")
    plt.title("Top "+str(N)+" songs, sorted by time")
    plt.xticks(rotation = 90)
    plt.subplots_adjust(bottom=0.4)
    plt.show()

# Top N artists sorted by time 
def topNArtistsT(N):
    out_tmp = {}
    for key in out.keys():
        out_tmp[key] = list(out[key])
    for i in range(len(out_tmp["artists"])):
        out_tmp["sT"][i], out_tmp["sN"][i], out_tmp["songs"][i] = zip(*sorted(zip(out_tmp["sT"][i], out_tmp["sN"][i], out_tmp["songs"][i])))
    out_tmp["aT"], out_tmp["artists"], out_tmp["sT"]= zip(*sorted(zip(out_tmp["aT"], out_tmp["artists"], out_tmp["sT"])))
    artists = out_tmp["artists"][-N:]
    times_played =list(out_tmp["sT"][-N:])
    for n,l in enumerate(times_played):
        times_played[n] = np.array(l)/3600000
    colors = []
    for i in range(len(artists)):
        num_songs = len(times_played[i])
        color_range = np.random.rand(num_songs, 3)  # Generate random RGB values
        colors.extend(color_range)
    # Plotting the stacked bar graph
    fig, ax = plt.subplots()
    # Iterate over each artist
    for i in range(len(artists)):
        # Determine the position for the current artist
        x = [i] * len(times_played[i])
        B = []
        for n in range(len(times_played[i])):
            B.append(sum(times_played[i][:n]))
        # Plot the bars for each song of the artist with corresponding colors
        ax.bar(x, times_played[i], bottom=B, color=colors[:len(times_played[i])])
        colors = colors[len(times_played[i]):]  # Remove used colors
    ax.set_ylabel('Hours listened')
    ax.set_xticks(range(len(artists)))
    ax.set_xticklabels(artists, rotation=90)
    plt.title("Top "+str(N)+" artists, each song is a different color")
    plt.subplots_adjust(bottom=0.4,left=0.05, right=0.99)
    plt.show()