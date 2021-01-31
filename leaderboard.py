import pickle
from circle_class import draw_text, BLACK

filename = 'ldrbrd.p'


def load_leader_board():
    try:
        leader_board = pickle.load(open(filename, "rb"))
    except:
        leader_board = {}

    return leader_board


def save_leader_board(leader_board):
    pickle.dump(leader_board, open(filename, "wb"))


def sort_leaderboard(leaderboard, metric):
    return


def draw_leader_board(screen, sorting_metric, x, y, c, *,Left_justified=False,Right_justified=False,fill_back=False,Back_color=BLACK):
    leader_board = load_leader_board()
    temp = sorted(leader_board, key=lambda user_dict: leader_board[user_dict][sorting_metric],reverse=True)

    if Left_justified:
        draw_text(screen, f'Leaderboard :{sorting_metric}', x, y + (-1 * 40), c, Left_justified=True,fill_back=fill_back,Back_color=Back_color)
    elif Right_justified:
        draw_text(screen, f'Leaderboard :{sorting_metric}', x, y + (-1 * 40), c, Right_justified=True,fill_back=fill_back,Back_color=Back_color)

    for z, u in enumerate(temp):
        if Left_justified:
            draw_text(screen, f'{u}:{leader_board[u][sorting_metric]}', x, y + (z * 40), c,Left_justified=True,fill_back=fill_back,Back_color=Back_color)
        elif Right_justified:
            draw_text(screen, f'{u}:{leader_board[u][sorting_metric]}', x, y + (z * 40), c,Right_justified=True,fill_back=fill_back,Back_color=Back_color)

        if z >= 5:
            break


def update_user_kills(username):
    leaderboard = load_leader_board()
    if username not in leaderboard:
        leaderboard[username] = {
            'wins': 0,
            'kills': 1
        }
    else:
        leaderboard[username]['kills'] += 1

    save_leader_board(leaderboard)


def update_user_wins(username):
    leaderboard = load_leader_board()
    if username not in leaderboard:
        leaderboard[username] = {
            'wins': 1,
            'kills': 0
        }
    else:
        leaderboard[username]['wins'] += 1
    save_leader_board(leaderboard)


if __name__ == '__main__':
    print(load_leader_board())
