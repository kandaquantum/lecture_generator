import os
import yaml
import anthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()  # .envファイルから環境変数を読み込む


class DialogueGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")  # 環境変数からAPI keyを取得
        )

    def generate_dialogue_content(self, person_a, person_b, theme_x):
        with open("ais/dialogue_generator.md", "r") as f:
            prompt = f.read().format(
                person_a=person_a, person_b=person_b, theme_x=theme_x
            )

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )

        return response.content[0].text.strip()


class ImpressionGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")  # 環境変数からAPI keyを取得
        )

    def generate_impression_content(self, dialogue_content, person_a, person_b):
        with open("ais/impression_generator.md", "r") as f:
            prompt = f.read().format(
                dialogue_content=dialogue_content, person_a=person_a, person_b=person_b
            )

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0.5,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )

        return response.content[0].text.strip()


def main():
    # aisディレクトリがなければ作成
    os.makedirs("ais", exist_ok=True)

    # h2のドキュメントを記述
    with open("ais/dialogue_generator.md", "w") as f:
        f.write(
            """
## 💬 対談生成AI

人物A、人物B、テーマXから、対談の内容を生成するAI

<details>
<summary>🎯 入力</summary>

- 人物A (テキスト): {person_a}
- 人物B (テキスト): {person_b}
- 対談のテーマX (テキスト): {theme_x}

</details>

<details>
<summary>📚 出力</summary>

- md形式の対談内容 (テキスト)
  - 人物A:「〇〇〇」
  - 人物B:「△△△」
  - ...

</details>

<details>
<summary>🛠️ 処理</summary>

以下の構成で、人物A、人物B、テーマXから、自然な対談の流れを生成します。各人物の発言は、その人物の知識や立場、個性を反映したものにします。

1. 📝 対談の導入（200文字程度）
   - テーマXについて、人物Aと人物Bが対談を始める様子を描写します。
   - 対談の目的や背景などを簡潔に説明します。

2. 💬 対談の本編（10回の発言、各200文字程度）
   - 人物Aと人物Bが交互に発言します。各発言は200文字程度とします。
   - 発言内容は、テーマXについての各人物の意見、経験、考えなどを自然な会話の流れで表現します。
   - 各発言は、前の発言を受けて展開するようにし、対話的な印象を与えます。

3. 📋 対談のまとめ（200文字程度）
   - 対談の内容を振り返り、重要なポイントや結論をまとめます。
   - 今後の展望や、対談を通じて得られた新しい視点などにも触れます。

</details>

<details>
<summary>✅ テスト</summary>

- [ ] 人物Aと人物Bの発言が交互に表示されているか
- [ ] 各発言が200文字程度に収まっているか
- [ ] 対談の導入とまとめが適切に記載されているか
- [ ] テーマXについての意見や考えが自然な会話の流れで表現されているか

</details>
""".strip()
        )

    with open("ais/impression_generator.md", "w") as f:
        f.write(
            """
## 💭 感想生成AI

対談内容から、人物Aの感想を生成するAI

<details>
<summary>🎯 入力</summary>

- 対談内容 (テキスト): {dialogue_content}

</details>

<details>
<summary>📝 出力</summary>

- md形式の人物Aの感想（500文字程度）

</details>

<details>
<summary>🛠️ 処理</summary>

1. 対談内容を分析し、重要なポイントや印象的な発言を抽出
2. 抽出した内容をもとに、人物Aの立場や個性を反映した感想を生成
   - 対談を通じて得られた新しい気づきや学び
   - 人物Bの発言に対する共感や意見
   - 今後の展望や抱負など
3. 生成した感想を、自然な文章になるように整形

</details>

<details>
<summary>⚠️ 注意</summary>

- 感想は人物Aの視点で書く
- 対談内容を踏まえつつ、人物Aならではの感想になるようにする
- 感想は読み手に伝わりやすい、わかりやすい文章にまとめる

</details>
""".strip()
        )

    # dialogue.yamlを読み込み
    with open("dialogue.yaml", "r") as f:
        dialogues = yaml.safe_load(f)

    dialogue_generator = DialogueGenerator()
    impression_generator = ImpressionGenerator()

    for i, dialogue in enumerate(tqdm(dialogues, desc="Generating dialogues"), start=1):
        print(f"Generating dialogue {i}/{len(dialogues)}...")

        if i < 20:
            continue

        # 対談ごとのフォルダを作成
        dialogue_dir = f"book_dialogue/dialogue_{i}"
        os.makedirs(dialogue_dir, exist_ok=True)

        # テーマごとの対談と感想を生成
        # for theme in tqdm(
        #     dialogue["themes"], desc=f"Generating themes for dialogue {i}"
        # ):

        dialogue = dialogue["対談" + str(i)]
        theme = dialogue["テーマ"]
        person_a = dialogue["登場人物"][0]
        person_b = dialogue["登場人物"][1]

        print(f"Generating theme '{theme}' for dialogue {i}...")

        # 対談を生成
        dialogue_content = dialogue_generator.generate_dialogue_content(
            person_a=person_a,
            person_b=person_b,
            theme_x=theme,
        )

        # 感想を生成
        impression_content = impression_generator.generate_impression_content(
            dialogue_content=dialogue_content,
            person_a=person_a,
            person_b=person_b,
        )

        # テーマのMarkdownファイルを作成
        with open(f"{dialogue_dir}/{theme}.md", "w") as f:
            f.write(f"# {theme}\n\n")
            f.write(f"## 対談\n\n{dialogue_content}\n\n")
            f.write(f"## {person_b}の感想\n\n{impression_content}\n")


if __name__ == "__main__":
    main()
