# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthSearch(problem, state, visited):
    visited.append(state)
    for successor in problem.getSuccessors(state):
        state = successor[0]
        direction = successor[1]
        if problem.isGoalState(state):
            return [direction]

        if state not in visited:
            search = depthSearch(problem, state, visited)
            if len(search) > 0:
                search.insert(0, direction)
                return search
    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    return depthSearch(problem, problem.getStartState(), [])


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    visited = []

    while not queue.isEmpty():
        current = queue.pop()
        currentState = current[0]
        currentPath = current[1]

        visited.append(currentState)

        for successor in problem.getSuccessors(currentState):
            state = successor[0]
            direction = successor[1]

            path = list(currentPath)
            path.append(direction)

            if problem.isGoalState(state):
                return path

            if state not in visited:
                queue.push((state, path))

    return []


def graphSearch(problem, allPaths):
    exploredNodes = []
    allPaths.push([(problem.getStartState(), "Stop", 0)])

    while not allPaths.isEmpty():
        path = allPaths.pop()

        lastNodeOfThePath = path[len(path) - 1]

        print(lastNodeOfThePath)

        lastNodeOfThePath = lastNodeOfThePath[0]

        if problem.isGoalState(lastNodeOfThePath):
            return [x[1] for x in path][1:]

        if lastNodeOfThePath not in exploredNodes:
            exploredNodes.append(lastNodeOfThePath)

            for nextNode in problem.getSuccessors(lastNodeOfThePath):
                if nextNode[0] not in exploredNodes:
                    nextNodePath = path[:]
                    nextNodePath.append(nextNode)
                    allPaths.push(nextNodePath)

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    costLambda = lambda aPath: problem.getCostOfActions([x[1] for x in aPath])
    allPaths = util.PriorityQueueWithFunction(costLambda)
    return graphSearch(problem, allPaths)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    nos = []
    queue = util.PriorityQueue()
    start = problem.getStartState()
    queue.push((start, []), heuristic(start, problem))
    while not queue.isEmpty():
        no, actions = queue.pop()

        if problem.isGoalState(no):
            return actions

        nos.append(no)

        for coord, direction, cost in problem.getSuccessors(no):
            if coord not in nos:
                new_actions = actions + [direction]
                custo = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                queue.push((coord, new_actions), custo)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
