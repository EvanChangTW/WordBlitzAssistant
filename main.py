"""
FB WordBlitz 遊戲助手

作者 Evan Chang & ChatGPT-4o 
版本 v20250511

註記:
1.除錯: 遇到("錯誤：偵測結果不是 4x4，請確認畫面或模板")時，調整threshold參數
2.字典: Words字典可以自行上網找 
3.這個程式碼寫的不是非常完整，但大概不會再更新了
4.有問題問第二的作者 不要問我
"""
# 匯入必要的模組
import sys
import os 
import cv2
import pyautogui
import numpy as np
# %% 判釋4*4內容（建立棋盤）====================================================
"""
從螢幕擷取畫面，搜尋指定資料夾中的字母圖片，回傳 4x4 的字母 board。
"""
# === 參數設定 ===
folder_path = "Capture"         # 儲存字母圖樣的資料夾（每張圖命名為 A.jpg、B.jpg ...）
threshold = 0.88                # 模板匹配的相似度門檻（越接近1越嚴格）
scale = 1                       # 模板圖的縮放比例（與螢幕上實際顯示尺寸一致）
distance_threshold = 10         # 匹配點的鄰近容許距離（小於此距離視為同一位置）
grid_rows, grid_cols = 4, 4     # 預期輸出的棋盤尺寸（4列4行）

# === 擷取當前螢幕畫面，並轉成 OpenCV 圖像格式 ===
screenshot = pyautogui.screenshot()
screen_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# === 工具函式 ===

# 判斷兩個點之間是否相近（距離小於 threshold）
def is_close(p1, p2, threshold):
    return np.hypot(p1[0] - p2[0], p1[1] - p2[1]) < threshold

# 對一組座標點進行簡單群聚，只保留不重複的位置
def cluster_points(points, threshold):
    clustered = []
    for pt in points:
        for cluster in clustered:
            if is_close(pt, cluster, threshold):
                break  # 如果與現有點太近就略過
        else:
            clustered.append(pt)  # 否則加入新點
    return clustered

# === 主處理流程 ===

matched_letters = []  # 儲存所有匹配到的 (位置, 字母)

# 逐一讀取資料夾中所有 .jpg 檔案
for filename in os.listdir(folder_path):
    if not filename.lower().endswith(".jpg"):
        continue  # 忽略非 JPG 圖片

    letter = os.path.splitext(filename)[0].upper()  # 取檔名轉為大寫字母，例：'A.jpg' → 'A'
    img_path = os.path.join(folder_path, filename)
    original_template = cv2.imread(img_path)
    if original_template is None:
        continue  # 圖片讀取失敗時跳過

    # 根據設定的縮放比例進行大小調整
    new_w = int(original_template.shape[1] * scale)
    new_h = int(original_template.shape[0] * scale)
    if new_w < 10 or new_h < 10:
        continue  # 太小的模板不比對

    resized_template = cv2.resize(original_template, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 執行模板匹配
    result = cv2.matchTemplate(screen_img, resized_template, cv2.TM_CCOEFF_NORMED)

    # 找出所有高於相似度門檻的匹配點
    locations = np.where(result >= threshold)
    raw_points = list(zip(*locations[::-1]))  # 將 (row, col) 轉成 (x, y)

    # 去除重複或相鄰太近的點
    clustered = cluster_points(raw_points, distance_threshold)

    # 將匹配點與對應字母記錄下來
    for pt in clustered:
        pt = (int(pt[0]), int(pt[1]))
        matched_letters.append((pt, letter))

# === 空間排序處理 ===

# 先依 y（垂直）排序，再依 x（水平）排序，確保順序一致
matched_letters.sort(key=lambda x: (x[0][1], x[0][0]))

# 按行進行分組
rows = []
row = []
last_y = None
for pt, letter in matched_letters:
    x, y = pt
    if last_y is None:
        last_y = y
    # 若 y 與前一筆的差異過大，則視為新一列
    if abs(y - last_y) > 50 and len(row) > 0:  # 可依實際畫面調整閾值
        rows.append(row)
        row = []
        last_y = y
    row.append(((x, y), letter))  # 將完整座標 (x, y) 放入


# 加入最後尚未加入的那一列
if row:
    rows.append(row)

# 每列中再依 x 排序，建立 board 與 board_positions（位置）
board = []
board_positions = []
for r in rows:
    r.sort(key=lambda item: item[0][0])  # item[0] 是 (x, y)，item[0][0] 是 x
    board.append([letter for _, letter in r])
    board_positions.append([(int(pt[0]), int(pt[1])) for pt, _ in r])  # 確保為 int tuple

# === 檢查是否為 4x4 棋盤，並輸出 ===
if len(board) == 4 and all(len(r) == 4 for r in board):
    print("board = [")
    for row in board:
        print("    " + str(row) + ",")
    print("]")
    
    print("\nboard_positions = [")
    for row in board_positions:
        print("    " + str(row) + ",")
    print("]")
    
    # # 等待使用者按下數字鍵盤 Enter 鍵
    # print("\n請檢查棋盤與位置是否正確，若正確請按數字鍵盤的 Enter 鍵繼續...")
    # keyboard.wait("num enter")
else:
    print("錯誤：偵測結果不是 4x4，請確認畫面或模板")
    print("board = [")
    for row in board:
        print("    " + str(row) + ",")
    print("]")
    
    # print("\nboard_positions = [")
    # for row in board_positions:
    #     print("    " + str(row) + ",")
    # print("]")
    
    sys.exit(1)  # 強制中止程式，非 0 表示錯誤結束
# %% 主程式（暫時手動輸入 board 和 score）======================================

if __name__ == "__main__":
    # 檢查是否為 4x4
    if len(board) == 4 and all(len(row) == 4 for row in board):

        scores = [
            [1,1,1,1],
            [1,1,1,1],
            [1,1,1,1],
            [1,1,1,1]
        ]
        
        from word_finder import load_words, filter_feasible_words, build_trie, find_words_fast

        # 步驟一：載入字典
        dictionary = load_words("words.txt")
        
        # 步驟二：先篩掉不可能組出的單字
        filtered = filter_feasible_words(dictionary, board)
        
        # 步驟三：建立 Trie
        trie = build_trie(filtered)
        
        # 步驟四：搜尋單字
        found = find_words_fast(board, scores, trie)

        # # 顯示結果
        # for word, (score, path) in sorted(found.items(), key=lambda x: -x[1][0]):
        #     print(f"{word.upper()} | 分數: {score} | 路徑: {path}")
        
        # 步驟五：瘋狂輸出
        from mouse_tracer import trace_multiple_words

        print("按著ENTER繼續")
        trace_multiple_words(
            found_words=found,
            board_positions=board_positions,
            top_n=500,          # 只畫出分數最高的前 5 個單字
            delay=0.0002,         # 每個字母之間移動延遲
            interval=0.005        # 單字與單字間的間隔
        )

            
    else:
        print("錯誤：board 必須是 4x4")
