import random
from operator import itemgetter
from tqdm import tqdm
N = 8
win = 0
stop = False
C = 0
REPS = 10
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

def generate_population(p_size):
	population = [[random.randint(0, 7) for x in range(N)] for i in range(p_size)]
	for i in range(p_size):
		population[i] = [population[i], conflicts(population[i])]
	return sorted(population, key=itemgetter(1))

def kinda_random(population):
	best = []
	p = population.copy()
	p = p[:25]
	o = random.randint(0, len(p)-1)
	best.append(p[0])
	del p[0]
	best.append(p[random.randint(0, len(p)-1)])
	return best

# def kinda_random_two(population):
# 	best = []
# 	temp = []
# 	first = random.uniform(0, 1)
# 	second = random.uniform(0, 1)
# 	p = population.copy()
# 	s = 0
# 	for i in range(len(p)):
# 		s += p[i][1]
# 	for i in range(len(p)):
# 		if i == 0:
# 			temp.append([p[i][0],p[i][1],p[i][1]/s])
# 		else:
# 			temp.append([p[i][0],p[i][1],float("{0:.5f}".format(((p[i][1]/s)+temp[i-1][2])))])
# 			if temp[i][2] > 1:
# 				temp[i][2] = 1.0
# 	temp[len(p)-1][2] = 1.0
# 	x = 0
# 	while first > temp[x][2]:
# 		# print('*',first,temp[x][2])
# 		x+=1
# 	best.append(temp[x])
# 	y = 0
# 	while second > temp[y][2]:
# 		# print(second,temp[y][2])
# 		y+=1
# 	best.append(temp[y])
# 	# print(temp)
# 	return best


def crossover(pop, m):
	global stop
	global win
	global C
	for i in range(0,len(pop)):
		cross = random.randint(1, 7)
		ran = kinda_random(pop)
		one = ran[0]
		two = ran[1]
		check_h = min(one[1],two[1])
		front_one = one[0][:cross]
		if random.uniform(0, 1) < m:
			mut = random.randint(0, len(front_one)-1)
			front_one[mut] = random.randint(0, 7)
		end_one = one[0][cross:]
		if random.uniform(0, 1) < m:
			mut = random.randint(0, len(end_one)-1)
			end_one[mut] = random.randint(0, 7)
		front_two = two[0][:cross]
		if random.uniform(0, 1) < m:
			mut = random.randint(0, len(front_two)-1)
			front_two[mut] = random.randint(0, 7)
		end_two = two[0][cross:]
		if random.uniform(0, 1) < m:
			mut = random.randint(0, len(end_two)-1)
			end_two[mut] = random.randint(0, 7)
		pop.append([front_one+end_two, conflicts(front_one+end_two)])
		pop.append([front_two+end_one, conflicts(front_two+end_one)])
		C += 1
		if check_h == 0 or conflicts(front_one+end_two) == 0 or conflicts(front_two+end_one) == 0:
			stop = True
			win += 1
			break
		if C == 2000:
			stop = True
			C = 0
			break
	# pop = kill_em(pop)
	return sorted(pop, key=itemgetter(1))


mutation_rate = .2
for x in tqdm(range(REPS)):
	starting_population = generate_population(100)
	pop = crossover(starting_population, mutation_rate)
	while not stop:
		pop = crossover(pop, mutation_rate)
	stop = False
print(win)