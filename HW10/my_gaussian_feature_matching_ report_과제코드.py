import numpy as np
import cv2
import random
from cv2 import DMatch

def my_padding(src, filter):
    (h, w, c) = src.shape
    h_pad, w_pad = filter.shape
    h_pad = h_pad // 2
    w_pad = w_pad // 2
    padding_img = np.zeros((h+h_pad*2, w+w_pad*2, c))
    padding_img[h_pad:h+h_pad, w_pad:w+w_pad] = src

    # repetition padding
    # up
    padding_img[:h_pad, w_pad:w_pad + w] = src[0, :]
    # down
    padding_img[h_pad + h:, w_pad:w_pad + w] = src[h - 1, :]
    # left
    padding_img[:, :w_pad] = padding_img[:, w_pad:w_pad + 1]
    # right
    padding_img[:, w_pad + w:] = padding_img[:, w_pad + w - 1:w_pad + w]
    return padding_img

def my_bilinear(img, x, y):
    floorX, floorY = int(x), int(y)

    t, s = x - floorX, y - floorY

    zz = (1 - t) * (1 - s)
    zo = t * (1 - s)
    oz = (1 - t) * s
    oo = t * s

    interVal = img[floorY, floorX, :] * zz + img[floorY, floorX + 1, :] * zo + \
               img[floorY + 1, floorX, :] * oz + img[floorY + 1, floorX + 1, :] * oo

    return interVal

def backward(img1, img2, M):
    h, w, c = img2.shape
    h1, w1, c = img1.shape
    result = np.zeros((h, w, c))

    for row in range(h):
        for col in range(w):
            xy = (np.linalg.inv(M)).dot(np.array([[col, row, 1]]).T)

            x_ = xy[0, 0]
            y_ = xy[1, 0]

            if x_ < 0 or y_ < 0 or (x_ + 1) >= w1 or (y_ + 1) >= h1:
                continue

            result[row, col, :] = my_bilinear(img1, x_, y_)

    return result

def my_ls(matches, kp1, kp2):
    A = []
    B = []
    for idx, match in enumerate(matches):
        trainInd = match.trainIdx
        queryInd = match.queryIdx

        x, y = kp1[queryInd].pt
        x_prime, y_prime = kp2[trainInd].pt

        A.append([x, y, 1, 0, 0, 0])
        A.append([0, 0, 0, x, y, 1])
        B.append([x_prime])
        B.append([y_prime])

    A = np.array(A)
    B = np.array(B)

    try:
        ATA = np.dot(A.T, A)
        ATB = np.dot(A.T, B)
        X = np.dot(np.linalg.inv(ATA), ATB)

    except:
        print('can\'t calculate np.linalg.inv((np.dot(A.T, A)) !!!!!')
        X = None
    return X

def my_get_Gaussian_filter(fshape, sigma=1):
    (f_h, f_w) = fshape
    y, x = np.mgrid[-(f_h // 2): (f_h // 2) + 1, -(f_w // 2): (f_w // 2) + 1]

    scalar = 1 / (2 * np.pi * sigma ** 2)
    exponential = np.exp(-((x ** 2 + y ** 2) / (2 * sigma ** 2)))
    mask = scalar * exponential
    gaussian_mask = mask / np.sum(mask)

    return gaussian_mask

def L2_distance(vector1, vector2):
    return np.sqrt(np.sum((vector1 - vector2) ** 2))

def my_feature_matching(des1, des2):
    ##########################################
    # TODO Brute-Force Feature Matching 구현
    # matches: cv2.DMatch의 객체를 저장하는 리스트
    # cv2.DMatch의 배열로 구성
    # cv2.DMatch:
    # trainIdx: img1의 kp1, des1에 매칭되는 index
    # queryIdx: img2의 kp2, des2에 매칭되는 index
    # kp1[queryIdx]와 kp2[trainIdx]는 매칭된 점
    # return 값 : matches
    ##########################################

    matches = list()
    dist_arr = list()
    for i in range(len(des1)):
        for j in range(len(des2)):
            dist_arr.append(L2_distance(des1[i], des2[j]))
        min_dist = np.min(dist_arr)
        matches.append(cv2.DMatch(i, np.argmin(dist_arr), 0, min_dist))
        dist_arr = list()

    return matches

def get_matching_keypoints(img1, img2, keypoint_num):
    '''
    :param img1: 변환시킬 이미지
    :param img2: 변환 목표 이미지
    :param keypoint_num: 추출한 keypoint의 수
    :return: img1의 특징점인 kp1, img2의 특징점인 kp2, 두 특징점의 매칭 결과
    '''
    sift = cv2.SIFT_create(keypoint_num)

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    ##########################################
    # TODO Brute-Force Feature Matching 구현
    ##########################################

    my_matches = my_feature_matching(des1, des2)

    ############################################################
    # TODO TEST 내장 함수를 사용한 것과 직접 구현 것의 결과 비교
    # 다음 3가지 중 하나라도 통과하지 못하면 잘못 구현한것으로 판단하여 프로그램 종료
    # 오류가 없다면 "매칭 오류 없음" 출력
    bf = cv2.BFMatcher_create(cv2.NORM_L2)
    matches = bf.match(des1, des2)
    # 1. 매칭 개수 비교
    assert len(matches) == len(my_matches)
    # 2. 매칭 점 비교
    for i in range(len(matches)):
        if (matches[i].trainIdx != my_matches[i].trainIdx) \
                or (matches[i].queryIdx !=
                                        my_matches[i].queryIdx):
            print("matching error")
            return

    # 3. distance 값 비교
    for i in range(len(matches)):
        if int(matches[i].distance) != int(my_matches[i].distance):
            print("distance calculation error")
            return

    print("매칭 오류 없음")
    ##########################################################

    # DMatch 객체에서 distance 속성 값만 가져와서 정렬
    my_matches = sorted(my_matches, key=lambda x: x.distance)
    # 매칭된 점들 중 20개만 가져와서 표시
    result = cv2.drawMatches(img1, kp1, img2, kp2, my_matches[:20], outImg=None, flags=2)

    cv2.imshow('My BF matching result', result)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return kp1, kp2, my_matches

def feature_matching_RANSAC(img1, img2, keypoint_num=None, iter_num=500, threshold_distance=5, check=1):
    '''
    :param img1: 변환시킬 이미지
    :param img2: 변환 목표 이미지
    :param keypoint_num: sift에서 추출할 keypoint의 수
    :param iter_num: RANSAC 반복횟수
    :param threshold_distance: RANSAC에서 inlier을 정할때의 거리 값
    :return: RANSAC을 이용하여 변환 된 결과
    '''

    kp1, kp2, matches = get_matching_keypoints(img1, img2, keypoint_num)

    matches_shuffle = matches.copy()

    inliers = []  # 랜덤하게 고른 n개의 point로 구한 inlier개수 결과를 저장
    M_list = []  # 랜덤하게 고른 n개의 point로 만든 affine matrix를 저장
    for i in range(iter_num):
        random.shuffle(matches_shuffle)
        three_points = matches_shuffle[:3]
        X = my_ls(three_points, kp1, kp2)
        M = np.array([[X[0][0], X[1][0], X[2][0]],
                      [X[3][0], X[4][0], X[5][0]],
                      [0, 0, 1]])
        M_list.append(M)
        inliers.append(0)
        for idx, match in enumerate(matches):
            trainInd = match.trainIdx
            queryInd = match.queryIdx

            x1, y1 = kp1[queryInd].pt
            array1 = np.array([x1, y1, 1]).T
            prime_array = np.dot(M, array1)
            x2, y2 = kp2[trainInd].pt
            vector1 = np.array([prime_array[0], prime_array[1]])
            vector2 = np.array([x2, y2])
            distance = L2_distance(vector1, vector2)
            if (distance < threshold_distance):
                inliers[i] += 1

    max_index = np.argmax(inliers)
    best_M = M_list[max_index]

    if check == 1:
        result = backward(img1, img2, best_M)
    elif check == 2:
        result = gaussian_backward(img1, img2, best_M)

    return result.astype(np.uint8)

def gaussian_backward(img1, img2, M):
    '''
    :param img1: 변환시킬 이미지
    :param M: 변환 matrix
    :return: 변환된 이미지
    '''
    fsize = 3
    sigma = 3
    filter = my_get_Gaussian_filter((fsize, fsize), sigma)

    h, w, c = img2.shape
    h1, w1, c1 = img1.shape
    result = np.zeros((h, w, c))
    f_h, f_w = filter.shape
    pad_img = my_padding(img1, filter)


    for row in range(h):
        for col in range(w):
            xy = (np.linalg.inv(M)).dot(np.array([[col, row, 1]]).T)

            x_ = xy[0, 0]
            y_ = xy[1, 0]

            for i in range(f_h):
                for j in range(f_w):
                    new_x = x_ + i
                    new_y = y_ + j
                    if new_x < 0 or new_y < 0 or (new_x + 1) >= w1 or (new_y + 1) >= h1:
                        continue
                    result[row, col, :] += my_bilinear(pad_img, new_x, new_y) * filter[i, j]
    return result.astype(np.uint8)

def feature_matching_gaussian(img1, img2, keypoint_num=None, iter_num=500, threshold_distance=5):
    '''
    :param img1: 변환시킬 이미지
    :param img2: 변환 목표 이미지
    :param keypoint_num: sift에서 추출할 keypoint의 수
    :param iter_num: RANSAC 반복횟수
    :param threshold_distance: RANSAC에서 inlier을 정할때의 거리 값
    :return: RANSAC을 이용하여 변환 된 결과
    '''

    result = feature_matching_RANSAC(img1, img2, keypoint_num, iter_num, threshold_distance, 2)

    return result.astype(np.uint8)


def main():
    src = cv2.imread('Lena.png')
    src = cv2.resize(src, None, fx=0.5, fy=0.5)
    src2 = cv2.imread('Lena_transforms.png')

    result = feature_matching_RANSAC(src, src2)
    gussian_result = feature_matching_gaussian(src, src2)

    cv2.imshow("input", src)
    cv2.imshow("goal", src2)
    cv2.imshow('201802101_result', result)
    cv2.imshow('201802101_gaussian result', gussian_result)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
