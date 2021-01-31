from circle_class import *
from leaderboard import update_user_kills, update_user_wins, draw_leader_board
import time

bot_names = ['joe', 'moe', 'bob', 'bobby', 'steve', 'master cheif', 'joey', 'cloey', 'babbaduke', 'pepega bob', 'randy',
             'big mamba', 'goku', 'jay jay the jetplane', 'lasagna', 'arbiter', 'megaman', 'comically_large_spoon']

class Koth():
    def __init__(self):
        self.player_lim = 20
        self.time_lim_lobby = 30
        self.time_lim_play = 60

        self.screen = None
        self.Chat_data_queue = None
        self.Ready_player_counter = 0
        self.Player_count = 0
        self.alive_players = self.player_lim
        self.State = 'init'
        self.timer_delta_i = time.time()
        self.timer_delta_e = time.time()
        self.DONE = False
        self.players = {}
        self.Hill = Circle('THE HILL')
        self.Hill.coord.x = WIDTH / 2 - 300
        self.Hill.coord.y = HEIGHT / 2
        self.Hill.radius = HEIGHT / 2
        self.Hill.basecolor = BLACK
        self.kill_strings = []

    def time_delt(self):
        return int(self.timer_delta_e - self.timer_delta_i)
    def reset_timer(self):
        self.timer_delta_i = time.time()
        self.timer_delta_e = time.time()
    def update_timer(self):
        self.timer_delta_e = time.time()

    def update_players(self):
        flag = True
        while flag:
            try:
                data = self.Chat_data_queue['queueue'].get(0)
                username = data['user']['name']
                user_input = data['args']
                if 'logo' in data:
                    user_logo = data['logo']
                else:
                    user_logo = None
                print(f'data from user: {username} received')
            except:
                flag = False
                username = None
                user_input = None


            if username == 'adeadzeplin' or self.time_delt() > self.time_lim_lobby:
                user_flag = False
                if user_input != None:
                    if (user_input[0] == 'start') and self.State == 'init':
                        user_flag = True
                if user_flag or (
                        self.time_delt() >self.time_lim_lobby and self.State == 'init'):

                    name_list = []
                    request_count = self.player_lim
                    self.Chat_data_queue['request_export'].put({'insults': request_count})

                    while len(name_list) < request_count:
                        try:
                            temp = self.Chat_data_queue['request_import'].get(0)['insult']
                            if temp not in [None, 'None'] and temp not in name_list:
                                # print(temp)
                                name_list.append(temp)
                            elif temp in name_list:
                                print('requesting new name for bot')
                                self.Chat_data_queue['request_export'].put({'insults': 1})

                        except:
                            pass

                    self.State = 'play'
                    for i in range(0, self.player_lim - self.Player_count):
                        randy = random.randint(0, len(name_list) - 1)
                        temp_name = name_list.pop(randy)
                        tempstr = f'@{temp_name}'
                        # print(tempstr)
                        self.Ready_player_counter+= 1
                        self.players[tempstr] = Circle(tempstr, 0, 0)
                        self.players[tempstr].status = True
                        self.players[tempstr].basecolor = GREEN
                        self.players[tempstr].is_bot = True

                    temp_list = list(self.players)
                    random.shuffle(temp_list)
                    for n, j in enumerate(temp_list):
                        placement_flag = True
                        while placement_flag:
                            # j = random.randint(0,100)
                            t = n + self.players[j].radius *2
                            bet = self.Hill.radius - self.players[j].radius*2 - 50
                            x = (bet + t) * math.cos(t)
                            y = (bet + t) * math.sin(t)
                            self.players[j].coord = pygame.Vector2(x+self.Hill.coord.x,y+self.Hill.coord.y)
                            if not self.Hill.check_map_colision(self.players[j]):
                                placement_flag = False

                    self.reset_timer()

            if user_input != None:
                    if user_input[0] == 'reset':
                        self.State = 'REBOOT'

            if self.State == 'REBOOT':
                self.reset_timer()
                self.State = 'init'
                self.players = {}
                self.kill_strings.clear()
                self.alive_players = self.player_lim
                self.Ready_player_counter = 0
                self.Player_count = 0
                self.Hill.radius = HEIGHT / 2
                self.Hill.coord.x = WIDTH / 2 - 300
                print('game reset')

            if self.State == 'init' and user_input != None and self.Player_count < self.player_lim:
                if user_input[0].lower() == 'join':
                    if username not in self.players:
                        self.players[username] = Circle(username, 0, 0,user_logo)
                        self.Player_count += 1
                        self.players[username].coord = pygame.Vector2(
                                random.randint(self.Hill.coord.x - 200, self.Hill.coord.x + 200),
                                random.randint(self.Hill.coord.y - 200, self.Hill.coord.y + 200)
                        )

            elif self.State == 'play' and user_input != None:
                if username in self.players and len(user_input) == 2:
                    if not self.players[username].is_dead:
                        if user_input[0].isnumeric() and user_input[1].isnumeric():
                            userdirection = int(user_input[0]) % 360
                            userpower = int(user_input[1])
                            if userpower > 100:
                                userpower = 100
                            # print(userdirection,userpower*2)
                            self.players[username].direction = (userdirection - 90) * math.pi / 180
                            self.players[username].power = userpower
                            self.players[username].status = True

                            self.Ready_player_counter += 1
                            # accept an input for that player
                            pass


    def run_king_of_the_hill(self,q):

        self.Chat_data_queue = q
        # Set the width and height of the screen [width, height]
        size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(size)
        pygame.init()

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        print('King of the hill booting')
        # -------- Main Program Loop -----------
        done = False
        while not done:
            pygame.display.set_caption(f"KING OF THE HILL: {self.State}")
            self.update_players()

            if self.DONE:
                done = True
                print("reset")

            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            # --- Game logic should go here

            if self.State == 'init':
                self.update_timer()

            if self.State == 'play':
                # print(len(Players),Ready_player_counter)
                self.update_timer()

                if self.Ready_player_counter >= self.alive_players or self.time_delt() > self.time_lim_play:
                    # print'IMPULSE!!!')
                    self.Ready_player_counter = 0

                    for p in self.players:
                        if not self.players[p].is_dead:
                            if self.players[p].is_bot:
                                self.Ready_player_counter += 1
                                self.players[p].bot_ai(self.Hill)
                            self.players[p].impulse()

                    if self.Hill.radius < 10:
                        self.Hill.coord.x += 10
                    else:
                        self.Hill.radius -= 10
                    self.reset_timer()
                checked = []
                for p in self.players:
                    if not self.players[p].is_dead:
                        checked.append(p)
                        for pp in self.players:
                            if p != pp and pp not in checked:
                                if not self.players[pp].is_dead:
                                    self.players[p].check_colision(self.players[pp])

                        self.players[p].update()
                for p in self.players:
                    if not self.players[p].is_dead:

                        if self.Hill.check_map_colision(self.players[p]):
                            # print(f'User: {p} Has been eliminated')
                            if self.players[p].last_collided_with != None:
                                update_user_kills(self.players[p].last_collided_with)
                                self.players[self.players[p].last_collided_with].recent_kills +=1
                                killdict = {
                                    'user': self.players[p].last_collided_with,
                                    'time': time.time(),
                                    'victim':p,
                                    'active': True
                                }
                                self.kill_strings.append(killdict)

                            self.players[p].is_dead = True
                            self.Hill.radius -=5
                            self.alive_players -= 1
                            if '@' in p:
                                self.Ready_player_counter-=1

                            if self.alive_players == 1:
                                self.State = 'END'
                                self.reset_timer()
                                for i in self.players:
                                    if not self.players[i].is_dead:
                                        update_user_wins(i)
                                        break
                            break


            if self.State == 'END':
                self.update_timer()
                if self.time_delt() >self.time_lim_lobby:
                    self.State = 'REBOOT'
                    self.reset_timer()

            self.screen_draw_stuff()
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)

        print('King of the hill terminating')

        pygame.quit()

    def Kill_feed(self):
        # text_height = 0
        tie = time.time()
        for i, d in enumerate(reversed(self.kill_strings)):
            if 'medal' in d:
                if d['medal']:
                    if int(tie - d['time']) < 2:
                        draw_text(self.screen, f"{d['user']} {d['num']}x Kills!", self.Hill.coord.x+self.Hill.radius,HEIGHT - 240 + (i * 24), BLACK, Left_justified=True, Font_size=25)

            else:
                if self.players[d['user']].recent_kills == 1:
                    self.players[d['user']].kill_start = time.time()
                if int(tie - d['time']) < 2:
                    draw_text(self.screen,f"{d['user']} killed {d['victim']}",self.Hill.coord.x+self.Hill.radius, HEIGHT - 240 + (i*24), BLACK,Left_justified=True,Font_size=25)
                    self.players[d['user']].kill_start = time.time()
                else:
                    if time.time() - self.players[d['user']].kill_start > 2 and self.players[d['user']].is_bot == False:
                        if self.players[d['user']].recent_kills > 1:
                            self.players[d['user']].mulitkill_flag = True
                        # self.players[d['user']].kill_run = False

        for i, d in enumerate(reversed(self.kill_strings)):
            if self.players[d['user']].mulitkill_flag == True:
                self.players[d['user']].mulitkill_flag =False
                file_name = None
                killdict = {
                    'user': d['user'],
                    'time': time.time(),
                    'medal': True,
                    'active': True,
                    'num':self.players[d['user']].recent_kills
                }
                self.kill_strings.append(killdict)

                if self.players[d['user']].recent_kills == 2:
                    file_name = 'doublekill'
                elif self.players[d['user']].recent_kills == 3:
                    file_name = 'triplekill'
                elif self.players[d['user']].recent_kills == 4:
                    file_name = 'overkill'
                elif self.players[d['user']].recent_kills == 5:
                    file_name = 'halokilltac'
                elif self.players[d['user']].recent_kills == 6:
                    file_name = 'halokilltrocity'
                elif self.players[d['user']].recent_kills == 7:
                    file_name = 'halokillamanjaro'
                elif self.players[d['user']].recent_kills == 8:
                    file_name = 'halokilltastrofy'
                elif self.players[d['user']].recent_kills == 9:
                    file_name = 'halokilpocalypse'
                elif self.players[d['user']].recent_kills >= 10:
                    file_name = 'halokillianare'

                self.players[d['user']].recent_kills = 0
                if file_name != None:
                    self.Chat_data_queue['request_export'].put({'bbb': file_name})

    def screen_draw_stuff(self):
        # --- Screen-clearing code goes here
        self.screen.fill(ORANGE)

        # --- Drawing code should go here

        self.Hill.Hdraw(self.screen)
        draw_text(self.screen, f"Time Left:", 160, 30, BLACK, Right_justified=True, Font_size=20)
        if self.State == 'play':
            draw_text(self.screen,f"{self.time_lim_play - self.time_delt() + 1}", 130, 70, BLACK, Right_justified=True, Font_size=50)
        else:
            draw_text(self.screen,f"{self.time_lim_lobby - self.time_delt() + 1}", 130, 70, BLACK, Right_justified=True, Font_size=50)

        for p in self.players:
            if not self.players[p].is_dead:
                # if p == 'adeadzeplin':
                # self.players[p].draw_sprite(self.screen)
                # else:
                self.players[p].draw(self.screen)
        self.Kill_feed()
        if self.State == 'END':
            for i in self.players:
                if not self.players[i].is_dead:

                    draw_text(self.screen, f"{i} Has won king of the hill!!", 50, HEIGHT / 2,
                      WHITE, fill_back=True,Left_justified=True)

            draw_leader_board(self.screen, 'wins', 400, HEIGHT - 240, BLACK,Right_justified=True,fill_back=True,Back_color=ORANGE)
            draw_leader_board(self.screen, 'kills', 450, HEIGHT - 240, BLACK,Left_justified=True,fill_back=True,Back_color=ORANGE)






def play_Koth(q):
    Da_gaem = Koth()
    Da_gaem.run_king_of_the_hill(q)
if __name__ == '__main__':
    play_Koth(None)
