import cv2 as cv
import numpy as np

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


def alignImages(im1, im2):
    # Chuyển ảnh màu sang ảnh grayscale
    im1Gray = cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
    im2Gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)

    # Tạo đối tượng ORB với số lượng điểm đặc trưng tối đa
    orb = cv.ORB_create(MAX_FEATURES)
    a=orb.shape()
    print(a)
    # Tìm kiếm và tính toán điểm đặc trưng và mô tả của ảnh 1 và ảnh 2
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Tạo bộ matcher để so khớp các điểm đặc trưng
    matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    # So khớp các mô tả của ảnh 1 và ảnh 2
    matches = matcher.match(descriptors1, descriptors2, None)
    matches = list(matches)

    # Sắp xếp các đối tượng khớp theo khoảng cách tăng dần
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Chọn số lượng khớp tốt nhất dựa trên tỷ lệ đã cho
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Vẽ các khớp trên ảnh gốc và lưu lại
    imMatches = cv.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv.imwrite("matches.jpg", imMatches)

    # Lấy các điểm ảnh từ các khớp tìm được
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Tìm ma trận homography bằng phương pháp RANSAC
    h, mask = cv.findHomography(points1, points2, cv.RANSAC)

    # Lấy chiều cao, chiều rộng và số kênh của ảnh đích
    height, width, channels = im2.shape
    # Biến đổi ảnh gốc sử dụng ma trận homography để đưa ảnh về cùng một khung cảnh với ảnh đích
    im1Reg = cv.warpPerspective(im1, h, (width, height))

    return im1Reg


if __name__ == '__main__':
    refFilename = None  # Đường dẫn ảnh tham chiếu
    imReference = cv.imread(refFilename, cv.IMREAD_COLOR)

    imFilename = None  # Đường dẫn ảnh cần điều chỉnh
    im = cv.imread(imFilename, cv.IMREAD_COLOR)

    print("Aligning images ...")

    # Điều chỉnh ảnh và lấy ma trận homography
    imReg, h = alignImages(im, imReference)
    # Thay đổi kích thước ảnh điều chỉnh thành kích thước mong muốn
    imReg = cv.resize(imReg, (224, 224))

    outFilename = "aligned.jpg"
    # Hiển thị ảnh điều chỉnh
    cv.imshow(outFilename, imReg)
    cv.waitKey(0)
