import speedtest
import datetime
import time
import os
import sys

INTERVAL_SEC = 60

# デスクトップのパス　取得
desktop_dir = os.path.expanduser(r'~/Desktop\\server_speed\\')


def Make_dir(path_w):

    try:
        if(os.path.isdir(path_w)):
            pass
        else:
            os.makedirs(path_w)
    except FileExistsError:
        print('関数名:Check_Dir ::: ディレクトリ作成エラー')


def get_speed_tester():
    servers = []
    stester = speedtest.Speedtest()
    stester.get_servers(servers)
    stester.get_best_server()
    return stester


def get_timestamp():
    date = datetime.datetime.now()
    timestamp = str(date.strftime('%Y-%m-%d %H:%M:%S'))
    return timestamp


def test_speed(stester):
    down_result = str(int(stester.download()))
    up_result = str(int(stester.upload()))
    return down_result, up_result


# === 桁数をつける
def cut_result(str_num):
    if len(str_num) == 9:
        tmp_str_num = str_num[:4]
        tmp_str_num = int(tmp_str_num) / 10
        return str(tmp_str_num)

    else:
        tmp_str_num = str_num[:3]
        tmp_str_num = int(tmp_str_num) / 10
        return str(tmp_str_num)

# === ファイル　書き込み


def File_Write(path_w, write_file):
    with open(path_w, mode="wb") as f:
        f.write(write_file.encode('utf-8'))

# === ファイル 追記用


def File_Append(path_w, write_file):
    with open(path_w, mode="ab") as f:
        f.write(write_file.encode('utf-8'))


def command_line_runner():
    stester = get_speed_tester()
    print('time,down(bps),up(bps)')
    while True:
        t1 = time.time()
        timestamp = get_timestamp()
        down_result, up_result = test_speed(stester)

        tmp_down_result = cut_result(down_result)
        tmp_up_result = cut_result(up_result)

        # フォルダ　作成
        Make_dir(desktop_dir)

        print(timestamp + ',' + '下り速度:::' +
              tmp_down_result + 'Mbit/s' + ',' + '上り速度:::' + tmp_up_result + 'Mbit/s')

        # ファイル挿入用
        file_str = timestamp + ',' + '下り速度:::' + tmp_down_result + \
            'Mbit/s' + ',' + '上り速度:::' + tmp_up_result + 'Mbit/s' + '\n'

        # ファイル存在チェック
        file_name = 'server_speed.txt'
        if os.path.exists(desktop_dir + file_name):  # python/test/back_up
            File_Append(desktop_dir + file_name, file_str)
        else:
            File_Write(desktop_dir + file_name, file_str)

        t2 = time.time()
        next_sleep_time = int(INTERVAL_SEC - (t2 - t1))
        time.sleep(next_sleep_time)


if __name__ == '__main__':
    command_line_runner()
