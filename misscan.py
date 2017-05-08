from simpleai.search import SearchProblem, breadth_first, depth_first
from simpleai.search.viewers import ConsoleViewer

'''
Implementation of a problem definion for Missionaries and Cannibals ridle.
Using simpleai python library   https://github.com/simpleai-team/simpleai
'''
# initial and goal state of the problem
initial_state = "33B--00"
GOAL = "00--33B"

def from_string_to_list(string):
    ''' Converts string representation of a state to two dimensional list synonym. \
        Result is stripped of dashes.  \
        string repr. of initial state: "33B--00"  =converted=> [[3, 3, "B"], [0, 0]]   \
        Same applies to from_string_to_list_2 function below'''
    a = [(int(string[i]) if string[i] != "B" else "B") for i in range(3) if string[i] != "-"]
    b = [(int(string[i]) if string[i] != "B" else "B") for i in range(3, 7) if string[i] != "-"]
    return [a, b]

# different implementation of from_string_to_list, using map, filter, and lambdas
def from_string_to_list_2(string):
    a = list(map(lambda x: int(x) if x != "B" else "B", filter(lambda x: x != "-", string[:3])))
    b = list(map(lambda x: int(x) if x != "B" else "B", filter(lambda x: x != "-", string[3:])))
    return [a, b]

def from_list_to_string(listt):
    ''' converts list representation of a state to its string synonym \
        string state looks as follows: \
        one side of the river: number.of.cannibals_number.of.missionaries_boat(if boat) \
        separated by double dash \
        other side of the river implemented as the first one \
        for instance:  "22B--11"     '''
    n = "".join(str(i) for i in listt[0])
    m = "".join(str(i) for i in listt[1])
    return n + "--" + m

def actions_helper(state, action, x=0, y=1):
    ''' Performs basic arithmetic operation on a list representation of a state. \
        Result is changed state. actions_helper is used in result function'''
    if len(action) > 3:
        canibal_command = int(action[1])
        missionary_command = int(action[3])
        state[x][0] -= canibal_command
        state[y][0] += canibal_command
        state[x][1] -= missionary_command
        state[y][1] += missionary_command
        return (state)
    else:
        if "C" in action:
            canibal_command = int(action[1])
            state[x][0] -= canibal_command
            state[y][0] += canibal_command
        else: # "M" in actions
            missionary_command = int(action[1])
            state[x][1] -= missionary_command
            state[y][1] += missionary_command
        return (state)


class MissionriesCannibals(SearchProblem):
    def __init__(self, initial_state=None):
        self.initial_state = initial_state

    def actions(self, state):
        ''' All legal actions from particular state'''
        state = from_string_to_list_2(state)
        if state == [[3, 3, "B"], [0, 0]]:
            return ["C1", "C2", "C1M1"]
        elif state == [[2, 3], [1, 0, "B"]]:
            return ["C1"]
        elif state == [[1, 3], [2, 0, "B"]]:
            return ["C1", "C2"]
        elif state == [[2, 2], [1, 1, "B"]]:
            return ["M1", "C1M1"]
        elif state == [[2, 3, "B"], [1, 0]]:
            return ["M1", "C1", "C2"]
        elif state == [[0, 3], [3, 0, "B"]]:
            return ["C1", "C2"]
        elif state == [[1, 3, "B"], [2, 0]]:
            return ["C1", "M2"]
        elif state == [[1, 1], [2, 2, "B"]]:
            return ["C1M1", "M2"]
        elif state == [[2, 2, "B"], [1, 1]]:
            return ["C1M1", "M2"]
        elif state == [[2, 0], [1, 3, "B"]]:
            return ["M2", "C1"]
        elif state == [[3, 0, "B"], [0, 3]]:
            return ["C1", "C2"]
        elif state == [[1, 0], [2, 3, "B"]]:
            return ["C2", "C1", "M1"]
        elif state == [[1, 1, "B"], [2, 2]]:
            return ["C1M1", "M1"]
        elif state == [[2, 0, "B"], [1, 3]]:
            return ["C2", "C1"]
        elif state == [[0, 0], [3, 3, "B"]]:
            return ["C2", "C1", "C1M1"]
        elif state == [[1, 0, "B"], [2, 3]]:
            return ["C1"]
        else: return []

    def result(self, state, action):
        '''Transition model'''
        state = from_string_to_list_2(state)
        if "B" in state[0]:
            state[1] = state[1] + (list(state[0].pop()))
            return from_list_to_string(actions_helper(state, action))
        if "B" in state[1]:
            state[0] = state[0] + (list(state[1].pop()))
            return from_list_to_string(actions_helper(state, action, x=1, y=0))

    def is_goal(self, state):
        ''' Checks if particular state is a goal state'''
        return state == GOAL

problem = MissionriesCannibals(initial_state)
result = depth_first(problem, graph_search=True)
print(result.path())
print(result.state)

#for act, state in result.path():
#    print("Action taken {}".format(act))
#    print("resulting state {}".format(state))
