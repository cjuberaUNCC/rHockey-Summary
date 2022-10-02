import requests
import praw
import auth
import pandas as pd


reddit = praw.Reddit(client_id=auth.reddit_clientId,
                     client_secret=auth.reddit_clientSecret,
                     username=auth.username,
                     password=auth.password,
                     user_agent='rHockeyBot by Charlie v1.0')


subbreddit = reddit.subreddit('charliestestreddit')

for comment in subbreddit.stream.comments(skip_existing=True):
    if hasattr(comment, "body"):
        comment_lower = comment.body.lower()
        if "_/summarize" in comment_lower:
            comment_to_reply_to = comment
            thread = comment.submission

            with open('/Users/charlie/Programing/rHockey_Summary/NHL_player_career_stats.csv', 'r') as csv_file:
                data = pd.read_csv(csv_file)
                data["mentions"] = 0
                data["score"] = 0
                for comment in thread.comments.list():
                    lower = comment.body.lower()
                    score = comment.score

                    for index, row in data.iterrows():
                        if row['fullName'].lower() in lower:
                            data["mentions"].iloc[index] += 1
                            data["score"].iloc[index] += score
                            print(data["mentions"].iloc[index])
                mentioned_players = data.loc[data["mentions"] > 0]
                mentioned_players.sort_values(by='mentions', ascending=False, inplace=True)
                comment_to_reply_to.reply(body=
                    f"""Player | Metions | Upvotes
                ---|---|----
                {mentioned_players['fullName'].iloc[0]} | {mentioned_players['mentions'].iloc[0]} | {mentioned_players['score'].iloc[0]}
                {mentioned_players['fullName'].iloc[1]} | {mentioned_players['mentions'].iloc[1]} | {mentioned_players['score'].iloc[1]}
                {mentioned_players['fullName'].iloc[2]} | {mentioned_players['mentions'].iloc[2]} | {mentioned_players['score'].iloc[2]}
                {mentioned_players['fullName'].iloc[3]} | {mentioned_players['mentions'].iloc[3]} | {mentioned_players['score'].iloc[3]}
                {mentioned_players['fullName'].iloc[4]} | {mentioned_players['mentions'].iloc[4]} | {mentioned_players['score'].iloc[4]}""")
# class HockeyBot:
#     def __init__(self):
#         pass

#     def grab_thread(comment):

#         return comment.submission 

#     def mentioned_players(self, thread):
#         with open('NHL_players_careers_stats', 'r') as csv_file:
#             data = pd.read_csv(csv_file)

#             for comment in thread.comments.list():
#                 comment_number += 1

#                 lower = comment.body.lower()
#                 score = comment.score

#                 for key, value in data.items():
#                     if key.lower() in lower:
#                         value["mentions"] += 1
#                         value["score"] += score
#                         print(key)


#     def reply_summary(self, thread_summary):
#         pass