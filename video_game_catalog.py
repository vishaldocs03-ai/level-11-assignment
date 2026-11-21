# Level 11 Assignment - Video Game Catalog Manager
# IS 303
# Reads the video game csv, lets the user change a status, marks which games
# are recommended and then saves everything to a new file

import pandas as pd

# read in the raw file
dfGames = pd.read_csv("video_games_raw.csv")

print("VIDEO GAME CATALOG MANAGER")
print()

# ask which row they want to look at
iRow = int(input("Enter a row number to inspect: "))

# make sure the row is actually in the file, keep asking if not
iTotalRows = len(dfGames)
while iRow < 0 or iRow >= iTotalRows:
    print("That row does not exist. Pick a number from 0 to " + str(iTotalRows - 1))
    iRow = int(input("Enter a row number to inspect: "))

# grab the row by its position
selectedGame = dfGames.iloc[iRow]

sTitle = selectedGame["Title"]
sPlatform = selectedGame["Platform"]
sGenre = selectedGame["Genre"]
fRating = selectedGame["Rating"]
sStatus = selectedGame["Status"]

print()
print("Selected Game:")
print("Title: " + str(sTitle))
print("Platform: " + str(sPlatform))
print("Genre: " + str(sGenre))
print("Rating: " + str(fRating))
print("Current Status: " + str(sStatus))
print()

# get the new status from the user
print("Enter a new status:")
sNewStatus = input()
sNewStatus = sNewStatus.strip()
sNewStatus = sNewStatus.title()

# if they just hit enter then leave the status how it was
if sNewStatus == "":
    sNewStatus = sStatus

# .at needs the index label, not the position, so get the label for that row
rowLabel = dfGames.index[iRow]
dfGames.at[rowLabel, "Status"] = sNewStatus

# add the Recommended column, start everything out blank
dfGames["Recommended"] = ""

# Yes if the rating is 8 or higher AND the price is 40 or under
dfGames.loc[(dfGames["Rating"] >= 8) & (dfGames["Price"] <= 40), "Recommended"] = "Yes"

# everything else gets a No
dfGames.loc[(dfGames["Rating"] < 8) | (dfGames["Price"] > 40), "Recommended"] = "No"

# anything still blank (like a missing rating or price) should be No too
dfGames.loc[dfGames["Recommended"] == "", "Recommended"] = "No"

# show only the recommended ones
dfRecommended = dfGames.query("Recommended == 'Yes'")

print()
print("Recommended Games:")
print(dfRecommended[["Title", "Platform", "Price", "Rating"]])
print()

# save to a new file so the original one doesn't get changed
dfGames.to_csv("video_games_cleaned.csv", index=False)

print("The catalog has been updated.")
print("Saved as video_games_cleaned.csv.")
