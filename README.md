# -Graphics
Cnu Computer Graphics Homework

HW5: harris corner Detection

<img width="349" alt="hw5결과" src="https://user-images.githubusercontent.com/44044119/209357867-7e679c3e-ef5d-4299-ae17-63a757eef81b.PNG">

HW6 : Harris Corner Detection
- 설명 : integral 사용과 integral 사용하지 않았을 때의 Harris Corner Detection

<img width="391" alt="hw6결과" src="https://user-images.githubusercontent.com/44044119/209358461-bc87e56f-42c9-4f85-b3aa-b92e157de7a4.PNG">

HW7: SIFT

SIFT 과정
- Multi-scale extrema detection
- Keypoint localization
- Orientation assignment
- Keypoint descriptor

과제
- Multi-scale extrema detection과 Keypoint localization은 구현하지 않고 harris corner에서 얻은 keypoint를 사용
- Orientation assignment와 Keypoint descriptor를 구현하여 matching을 하는 것이 목표

<img width="470" alt="hw7결과" src="https://user-images.githubusercontent.com/44044119/209358915-43d1fd34-2961-4555-85df-bd5f390df8d6.PNG">

HW9: RANSAC

과제
- RANSAC을 이용하여 affine transform하여 결과를 확인하기

RANSAC을 이용한 affine transform
- 랜덤하게 n개의 point를 결정한다.
- Point를 이용하여 affine matrix를 구하기
* 실습에는 모든 point를 사용하여 affine matrix를 구함
- 현재 얻은 affine matrix의 inlier의 수를 구하기
* Inlier의 개수를 고르기 위해서 L2 distance 사용
- 3가지 단계를 m번 반복하여 가장 많은 inlier를 가지고 있는 affine matrix를 채택함

<img width="341" alt="hw9결과" src="https://user-images.githubusercontent.com/44044119/209359511-ac7ff4a4-7ef1-49d8-b0ec-f2cc95ab6281.PNG">

HW10: Brute-Force Descriptor Matcher와 Gaussian Backward

Brute-Force Matching 과정
1. 원본 이미지과 목표 이미지에서의 특징점(Keypoints)과 특징기술자(Descriptors)를 각각 구한다.
2. 원본 이미지에서의 특징 기술자의 집합을 𝐷1 ∈ ℝ𝑁1 × 𝐶, 목표 이미지에서의 특징 기술자의 집합을 𝐷2 ∈ ℝ𝑁2 × 𝐶
(𝑁1: 원본 이미지에서의 Keypoint 개수, 𝑁2: 목표 이미지에서의 Keypoint 개수, 𝐶 : 특징 기술자의 차원)이라고 하자.
3. 원본 이미지의 각 특징점에 대한 특징 기술자와 목표 이미지에서의 모든 특징 기술자와의 𝐿2 𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒를 구한다.
4. 그 거리 값이 최솟값일 때의 특징점들을 매칭한다.

Gaussian backward 구현
- 역행렬을 사용하여 얻은 원본 이미지의 좌표에서 bilinear interpolation을 수행하기 전에 주변 이웃 픽셀 값도 같이 고려(이미지 필터링)
- 이때 filter로 gaussian filter를 사용
- 변환된 좌표의 주변 픽셀도 bilinear interpolation 수행 후 각 위치에 있는 filter 값을 곱해서 모두 더함

<img width="344" alt="hw10결과_1" src="https://user-images.githubusercontent.com/44044119/209360470-16edeafd-a39e-4bec-a9f8-500679db9bb1.PNG">
<img width="333" alt="hw10결과_2" src="https://user-images.githubusercontent.com/44044119/209360506-ca4e1ffa-4646-4057-b122-a721e5dbdbdc.PNG">


