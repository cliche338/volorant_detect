import argparse
import os
import cv2
import subprocess
import threading

MODEL_PATH = 'runs/detect/train5/weights/best.pt'


def get_latest_predict_folder(base_folder):
    """
    找到 runs/detect 目錄下最新建立的 predict 資料夾
    """
    predict_folders = [f for f in os.listdir(base_folder) if f.startswith('predict')]
    if not predict_folders:
        return None
    latest_folder = max(predict_folders, key=lambda x: os.path.getctime(os.path.join(base_folder, x)))
    return os.path.join(base_folder, latest_folder)

def process_image(image_path):
    """處理單張圖片並從最新 predict 資料夾讀取"""
    print(f"正在處理檔案: {image_path}")

    # 執行 YOLO 預測命令（不修改 YOLO 輸出邏輯）
    command = f"yolo predict model={MODEL_PATH} source={image_path} classes=0 conf=0.3 iou=0.5 " 
    #classes : 表要的類別(0 : enemy, 1 : non)
    #conf    : 最低信心值門檻
    #iou     : 非極大值抑制（NMS）的 IoU 門檻

    subprocess.run(command, shell=True)  # 執行 YOLO 命令

    # 找到 YOLO 最新輸出資料夾（僅用於讀取）
    base_folder = os.path.join('runs', 'detect')
    latest_folder = get_latest_predict_folder(base_folder)
    if not latest_folder:
        print("未找到 YOLO 預測輸出資料夾！")
        return

    # 構造最新輸出圖片路徑
    output_image_path = os.path.join(latest_folder, os.path.basename(image_path).replace('.png', '.jpg'))
    print(f"從資料夾讀取結果: {output_image_path}")

    # 顯示圖片
    if os.path.exists(output_image_path):
        img = cv2.imread(output_image_path)
        cv2.imshow(f'Predicted: {os.path.basename(image_path)}', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"未找到結果：{output_image_path}")


def show_image(output_image_path, window_name):
    """以非阻塞方式顯示圖片"""
    if os.path.exists(output_image_path):
        img = cv2.imread(output_image_path)
        cv2.imshow(window_name, img)
        cv2.waitKey(1)  # 讓視窗立即顯示
    else:
        print(f"無法找到預測結果：{output_image_path}")
        

def process_folder(folder_path):
    """處理資料夾中的所有圖片"""
    if not os.path.exists(folder_path):
        print(f"資料夾 {folder_path} 不存在！")
        return

    # 遍歷資料夾中的所有圖片文件
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        
        # 只處理圖片檔案 (根據需要可以調整篩選格式)
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(image_path)


def process_video(video_path):
    """逐幀處理影片並即時顯示預測結果"""
    if not os.path.exists(video_path):
        print(f"影片檔案 {video_path} 不存在！")
        return

    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    threads = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1
        frame_image_path = f"temp_frame_{frame_num}.jpg"
        cv2.imwrite(frame_image_path, frame)

        # 將圖片處理交由執行緒
        thread = threading.Thread(target=process_image, args=(frame_image_path,))
        threads.append(thread)
        thread.start()

        # 刪除臨時幀圖片
        os.remove(frame_image_path)
        

    # 等待所有執行緒完成
    for thread in threads:
        thread.join()

    cap.release()
    cv2.destroyAllWindows()  # 確保視窗關閉


def main():
    # 設置命令行參數解析
    parser = argparse.ArgumentParser(description="使用YOLO模型進行圖片或影片預測")
    parser.add_argument('input_path', type=str, help="輸入的圖片、資料夾或影片路徑")
    parser.add_argument('model_path', type=str, help="訓練好的YOLO模型路徑")
    args = parser.parse_args()

    # 根據輸入的路徑處理不同情況
    input_path = args.input_path

    # 判斷輸入的是圖片、資料夾還是影片
    if os.path.isfile(input_path):  # 單個檔案
        if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):  # 圖片
            process_image(input_path)
        elif input_path.lower().endswith(('.mp4', '.avi', '.mov')):  # 影片
            process_video(input_path)
        else:
            print(f"無法處理的檔案類型：{input_path}")
    elif os.path.isdir(input_path):  # 資料夾
        process_folder(input_path)
    else:
        print(f"無效的路徑：{input_path}")
        

def parse_args():
    """解析命令行參數"""
    parser = argparse.ArgumentParser(description="YOLOv5 物件偵測")
    parser.add_argument("image", type=str, help="圖片檔案路徑")
    return parser.parse_args()

if __name__ == "__main__":
    # 解析命令行參數
    args = parse_args()
    
    # 呼叫處理函數
    process_image(args.image)

