"""
state = {
	"team-code": "ani's_friends",
	"game": "sym",
	"opponent-name": "mighty-ducks",
	"prev-repetitions": None, #Might be None if first game ever, or other number
	"last-opponent-play": 1, #0 or 1 depending on strategy played
	"last-outcome": None, #Might be None if first game, or whatever outcome of play is
	"prospects": [
	[4,3],
	[5,2]
	]
}

info = {
	"player_behavior": {},
	"last_player": None,
	"last_prospects": None,
	"n_values": [],
	"new_game": 0,
	"round_counter": 0,
	"num_safe": 0,
	"risky": 0,
	"preferred": 0,
	"dominant": None,
	"last_move": None
}
"""
def get_move(state):
	info = load_info()
	if len(info) == 0 or info is None:
		info = {
		"player_behavior": {},
		"last_player": None,
		"last_prospects": None,
		"n_values": [],
		"new_game": 0,
		"round_counter": 0,
		"num_safe": 0,
		"risky": 0,
		"preferred": 0,
		"dominant": None,
		"last_move": None
		}

	process_info(state)

	#evaluate board
	if info["new_game"]:
		eval_board(state)
	ans = choose_strat(state)
	info["round_counter"] = info["round_counter"] + 1
	info["last_move"] = ans
	save_info(info)
	return {"team-code": state["team-code"], #identifying team by the code assigned by game-program
		"move": ans #Can be 0 or 1 only
		}


def choose_strat(state):

	if info["dominant"] is not None:
		return info["dominant"]

	#if in first game
	if info["player_behavior"][state["opponent-name"]]["game2"] is None:
		return first_game(state)

	#if in second game
	else:
		if info["player_behavior"][state["opponent-name"]]["smart"]:
			return safe_game(state)

		else:
			return risky_game(state)




def eval_score(mat, score):
	list = [mat[0][0],mat[0][1],mat[1][1],mat[1][0]]
	list.sort()
	print(list)
	if score is list[0]:
		return -1
	elif score is list[1]:
		return 0
	elif score is list[2]:
		return 1
	else:
		return 2


def eval_board(state):
	a = state["prospects"][0][0]
	b = state["prospects"][0][1]

	c = state["prospects"][1][0]
	d = state["prospects"][1][1]

	if (a >= c and b >= d):
		info["dominant"] = 0
	elif (a <= c and b <= d):
		info["dominant"] = 1
	else:
		info["dominant"] = None

	avg_0 = (a+b)/2
	avg_1 = (c+d)/2

	if avg_0 > avg_1:
		info["preferred"] = 0
	elif avg_1 > avg_0:
		info["preferred"] = 1
	else:
		info["preferred"] = None

	if abs(b-a) > abs(d-c):
		info["risky"] = 0
	elif abs(d-c) > abs(b-a):
		info["risky"] = 1
	else:
		info["risky"] = None

def get_stats(arr):
	mean = 0
	for i in arr:
		mean += i
	mean /= (1.0 * len(arr))
	std = 0
	for i in arr:
		std += (i - mean)**2
	std /= (len(arr) - 1)
	std = std ** (0.5)
	return mean, std

def process_info(state):
	if ((state["opponent-name"] != info["last_player"]) or (state["prospects"] is not info["last_prospects"])):
		#New game
		info["new_game"] = 1
		info["round_counter"] = 0
		info["num_safe"] = 0
		if state["last-outcome"] is not None:
			# if info["last_player"] is None:
			# 	info["last_player"] = state["opponent-name"]
			uni_score = eval_score(info["last_prospects"], state["last-outcome"])
			info["player_behavior"][info["last_player"]]["game1"].append(uni_score)

		if state["opponent-name"] in info["player_behavior"]:
			#have played before (ie second go around)
			info["player_behavior"][state["opponent-name"]]["game2"] = []

		else:
			#First game against this opponent
			info["player_behavior"][state["opponent-name"]] = {"game1": [], "game2": None, "smart": False, "score": None}

		if state["prev-repetitions"] is not None:
			#Add how many rounds last game was
			info["n_values"].append(state["prev-repetitions"])
			#Evaluate Last-player
			tot_sum = sum(info["player_behavior"][info["last_player"]]["game1"])
			info["player_behavior"][info["last_player"]]["score"] = tot_sum/state["prev-repetitions"]
			#Determine if player was smart for next game against opponent
			if (info["player_behavior"][info["last_player"]]["score"] < 1):
				info["player_behavior"][info["last_player"]]["smart"] = True

		info["last_player"] = state["opponent-name"]
		info["last_prospects"] = state["prospects"]

	else:
		#Same game, different round
		if info["player_behavior"][state["opponent-name"]]["game2"] is None:
			#We are in game 1, store last score in array
			info["new_game"] = 0
			uni_score = eval_score(state["prospects"], state["last-outcome"])
			info["player_behavior"][state["opponent-name"]]["game1"].append(uni_score)


#Function for the first game against any opponent, plays the first num_safe games safe,
# If after num_safe games, the outcome was not 2, it switches moves
def first_game(state):
	if info["new_game"] is 1:
		if len(info["n_values"]) > 1:
			info["num_safe"] = (int)(get_stats(info["n_values"])[0] * 0.2)

		else:
			info["num_safe"] = 3

	if info["round_counter"] <= info["num_safe"]:
		if info["risky"] is None:
			if info["preferred"] is not None:
				return info["preferred"]

			return 0

		if info["preferred"] is None:
			if info["risky"] is 0:
				return 1
			else:
				return 0

		if info["preferred"] is not info["risky"]:
			return info["preferred"]

		else:
			if info["preferred"] is 1:
				return 0
			return 1
	else:
		outcomes = info["player_behavior"][state["opponent-name"]]["game1"]
		if outcomes[len(outcomes)-1] is 2:
			return info["last_move"]
		else:
			if info["last_move"] == 1:
				return 0
			else:
				return 1

#Function if the opponent is determined to be dumb, picks the risky option first
#If the payout from the previous move is not 2, it switches
def risky_game(state):

	if info["round_counter"] is 1:
		if info["risky"] is None:
			if info["preferred"] is not None:
				return info["preferred"]
			return 0

		if info["preferred"] is None:
			if info["risky"] is 0:
				return 1
			else:
				return 0

		return info["risky"]


	else:
		outcomes = info["player_behavior"][state["opponent-name"]]["game2"]
		if outcomes[len(outcomes)-1] is 2:
			return info["last_move"]
		else:
			if info["last_move"] == 1:
				return 0
			else:
				return 1

#Function if the opponent is determined to be smart, starts off with the non-risky move
#If the outcome of the last round was 1 or greater (ie a good but not necessarily the best result, it picks the same move again)
#otherwise it switches moves
def safe_game(state):

	if info["round_counter"] is 1:
		if info["risky"] is None:
			if info["preferred"] is not None:
				return info["preferred"]
			return 0

		if info["preferred"] is None:
			if info["risky"] is 0:
				return 1
			else:
				return 0

		if info["preferred"] is not info["risky"]:
			return info["preferred"]

	else:
		outcomes = info["player_behavior"][state["opponent-name"]]["game2"]
		if outcomes[len(outcomes)-1] >= 1:
			return info["last_move"]
		else:
			if info["last_move"] == 1:
				return 0
			else:
				return 1




#TEST CODE
counter = 0
while (True):
	state["opponent-name"] = input("Opponent Name: ")
	state["last-outcome"] = int(input("Previous Outcome: "))
	state["prev-repetitions"] = int(input("Repetitions: "))
	if counter is 0:
		state["last-outcome"] = None
		state["prev-repetitions"] = None
	move = get_move(state)
	print("---------INFO----------")
	print(info)
	print("---------MOVE-----------")
	print(move)

	counter = counter + 1
