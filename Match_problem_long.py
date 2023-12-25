import random
from datetime import datetime
random.seed(datetime.now().timestamp())

COMBINATIONS_LIMIT = 100000

NULL = 0
MOVE = -2
RECEIVE = 1
GIVE = -RECEIVE

NB_MAX_MOVES = 2

numbers = ["1","2","3","4","5","6","7","8","9","0"]
operators = ["+","-","/", "="]

class Symbol:
    def __init__(self, visual, trade):
        self.visual = visual
        self.trade = trade
"""
=====================================================
CONSTANTS
"""
symbols_for = {
    "0":{"0":NULL, "6":MOVE,     "8":RECEIVE,"9":MOVE},
    "1":{"1":NULL, "7":RECEIVE},
    "2":{"2":NULL, "3":MOVE},
    "3":{"3":NULL, "2":MOVE,    "5":MOVE,    "9":RECEIVE},
    "4":{"4":NULL, },
    "5":{"5":NULL, "3":MOVE,    "6":RECEIVE, "9":RECEIVE},
    "6":{"6":NULL, "0":MOVE,    "5":GIVE,    "8":RECEIVE,   "9":MOVE},
    "7":{"7":NULL, "1":GIVE},
    "8":{"8":NULL, "0":GIVE,    "6":GIVE,    "9":GIVE},
    "9":{"9":NULL, "0":MOVE,    "3":GIVE,    "5":GIVE,      "6":MOVE, "8":RECEIVE},
    "+":{"+":NULL, "-":GIVE,    "=":MOVE},
    "-":{"-":NULL, "+":RECEIVE, "=":RECEIVE},
    "/":{"/":NULL, "-":MOVE},
    "=":{"=":NULL, "-":GIVE,    "+":MOVE}
}

"""
=====================================================
MATHS
"""
def calculate(expression):
    while len(expression)!=1:
        if expression.count("/"):
            div_index = expression.index("/")
            operand_1 = expression[div_index-1]
            operand_2 = expression[div_index+1]
            op_result = int(operand_1)/int(operand_2)
            del expression[div_index-1]
            del expression[div_index-1]
            del expression[div_index-1]
            expression.insert(div_index-1, op_result)
            
        else:
            if expression.count("-"):
                min_index = expression.index("-")
                operand_1 = expression[min_index-1]
                operand_2 = expression[min_index+1]
                op_result = int(operand_1)-int(operand_2)
                del expression[min_index-1]
                del expression[min_index-1]
                del expression[min_index-1]
                expression.insert(min_index-1, op_result)
            else:
                if expression.count("+"):
                    plus_index = expression.index("+")
                    operand_1 = expression[plus_index-1]
                    operand_2 = expression[plus_index+1]
                    op_result = int(operand_1)+int(operand_2)
                    del expression[plus_index-1]
                    del expression[plus_index-1]
                    del expression[plus_index-1]
                    expression.insert(plus_index-1, op_result)
            
    return int(expression[0])

def get_nb_combinations(tokens):
    values = tokens.copy()
    for i in range(len(tokens)):
        symbol = tokens[i]
        values[i] = len(list(symbols_for[symbol].keys()))

    nb_combinations = values[0]
    for j in range(len(values)):
        value = values[j]
        nb_combinations *= value

    return nb_combinations

"""
=====================================================
MAIN
"""
def main():
    print(" __  __       _______ _____ _    _       _____  _____    ____  ____  _      ______ __  __  ")
    print("|  \/  |   /\|__   __/ ____| |  | |     |  __ \|  __ \  / __ \|  _ \| |    |  ____|  \/  | ")
    print("| \  / |  /  \  | | | |    | |__| |     | |__) | |__) || |  | | |_) | |    | |__  | \  / | ")
    print("| |\/| | / /\ \ | | | |    |  __  |     |  ___/|  _  / | |  | |  _ <| |    |  __| | |\/| | ")
    print("| |  | |/ ____ \| | | |____| |  | |     | |    | | \ \ | |__| | |_) | |____| |____| |  | | ")
    print("|_|  |_/_/    \_\_|  \_____|_|  |_|     |_|    |_|  \_\ \____/|____/|______|______|_|  |_| ")

    print("Welcome to this match problem game \n Press G to receive a match problem, or V to display the answers to a match problem")
    m = ""
    while True:
        m = input()
        if(m == "V" or m == "G"):
            break
        else:
            print("Mauvaise entrée")
    
    if m=="G":
        found = False
        answer = []
        tokens = []
        while not(found):
            tokens = random_tokens()
            print("Our token is:",tokens)
            answer = solve(tokens)
            if(len(answer)):
                found = True
                print("Found a valid combination")
            else:
                print("random combination is invalid")
        
        ask_user_solve = "Solve "+"".join(tokens)+": "
        u_response = input(ask_user_solve)
        
        if u_response in answer:
            print("Correct!")
        else:
            print("No")
            print("Correct answer was",answer)

    else:
        validator()

def random_tokens():
    tokens = []
    size = random.randint(3,3)
    for i in range(size):
        tokens.append(numbers[random.randint(0,len(numbers)-1)])

    tokens.insert(random.randint(1,len(tokens)-1), "=")

    sub_operators = operators.copy()
    sub_operators.pop()
    j=0
    while j!=len(tokens)-1:
        if (tokens[j] in numbers) and (tokens[j+1] in numbers):
            tokens.insert(j+1, sub_operators[random.randint(0,len(sub_operators)-1)])
        j+=1

    return tokens

"""
=====================================================
VALIDATOR
"""
def validator():
    while(True):
        problem_input = input("Enter match problem: ")
        if not(validate_input(problem_input)): continue
        
        tokens = get_tokens(problem_input)
        if(not(validate_tokens(tokens))): continue

        answers = solve(tokens)

        if(len(answers)):
            print()
            print("VALID PROBLEM!")
            print("Possible solutions:")
            for answer in answers:
                print(answer)
        print()

def solve(tokens):
    answers = []
    nb_combinations = get_nb_combinations(tokens)
        
    if(nb_combinations>COMBINATIONS_LIMIT):
        print(nb_combinations,"combinations possible: too much!")
        return []
    print(nb_combinations,"combinations possible: valid!")

    print()
    max_moves = NB_MAX_MOVES

    combinations = []
    recurs_combination(0, tokens, [], combinations)

    answers = get_valid_combinations(tokens, combinations, max_moves)

    if(len(answers)): return answers
    else:
        print()
        print("INVALID PROBLEM!")
        print("No solutions exist for this problem")
        return []
    
"""
=====================================================
VALIDATION
"""
def validate_input(problem_input):
    valid = True
    found_equal = False
    nb_equal = -1
    
    for i in problem_input:
        if not(i in numbers or i in operators): valid = False
        if i=="=":
            found_equal = True
            nb_equal += 1
    
    if not(found_equal) or nb_equal: valid = False

    if not(valid):
        print("Expression not valid: no '=' found")
        print()
        return False

    #At this point, expression is valid
    return True

def validate_tokens(tokens):
    valid = True
    nb_tokens = len(tokens)
    for i in range(nb_tokens):
        t = tokens[i]
        if t in operators:
            if i==0:
                valid = False
                break
            elif i==nb_tokens-1:
                valid = False
                break
            elif not(tokens[i-1] in numbers) or not(tokens[i+1] in numbers):
                valid = False
                break

        if t in numbers:
            if i==0: continue
            elif i==nb_tokens-1: continue
            elif not(tokens[i-1] in operators) or not(tokens[i+1] in operators):
                valid = False
                break

    if(valid): return True
    else:
        print("Expression invalid: duplicated number or symbol")
        return False
"""
=====================================================
GET TOKENS
"""
def get_tokens(problem_input):
    tokens = []
    for c in problem_input:
        tokens.append(c)
    return tokens

"""
=====================================================
RECURS COMBINATION
"""
def recurs_combination(c_token, tokens, combination, combinations):
    if c_token != len(tokens):
        trade = symbols_for[tokens[c_token]]
        for symbol in list(trade.keys()):
            new_combination = combination.copy()
            new_combination.append(symbol)
            recurs_combination(c_token+1, tokens, new_combination, combinations)
        
    else:
        if check_combination(combination):
            combinations.append(combination)

def get_valid_combinations(init_symbols, combinations, max_moves):
    trade_valid_combinations = get_trade_valid_combinations(init_symbols, combinations, max_moves)
    math_valid_combinations = get_math_valid_combinations(trade_valid_combinations)
    valid_combinations = math_valid_combinations
    return valid_combinations

def get_trade_valid_combinations(init_symbols, combinations, max_moves):
    trade_valid_combinations = []
    for combination in combinations:
        valid = True
        trades = 0
        nb_equ = 0
        nb_moves = 0
        for i in range(len(combination)):
            symbol = combination[i]
            if(symbol=="="): nb_equ+=1
            init_symbol = init_symbols[i]
            trade = symbols_for[init_symbol][symbol]
            if(trade==GIVE or trade==MOVE): nb_moves+=1
            if(trade!=MOVE): trades += trade

        if trades!=0: valid = False
        if nb_equ!=1: valid = False
        if nb_moves>max_moves: valid = False

        if(valid): trade_valid_combinations.append(combination)

    return trade_valid_combinations

def get_math_valid_combinations(combinations):
    math_valid_combinations = []
    for combination in combinations:
        equ_index = combination.index("=")
        left_side  = calculate(combination[0:equ_index])
        right_side = calculate(combination[equ_index+1:len(combination)])
        if(left_side==right_side): math_valid_combinations.append(combination)
    return math_valid_combinations

"""
=====================================================
CHECK COMBINATIONS
"""
def check_combination(combination):
    return True

"""
=====================================================
DISPLAY STEPS
"""
def display_steps(answer):
    print(answer)


if __name__ == "__main__":
    main()
