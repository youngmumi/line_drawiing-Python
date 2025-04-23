import cv2
import numpy as np
import os
import glob

# 입력 및 출력 폴더 설정
input_folder = './picture'
output_folder = './picture/output'
os.makedirs(output_folder, exist_ok=True)

# 이미지 확장자 목록
extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']

# 모든 이미지 경로 수집
image_paths = []
for ext in extensions:
    image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

# 각 이미지 처리
for img_path in image_paths:
    # 이미지 읽기
    img = cv2.imread(img_path)
    if img is None:
        print(f"이미지를 열 수 없습니다: {img_path}")
        continue

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

    # 파일 저장
    base_name = os.path.basename(img_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_folder, f"{name}_lineart{ext}")
    cv2.imwrite(output_path, result)

    print(f"저장 완료: {output_path}")
