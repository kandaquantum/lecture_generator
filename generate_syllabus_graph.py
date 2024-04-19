
import yaml
from graphviz import Digraph

# syllabusデータの作成 （型：リスト[dict]）
syllabus = yaml.safe_load('''
- 章: 1
  主題:
    - 人間の生理的特徴に関する哲学的考察
  節:
    - タイトル: 人間はなぜ寝るときに目を閉じるのか？
      説明: |
        ソクラテスとの対話を通じて、睡眠中に目を閉じる理由について哲学的に探求する。
- 章: 2
  主題:
    - 物理法則の変化が人生に与える影響
  節:
    - タイトル: もしも重力が逆向きだったら、人生はどう変わるか？
      説明: |
        アインシュタインとの対話により、重力の逆転が日常生活や社会構造にもたらす変化を想像する。
- 章: 3
  主題:
    - 地球外知的生命体の存在と人類との関係性
  節:
    - タイトル: 宇宙人が地球に来ないのは、我々が彼らのペットだからなのか？
      説明: |
        カール・セーガンとの対話で、宇宙人が地球に来ない理由を、人類が彼らのペットである可能性から考察する。
- 章: 4
  主題:
    - 時間旅行の実現に伴う社会的・倫理的問題
  節:
    - タイトル: 時間旅行が可能になったら、歴史上の偉人とトイレを借りる権利を争うことになるのか？
      説明: |
        スティーブン・ホーキングとの対話を通じて、時間旅行の実現により生じる、歴史上の偉人とのトイレ借用権をめぐる争いについて議論する。
- 章: 5
  主題:
    - 空想上の生物の存在と特性に関する考察
  節:
    - タイトル: ユニコーンが存在しないのは、彼らがニンジャだからなのか？
      説明: |
        J・R・R・トールキンとの対話で、ユニコーンが存在しない理由を、彼らがニンジャであるという仮説から探る。
''')

# Graphvizを使ってグラフを作成。コメントに'Syllabus Graph'を指定。
graph = Digraph(comment='Syllabus Graph')

# 週のボックスノードと講義サブボックスの作成
for i, week in enumerate(syllabus):
    # 週のインデックスを取得
    week_index = i + 1
    
    # 週のトピックを取得し、カンマ区切りの文字列に変換
    week_topics = ', '.join(week['主題'])
    
    # 週のノード名を作成（例: "Week 1\n基礎開発ツール講習"）
    week_node_name = f"Chapter {week_index}\n{week_topics}"
    
    # 週のノードを作成。ボックス形状、塗りつぶし、水色の背景色を指定。
    graph.node(week_node_name, shape='box', style='filled', fillcolor='lightblue')
    
    # 週ごとのサブグラフを作成
    with graph.subgraph(name=f'cluster_week_{week_index}') as subgraph:
        # 講義のタイトルをリストアップし、改行区切りの文字列に変換
        lecture_titles = '\n'.join([lecture['タイトル'] for lecture in week['節']])
        
        # サブグラフ内に講義一覧のノードを作成。ボックス形状、ラベルに講義一覧を指定。
        subgraph.node(f'lectures_week_{week_index}', shape='box', label=lecture_titles)
        
        # 週のノードと講義一覧のノードを破線で接続
        # 週ボックスノードの下部（south）からエッジを始め、headport='sw'はサブグラフの左下（south-west）にエッジを接続するように指定
        graph.edge(week_node_name, f'lectures_week_{week_index}', style='dashed', tailport='s', headport='sw')

# 隔週ごとの矢印の接続
for i in range(len(syllabus) - 1):
    # 現在の週のデータを取得
    current_week = syllabus[i]
    
    # 次の週のデータを取得
    next_week = syllabus[i + 1]
    
    # 現在の週のノード名を作成
    current_week_node_name = f"Chapter {i + 1}\n{', '.join(current_week['主題'])}"
    
    # 次の週のノード名を作成
    next_week_node_name = f"Chapter {i + 2}\n{', '.join(next_week['主題'])}"
    
    # 現在の週のノードと次の週のノードを矢印で接続
    graph.edge(current_week_node_name, next_week_node_name)

# グラフの保存と表示
graph.render('syllabus_graph', view=True)
