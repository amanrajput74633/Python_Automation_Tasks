import cv2
from cvzone.FaceDetectionModule import FaceDetector

def capture_face(prompt_key, detector, cap):
    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f"Press '{prompt_key.upper()}' to capture", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)
        if key == ord(prompt_key.lower()):
            return frame.copy()
        elif key == ord('q'):
            return None

def face_swap(face1, face2, detector):
    face1 = cv2.resize(face1, (640, 480))
    face2 = cv2.resize(face2, (640, 480))

    face1_detected, bboxs1 = detector.findFaces(face1)
    face2_detected, bboxs2 = detector.findFaces(face2)

    if bboxs1 and bboxs2:
        x1, y1, w1, h1 = map(int, bboxs1[0]['bbox'])
        x2, y2, w2, h2 = map(int, bboxs2[0]['bbox'])

        crop1 = face1[y1:y1+h1, x1:x1+w1]
        crop2 = face2[y2:y2+h2, x2:x2+w2]

        target_w = min(w1, w2)
        target_h = min(h1, h2)

        crop1_resized = cv2.resize(crop1, (target_w, target_h))
        crop2_resized = cv2.resize(crop2, (target_w, target_h))

        end_y1 = min(y1 + target_h, face1.shape[0])
        end_x1 = min(x1 + target_w, face1.shape[1])
        end_y2 = min(y2 + target_h, face2.shape[0])
        end_x2 = min(x2 + target_w, face2.shape[1])

        face1[y1:end_y1, x1:end_x1] = crop2_resized
        face2[y2:end_y2, x2:end_x2] = crop1_resized

        cv2.imshow("Swapped Face 1", face1)
        cv2.imshow("Swapped Face 2", face2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Face not detected in one or both photos.")

# Main Execution
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    print("📸 Face Swapper Ready!")
    print("➡ Press 's' to take Face 1")
    print("➡ Press 'd' to take Face 2")
    print("➡ Press 'q' to quit")

    while True:
        face1 = capture_face('s', detector, cap)
        if face1 is None:
            break

        print("✅ Face 1 captured.")

        face2 = capture_face('d', detector, cap)
        if face2 is None:
            break

        print("✅ Face 2 captured. Swapping...")
        face_swap(face1, face2, detector)

        print("🔁 Press 'q' to quit or any other key to continue.")
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
