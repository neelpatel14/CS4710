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
	"n_values": []
}
def get_move(state):

	ans = {"team-code": "eef8976e", #identifying team by the code assigned by game-program
	"move": 1 #Can be 0 or 1 only
	}
	save_info(state)
	print(get_Num(state))
	return ans


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

def get_Num(state):
	a = state["prospects"][0][0]
	b = state["prospects"][0][1]

	c = state["prospects"][1][0]
	d = state["prospects"][1][1]

	print([(a,a), (b,c)])
	print([(c,b), (d,d)])

	if (a > c and b > d):
		return 0
	if (a < c and b < d):
		return 1

	avg_0 = (a + b)/2
	avg_1 = (c+d)/2

	if avg_0 > avg_1:
		preferred = 0
	elif avg_1 > avg_0:
		preferred = 1
	else:
		preferred = None

	maximum = max(a,b,c,d)
	minimum = min(a,b,c,d)

	if  maximum == a and minimum == b:
		risky = 0
	elif maximum == c and minimum == d:
		risky = 1
	elif abs(b-a) > abs(d-c):
		risky = 0
	elif abs(d-c) > abs(b-a):
		risky = 1
	else:
		risky = None

	print(avg_0, avg_1)
	print("Pref: " + str(preferred))
	print("Risky: " + str(risky))

	if preferred != None:
		return preferred
	else:
		if risky == 1:
			return 0
		else:
			return 1



#
# def get_stats(arr):
# 	mean = 0
#     for i in arr:
#         mean += i
#     mean /= (1.0 * len(arr))
#     std = 0
#     for i in arr:
#         std += (i - mean)**2
#     std /= (len(arr) - 1)
#     std = std ** (0.5)
#     return mean, std

def save_info(state):
	if ((state["opponent-name"] != info["last_player"]) or (state["prospects"] is not info["last_prospects"])):
		#New game
		print("NEW GAME !!!!!!!!!!!!!!!!!!")
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
			uni_score = eval_score(state["prospects"], state["last-outcome"])
			info["player_behavior"][state["opponent-name"]]["game1"].append(uni_score)



counter = 0
while (True):
	state["opponent-name"] = input("Opponent Name: ")
	state["last-outcome"] = int(input("Previous Outcome: "))
	state["prev-repetitions"] = int(input("Repetitions: "))
	if counter is 0:
		state["last-outcome"] = None
		state["prev-repetitions"] = None
	get_move(state)
	print(info)
	print("-------------------------")
	counter = counter + 1
