# eight queen problem solved by genetics algorithm
import random
import time

solutions = []
def generate_parent(pop, n_pop):
    colList = list(range(8))   # columns from 0 to 7
    for _ in range(n_pop):
        random.shuffle(colList)
        pop.append(colList)
    return pop

def crossover(parent1, parent2, crossOver):
    newInstance = []
    for i in range(crossOver):
        newInstance.append(parent1[random.randint(0, 7)])   # first part of child is from parent1
    for i in range(crossOver, 8):
        newInstance.append(parent2[random.randint(0, 7)])   # second part of child is from parent2
    return newInstance


def fitness(pop):
    fitness = []
    
    # initialize lists to keep track of occupied rows and diagonals
    rows = [0] * 8
    diags1 = [0] * 15
    diags2 = [0] * 15
    
    for board in pop:
        attacks = 0
        
        for i, col in enumerate(board):
            # check if there is another queen in the same row
            if rows[col] == 1:
                attacks += 1
            
            # check if there is another queen in the same diagonal (ascending)
            if diags1[i + col] == 1:
                attacks += 1
            
            # check if there is another queen in the same diagonal (descending)
            if diags2[i - col + 7] == 1:
                attacks += 1
            
            # mark the current row and diagonals as occupied
            rows[col] = 1
            diags1[i + col] = 1
            diags2[i - col + 7] = 1
        
        # reset the values to 0 for the next board
        rows = [0] * 8
        diags1 = [0] * 15
        diags2 = [0] * 15
        
        fitness.append(attacks)
        
        if attacks == 0 and board not in solutions:
            print_solution(board)
            solutions.append(board)

    return fitness


def mutation(board):    # there is a chance to change column for each queen
    mutation_rate = 0.98
    for row in range(8):
        if random.random() < mutation_rate:
            board[row] = random.randint(0,7)

def print_solution(board):
    row = [ '.' for _ in range(8)]
    for i in range(8):
        row[board[i]] = 'Q'
        print(' '.join(row))
        row[board[i]] = '.'
    print("\n")
        

if __name__ == "__main__":
    num_of_solutions = int(input())     # 1 - 92
    start = time.time()
    
    n_pop = 20  # number of random boards for initial population(pop)
    crossOver = 5
    pop = []
    pop = generate_parent(pop, n_pop)

    while len(solutions) < num_of_solutions:
        fitnesses = fitness(pop)
        fitnesses = list(enumerate(fitnesses))
        parents_with_fit = sorted(fitnesses, key=lambda x:x[1])     # sorted by fitness score

        #divide parents to best and weak based on their fitness
        best_parents = [pop[element[0]] for element in parents_with_fit[:int(n_pop/2)]]   
        weak_parents = [pop[element[0]] for element in parents_with_fit[int(n_pop/2 + 1):]]
        weak_parents = list(reversed(weak_parents))

        # also three of the best parents remain in the new generation
        temp = [pop[element[0]] for element in best_parents[:3]] 
        pop = temp

        # one of the best parents and one of the weak parents make a child.(generally 20 children)
        for parent1, parent2 in zip(best_parents, weak_parents):
            pop.append(crossover(parent1, parent2, crossOver))
            pop.append(crossover(parent2, parent1, crossOver))

        # make some random changes to the generation(pop)
        for board in pop:
            mutation(board)

    spent_time = time.time() - start

    print(f"time spent: {spent_time} seconds")