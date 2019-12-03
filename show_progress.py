import time
import random


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 進捗を管理するクラス
# 表示方法をいろいろ増やしたい。バーのタイプとかクルクル回るやつとか...
# show_and_progressを連打すればそれっぽい感じに表示できる
#
# c = ShowProgress(始まりの数字, 終わりの数字, 一回の進む量(デフォルトは1))
class ShowProgress:
    def __init__(self, start: int, end: int, step=1, row=0):
        self.start = start
        self.end = end
        self.step = step
        self.progress = self.start
        self.row = row

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

    def set_row(self, num: int):
        self.row = num

    def seek_to(self, num: float):
        self.progress = num

    def show(self):
        progre = self.progress / (self.end - self.start) * 100
        if progre >= 100:   # 100以上なら100ぴったりに
            progre = 100

        if self.row > 0:
            string = "\033[%dA\r[*] %s %2.3f%%" % (self.row, self.get_progress_bar(20, progre), progre)
            string = string + ("\n" * self.row)
        elif self.row == 0:
            string = "\r[*] %2.3f%%" % progre
        else:
            string = "Invalid row."

        print(string, end="")
        if self.row == 0 and progre == 100:
            print()

    
    def get_progress_bar(self, width: int, progre: int):
        block_num = width * progre / 100
        bar = "[" + "▮" * int(block_num) + " " * (width - int(block_num)) + "]"
        return bar
    

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
    test_list1 = [random.random() for x in range(100)]
    # 進捗管理クラスのインスタンス作成
    # 始まりと終わりの設定を間違うと100%にたどり着かないかも
    progress = ShowProgress(1, len(test_list) + 1, step=1, row=2)
    progress1 = ShowProgress(1, len(test_list1) + 1, row=1)
    # コルーチン関数の作成
    coru = progress.show_and_progress()
    coru1 = progress1.show_and_progress()

    print("[-] Process start.")
    print("[-] Something info.")
    print("[-------------------]")
    print("1111111111111111111")
    print("2222222222222222222")
    print("3333333333333333333")
    print("4444444444444444444")
    print("5555555555555555555")
    for i in test_list:     # リストに何らかの処理をするようなイメージ
        # 何らかの処理 (printはしないで欲しい)
        time.sleep(0.05)

        # コルーチン関数を進める
        next(coru)          # 進める間にprintすると表示がずれるのが欠点
    else:
        print("[-] Done.")
