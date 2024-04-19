import yaml
import anthropic
import os
from dotenv import load_dotenv
from graphviz import Digraph

load_dotenv()
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")


def generate_dialogue(transcript):
    """
    文字起こし情報から対談の内容を作成する関数
    Args:
        transcript (str): 文字起こし情報
    Returns:
        str: 対談の内容
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)
    prompt = f"""
    以下の文字起こし情報から対談の内容を作成してください。
    対談の内容はyaml形式で出力してください。
    文字起こし情報: {transcript}
    以下を例として（人物A、人物B、テーマXなど考えて記述）
    - 人物A:
    - 人物B:
    - テーマX:
    """
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    )
    dialogue_yaml = response.content[0].text.strip()
    dialogue_yaml = dialogue_yaml.replace("```yaml", "").replace("```", "")
    return dialogue_yaml


def generate_dialogue_graph():
    """
    dialogueの内容からグラフを生成する関数
    Args:
        dialogue (dict): dialogueの内容が入った辞書
    Returns:
        None
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)
    with open("./dialogue.yaml", "r") as file:
        dialogue = file.read()
    prompt = f"""
    dialogue: {dialogue}
    上記の対談から、
    以下のPythonコードを生成してください。
    以下の「人物A」、「人物B」、「テーマX」に関してはyamlファイルを見て適宜変える
    # dialogueデータの作成（型：dict）
    # Graphvizを使ってグラフを作成。コメントに'Dialogue Graph'を指定。
    # 人物Aと人物Bのノードを作成。ノード形状は楕円形、塗りつぶしあり、水色の背景色を指定。
    # テーマXのノードを作成。ノード形状は長方形、塗りつぶしあり、黄色の背景色を指定。
    # 人物Aと人物BのノードをテーマXのノードに接続。
    # グラフの保存と表示
    # グラフを'dialogue_graph.png'という名前で保存し、表示する
    pythonのコードブロックのみ出力。その他説明は書かないこと。
    """
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    )
    code = response.content[0].text.strip()
    code = code.replace("```python", "").replace("```", "")
    with open("generate_dialogue_graph.py", "w") as f:
        f.write(code)
    exec(code)


from tqdm import tqdm
import time

steps = [
    "📜 文字起こしデータの読み込み",
    "💬 対談の生成",
    "💾 対談のテキストファイルへの保存",
    "📂 ファイル名変更",
    "📊 対談からグラフの生成",
]

for step in tqdm(steps):
    if step == "📜 文字起こしデータの読み込み":
        with open("./transcript.txt", "r") as f:
            transcript = f.read()
        print(f"{step}完了！")
    elif step == "💬 対談の生成":
        dialogue = generate_dialogue(transcript)
        print(f"{step}完了！")
    elif step == "💾 対談のテキストファイルへの保存":
        with open("dialogue.txt", "w") as f:
            f.write(dialogue)
        print(f"{step}完了！")
    elif step == "📂 ファイル名変更":
        os.rename("dialogue.txt", "dialogue.yaml")
        print(f"{step}完了！")
    elif step == "📊 対談からグラフの生成":
        generate_dialogue_graph()
        print(f"{step}完了！")
    time.sleep(0.5)

print(
    "✏️ 対談の内容は dialogue.yaml を書き換えることで、ご自身の求めている形に変更できます。"
)
print("📜 dialogue.yamlのリンク: ./dialogue.yaml")
