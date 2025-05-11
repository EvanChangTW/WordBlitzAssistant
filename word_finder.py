# word_finder.py

from collections import Counter
from itertools import product

# === 字首樹節點定義 ===
class TrieNode:
    def __init__(self):
        self.children = {}     # 每個子節點以字母為 key，對應 TrieNode 為 value
        self.is_word = False   # 若此節點代表一個完整單字的結尾，則為 True

# === 載入字典檔（每行一個單字），並過濾掉長度 < 2 的 ===
def load_words(file_path="words.txt"):
    with open(file_path) as word_file:
        words = set(word.strip().lower() for word in word_file if len(word.strip()) >= 2)
    return words

# === 檢查單字是否可由棋盤字母組成（不超過次數限制）===
def filter_feasible_words(dictionary, board):
    board_letters = Counter(ch.lower() for row in board for ch in row)
    feasible_words = set()
    for word in dictionary:
        word_letters = Counter(word.lower())
        if all(word_letters[c] <= board_letters.get(c, 0) for c in word_letters):
            feasible_words.add(word)
    return feasible_words

# === 建立 Trie 樹結構 ===
def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    return root

# === 主函式：從棋盤中尋找所有合法單字，並回傳分數與位置 ===
def find_words_fast(board, scores, trie_root):
    found_words = {}  # 結構：{ word: (score, [(x1,y1), (x2,y2), ...]) }
    rows, cols = len(board), len(board[0])
    visited = [[False]*cols for _ in range(rows)]

    def dfs(x, y, node, word, score, path):
        if not (0 <= x < rows and 0 <= y < cols) or visited[x][y]:
            return

        ch = board[x][y].lower()
        if ch not in node.children:
            return

        visited[x][y] = True
        next_node = node.children[ch]
        new_word = word + ch
        new_score = score + scores[x][y]
        new_path = path + [(x, y)]

        if next_node.is_word and len(new_word) >= 2:
            if new_word not in found_words or new_score > found_words[new_word][0]:
                found_words[new_word] = (new_score, new_path)

        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx != 0 or dy != 0:
                dfs(x+dx, y+dy, next_node, new_word, new_score, new_path)

        visited[x][y] = False

    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie_root, "", 0, [])

    return found_words
