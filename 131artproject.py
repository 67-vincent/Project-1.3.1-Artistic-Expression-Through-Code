import turtle as trtl
import random as rand
import leaderboard as lb


#-----game configuration----
wn = trtl.Screen()
wn.title("Heart Clicker")
wn.setup(width=400, height=535)
trtl.bgcolor("white")

# Assets
heart_image = "heart5.gif"
panda_image = "panda1.gif"
wn.addshape(heart_image)
wn.addshape(panda_image)
wn.tracer(0)

leaderboard_file_name = "131leaderboard.txt"
player_name = wn.textinput("Player Name", "Enter your name:") # Get name at start

timer = 5
score = 0
timer_up = False
font_setup = ("Arial", 18, "bold")
message_font = ("Arial", 14, "italic") 

#-----initialize turtles-----

# 1. Background Heart Stamper
stamper = trtl.Turtle()
stamper.hideturtle() 
stamper.shape(heart_image)
stamper.penup()
stamper.speed(0)

# 2. Border Drawer
border = trtl.Turtle()
border.hideturtle()
border.speed(0)
border.pensize(2)

# 3. The Panda
panda = trtl.Turtle()
panda.penup()
panda.shape(panda_image)
panda.goto(115, -150) 

# 4. The Balloon String
string_drawer = trtl.Turtle()
string_drawer.hideturtle()
string_drawer.speed(0)

# 5. The Main Heart Balloon (Target)
balloon = trtl.Turtle()
balloon.shape(heart_image)
balloon.penup()
balloon.goto(0, 100)

# 6. UI Turtles
score_writer = trtl.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(115, 215)

counter = trtl.Turtle()
counter.hideturtle()
counter.penup()
counter.goto(-170, 215)

# 7. Bottom Message Turtle
text_writer = trtl.Turtle()
text_writer.hideturtle()
text_writer.penup()
text_writer.goto(0, -230) 

#-----functions--------

def draw_design():
    border.penup()
    border.goto(-180, 250)
    border.pendown()
    for _ in range(2):
        for _ in range(12): 
            border.forward(15); border.penup(); border.forward(15); border.pendown()
        border.right(90)
        for _ in range(16):
            border.forward(15); border.penup(); border.forward(15); border.pendown()
        border.right(90)

def write_bottom_message():
    text_writer.clear()
    # Change "Panda Game" to whatever you want later!
    text_writer.write("Panda Game", align="center", font=message_font)

def draw_string():
    string_drawer.clear()
    if not timer_up:
        string_drawer.penup()
        string_drawer.goto(75, -135) 
        string_drawer.pendown()
        string_drawer.pensize(2)
        string_drawer.goto(balloon.xcor(), balloon.ycor())

def update_score(): #score update
  global score
  score += 1
  score_writer.clear()
  score_writer.write(score, font=font_setup)

def move_balloon():
    if not timer_up:
        # 1. Use STAMPER to leave the mark (keeps main balloon clickable)
        stamper.goto(balloon.xcor(), balloon.ycor())
        stamper.stamp() 
        
        # 2. Move balloon to new spot
        new_x = rand.randint(-130, 130)
        new_y = rand.randint(-50, 180)
        balloon.goto(new_x, new_y)
        
        draw_string()
        wn.update()

def countdown():
    global timer, timer_up
    counter.clear()
    if timer <= 0:
        counter.write("Time's Up!", font=font_setup)
        timer_up = True
        manage_leaderboard()
    else:
        counter.write(f"Time: {timer}", font=font_setup)
        timer -= 1
        wn.ontimer(countdown, 1000)

def manage_leaderboard():
    global score
    # 1. Load current leaderboard
    leader_names_list = lb.get_names(leaderboard_file_name)
    leader_scores_list = lb.get_scores(leaderboard_file_name)

    # 2. Check if player qualifies for leaderboard
    if (len(leader_scores_list) < 5 or score > leader_scores_list[4]):
        lb.update_leaderboard(leaderboard_file_name, leader_names_list, leader_scores_list, player_name, score)
        lb.draw_leaderboard(True, leader_names_list, leader_scores_list, text_writer, score)
    else:
        lb.draw_leaderboard(False, leader_names_list, leader_scores_list, text_writer, score)
    
    # Hide game elements
    balloon.hideturtle()
    string_drawer.clear()
    wn.update()

# This new function checks if the screen click was near the heart
def handle_click(x, y):
    if not timer_up:
        # Distance check bypasses the "invisible shield" of GIF borders
        if balloon.distance(x, y) < 35: 
            update_score()
            move_balloon()

#-----main execution-----
draw_design()
write_bottom_message()
draw_string()
score_writer.write(f"Score: {score}", align="center", font=font_setup)
wn.update()

# BIND CLICK TO SCREEN INSTEAD OF BALLOON
wn.onclick(handle_click) 
wn.ontimer(countdown, 1000)
wn.mainloop()