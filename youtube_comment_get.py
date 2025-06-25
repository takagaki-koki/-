from googleapiclient.discovery import build
import time

# APIキーを入力
api_key = 'AIzaSyCxCO8q5ih0jX2pU6LtMiJn4a-Cm81y5fs'
video_id = 'klIxS5o65C4'# 動画ID

youtube = build('youtube', 'v3', developerKey=api_key)

def get_all_comments(video_id, max_total=None):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat='plainText'
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if max_total and len(comments) >= max_total:
            break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

        time.sleep(1)

    return comments[:max_total] if max_total else comments


# 実行
comments = get_all_comments(video_id)

# 保存するファイル名
# (パス\卒業研究\曲名_youtube_comments.txt)
with open(r'C:\Users\adadb\Desktop\卒業研究\ダイダイダイダイダイキライ_youtube_comments.txt', 'w', encoding='utf-8') as f:
    for c in comments:
        f.write(c.replace('\n', ' ') + '\n')

print(f"{len(comments)} 件のコメントを保存しました。")