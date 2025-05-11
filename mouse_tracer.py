# mouse_tracer.py

import pyautogui
import time
import keyboard

def trace_word_path(path, board_positions, delay=0.01):
    if not path:
        return

    # 強制轉成標準 int，避免 numpy 類型錯誤
    screen_path = [(int(board_positions[i][j][0]), int(board_positions[i][j][1])) for (i, j) in path]

    pyautogui.moveTo(*screen_path[0], duration=0.1)
    pyautogui.mouseDown()

    for pos in screen_path[1:]:
        pyautogui.moveTo(*pos, duration=delay)

    pyautogui.mouseUp()


def trace_multiple_words(found_words, board_positions, top_n=None, delay=0.05, interval=0.5):
    """
    依序模擬滑鼠操作畫出多個單字。
    
    Parameters:
    - found_words: dict { word: (score, [(i, j), ...]) }
    - board_positions: [[(x, y), ...], ...]
    - top_n: 若指定，只 trace 分數最高的前 N 個單字
    - delay: 每一步滑鼠移動的延遲
    - interval: 每個單字間的間隔時間
    """
    # 按分數由高到低排序單字
    sorted_words = sorted(found_words.items(), key=lambda x: -x[1][0])
    if top_n:
        sorted_words = sorted_words[:top_n]

    for idx, (word, (score, path)) in enumerate(sorted_words):


        print(f"[{idx+1}] Tracing '{word.upper()}' | score={score} | path={path}")
        trace_word_path(path, board_positions, delay=delay)
        time.sleep(interval)

        # 按著ENTER繼續
        if (idx + 1) % 1 == 0:
           keyboard.wait("enter")