import random
from operator import itemgetter
from tqdm import tqdm
n = 8
win = 0
stop = False
c = 0
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
	population = [[random.randint(0, 7) for x in range(n)] for i in range(p_size)]
	for i in range(p_size):
		population[i] = [population[i], conflicts(population[i])]
	return sorted(population, key=itemgetter(1))


def crossover(pop, m):
	global stop
	global win
	global c
	for i in range(0,len(pop),2):
		cross = random.randint(1, 7)
		one = pop[random.randint(0, len(pop)-1)]
		two = pop[random.randint(0, len(pop)-1)]
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
		c += 1
		if check_h == 0 or conflicts(front_one+end_two) == 0 or conflicts(front_two+end_one) == 0:
			stop = True
			win += 1
			break
		if c == 50:
			stop = True
			c = 0
			break
	# pop = kill_em(pop)
	return sorted(pop, key=itemgetter(1))


mutation_rate = .2
for x in tqdm(range(1000)):
	starting_population = generate_population(1000)
	pop = crossover(starting_population, mutation_rate)
	while not stop:
		pop = crossover(pop, mutation_rate)
	stop = False
print(win)