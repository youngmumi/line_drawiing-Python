import cv2
import os
import glob

# 입력 폴더와 출력 폴더 설정
input_folder = './picture'
output_folder = './picture/output'
os.makedirs(output_folder, exist_ok=True)

# 이미지 확장자 목록 (필요하면 추가 가능)
extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']

# 모든 이미지 파일 경로 가져오기
image_paths = []
for ext in extensions:
    image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

# 이미지 처리 반복
for img_path in image_paths:
    # 이미지 불러오기
    img = cv2.imread(img_path)
    if img is None:
        print(f"이미지를 열 수 없습니다: {img_path}")
        continue

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Bilateral Filtering으로 노이즈 제거 및 경계 유지
    bilateral = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # 3. Sobel 필터로 에지 감지 (세밀한 경계)
    sobel_x = cv2.Sobel(bilateral, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(bilateral, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edge = cv2.magnitude(sobel_x, sobel_y)

    # 4. Canny Edge Detection (세밀한 선 강조를 위한 Canny 추가)
    canny_edge = cv2.Canny(bilateral, threshold1=50, threshold2=150)

    # 5. Sobel와 Canny를 결합하여 더욱 세밀한 에지 생성
    combined_edges = cv2.bitwise_or(sobel_edge.astype('uint8'), canny_edge)

    # 6. 선을 반전시켜 흰 배경, 검은 선으로 만들기
    line_art = cv2.bitwise_not(combined_edges)

    # 7. 샤프닝을 적용하여 선을 더 선명하게 만들기 (선택적으로 줄임)
    sharpened = cv2.addWeighted(line_art, 1.2, line_art, -0.2, 0)  # 샤프닝 강도를 낮춤

    # 8. Adaptive Thresholding을 통해 세밀한 선 강조
    adapt_thresh = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 11, 5)  # 임계값을 다소 넓게 설정

    # 9. 최종 이미지 (세밀하게 강조된 선화)
    final_result = cv2.bitwise_not(adapt_thresh)

    # 10. 선 굵기를 얇게 하기 위해 dilate를 제거 (선 두께를 얇게 유지)
    # final_result = cv2.dilate(final_result, None, iterations=1)  # 이 부분을 제거하여 얇은 선을 유지

    # 11. 흰 배경 만들기 (반전된 결과에 흰색 배경을 추가)
    final_result_with_white_bg = cv2.bitwise_not(final_result)

    # 저장 파일 이름 구성
    base_name = os.path.basename(img_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_folder, f"{name}_lineart{ext}")

    # 선화 이미지 저장
    cv2.imwrite(output_path, final_result_with_white_bg)
    print(f"저장 완료: {output_path}")
