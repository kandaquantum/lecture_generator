# 📚 書籍_対談生成AI
対談生成AIと感想生成AIを使った書籍生成プログラムの仕様

<details>
<summary>📥 入力</summary>

- 対談のYAMLファイル（`dialogue.yaml`）
- 対談の人物A、人物B、テーマXが記載されたYAMLファイル

</details>

<details>
<summary>📤 出力</summary>

- `book_dialogue`ディレクトリ
  - 対談N ディレクトリ
    - テーマ.md

</details>

<details>
<summary>🛠️ 処理の流れ</summary>

1. `dialogue.yaml`を読み込み、対談リスト（辞書型のリスト）を取得 📖
   1. 対談（リストの要素）（辞書型）：
      1. 登場人物（strのリスト、要素数2）人物A(str)、人物B（str））、
      2. テーマ名(str)
      3. 内容(str)
2. 対談毎に`book_dialogue/`の中にディレクトリを作成 📂
3. 各対談のディレクトリについて以下の処理を繰り返す：
   1. テーマ名でMarkdownファイルを作成 📝
   2. 対談生成AIを使って、登場人物、テーマ名から対談を生成（内容をより面白くするか、0から生成） 🤖📚
   3. 感想生成AIを使って、人物Bの対談の感想を生成 🤖💬
   4. 生成された対談と感想をテーマ名のMarkdownファイルに出力 ✍️
   5. テーマの小項目があれば目次として追加 📋
4. 完成した各テーマのMarkdownファイルを`book_dialogue/`の対応するディレクトリに出力 📚

</details>

<details>
<summary>📝 プログラムの構成</summary>

以下のファイルは作成し、記述をする必要があります

- `main.py`
  - メインの処理を行うPythonスクリプト
  - `dialogue.yaml`の読み込み、AIの呼び出し、対談ごとのフォルダ作成とテーマごとの対談、感想の生成を行う 📂🤖
- `book_dialogue`ディレクトリ
  - 対談N ディレクトリ
    - テーマ.md
- `dialogue_generator.py`
  - 対談生成AIの仕様書（`AIdocs/対談生成AI.md`）を読み込み、Claude APIを使って対談を生成する関数 `generate_dialogue_content()` を定義 💬🤖
- `impression_generator.py`
  - 感想生成AIの仕様書（`AIdocs/感想生成AI.md`）を読み込み、Claude APIを使って感想を生成する関数 `generate_impression_content()` を定義 💭🤖

</details>

<details>
<summary>🌟 プログラムの特徴</summary>

- 📝 YAMLファイルで対談の人物とテーマを柔軟に定義可能！
- 🤖 対談生成AIと感想生成AIの2つのAIを組み合わせて自動生成！
- 📚 生成された対談と感想は1つのMarkdownファイルにまとめて書籍として出力！

</details>

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

## 💭 感想生成AI

対談内容から、人物Aの感想を生成するAI

<details>
<summary>🎯 入力</summary>

- 対談内容 (テキスト): {dialogue_content}

</details>

<details>
<summary>📝 出力</summary>

- md形式の人物Bの感想（500文字程度）

</details>

<details>
<summary>🛠️ 処理</summary>

1. 対談内容を分析し、重要なポイントや印象的な発言を抽出
2. 抽出した内容をもとに、人物Bの立場や個性を反映した感想を生成
   - 対談を通じて得られた新しい気づきや学び
   - 人物Aの発言に対する共感や意見
   - 今後の展望や抱負など
3. 生成した感想を、自然な文章になるように整形

</details>

<details>
<summary>⚠️ 注意</summary>

- 感想は人物Bの視点で書く
- 対談内容を踏まえつつ、人物Bならではの感想になるようにする
- 感想は読み手に伝わりやすい、わかりやすい文章にまとめる

</details>
