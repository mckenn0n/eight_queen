import random
from operator import itemgetter
from tqdm import tqdm
n = 8
FC_sol = 0
FC_c = 0
SD_sol = 0
SD_c = 0
resets = 0

change_list = list(range(n))
def print_state(s):
	print('Vector representation of state:\n',s,'\n\nMatrix representation of state:')
	print("\n".join(' 0 ' * i + ' 1 ' + ' 0 ' * (n-i-1) for i in s) + "\n\n")
	print('h =',conflicts(s))

def conflicts(s):
	h = 0
	for i in range(len(s)):
		for j in range(i+1,len(s)):
			v = i-j
			v = v*v
			v2 = s[i]-s[j]
			v2 = v2*v2
			if s[i] == s[j]:
				h += 1
			# if abs(i-j) == abs(s[i]-s[j]):
			if v == v2:
				h += 1
	return h

def first_choice(s,c):
	temp = s.copy()
	BL_h = conflicts(temp)
	if BL_h == 0:
		# print('Soultion found')
		return 1, c
	else:
		for i in range(len(temp)):
			temp = s.copy()
			for number in change_list:
				temp[i] = number
				c += 1
				if BL_h > conflicts(temp):
					# print('\n*First Choice*\nA better state was found.')
					# print_state(temp)
					return first_choice(temp, c)
		return 0, c

def first_choice_RR(s, r):
	temp = s.copy()
	BL_h = conflicts(temp)
	if BL_h == 0:
		# print('Soultion found')
		return r
	else:
		for i in range(len(temp)):
			temp = s.copy()
			for number in change_list:
				temp[i] = number
				if BL_h > conflicts(temp):
					# print('\n*First Choice*\nA better state was found.')
					# print_state(temp)
					return first_choice_RR(temp, r)
		r += 1
		return random_restart(r)

def steepest_descent(s, c):
	temp = s.copy()
	BL_h = conflicts(temp)
	states = []
	if BL_h == 0:
		# print('Soultion found')
		return 1, c
	else:
		for i in range(len(temp)):
			temp = s.copy()
			for number in change_list:
				temp[i] = number
				c += 1
				if BL_h > conflicts(temp):
					st = temp.copy()
					states.append([st, conflicts(temp)])
					# return first_choice(temp)
		states = sorted(states, key=itemgetter(1))
		if len(states) != 0:
			return steepest_descent(states[0][0], c)
		else:
			return 0, c

def random_restart(r):
	state = [random.randint(0, 7) for x in range(n)]
	return first_choice_RR(state, r)

t = 1000

for i in tqdm(range(t)):
	state = [random.randint(0, 7) for x in range(n)]
	FC = first_choice(state,0)
	SD = steepest_descent(state,0)
	FC_sol += FC[0]
	FC_c += FC[1]
	SD_sol += SD[0]
	SD_c += SD[1]
	resets += random_restart(0)

print('FC =',FC_sol,FC_c,'\nSD =',SD_sol,SD_c,'\nRR =',resets)

