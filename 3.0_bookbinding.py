import os
from tqdm import tqdm


def main():
    # 📝 目次用のMarkdownファイルを作成
    # with open("book_dialogue/README.md", "w") as index_file:
    target_dir = "gen_ai_jyuku/week2/lecture_generator/book_dialogue"
    with open(
        "gen_ai_jyuku/week2/lecture_generator/book_dialogue/README.md", "w"
    ) as index_file:

        index_file.write("# 対談集\n\n")

        # book_dialogueディレクトリ内のディレクトリを取得
        dialogue_dirs = [
            d
            # for d in os.listdir("book_dialogue")
            for d in os.listdir(target_dir)
            # if os.path.isdir(os.path.join("book_dialogue", d))
            if os.path.isdir(os.path.join(target_dir, d))
        ]

        for i, dialogue_dir in enumerate(
            tqdm(dialogue_dirs, desc="Generating index"), start=1
        ):
            # 対談ディレクトリ内のMarkdownファイルを取得
            dialogue_files = [
                f
                # for f in os.listdir(os.path.join("book_dialogue", dialogue_dir))
                for f in os.listdir(os.path.join(target_dir, dialogue_dir))
                if f.endswith(".md")
            ]

            if not dialogue_files:
                continue

            # 対談のタイトルを取得
            with open(
                # os.path.join("book_dialogue", dialogue_dir, dialogue_files[0]), "r"
                os.path.join(target_dir, dialogue_dir, dialogue_files[0]),
                "r",
            ) as f:
                dialogue_title = f.readline().strip("# \n")

            # 目次に対談へのリンクを追加
            index_file.write(f"## 対談{i}\n\n")
            index_file.write(
                f"- [{dialogue_title}](./{dialogue_dir}/{dialogue_files[0]})\n"
            )

            # 感想へのリンクを追加
            index_file.write(
                f"  - [感想](./{dialogue_dir}/{dialogue_files[0]}#感想)\n\n"
            )


if __name__ == "__main__":
    main()
