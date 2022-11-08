import heapq
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

#TODO: Import any modules you want to use

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

#  The cost function is used to calculate the cost of a node based on the algorithm used
def costFunction(algo: str, idx: int, cost: int, problem: Problem[S, A], state: S, child:S, action: A, heuristic: HeuristicFunction) -> int:
    if algo == 'BFS':
        return idx # the cost increase as level increase
    elif algo == 'DFS':
        return -idx # the cost increase as level decrease
    elif algo == 'UCS':
        return cost + problem.get_cost(state, action) # the cost is the cumulative cost of the path
    elif algo == 'A*':
        return cost - heuristic(problem, state) + problem.get_cost(state, action)+ heuristic(problem, child) # the cost is the cumulative cost of the path + the heuristic value. We removed the heuristic value of the parent as heuristic can't be summed up
    elif algo == 'GBFS':
        return heuristic(problem, child)  # the cost is the heuristic value
    else:
        raise Exception('Invalid algorithm')

# A generic graph search function which is used by all the search functions
def graphSearch (frontier: list, problem: Problem[S, A], algo: str, heuristic: HeuristicFunction) -> Solution:
    idx = 0
    # N.B. The index is added for two reasons:
    # 1. To differentiate between nodes with the same state but different parents(common problem in the graph search).
    # 2. To stop the heapq from comparing between the GraphNode and DungeonNode and raising an exception.
    # 1. Create a set to store the explored nodes
    explored = set()                  # set of states already evaluated
    # 2. loop over the nodes in the frontier to explore them
    while frontier:                   # frontier is not empty
        # 3. Get the next node to explore from the frontier
        cost, (_, state), path = heapq.heappop(frontier) # pop the element with the highest priority -shallowest-
        # 4. Check if the node wasn't explored before
        if state not in explored: # if the node was not already explored
            # 5. Check if the node is the goal
            if problem.is_goal(state):   # if the node contains a goal state then return the corresponding solution
                return path
            # 6. Mark the node as explored
            explored.add(state) # Node is already explored, so add it to the explored set. Added after goal checking to avoid adding the goal state to the explored set
            # 7. Add the node's children to the frontier(we can find the child nodes by applying the actions to the current node)
            for action in problem.get_actions(state): # expand the chosen node, adding the resulting nodes to the frontier
                child = problem.get_successor(state, action)
                idx+=1
                # 8. The cost is calculated based on the algorithm used
                childCost = costFunction(algo, idx, cost, problem, state, child, action, heuristic)
                # 9. Add the child to the frontier
                if child not in explored and child not in frontier: 
                    # if(algo == 'BFS' and problem.is_goal(child)): return path + [action] # if the node contains a goal state then return the corresponding solution
                    heapq.heappush(frontier, (
                        childCost,
                        (idx, child), 
                        path + [action])) 
                # No need yo check if a better path exists, as all nodes are unique(due to having an index associated with it) and the cost is always increasing

    # 10. If you reached this point, then there is no solution
    return None
   

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution: 
    # Each entry is added to the frontier as a tuple ((index, node), path)   
    frontier = [(0, (0, initial_state), [])] # we used an index to differentiate between nodes with the same state but different parents(common problem in the graph search)
    return graphSearch(frontier, problem, 'BFS', None)

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
   # Each entry is added to the frontier as a tuple ((index, node), path)   
    frontier = [(0, (0, initial_state), [])] # we used an index to differentiate between nodes with the same state but different parents(common problem in the graph search)
    return graphSearch(frontier, problem, 'DFS', None)
    
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Each entry is added to the frontier as a tuple (cumulative_path_cost, (index, node), path)   
    frontier = [(0, (0, initial_state), [])] # we used an index to differentiate between nodes with the same state but different parents(common problem in the graph search)
    return graphSearch(frontier, problem, 'UCS', None)

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Each entry is added to the frontier as a tuple (cumulative_path_cost, (idx, node), path)   
    frontier = [(heuristic(problem, initial_state) + 0, (0, initial_state), [])] # we used an index to differentiate between nodes with the same state but different parents(common problem in the graph search)
    return graphSearch(frontier, problem, 'A*', heuristic)

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Each entry is added to the frontier as a tuple (cumulative_path_cost, (idx, node), path)   
    frontier = [(heuristic(problem, initial_state), (0, initial_state), [])] # we used an index to differentiate between nodes with the same state but different parents(common problem in the graph search)
    return graphSearch(frontier, problem, 'GBFS', heuristic)








 