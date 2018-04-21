TEAM_NAME = "anis_friends"
MEMBERS = ["np2ch", "aml5ha", "rw5dc", "afc5fb"]

anis_friends_json = {
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
	"last_move": None,
	"consecutive_plays": 0,
	"last_oponenet_move": None,
    "split": None,
	"game_lengths": []

}


def get_move(state):
	process_info(state)
	#evaluate board
	if anis_friends_json["new_game"]:
		eval_board(state)
	ans = choose_strat(state)
	anis_friends_json["round_counter"] = anis_friends_json["round_counter"] + 1
	anis_friends_json["last_move"] = ans
	return {"team-code": state["team-code"], #identifying team by the code assigned by game-program
		"move": ans #Can be 0 or 1 only
		}


def choose_strat(state):

	if anis_friends_json["dominant"] is not None:
		return anis_friends_json["dominant"]

	if len(anis_friends_json["game_lengths"])>=3 and anis_friends_json["round_counter"]>max(get_stats(anis_friends_json["game_lengths"])[0]-2*anis_friends_json["game_lengths"][1], 6):
	# if there are more than 3 games played
	# and the current round is greater than 1 standard deviation lower than the mean game number
	# we assume normality of distribution because prof. said so
		if anis_friends_json["risky"] is not None:
		#if there exiss a risky move
			if anis_friends_json["last_move"]!=anis_friends_json["risky"]:
			#if the opponent's last move was risky
				rr = anis_friends_json["prospects"][anis_friends_json["risky"]][anis_friends_json["risky"]]
				rs = anis_friends_json["prospects"][anis_friends_json["risky"]][1 - anis_friends_json["risky"]]
				sr = anis_friends_json["prospects"][1 - anis_friends_json["risky"]][anis_friends_json["risky"]]
				ss = anis_friends_json["prospects"][1 - anis_friends_json["risky"]][1 - anis_friends_json["risky"]]
				if (.8*rs-.2*rr)-(.8*ss-.2*sr)>0:
					#we estimate opponent will chose safe 80% of the time
					#if estimated return when chosing risky - opportunity cost of chosing safe > 0
					return anis_friends_json["risky"]

	# if what they played last time is equal to what they played the time before that, add one to counter
	if state["last-opponent-play"] == anis_friends_json["last_oponenet_move"]:
		anis_friends_json["consecutive_plays"] +=1
	else: #else, set back to 0
		anis_friends_json["consecutive_plays"] = 0

	#if in first game
	if anis_friends_json["player_behavior"][state["opponent-name"]]["game2"] is None:
		return first_game(state)

	#if in second game
	else:
		if anis_friends_json["player_behavior"][state["opponent-name"]]["smart"]:
			return safe_game(state)

		else:
			return risky_game(state)




def eval_score(mat, score):
	list = [mat[0][0],mat[0][1],mat[1][1],mat[1][0]]
	list.sort()
	#print(list)
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

	if (a==d and b == c):
		anis_friends_json["split"] = (max(a, b))

	if (a >= c and b >= d):
		anis_friends_json["dominant"] = 0
	elif (a <= c and b <= d):
		anis_friends_json["dominant"] = 1
	else:
		anis_friends_json["dominant"] = None

	avg_0 = (a+b)/2
	avg_1 = (c+d)/2

	if avg_0 > avg_1:
		anis_friends_json["preferred"] = 0
	elif avg_1 > avg_0:
		anis_friends_json["preferred"] = 1
	else:
		anis_friends_json["preferred"] = None

	if abs(b-a) > abs(d-c):
		anis_friends_json["risky"] = 0
	elif abs(d-c) > abs(b-a):
		anis_friends_json["risky"] = 1
	else:
		anis_friends_json["risky"] = None

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
	if ((state["opponent-name"] != anis_friends_json["last_player"]) or (state["prospects"] is not anis_friends_json["last_prospects"])):
		#New game
		anis_friends_json["game_lengths"].append(anis_friends_json["round_counter"])
		anis_friends_json["new_game"] = 1
		anis_friends_json["round_counter"] = 0
		anis_friends_json["num_safe"] = 0
		if state["last-outcome"] is not None:
			# if info["last_player"] is None:
			# 	info["last_player"] = state["opponent-name"]
			uni_score = eval_score(anis_friends_json["last_prospects"], state["last-outcome"])
			anis_friends_json["player_behavior"][anis_friends_json["last_player"]]["game1"].append(uni_score)

		if state["opponent-name"] in anis_friends_json["player_behavior"]:
			#have played before (ie second go around)
			anis_friends_json["player_behavior"][state["opponent-name"]]["game2"] = []

		else:
			#First game against this opponent
			anis_friends_json["player_behavior"][state["opponent-name"]] = {"game1": [], "game2": None, "smart": False, "score": None}

		if state["prev-repetitions"] is not None:
			#Add how many rounds last game was
			anis_friends_json["n_values"].append(state["prev-repetitions"])
			#Evaluate Last-player
			tot_sum = sum(anis_friends_json["player_behavior"][anis_friends_json["last_player"]]["game1"])
			anis_friends_json["player_behavior"][anis_friends_json["last_player"]]["score"] = tot_sum / state["prev-repetitions"]
			#Determine if player was smart for next game against opponent
			if (anis_friends_json["player_behavior"][anis_friends_json["last_player"]]["score"] < 1):
				anis_friends_json["player_behavior"][anis_friends_json["last_player"]]["smart"] = True

		anis_friends_json["last_player"] = state["opponent-name"]
		anis_friends_json["last_prospects"] = state["prospects"]
		anis_friends_json["consecutive_plays"] = 0
		anis_friends_json["last_oponenet_move"] = None
		anis_friends_json["split"] = None

	else:
		#Same game, different round
		if anis_friends_json["player_behavior"][state["opponent-name"]]["game2"] is None:
			#We are in game 1, store last score in array
			anis_friends_json["new_game"] = 0
			uni_score = eval_score(state["prospects"], state["last-outcome"])
			anis_friends_json["player_behavior"][state["opponent-name"]]["game1"].append(uni_score)
			anis_friends_json["last_oponenet_move"] = state["last-opponent-play"]


#Function for the first game against any opponent, plays the first num_safe games safe,
# If after num_safe games, the outcome was not 2, it switches moves
def first_game(state):


	if anis_friends_json["new_game"] is 1:
		if len(anis_friends_json["n_values"]) > 1:
			anis_friends_json["num_safe"] = (int)(get_stats(anis_friends_json["n_values"])[0] * 0.2)

		else:
			anis_friends_json["num_safe"] = 3

	if anis_friends_json["round_counter"] <= anis_friends_json["num_safe"]:


		#basically, if twice in a row the opponent plays the same thing, and the board is split, and last thing we got was not the max of the board, return 1 - what the oponnent played. 
		if anis_friends_json["consecutive_plays"] >= 2 and anis_friends_json["split"] is not None and state["last-outcome"] != info["split"]:
			return 1 - state["last-opponent-play"]
		
		if anis_friends_json["consecutive_plays"] >= 4:
			return anis_friends_json["risky"]


		if anis_friends_json["risky"] is None:
			if anis_friends_json["preferred"] is not None:
				return anis_friends_json["preferred"]

			return 0

		if anis_friends_json["preferred"] is None:
			if anis_friends_json["risky"] is 0:
				return 1
			else:
				return 0

		if anis_friends_json["preferred"] is not anis_friends_json["risky"]:
			return anis_friends_json["preferred"]

		else:
			if anis_friends_json["preferred"] is 1:
				return 0
			return 1
	else:
		outcomes = anis_friends_json["player_behavior"][state["opponent-name"]]["game1"]
		if outcomes[len(outcomes)-1] is 2:
			return anis_friends_json["last_move"]
		else:
			#https://stackoverflow.com/questions/1779286/swapping-1-with-0-and-0-with-1-in-a-pythonic-way
			#binary not operator substitute
			return 1 - anis_friends_json["last_move"]

#Function if the opponent is determined to be dumb, picks the risky option first
#If the payout from the previous move is not 2, it switches
def risky_game(state):

	if anis_friends_json["round_counter"] is 1:
		if anis_friends_json["risky"] is None:
			if anis_friends_json["preferred"] is not None:
				return anis_friends_json["preferred"]
			return 0

		if anis_friends_json["preferred"] is None:
			if anis_friends_json["risky"] is 0:
				return 1
			else:
				return 0

		return anis_friends_json["risky"]


	else:
		outcomes = anis_friends_json["player_behavior"][state["opponent-name"]]["game2"]
		if outcomes[len(outcomes)-1] is 2:
			return anis_friends_json["last_move"]
		else:
			if anis_friends_json["last_move"] == 1:
				return 0
			else:
				return 1

#Function if the opponent is determined to be smart, starts off with the non-risky move
#If the outcome of the last round was 1 or greater (ie a good but not necessarily the best result, it picks the same move again)
#otherwise it switches moves
def safe_game(state):
	
	if anis_friends_json["consecutive_plays"] >= 2 and anis_friends_json["split"] is not None and state["last-outcome"] != info["split"]:
		return 1 - state["last-opponent-play"]
		
	
	if anis_friends_json["round_counter"] is 1:
		if anis_friends_json["risky"] is None:
			if anis_friends_json["preferred"] is not None:
				return anis_friends_json["preferred"]
			return 0

		if anis_friends_json["preferred"] is None:
			if anis_friends_json["risky"] is 0:
				return 1
			else:
				return 0

		if anis_friends_json["preferred"] is not anis_friends_json["risky"]:
			return anis_friends_json["preferred"]

	else:
		outcomes = anis_friends_json["player_behavior"][state["opponent-name"]]["game2"]
		if outcomes[len(outcomes)-1] >= 1:
			return anis_friends_json["last_move"]
		else:
			if anis_friends_json["last_move"] == 1:
				return 0
			else:
				return 1





