import cv2
import mediapipe as mp
import time
import math 

# 1. Khởi tạo AI
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


pose_tracker = 0
FALL_TIME_THRESHOLD = 60 #2s
is_alert = False

cap = cv2.VideoCapture(0)
cv2.namedWindow('VGU Fall Detection Project', cv2.WINDOW_NORMAL)

print("--- HE THONG DANG CHAY (BAN NANG CAP PHAN BIET CUI/NGA) ---")
print("Nhan 'q' de thoat.")

# Hàm toán học tính góc Torso
def calculate_torso_angle(sh_y, sh_x, hip_y, hip_x):
    if hip_x == sh_x: return 90 # Tránh chia cho 0
    # Tính góc dựa trên tan = dY / dX
    angle_rad = math.atan2(abs(hip_y - sh_y), abs(hip_x - sh_x))
    return math.degrees(angle_rad)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    label_text = "Trang thai: Binh thuong"
    label_color = (0, 255, 0) # Xanh lá

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark
        
        # 1. Lấy tọa độ Y của Đầu và Hông để xét "Độ thấp"
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        y_hip_center = (left_hip.y + right_hip.y) / 2
        
        # 2. Lấy tọa độ Tâm Vai và Tâm Hông để tính Góc
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        y_shoulder_center = (left_shoulder.y + right_shoulder.y) / 2
        x_shoulder_center = (left_shoulder.x + right_shoulder.x) / 2
        x_hip_center = (left_hip.x + right_hip.x) / 2

        # 3. Tính độ thấp của đầu so với hông và GÓC TORSO
        head_to_hip_dist = abs(nose.y - y_hip_center)
        torso_angle = calculate_torso_angle(y_shoulder_center, x_shoulder_center, y_hip_center, x_hip_center)

        # --- LOGIC NHẬN DIỆN "THẬT" ---
        # 1. Đầu thấp so với hông (người nằm chĩa vào cam) HOẶC Góc Torso nằm ngang (< 30 độ)
        if head_to_hip_dist < 0.25 or torso_angle < 30:
            pose_tracker += 1
            label_text = "Canh bao: Co dau hieu Nga..."
            label_color = (0, 165, 255) # Màu cam
        else:
            pose_tracker = 0
            is_alert = False

        # 2. CHỈ xác nhận ngã nếu tư thế này được duy trì quá 2 giây
        if pose_tracker > FALL_TIME_THRESHOLD:
            is_alert = True

    # Hiển thị trạng thái lên góc màn hình
    cv2.putText(frame, label_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, label_color, 2)

    if is_alert:
        cv2.rectangle(frame, (0, 0), (640, 80), (0, 0, 255), -1)
        cv2.putText(frame, "CANH BAO: NGA THAT!", (150, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    
    cv2.imshow('VGU Fall Detection Project', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()