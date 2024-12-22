上次修改 : 241219

- code_main.py 

    完全體
        使用方法 : 
            train模型在import下面改 目前有 train train2
            python code_main.py (圖片、資料夾、影片路徑)

- code_main_copy.py

    複製
        單純用來保存最原始版本
            用法跟code_main.py一樣

- code_img_detect.py
- code_video_detect.py

    為其他測試版本
        使用方法 : 
            在程式碼內修改圖片或影片路徑 也可以修改.xml檔案選擇主要偵測部分 修改完存檔執行

- Dataset

    先整理好圖片集
    再用labelImg自己框 (要用系統管理員身份打開labelImg.exe 不然會閃退)
    框選好分類+把.xml檔整理到一個資料夾
    就可以按照下面去分類 開始轉檔

- code_VtoY.py

    將.xml檔案轉成.txt檔案 這樣才能讓yolo辨識讀取
    轉換完就可以開始訓練了

- Train

    準備好dataset, 內容物必須包含
        dataset/
        ├── train/
        │   ├── images/
        │   │   ├── img1.jpg
        │   │   ├── img1.txt
        │   │   ├── img2.jpg
        │   │   ├── img2.txt
        │   
        ├── val/
        │   ├── images/
        │   │   ├── img3.jpg
        │   │   ├── img3.txt
        |   |   ├── img4.jpg
        │   |   ├── img4.txt

                準備好之後 輸入 yolo train model=yolov5s.pt data=data.yaml epochs=50 開始訓練
                訓練完之後 輸入 yolo predict model=runs/detect/<project_name>/best.pt source=path/to/test/images (路徑要改)
                    偵測完的檔案會跑到detect下 (code_main.py全包好了還有show)


