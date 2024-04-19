import os
import yaml
import anthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()  # .envファイルから環境変数を読み込む


class LectureGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get(
                "ANTHROPIC_API_KEY"
            ),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_lecture_content(self, lecture_title, lecture_description):
        with open("ais/講義資料生成AI.md", "r") as f:
            lecture_content_prompt = f.read().format(
                lecture_title=lecture_title, lecture_description=lecture_description
            )

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "type": "text", "text": lecture_content_prompt}
                    ],
                }
            ],
        )

        return response.content[0].text.strip()


class QuizGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get(
                "ANTHROPIC_API_KEY"
            ),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_quiz_content(self, lecture_title, lecture_description):
        with open("ais/問題生成AI.md", "r") as f:
            quiz_content_prompt = f.read().format(
                lecture_title=lecture_title, lecture_description=lecture_description
            )

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": quiz_content_prompt}],
                }
            ],
        )

        return response.content[0].text.strip()


def main():
    if not os.path.exists("ais"):
        os.makedirs("ais")

    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    lecture_generator = LectureGenerator()
    quiz_generator = QuizGenerator()

    for chapter in tqdm(syllabus, desc="Generating chapters"):
        chapter_dir = f"book/{chapter['章']}"
        os.makedirs(chapter_dir, exist_ok=True)

        for section in tqdm(
            chapter["節"],
            desc=f"Generating sections for chapter {chapter['章']}",
            leave=False,
        ):
            section_file = f"{chapter_dir}/{section['タイトル']}.md"

            lecture_content = lecture_generator.generate_lecture_content(
                section["タイトル"], section["説明"]
            )
            quiz_content = quiz_generator.generate_quiz_content(
                section["タイトル"], section["説明"]
            )

            with open(section_file, "w") as f:
                f.write(f"# {section['タイトル']}\n\n")
                f.write(f"{lecture_content}\n\n")
                f.write(f"{quiz_content}\n")


if __name__ == "__main__":
    main()
