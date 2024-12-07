import tkinter as tk
import random
from PIL import Image, ImageTk

# 기본 창 설정
root = tk.Tk()
root.title("탕후루 만들기 게임")
root.geometry("600x600")
root.config(bg="LightSteelBlue")

# 타이머 표시
time_left = 60
timer_label = tk.Label(root, text="남은 시간: 60", font=("교보 손글씨 2019", 18), bg="LightSteelBlue")
timer_label.pack(pady=5)

# 게임 화면
center_frame = tk.Frame(root, bg="LightSteelBlue", width=400, height=400)
center_frame.pack(expand=True, fill="both", padx=5, pady=5)

# 만들고 있는 탕후루 섹션
current_section = tk.Frame(center_frame, bg="LightSteelBlue")
current_section.pack(side=tk.LEFT, padx=20, pady=10, fill="y")

current_label = tk.Label(current_section, text="만들고 있는 탕후루", font=("교보 손글씨 2019", 14), bg="LightSteelBlue")
current_label.pack(pady=5)

current_tanghuru = tk.Frame(current_section, width=100, height=300)
current_tanghuru.pack(pady=10, expand=True, fill="both")

# 만들어야 할 탕후루 섹션
goal_section = tk.Frame(center_frame, bg="LightSteelBlue")
goal_section.pack(side=tk.RIGHT, padx=20, pady=10, fill="y")

goal_label = tk.Label(goal_section, text="만들어야 할 탕후루", font=("교보 손글씨 2019", 14), bg="LightSteelBlue")
goal_label.pack(pady=5)

goal_tanghuru = tk.Frame(goal_section, width=100, height=300)
goal_tanghuru.pack(pady=10, expand=True, fill="both")

# 재료 버튼
ingredients_frame = tk.Frame(root)
ingredients_frame.pack(side=tk.BOTTOM, pady=20)

ingredients = ["딸기", "청포도", "포도", "귤"]
buttons = []
current_ingredients = []  # 현재 탕후루 재료 리스트

for ingredient in ingredients:
    button = tk.Button(ingredients_frame, text=ingredient, font=("교보 손글씨 2019", 14), width=10, height=2, background="LightSteelBlue", activeforeground="SteelBlue")
    button.pack(side=tk.LEFT, padx=10, pady=10)
    buttons.append(button)

# 화면 중앙에 결과 O, X 표시
result_display = tk.Label(root, font=("교보 손글씨 2019", 40), bg="LightSteelBlue", width=5, height=2)
result_display.place(relx=0.5, rely=0.5, anchor="center")

# 점수 레이블
score = 0
score_label = tk.Label(root, text="현재 점수: 0", bg="LightSteelBlue", font=("교보 손글씨 2019", 16))
score_label.place(relx=0.5, rely=0.25, anchor="center")

# 기회 레이블
lives = 3
lives_label = tk.Label(root, text="남은 기회: 3", bg="LightSteelBlue", font=("교보 손글씨 2019", 16))
lives_label.place(relx=0.5, rely=0.3, anchor="center")


### 여기까지 화면 설계 ###
### 아래부터 기능 설계 ###

# 이미지 로드 함수
def load_image(image_path, width=50, height=50):  # 이미지 크기 조정
    try:
        image = Image.open(image_path)
        image = image.resize((width, height))
        return ImageTk.PhotoImage(image)
    except FileNotFoundError:
        print(f"Error: {image_path} not found.")
        return None

game_running = True # 게임 상태 확인
timer_id = None # 타이머 중복 방지

# 타이머 업데이트 함수
def update_timer():
    global time_left, timer_id
    if game_running and time_left > 0:
        time_left -= 1

        # 남은 시간이 10초 이하일 경우 글씨 색을 빨간색으로 변경
        if time_left <= 10:
            timer_label.config(text=f"남은 시간: {time_left}", fg="red")
        else:
            timer_label.config(text=f"남은 시간: {time_left}", fg="black")

        # 기존 예약 작업 취소 후 새 작업 예약
        if timer_id is not None:
            root.after_cancel(timer_id)  # 기존 작업 취소
        timer_id = root.after(1000, update_timer)  # 새 작업 예약
    else:
        game_over()  # 시간이 다 되면 게임 종료
        timer_id = None  # 타이머 ID 초기화

# 문제 출제 함수
def generate_problem():
    global goal_ingredients
    
    # 재료를 랜덤으로 1~5개 선택 (중복 가능)
    num_ingredients = random.randint(1, 5)
    goal_ingredients = [random.choice(ingredients) for _ in range(num_ingredients)]
    
    random.shuffle(goal_ingredients)  # 섞기
    
    # 섞인 재료의 이미지 파일을 오른쪽 화면에 표시
    images = []
    for ingredient in goal_ingredients:
        img_path = f"img/{ingredient}.png"  # img 폴더 내의 이미지 파일 경로
        img = load_image(img_path)
        images.append(img)
    
    # 기존 이미지를 지우고 새로운 이미지를 표시
    for widget in goal_tanghuru.winfo_children():
        widget.destroy()
    
    # 이미지들을 아래에서 위로 배치
    for img in images:
        label = tk.Label(goal_tanghuru, image=img)
        label.image = img  # reference to keep the image object alive
        label.pack(side=tk.BOTTOM, pady=3)  # 아래에서 위로 배치
    
    return goal_ingredients  # 목표 재료 리스트 반환

# 탕후루 만들기
def make_tanghuru(ingredient):
    global current_ingredients, goal_ingredients, score, lives

    # 만들고 있는 탕후루에 보여주기
    img_path = f"img/{ingredient}.png"  # img 폴더 내의 이미지 파일 경로
    img = load_image(img_path)
    label = tk.Label(current_tanghuru, image=img)
    label.image = img
    label.pack(side=tk.BOTTOM, pady=3)  # 아래에서 위로 배치
    
    # 재료를 추가한 후, 목표 재료의 첫 번째와 비교
    if goal_ingredients and ingredient == goal_ingredients[0]:
        # 맞는 재료일 경우 추가
        current_ingredients.append(ingredient)

        # 목표 재료 리스트에서 첫 번째 재료 제거
        goal_ingredients.pop(0)

        # 만약 목표 재료 리스트가 비었으면
        if not goal_ingredients:
            # 목표 탕후루의 재료 개수만큼 점수 추가
            score += len(current_ingredients)
            score_label.config(text=f"현재 점수: {score}")

            # "O" 표시
            result_display.config(text="O", fg="green")
            root.after(1000, lambda: result_display.config(text=""))  # 1초 후 사라지게

            # 새로운 문제 출제
            current_ingredients.clear()
            for widget in current_tanghuru.winfo_children():
                widget.destroy()
            goal_ingredients = generate_problem()
    else:
        # 틀렸을 경우
        # 기회 차감
        lives -= 1
        lives_label.config(text=f"남은 기회: {lives}")

        # "X" 표시
        result_display.config(text="X", fg="red")
        root.after(1000, lambda: result_display.config(text=""))  # 1초 후 사라지게

        # 현재 탕후루 리셋
        current_ingredients.clear()
        for widget in current_tanghuru.winfo_children():
            widget.destroy()

        # 기회이 0이면 게임 오버
        if lives == 0:
            game_over()
        else:
            # 새로운 문제 출제
            goal_ingredients = generate_problem()
            
def game_over():
    global game_running
    if not game_running:  # 이미 게임이 종료된 상태라면 중복 실행 방지
        return
    game_running = False  # 게임 실행 중지
    
    # 버튼 비활성화
    for button in buttons:
        button.config(state="disabled")
    
    game_over_window = tk.Toplevel(root)
    game_over_window.title("게임 종료")
    game_over_window.geometry("400x300")

    # 게임 오버 메시지와 점수
    game_over_label = tk.Label(game_over_window, text=f"GAME OVER! \n 최종 점수: {score}", font=("교보 손글씨 2019", 18), fg="red")
    game_over_label.pack(pady=30)
    
    # 버튼 컨테이너
    button_frame = tk.Frame(game_over_window)
    button_frame.pack(pady=20)
    
    # 다시하기 버튼
    restart_button = tk.Button(button_frame, text="다시하기", font=("교보 손글씨 2019", 14), height=1, background="LightSteelBlue", activeforeground="SteelBlue", command=lambda: restart_game(game_over_window))
    restart_button.pack(side=tk.LEFT, pady=10)
    
    # 종료 버튼
    exit_button = tk.Button(button_frame, text="그만하기", font=("교보 손글씨 2019", 14), height=1, activeforeground="LightSteelBlue", command=root.destroy)
    exit_button.pack(side=tk.LEFT, padx=10)

# 게임 초기화 함수
def initialize_game():
    global score, lives, goal_ingredients, time_left, game_running
    
    score = 0
    score_label.config(text=f"현재 점수: {score}")
    
    lives = 3
    lives_label.config(text=f"남은 기회: {lives}")
    
    time_left = 60
    timer_label.config(text=f"남은 시간: {time_left}")
    
    # 게임 화면 구성
    timer_label.pack(pady=10)
    center_frame.pack(expand=True, fill="both", padx=10, pady=10)
    ingredients_frame.pack(side=tk.BOTTOM, pady=20)
    score_label.place(relx=0.5, rely=0.25, anchor="center")
    lives_label.place(relx=0.5, rely=0.3, anchor="center")
    
    # 현재 탕후루 리셋
    current_ingredients.clear()
    for widget in current_tanghuru.winfo_children():
        widget.destroy()
    
    game_running = True  # 게임 실행 상태 복구
    goal_ingredients = generate_problem()  # 목표 재료 생성
    
    # 타이머 다시하기
    update_timer()
    
    # 버튼 활성화
    for button in buttons:
        button.config(state="normal")
    
# 다시하기 버튼 클릭 시 게임 초기화 후 창 닫기
def restart_game(game_over_window):
    initialize_game()
    start_countdown()
    game_over_window.destroy()  # 게임 오버 창 닫기


# 카운트다운 함수
def start_countdown():
    # 게임 화면 숨기기
    timer_label.pack_forget()
    center_frame.pack_forget()
    ingredients_frame.pack_forget()
    score_label.place_forget()
    lives_label.place_forget()
    
    root.config(bg="LightSteelBlue")
    title_label = tk.Label(root, text="♥탕후루 만들기♥", font=("교보 손글씨 2019", 18), bg="LightSteelBlue")
    title_label.place(relx=0.5, rely=0.4, anchor="center")
    countdown_label = tk.Label(root, text="", font=("교보 손글씨 2019", 48, "bold"), fg="red", bg="LightSteelBlue")
    countdown_label.place(relx=0.5, rely=0.5, anchor="center")

    def countdown(n):
        if n > 0:
            countdown_label.config(text=str(n))
            root.after(1000, lambda: countdown(n - 1))  # 1초 후 다음 숫자로 갱신
        else:
            countdown_label.destroy()  # 카운트다운 끝나면 라벨 제거
            initialize_game()          # 게임 초기화

    countdown(3)  # 카운트다운 시작

for button, ingredient in zip(buttons, ingredients):
    button.config(command=lambda ing=ingredient: make_tanghuru(ing))

start_countdown()
update_timer()
root.mainloop()