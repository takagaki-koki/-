# ターミナルで
# pip install janome
# をインストールしてください


# コメントファイルを読み込む
# 指定された品詞の各単語の出現回数を数える
# 上位20個（可変）の単語と出現回数・割合をtxtとして保存する
# この時日本語が一文字も含まれていないコメント・数字は除外する
# また、除外したい単語や、逆に残したい数字の指定も可能


import re
from janome.tokenizer import Tokenizer
from collections import Counter
from pathlib import Path

# 読み込む元のファイル名（変更可能）
input_path = Path(r"C:\Users\adadb\Desktop\卒業研究\ダイダイダイダイダイキライ\youtube_comments.txt")
# ↑()内r以下""でtxtの絶対パス

# コメントファイルを読み込み
with input_path.open(encoding="utf-8")as f:
  lines = f.readlines()

# 外国語コメントの除去
# 日本語（ひらがな・カタカナ・漢字）を1文字以上含むものだけ残す
japanese_only_lines = [line.strip()for line in lines if re.search(r'[\u3040-\u30FF\u4E00-\u9FFF]', line)]

# 1つのテキストにまとめる
text = '\n'.join(japanese_only_lines)

# 特定の単語（「100万再生おめでとう！」の「万再生」みたいなの）を消去
# 変更可能
text = re.sub(r'\d+(万)?(回|再生|コメント)?', '', text)

# Janomeで形態素解析
tokenizer = Tokenizer()
words = []

# 品詞を抽出。（変更可能）使える品詞は以下
# 名詞 動詞 形容詞 形容動詞 副詞 連体詞 接続詞 感動詞 助詞 助動詞 記号
for token in tokenizer.tokenize(text):
  part_of_speech = token.part_of_speech.split(',')[0]
  if part_of_speech in ['名詞', '動詞', '形容詞']:
    base = token.base_form 
    # 特定の数字は残してそれ以外の数字は除外
    if base in ['888', '39']: # 残したい数字（変更可能）
      words.append(base)
    elif not re.fullmatch(r'\d+', base): 
      words.append(base)

# 除外ワードのリストを定義（変更可能）
stopwords = {
  ')','(','れる','する','ん','ある','いる','なる','てる','の','こと','これ','それ','あれ',':'
}

# リストのワードを除外
filtered_words = [w for w in words if w not in stopwords]

# 単語の出現頻度をカウント
counter = Counter(filtered_words)

# 出力ファイルを作成（変更可能）
# デフォは｢単語頻度カウント_元のファイル名｣になるようにしてある
output_path = input_path.with_name("単語頻度カウント_" + input_path.name) 

# 結果を書き込み
with output_path.open('w', encoding='utf-8')as f:
  total = sum(counter.values()) # 全単語数を取得
  for word, count in counter.most_common(30):
    ratio = count / total * 100
    f.write(f"{word}\t{count}\t{ratio:.1f}%\n")
                                #.1は有効数字（変更可能）

print(f"単語頻度カウント結果を保存しました: {output_path}")