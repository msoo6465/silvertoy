import cv2

cap = cv2.VideoCapture(-1)

while True:
    ret, frame = cap.read()
    print(frame.shape)
    break

    if not ret:
        break

    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)

    if key == ord('Q') or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()