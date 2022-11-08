from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use


def closestToExit(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # We want to find the nearest coin.
    # If the coin is close to the exit, we want to go to the coin.
    # If there are no coins, we want to go to the exit.
    if len(state.remaining_coins) == 0: # If there are no coins, we want to go to the exit.
        return manhattan_distance(state.player, problem.layout.exit)
    leastDistance: float = float('inf')
    for coin in state.remaining_coins: 
        currentDistance: float = \
            manhattan_distance(state.player, coin) + \
            manhattan_distance(coin, problem.layout.exit) * 0.5 # If the coin is close to the exit, we want to go to the coin.
        leastDistance = min(leastDistance, currentDistance)
    return leastDistance

def closestToOthers(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # We want to the coin that is close to other coins.
    # If there are no coins, we want to go to the exit.
    if len(state.remaining_coins) == 0: # If there are no coins, we want to go to the exit.
        return manhattan_distance(state.player, problem.layout.exit)
    coins = list(state.remaining_coins)
    leastDistance: float = float('inf')
    for i in range(len(coins)):
        currentDistance: float = manhattan_distance(state.player, coins[i]) + \
            sum([manhattan_distance(coins[i], coins[j]) for j in range(len(coins)) if i != j]) * 0.5
        leastDistance = min(leastDistance, currentDistance)
    return leastDistance

def bestMidWay(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # We want to get a close coin that is also close to the exit.
    coins = state.remaining_coins
    if len(coins) == 0:
        return manhattan_distance(state.player, problem.layout.exit) # If there are no coins, we want to go to the exit.
    midWayDistance = - float('inf')
    for coin in coins:
        coinDistance = manhattan_distance(state.player, coin) + manhattan_distance(coin, problem.layout.exit)
        midWayDistance = max(midWayDistance, coinDistance)
    return midWayDistance

# DP Implementations

def DP_closestToOthers(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # Use dynamic programming to find the minimum distance to collect all the coins
    # Implements the closestToOthers heuristic using dynamic programming    
    # 1. Get the memoization table
    memo = problem.cache()
    # 2. Check if the state is in the memoization table
    currentState = (state.player, state.remaining_coins)
    if currentState in memo:
        return memo[currentState]
    # 3.1. If the state is not in the memoization table, add the base case
    coins = list(state.remaining_coins)
    if len(coins) == 0:
        memo[currentState] = manhattan_distance(state.player, problem.layout.exit)
        return memo[currentState]
    # 3.2. If the state is not in the memoization table, add the recursive case
    memo[currentState]: float = float('inf')
    currentStateCoins = set(coins) # Copy the coins to a set, to be able to remove coins
    for i, coin in enumerate(coins):
        currentStateCoins.remove(coin) # Remove the coin from the set, to simulate collecting it
        newCoins = list(currentStateCoins)
        new_state = DungeonState(layout=state.layout, player=coins[i], remaining_coins=frozenset(currentStateCoins)) # Create a new state with the coin collected
        currentDistance: float = manhattan_distance(state.player, coin) + \
            sum([manhattan_distance(coin, newCoins[j]) for j in range(len(newCoins)) if i != j])
        # currentDistance += DP_closestToOthers(problem, new_state)
        memo[currentState] = min(memo[currentState], currentDistance)
        currentStateCoins.add(coin) # Add the coin back to the set, to simulate not collecting it
    # 4. Return the value in the memoization table
    return memo[currentState]

def DP_bestMidWay(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # Use dynamic programming to find the minimum distance to collect all the coins
    # Implements the bestMidWay heuristic using dynamic programming
    # 1. Get the memoization table
    memo = problem.cache()
    # 2. Check if the state is in the memoization table
    currentState = (state.player, state.remaining_coins)
    if currentState in memo:
        return memo[currentState]
    # 3.1. If the state is not in the memoization table, add the base case
    coins = list(state.remaining_coins)
    if len(coins) == 0:
        memo[currentState] = manhattan_distance(state.player, problem.layout.exit)
        return memo[currentState]
    # 3.2. If the state is not in the memoization table, add the recursive case
    memo[currentState]: float = - float('inf')
    currentStateCoins = set(coins) # Copy the coins to a set, to be able to remove coins
    for coin in coins:
        currentStateCoins.remove(coin) # Remove the coin from the set, to simulate collecting it
        new_state = DungeonState(layout=state.layout, player=coin, remaining_coins=frozenset(currentStateCoins)) # Create a new state with the coin collected       
        currentDistance = manhattan_distance(state.player, coin) + manhattan_distance(coin, problem.layout.exit)
        # currentDistance += DP_bestMidWay(problem, new_state)
        memo[currentState] = max(memo[currentState],  currentDistance)
        currentStateCoins.add(coin) # Add the coin back to the set, to simulate not collecting it
    # 4. Return the value in the memoization table
    return memo[currentState]

############################################################################################################
def bfs(initialPoint: Point, goalPoint: Point, problem: DungeonProblem) -> int:
    # A BFS to get the distance between two points
    #  By distance, we mean the number of nodes it needs to traverse to get to the goal
    # 1. Create the frontier
    frontier = [(initialPoint, [])] # The frontier is a list of tuples (point, path)
    # 2. Create the explored set
    explored = set()
    # 3. While the frontier is not empty
    while frontier:
        # 3.1. Get the first state in the frontier
        currentPoint, currentPath = frontier.pop(0)
        # 3.2. If the state is the goal, return the solution
        if currentPoint == goalPoint:
            return len(currentPath) # Return the length of the path
        # 3.3. If the state is not in the explored set
        if currentPoint not in explored:
            # 3.3.1. Add the state to the explored set
            explored.add(currentPoint)
            # 3.3.2. Add the children of the state to the frontier
            for direction in Direction:
                childPoint = currentPoint + direction.to_vector() # Get the child point
                if childPoint not in explored and childPoint in problem.layout.walkable:
                    frontier.append((childPoint, currentPath + [direction]))
    # 4. Return failure
    return 0

def getMinBfsDistance(startPoint : Point , coins : list, problem: DungeonProblem) -> int:
    # Get the distances between points using BFS
    distanceMemo = problem.cache()
    minDistance = float('inf')
    for coin in coins:  
        if (startPoint, coin) not in distanceMemo:
            distance = bfs(startPoint, coin, problem)
            minDistance = min(minDistance, distance)
            distanceMemo[(startPoint, coin)] = distanceMemo[(coin, startPoint)] = distance
        else:
            minDistance = min(minDistance, distanceMemo[(startPoint, coin)])
    return minDistance

def DP_weightedDistances(problem: DungeonProblem, state: DungeonState) -> float:
    # Approach:
    # Use dynamic programming to find the minimum distance to collect all the coins
    # get a weighted sum for all the distances in the problem
    # 1. Get the memoization table
    memo = problem.cache()
    # 2. Check if the state is in the memoization table
    currentState = (state.player, state.remaining_coins)
    if currentState in memo:
        return memo[currentState]
    # 3.1. If the state is not in the memoization table, add the base case
    coins = list(state.remaining_coins)
    if len(coins) == 0: # If there are no coins, we want to go to the exit.
        avgDistanceToExit = (euclidean_distance(state.player, problem.layout.exit) + manhattan_distance(state.player, problem.layout.exit)) * 0.5
        bfsDistanceToExit = bfs(state.player, problem.layout.exit, problem)
        memo[currentState] = (bfsDistanceToExit + avgDistanceToExit) / 2
        return memo[currentState]
    # 3.2. If the state is not in the memoization table, add the recursive case
    memo[currentState]: float = float('inf')
    currentStateCoins = set(coins) # Copy the coins to a set, to be able to remove coins
    for i, coin in enumerate(coins):
        currentStateCoins.remove(coin) # Remove the coin from the set, to simulate collecting it
        new_state = DungeonState(layout=state.layout, player=coin, remaining_coins=frozenset(currentStateCoins)) # Create a new state with the coin collected
        # Get the distance with the next nearest coin
        recursiveDistance = DP_weightedDistances(problem, new_state)
        # Get the distance to the current coin
        currentCoinDistance = manhattan_distance(state.player, coin) # use this instead if BFS to get 6 test cases passing
        # Get the distance to the exit
        exitDistance = (euclidean_distance(coin, problem.layout.exit) + manhattan_distance(coin, problem.layout.exit)) * 0.5
        # Get the coin distance to the exit
        coinDistanceToExit = manhattan_distance(coin, problem.layout.exit)
        # Get the total distance with the other coins
        totalDistanceOtherCoins = sum([euclidean_distance(state.player, otherCoin) for otherCoin in list(currentStateCoins)])
        # BFS to the coin
        bfsDistanceToNearestCoin = getMinBfsDistance(state.player , coins, problem) #bfs(state.player, coin, problem)
        # Add the distances to get the total distance
        totalDistance = 0.0 * currentCoinDistance + \
                        1.0 * recursiveDistance + \
                        1.0 * bfsDistanceToNearestCoin + \
                        0.0 * exitDistance + \
                        0.0 * coinDistanceToExit + \
                        0.0 * totalDistanceOtherCoins            
        memo[currentState] = min(memo[currentState], totalDistance)
        currentStateCoins.add(coin) # Add the coin back to the set, to simulate not collecting it
    # 4. Return the value in the memoization table
    return memo[currentState]

def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    return DP_weightedDistances(problem, state) # 10 test cases passing
    # return bestMidWay(problem, state) # 6 test cases passing
    # return DP_bestMidWay(problem, state) # 6 test cases passing
    # return closestToExit(problem, state) # 4 test cases passing
    # return DP_closestToOthers(problem, state) # 0 test cases passing
    # return closestToOthers(problem, state) # 0 test cases passing
    
