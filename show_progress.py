import time
import random


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 進捗を管理するクラス
# 表示方法をいろいろ増やしたい。バーのタイプとかクルクル回るやつとか...
# show_and_progressを連打すればそれっぽい感じに表示できる
#
# c = ShowProgress(始まりの数字, 終わりの数字, 一回の進む量(デフォルトは1))
class ShowProgress:
    def __init__(self, start: int, end: int, step=1):
        self.start = start
        self.end = end
        self.step = step
        self.progress = self.start

    def next(self):
        """
        表示はしないが次に進めたい時に使う関数
        :return: nothing
        """
        self.progress += self.step

    def back(self):
        """
        表示はしないが前に戻したい時に使う関数
        :return: nothing
        """
        self.progress -= self.step

    def reset(self):
        """
        表示はせずに進みをリセットする時に使う関数
        :return: nothing
        """
        self.progress = self.start

    def set_start(self, num: float):
        self.start = num

    def set_end(self, num: float):
        self.end = num

    def seek_to(self, num: float):
        self.progress = num

    def show(self):
        progre = self.progress / (self.end - self.start) * 100
        if progre >= 100:
            progre = 100
            print("\r[*] %2.3f%%" % progre)
        else:
            print("\r[*] %2.3f%%" % progre, end="")

    def show_and_progress(self):
        while True:
            # 進捗が終了条件より小さいとき
            self.show()
            if self.end >= self.progress:
                self.next()
                yield 1

            else:
                yield None

# end of class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":
    # 何らかのデータ
    test_list = [random.random() for x in range(100)]

    # 進捗管理クラスのインスタンス作成
    # 始まりと終わりの設定を間違うと100%にたどり着かないかも
    progress = ShowProgress(1, len(test_list) + 1)
    # コルーチン関数の作成
    coru = progress.show_and_progress()

    print("[-] Process start.")
    for i in test_list:     # リストに何らかの処理をするようなイメージ
        # 何らかの処理 (printはしないで欲しい)
        time.sleep(0.05)

        # コルーチン関数を進める
        next(coru)          # 進める間にprintすると表示がずれるのが欠点
    else:
        print("[-] Done.")
