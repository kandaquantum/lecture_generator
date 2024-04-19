import os
from tqdm import tqdm


def main():
    target_dir = "gen_ai_jyuku/week2/lecture_generator/book_dialogue"
    with open(
        "gen_ai_jyuku/week2/lecture_generator/book_dialogue/README2.md", "w"
    ) as index_file:

        index_file.write("# 対談集\n\n")

        # book_dialogueディレクトリ内のディレクトリを取得
        dialogue_dirs = [
            d
            for d in os.listdir(target_dir)
            if os.path.isdir(os.path.join(target_dir, d))
        ]

        for i, dialogue_dir in enumerate(
            tqdm(dialogue_dirs, desc="Generating book"), start=1
        ):
            # 対談ディレクトリ内のMarkdownファイルを取得
            dialogue_files = [
                f
                for f in os.listdir(os.path.join(target_dir, dialogue_dir))
                if f.endswith(".md")
            ]

            if not dialogue_files:
                continue

            # 対談のタイトルを取得
            with open(
                os.path.join(target_dir, dialogue_dir, dialogue_files[0]), "r"
            ) as f:
                dialogue_title = f.readline().strip("# \n")

            # 目次に対談へのリンクを追加
            index_file.write(f"## 対談{i}: {dialogue_title}\n\n")
            index_file.write(f"- [対談{i}へ](#対談{i})\n")
            index_file.write(f"- [感想へ](#感想{i})\n\n")

        # 対談と感想の内容を追加
        for i, dialogue_dir in enumerate(
            tqdm(dialogue_dirs, desc="Generating book"), start=1
        ):
            dialogue_files = [
                f
                for f in os.listdir(os.path.join(target_dir, dialogue_dir))
                if f.endswith(".md")
            ]

            if not dialogue_files:
                continue

            with open(
                os.path.join(target_dir, dialogue_dir, dialogue_files[0]), "r"
            ) as f:
                content = f.read()

            # 対談の内容を追加
            index_file.write(f'<a id="対談{i}"></a>\n')
            index_file.write(content)

            # 感想の内容を追加
            index_file.write(f'<a id="感想{i}"></a>\n')
            index_file.write("## 感想\n\n")
            impression_start = content.find("## 感想")
            if impression_start != -1:
                index_file.write(content[impression_start:])


if __name__ == "__main__":
    main()
