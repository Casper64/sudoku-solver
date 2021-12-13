import sudoku_generator
import numpy as np
import sys
import cv2
import pytesseract
import re
import json

def get_area(cnt):
    (x,y), (width, height), theta = cv2.minAreaRect(cnt)
    return width*height

def get_center(cnt):
    (x,y), (width, height), theta = cv2.minAreaRect(cnt)
    return (x+width/2, y+height/2)

def put_into_grid(row, col, number):
    sudoku_generator.grid[row][col] = int(number[0])

def get_contours(img, original_img, gray_img):
    # Get a black and white image and apply it as mask so the numbers will be easier recognized
    (_, black_white) = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areas = [get_area(cnt) for cnt in contours]
    container_area = max(areas)
    container = areas.index(container_area)
    (cx, cy, cw, ch) = cv2.boundingRect(contours[container])
    # print(cx, cy, cw, ch)
    cv2.drawContours(original_img, contours[container], -1, (0, 0, 255), 2)
    box_size = max(cw, ch) / 9

    big_squares_area = container_area/100
    small_squares_area = container_area/10  

    count = 0
    for index, cnt in enumerate(contours):
        print(f"{index} / {len(contours)}")
        (x, y, w, h) = cv2.boundingRect(cnt)
        area = get_area(cnt)

        # The 9 square have an area of approximately container_area/10 
        # So the little square have an area of approximateley container_area/100
        if area >= big_squares_area and area <= small_squares_area:
            # cv2.drawContours(original_img, cnt, -1, (255, 0, 0), 2)
            cropped = black_white[y:y+h, x:x+w]
            cropped_gray = gray_img[y:y+h, x:x+w]
            contrast = cropped_gray.std()
            if contrast < 25:
                continue

            count += 1
        
            # Extract the number out of the current square if there is one
            data = pytesseract.image_to_string(cropped, config="--psm 6 --psm 13") 
            if result := re.findall(r'\d', data):
                cv2.drawContours(original_img, cnt, -1, (0, 255, 0), 2)

                # Put into the grid
                # x, y = get_center(cnt)
                # Transform coordinates
                # Correction a bit extra to compensate for the thicker lines
                correction = box_size / 3
                x -= cx - correction
                y -= cy - correction
                # print(x, y)
                row = int(y // box_size)
                col = int(x // box_size)

                # img_copy = ResizeWithAspectRatio(original_img, height=720)
                # cv2.imshow("Sudoku", img_copy)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                put_into_grid(row, col, result)

def grid_splitted(img, original_img, gray_img):
    (_, black_white) = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    (w, h) = img.shape
    box_size = int(max(w, h) / 9)
    small_area = pow(box_size, 2) / 3
    big_area = pow(box_size*3, 2) 

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # for cnt in contours:
    #     area = get_area(cnt)
    #     if area > small_area and area < big_area:
    #         (x, y, w, h) = cv2.boundingRect(cnt)
    #         if min(w,h)/max(w,h) < 0.9:
    #             continue
    #         cv2.rectangle(original_img, (x, y), (x+box_size, y+box_size), (0,255,0), 1)

    #         # img_copy = ResizeWithAspectRatio(original_img, height=720)
    #         # cv2.imshow("Sudoku", img_copy)
    #         # cv2.waitKey(0)
    #         # cv2.destroyAllWindows()
    # return

    index = 0
    for cnt in contours:
        print(f"{index} / {len(contours)}")
        index += 1

        area = get_area(cnt)
        if area > small_area and area < big_area:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if min(w,h)/max(w,h) < 0.9:
                continue

            cropped = black_white[y:y+box_size, x:x+box_size]

            # Extract the number out of the current square if there is one
            data = pytesseract.image_to_string(cropped, config="--psm 6 --psm 13") 

            # img_copy = ResizeWithAspectRatio(original_img, height=720)
            # cv2.imshow("Sudoku", img_copy)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            if result := re.findall(r'\d', data):
                cv2.rectangle(original_img, (x, y), (x+box_size, y+box_size), (0,255,0), 1)
                x += box_size/2
                y += box_size/2
                row = int(y // box_size)
                col = int(x // box_size)
                put_into_grid(row, col, result)

                


def process_image():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        print("Input image!")
        sys.exit(1)

    img = cv2.imread(path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 3)
    img_canny = cv2.Canny(img_blur, 50, 50)
    img_copy = img.copy()

    grid_splitted(img_canny, img_copy, img_blur)

    # get_contours(img_canny, img_copy, img_blur)
    img_copy = ResizeWithAspectRatio(img_copy, height=720)

    # cv2.imshow("Sudoku", img_copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



# https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def main():
    process_image()
    # json_data = json.dumps(sudoku_generator.grid.tolist())
    print("Array")
    print(sudoku_generator.grid)
    print("End")

if __name__ == "__main__":
    main()
    