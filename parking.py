from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # The initial state is the same as the current state of the cars
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # The goal is to set all the cars in their parking slots
        for carNum, carPos in enumerate(state):
            if carPos in self.slots:
                if self.slots[carPos] != carNum: # If the car is in the wrong parking slot
                    return False
            else: # If the car is not in a parking slot
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # The possible actions are all the possible moves of all the cars
        # The move is possible if the new position is a passage and the new position is not occupied by another car
        actions : list = []
        for carNum, carPos in enumerate(state):
            for direction in Direction:
                newCarPos = carPos + direction.to_vector()
                if newCarPos in state: continue # Disallow walking into other cars
                if newCarPos not in self.passages: continue # Disallow walking into walls
                actions.append((carNum, direction))
        return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # The successor is the same as the current state, except for the car that moved
        # No need to check if the action is valid, because it is assumed that the action we get from the get_actions() is always valid
        direction : Direction = action[1] # Move the car to the new position
        newState : list = list(state) # Copy the state
        newState[action[0]] = state[action[0]] + direction.to_vector() # Move the car
        return tuple(newState) # Return the new state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # The cost of an action is 1 (every action has the same cost)
        # Except if the action resulted in a car being in other's parking slots, then the cost is 101
        direction : Direction = action[1]
        newCarPos : Point = state[action[0]] + direction.to_vector()
        if newCarPos in self.slots: # If the new position is a parking slot of another car
            if self.slots[newCarPos] != action[0]: # The car is in the wrong parking slot
                return 101
        return 1.0 # The cost of moving a car is 1
    
    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
