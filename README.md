# 사진을 선화로 변환


## 소개

> opencv를 사용해 이미지 전처리로 사진을 선화로 변환

<br>

---

## 사용 툴
<p>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="7%">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/opencv/opencv-original-wordmark.svg" width="7%"/>
</p>

> python (opencv): 이미지 전처리

<br>

---

## 코드

```
    # 그레이스케일로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러로 노이즈 제거
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Laplacian 연산으로 미세한 에지 검출 (얇은 선)
    laplacian = cv2.Laplacian(blur, cv2.CV_8U, ksize=3)

    # 선 강조 (조금 더 날카롭게)
    _, binary = cv2.threshold(laplacian, 20, 255, cv2.THRESH_BINARY_INV)

    # 흰 배경 보장 (3채널로 확장해서 흰 바탕으로 출력)
    lineart = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    white_background = np.full_like(lineart, 255)
    result = np.where(lineart < 128, 0, 255)
```