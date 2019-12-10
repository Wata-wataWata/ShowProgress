# class ShowProgress
パーセントで進捗を表示してくれる。一つのインスタンスにつき一つの進捗。
## 使い方

インスタンスを作って、`show_and_progress()`のコルーチンを作る。ひたすら`next(コルーチン)`する。

`next()`するタイミングで表示が更新されるので、遅い処理はクルクルが遅い。時間の表示も飛び飛びになる。

スレッドとかで常に（1秒に1回とかで）回るようにするべき？

```python
# 何らかのデータ
test_list = [random.random() for x in range(1000)]

# 進捗管理クラスのインスタンス作成
# 始まりと終わりの設定を間違うと100%にたどり着かないかも
progress = ShowProgress(1, len(test_list) + 1, step=1, row=0)

# コルーチン関数の作成
coru = progress.show_and_progress()

print("[-] Process start.")
print("[-] Something info.")
print("[-------------------]")
for i in test_list:     # リストに何らかの処理をする
  # 何らかの処理 (printはしないで欲しい)
  time.sleep(0.05)

  # コルーチン関数を進める
  next(coru)          # 進める間にprintすると表示がずれるのが欠点
else:
  print("[-] Done.")
```

# class timestamp

経過時間を計算するクラス。

## 使い方

ShowProgressで使うクラス。これ単体ではあまり使わない。でも割と汎用的な気がする。

1. `stamp_start_time()`で計測開始の時間を記録する。記録した時はTrue、しなかった時はFalseを返す。
2. `get_time_elapsed()` で記録した開始時間とメソッドを実行した時間の差分を返す。記録した開始時間がない場合はFalseを返す。
3. `get_string_time(time)`でtimeを`時間:分:秒.ミリ秒`の文字列にして返す。