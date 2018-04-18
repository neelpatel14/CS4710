state = {
	"team-code": "ani's_friends",
	"game": "sym",
	"opponent-name": "mighty-ducks",
	"prev-repetitions": 10, #Might be None if first game ever, or other number
	"last-opponent-play": 1, #0 or 1 depending on strategy played
	"last-outcome": 4, #Might be None if first game, or whatever outcome of play is
	"prospects": [
	[4,3],
	[5,2]
	]
}


def get_move(state):
	
	ans = {"team-code": "eef8976e", #identifying team by the code assigned by game-program
	"move": 1 #Can be 0 or 1 only
	}
	print(get_Num(state))
	return ans



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








get_move(state)


