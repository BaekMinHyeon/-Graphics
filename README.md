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
*실습에는 모든 point를 사용하여 affine matrix를 구함
- 현재 얻은 affine matrix의 inlier의 수를 구하기
* Inlier의 개수를 고르기 위해서 L2 distance 사용
- 3가지 단계를 m번 반복하여 가장 많은 inlier를 가지고 있는 affine matrix를 채택함

<img width="341" alt="hw9결과" src="https://user-images.githubusercontent.com/44044119/209359511-ac7ff4a4-7ef1-49d8-b0ec-f2cc95ab6281.PNG">
