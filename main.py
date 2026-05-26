import tkinter as tk
import random
from datetime import datetime

#window
WIDTH = 400
HEIGHT =600

root = tk.Tk()
root.title = "CAR RACING GAME"
root.resizable(False,False)

canvas = tk.Canvas(root, width = WIDTH, height = HEIGHT, bg = "black")
canvas.pack()

#road
road_left = 100
road_right = 300

canvas.create_rectangle(road_left, 0, road_right,HEIGHT, fill = "black")

#road_lines
road_lines = []
for i in range(0, HEIGHT ,100):
    line = canvas.create_rectangle(190, i, 210, i+60, fill = "white")
    road_lines.append(line)

#player car
player_car = canvas.create_rectangle(170, 500, 230, 580, fill = "blue")
player_speed = 20

#Enemy car
enemy_car = canvas.create_rectangle(
    random.randint(50,350),
    -100,

    random.randint(50,350) + 60,
    -20,
    fill = "red")
enemy_speed = 8

#score
score = 0
score_text = canvas.create_text(
    70,
    30,
    text = f"Score:{score}",
    fill = "white",
    font = ("Arial", 18, "bold")
)




#Movement
def move_left(event):
    if not game_over:
        pos = canvas.coords(player_car)
        if pos[0] > 20:
            canvas.move(player_car,-20, 0)

def move_right(event):
    if not game_over:
        pos = canvas.coords(player_car)
        if pos[2] < WIDTH -20:
            canvas.move(player_car, 20, 0)


root.bind("<Left>",move_left)
root.bind("<Right>",move_right)

#move road lines
def move_road():
    for line in road_lines:
        canvas.move(line, 0 ,10)
        pos = canvas.coords(line)

        if pos[1] >HEIGHT:
            canvas.coords(line, 190, -60, 210, 0)

#collision detection
def check_collision():
    player_pos = canvas.coords(player_car)
    enemy_pos = canvas.coords(enemy_car)

    overlap = (
        player_pos[0] < enemy_pos[2]
        and player_pos[2] > enemy_pos[0]
        and player_pos[1] < enemy_pos[3]
        and player_pos[3] > enemy_pos[1]
    )

    return overlap


#save in file
def save_score():
    with open("game_results.txt","a") as file:
        file.write(
            f"Final Score: {score}\n",            
        )

game_over = False

#GAme loop
def game_loop():
    global score, game_over, enemy_speed 

    if game_over:
        return

    move_road()
    #move enemy
    canvas.move(enemy_car, 0 , enemy_speed)
    enemy_pos = canvas.coords(enemy_car)

    #reset enemy
    if enemy_pos[1] > HEIGHT:
        x = random.randint(50,200)
        canvas.coords(enemy_car , x, -100, x + 60, -20)

        score += 1
        enemy_speed += 0.5
        canvas.itemconfig(score_text,text = f"Score:{score}")

    #collision
    if check_collision():
        game_over_screen()
        return

    root.after(50, game_loop)

#GAME OVER
def game_over_screen():
    global game_over
    game_over = True

    save_score()

    canvas.create_text(
        WIDTH//2,
        HEIGHT//2-20,
        text = "GAME OVER",
        fill = "yellow",
        font = ("Arial" , 28, "bold")
    ) 

    canvas.create_text(
        WIDTH/2,
        HEIGHT//2+20,
        text = f"FINAL SCORE:{score}",
        font = ("Arial", 20),
        fill = "white" 
    )

game_loop()
root.mainloop()