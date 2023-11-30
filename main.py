import cv2 as cv
import numpy as np


def video_matrix(n_row, n_col, nth_row, nth_col, cam_width, cam_height, frame):
    """
    N x M matrix

    Example: 3 x 3 matrix
        1   2   3
    1 |   |   |   |
    2 |   |   |   |
    3 |   |   |   |

    :param n_row: number of rows
    :param n_col: number of columns
    :param nth_row: chosen row to output
    :param nth_col: chosen column to output
    :return: return chosen video feed
    """
    portion_width = cam_width // n_col
    portion_height = cam_height // n_row

    y2 = int(portion_height * nth_row)
    y1 = int(y2 - portion_height)

    x2 = int(portion_width * nth_col)
    x1 = int(x2 - portion_width)

    roi = frame[y1:y2, x1:x2]
    return roi, y1, y2, x1, x2


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation=cv.INTER_AREA)


if __name__ == '__main__':
    camera = cv.VideoCapture(0)

    cam_width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
    cam_height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))

    n_row = 3
    n_col = 3
    nth_row = 2
    nth_col = 3

    if not camera.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture the video frame by frame
        ret, original = camera.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # OPERATIONS
        roi, y1, y2, x1, x2 = video_matrix(n_row, n_col, nth_row, nth_col, cam_width, cam_height, original)
        cv.putText(original, "Press 'Q' to quit", (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv.rectangle(original, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # SHOW OUTPUT
        cv.imshow('Original', original)
        roi_rescaled = rescale_frame(roi, percent=n_row*100)
        cv.imshow('Region of Interest', roi_rescaled)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv.destroyAllWindows()
