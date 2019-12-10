import time
import random

# 例外たち
class InvalidValue(Exception):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 進捗を管理するクラス
# 表示方法をいろいろ増やしたい。バーのタイプとかクルクル回るやつとか...
# show_and_progressを連打すればそれっぽい感じに表示できる
#
# c = ShowProgress(始まりの数字, 終わりの数字, 一回の進む量(デフォルトは1))
class ShowProgress:
    def __init__(self,
                 start: int,
                 end: int,
                 step=1,
                 row=0,
                 bar_width=30,
                 show_bar=True,
                 show_roll=True,
                 show_progress_time=True,
                 show_remaining_time=True):

        self.start = start
        self.end = end
        self.step = step
        self.progress = self.start
        self.row = row
        self.bar_width = bar_width

        # 表示するか否か系変数
        self.show_bar = show_bar
        self.show_roll = show_roll
        self.show_progress_time = show_progress_time
        self.show_remaining_time = show_remaining_time

        # 中で使うやつ
        self.roll_step = 0
        self.timestamp = timestamp()

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

    def set_bar_width(self, num: int):
        self.bar_width = num

    def seek_to(self, num: float):
        self.progress = num

    def show(self):
        string = self.get_string()
        print(string, end="")

    def get_string(self):
        self.timestamp.stamp_start_time()

        progre = self.progress / (self.end - self.start) * 100
        if progre >= 100:
            progre = 100

        string_list = list()
        
        # カーソル移動の文字列
        if self.row > 0:
            head = "\033[%dA\r" % self.row
        elif self.row == 0:
            head = "\r"
        else:
            raise InvalidValue()

        # くるくる
        if self.show_roll:
            head = head + "[" + self.get_roll_string() + "]"
        elif self.show_roll and progre == 100:
            head = head + "[-]"
        else:
            head = head + "[*]"

        string_list.append(head)

        # パーセンテージ
        foot = "%2.3f%%" % progre
        string_list.append(foot)

        # プログレスバー
        if self.show_bar:
            block_num = self.bar_width * progre / 100
            string_list.append("[" + "▮" * int(block_num) + " " * (self.bar_width - int(block_num)) + "]")

        # 経過時間
        if self.show_progress_time:
            string_list.append(self.timestamp.get_string_time(self.timestamp.get_time_elapsed()))

        foot = "\n" * self.row
        if self.row == 0 and progre == 100:
            foot = foot + "\n"
        string_list.append(foot)

        return " ".join(string_list)

    def get_roll_string(self):
        roll = ('-', '\\', '|', '/', '-', '\\', '|', '/')
        self.roll_step = (self.roll_step + 1) % len(roll)
        return roll[self.roll_step]

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

class timestamp:
    def __init__(self):
        self.start = 0
        self._doing = False
    
    def stamp_start_time(self):
        if not self._doing:
            self.start = time.time()
            self._doing = True
        else:
            pass

    def get_string_time(self, time: float):
        msecond = int((time - int(time)) * 100)
        second = int(time % 60)
        minute = int(time / 60)
        hour = int(time / 360)
        return "%02d:%02d:%02d.%02d" % (hour, minute, second, msecond)

    def reset(self):
        self.start = 0
        self._doing = False

    def get_time_elapsed(self):
        return time.time() - self.start

if __name__ == "__main__":
    # 何らかのデータ
    test_list = [random.random() for x in range(1000)]
    test_list1 = [random.random() for x in range(1000)]
    # 進捗管理クラスのインスタンス作成
    # 始まりと終わりの設定を間違うと100%にたどり着かないかも
    progress = ShowProgress(1, len(test_list) + 1, step=1, row=0)
    progress1 = ShowProgress(1, len(test_list1) + 1, row=1)
    # コルーチン関数の作成
    coru = progress.show_and_progress()
    coru1 = progress1.show_and_progress()

    time_stamp = timestamp()
    time_stamp.stamp_start_time()

    print("[-] Process start.")
    print("[-] Something info.")
    print("[-------------------]")
    for i in test_list:     # リストに何らかの処理をするようなイメージ
        # 何らかの処理 (printはしないで欲しい)
        time.sleep(0.05)

        # コルーチン関数を進める
        next(coru)          # 進める間にprintすると表示がずれるのが欠点
    else:
        print("[-] Done.")
    
    print(time_stamp.get_string_time(time_stamp.get_time_elapsed()))
