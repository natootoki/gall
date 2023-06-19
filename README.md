# 環境

Python 3.11.3  
pyinputインストール必要  
→pip install pyinput  
pygameインストール必要  
→pip install pygame  
コマンドプロンプトで.pyファイルを実行して遊びます  
今のメインはtest.py  

# できること

矢印キーで範囲内を移動  
Qキーで処理終了  

# 思考・作業ログ

新しいPCで何か色々するためのリポジトリ。  
この行はプッシュテスト。  
first.pyはpythonの準備運動。  
test.pyは開発テスト。  
帰りが遅い日は何もできないけど草は生やしたいんだぜ。  
長押しの実装はした。  
今度はボタン一回押下につき一回しか反応しない仕組みを実装したい。  
飲み会に出ると草を生やせないですね。  
ボタン押下一回につき一回しか反応しない仕組みは  
各ボタンについてフラグが必要になる。  
あるボタンが離されたときに更新するフラグであるから、  
共通のものではいけない。  
ボタン押下一回につき一回だけ処理される制御ができた。20230529  
x座標とy座標が数字で表示されている状態なので、  
四角形で場所を表現するようにしたい。  
　→できた  
作りたい物  
・迷路  
・テトリス  
・タイピングゲーム  
・マインスイーパー  
・トランプ系のゲーム  
座標の最小、最大を実装したい。20230530  
　→できた  
qで処理終了する。  
　→できた  
ステージの大きさを変数で管理したい。  
　→できた  
ゴールを設置したい。  
　→ゴールはplayerのスタート位置と重ならない  
　→辿り着いたら処理終了  
　→障害物よりゴールを先に作った方が良いのではないか  
　　→定位置に設置はできた  
　　　→位置をランダムにすることはできた  
台風のせいか眠い。20230602  
ステージのサイズをランダムにすることができた  20230603
障害物を設置したい。  
　→まずはランダムに置いてみる  
　　→プレイヤーともゴールとも重ならない必要がある  
　　　→被りのないランダムな位置に指定の個数を置く  
　　　　→できた  
ゴールできるステージができるようにする  
　→プレイヤーがそのマスに到達可能かどうかのリストを作る  
　　→到達可能なマスを1として、隣のマスに動けるかどうかでテストする  
　　　→できた  
難しい迷路を作りたい  
　→何手でゴールできるかという観点をテストに追加する  
　　→できた  
スタートからゴールまでの一本道を作れるようにする  
　→できた  
道を効率よく敷き詰めるには網状のフォーマットで壁を設置するといいのでは  
　→できた  
壁がポツンとひとつだけ孤立していても簡単に突破されてしまう  
　→孤立した壁が無くなるように迷路を生成する  
　　→できた  
短い行き止まりや道の合流を減らしたい  
見やすさのためにゲーム画面を作りたい  
　→pygameを使おう  
　　→ウィンドウの表示と図形の描画はできた  
　　　→pygameのウィンドウ上でプレーができるようになった  
迷路の難易度を上げたい  
　→短い壁を無くしたい  
　　→壁が何個つながっているかを管理するリストを作る  
　　　→wall_length：各マスにある壁が何個繋がっている壁なのか格納する  
----wall_length  
000000000  
077701030  
000700030  
010777030  
----  
　　　→wall_connect_list：繋がっている壁ひとつひとつの座標を格納する  
　　　→壁が何個繋がっているのかはスキャンの後から分かる情報  
　　　→リアルタイムで各マスに数字を当てはめていくのは難しい  
　　　→壁が繋がっている全てのマスについてwall_length更新をまとめて行うために使う  
----wall_connect_list
[1, 2], [2, 2], [3, 2], [3, 1], [3, 0], [4, 0], [5, 0]  
----
　　　　→できた  
壁ごとに色を変えることで迷路の難易度が視覚的に分かるかもしれない  
　→できた  
外壁の表示をして分かりやすく  
　→できた  
スタート地点から到達できるマスのうち  
もっとも道のりが長いマスをゴールにすれば  
難しくできるかもしれない  
　→できた  
プレイヤーが行けないマスを壁以外無くしたい。20230612  
　→どのように
　→迷路を作る  
　→到達可能なマスを調べる  
　→壁ではない、かつ、到達できないマスを対象に処理をする  
　→上下左右の壁をランダムにひとつ削る  
　　→削った先のマスが到達可能マスなら、対象のマスも到達可能となる  
　　→削った先のマスが到達不可能マスなら、今後はそのマスについて上記と同様の処理を行う  
----
5■7■■■0  
456■0■0  
3■5■■■■  
2345678  
1■5■7■■  

↓  

5■7■■■0  
45600■0  
3■5■■■■  
2345678  
1■5■7■■  

↓  

5■7■■■0  
45678■0  
3■5■■■■  
2345678  
1■5■7■■  
----  
　→できた
同一の壁が複数個所で外壁に繋がっていても、  
行けない場所が増えるだけで意味が無い  
　繋がっている壁は、1か所だけ外壁に繋がるようにする  
　　→できた  
行けないマスを無くすために壁を削ると、細切れの壁が出て来る  
今のロジックでは、削れないケースも出て来る  
　壁を作る時に、その都度、到達不可能なマスが  
　発生しないかどうかチェックするようにする  
怒涛の日曜日18時間勤務。タクシー帰り。