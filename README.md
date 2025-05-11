# WordBlitzAssistant 
相同的，以下內容為ChatGPT所寫

📌 WordBlitzAssistant – Auto-Aim Helper for Facebook Word Blitz 🔍
Description:
WordBlitzAssistant is an automated helper tool designed for the Facebook game Word Blitz. It captures screenshots of the 4x4 letter grid from the game board, reconstructs the board using letter template matching, and automatically finds all possible English words. It then simulates mouse movements to draw out high-scoring words based on their positions, enabling rapid plays and maximum firepower.

📦 Key Features:

✅ Visual Recognition:
Utilizes OpenCV and template matching techniques to automatically detect the 4x4 letter grid.

✅ Smart Search:
Employs a Trie structure to efficiently find all possible word combinations and sorts them by score.

✅ Auto Word Drawing:
Uses pyautogui to simulate mouse connections between letters, automatically inputting words into the game.

✅ Dictionary Filtering:
Speeds up the search process with a local dictionary file and pre-filtering steps.

✅ Error Prompts & Debugging:
Provides error messages when template detection fails, allowing parameter adjustments (e.g., threshold).

🛠️ Notes:

Letter template images must be prepared in the Capture/ folder, named as A.jpg, B.jpg, etc.

The words.txt dictionary can be replaced with any commonly used English word list.

If the board is not detected as a 4x4 grid, adjust the threshold or check the game screen alignment.

Requires word_finder.py and mouse_tracer.py modules to function properly.

📌 WordBlitzAssistant – 臉書單字爆爆自動瞄準助手
🔍 描述：
WordBlitzAssistant 是一款針對 Facebook 遊戲《Word Blitz》（單字爆爆）設計的自動輔助工具，能夠從螢幕截圖中辨識遊戲棋盤上的 4x4 字母方格，透過字母模板比對重建棋盤後，自動查找所有可組成的英文單字，並以滑鼠模擬方式依據字母位置自動劃出高分單字，實現快速出擊、火力全開。

📦 功能特色：
✅ 視覺辨識：利用 OpenCV 與模板匹配技術，自動偵測 4x4 字母方格。

✅ 智慧搜尋：採用 Trie 結構高效搜尋所有可組合的字詞，並根據分數排序。

✅ 自動劃字：使用 pyautogui 實現模擬滑鼠連線操作，自動在遊戲中輸入單字。

✅ 字典過濾：搭配本地字典檔與預篩選步驟，加快搜尋速度。

✅ 錯誤提示與除錯調整：遇到模板偵測失敗可依錯誤提示調整參數（如 threshold）。

🛠️ 注意事項：
1. 字母模板圖片需事先準備於 Capture/ 資料夾，命名為 A.jpg、B.jpg 等。
2. 搭配的 words.txt 字典可自行更換（支援常見英文詞庫）。
3. 若棋盤偵測錯誤（非 4x4），請調整 threshold 或檢查遊戲畫面對齊度。
4. 須搭配 word_finder.py 與 mouse_tracer.py 模組一同運作。



