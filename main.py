# Command: python main.py ex1.var1.txt ex1.con.txt
import copy
import sys

from utils import formatOutput, initializeConstraints, initializeVariables

# Initialize variables and constraints
variablesDictionary = initializeVariables(sys.argv[1])
numVariables = len(variablesDictionary)
constraintsArray = initializeConstraints(sys.argv[2])

# Step is global bc me lazy
step = [1]


def backtrackingSearch(domains, csp):
    return recursiveBacktracking({}, domains, csp)


def forwardCheckingSearch(domains, csp):
    return recursiveForwardChecking({}, domains, csp)


def selectUnassignedVariable(variableDomains, assignment, csp):
    """Select variable algorithm:

    - Select variable via the most constrained variable heuristic
    - Break ties by using most constraining variable heuristic
    - Break any remaining ties alphabetically"""

    # Store most constrained variable in list; if ties exist, store both in list
    # Each variable will be represented as a tuple: (variable_name, variable domain values)

    # Apply most constrained variable heuristic
    most_constrained_variable = []

    # Lets just use a lambda function to sort
    for variable, varDomain in variableDomains.items():
        # Skip if variable already in assignment
        if variable in assignment:
            continue

        # Set first variable as most constrained variable
        if len(most_constrained_variable) == 0:
            most_constrained_variable = [(variable, varDomain)]
            continue

        # Check if variable more constrained
        _, mcVariableDomain = most_constrained_variable[0]
        if len(varDomain) < len(mcVariableDomain):
            most_constrained_variable = [(variable, varDomain)]
        elif len(varDomain) == len(mcVariableDomain):
            most_constrained_variable.append((variable, varDomain))

    if len(most_constrained_variable) == 1:
        return most_constrained_variable[0][0]

    # If ties exist, apply most constraining variable heuristic
    most_constraining_variable = []

    for variable, _ in most_constrained_variable:
        # Find number of unassigned variables current variable constrains
        counter = 0
        for constraint in csp:
            if variable not in constraint:
                continue
            var1, operator, var2 = constraint.split(" ")
            if var1 in assignment or var2 in assignment:
                continue
            counter += 1

        if len(most_constraining_variable) == 0:
            most_constraining_variable = [(variable, counter)]
            continue

        _, mcVCount = most_constraining_variable[0]
        if counter > mcVCount:
            most_constraining_variable = [(variable, counter)]
        elif counter == mcVCount:
            most_constraining_variable.append((variable, counter))

    # for variable in most

    return most_constraining_variable[0][0]


def checkConstraint(key, num, assignment, csp):
    assignment[key] = num
    constBool = True
    for con in csp:
        splitCon = con.split(" ")

        if splitCon[0] in assignment and splitCon[2] in assignment:
            if splitCon[1] == ">":
                constBool = assignment[splitCon[0]] > assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "<":
                constBool = assignment[splitCon[0]] < assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "=":
                constBool = assignment[splitCon[0]] == assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "!":
                constBool = assignment[splitCon[0]] != assignment[splitCon[2]]
                if not constBool:
                    return False
        else:
            continue
    return True


def evaluate(x, operator, y):
    if operator == ">":
        return x > y
    elif operator == "<":
        return x < y
    elif operator == "=":
        return x == y
    else:  # This should never run
        print("THIS SHOULDN'T RUN")
        return False


def orderValuesUsingLeastConstrainingValuesHeuristic(
    variable, assignment, domains, csp
):
    """
    1. Make list of relevant constraints
    2. Sort values by least constraining
    """

    relevant_constraints = []

    for constraint in csp:
        if variable not in constraint:
            continue

        constraint_valid = True
        for assigned_variable in assignment:
            if assigned_variable in constraint:
                constraint_valid = False
                break

        if constraint_valid:
            relevant_constraints.append(constraint)

    ordered_values = []  # Format: (value, # invalid values)
    # Write logic to order constraints
    for value in domains[variable]:
        invalid_values = 0

        # Count # of invalid values for each constraint
        for constraint in relevant_constraints:
            var1, operator, var2 = constraint.split(" ")

            # Find other variable
            other_var = var1 if var1 != variable else var2

            for other_var_value in domains[other_var]:
                # Determine correct order
                isValid = (
                    evaluate(other_var_value, operator, value)
                    if other_var == var1
                    else evaluate(value, operator, other_var_value)
                )

                if not isValid:
                    invalid_values += 1
        ordered_values.append((value, invalid_values))

    sorted_values = sorted(ordered_values, key=lambda item: item[1])

    return [i[0] for i in sorted_values]


def recursiveBacktracking(assignment: dict, domains: dict, csp: list):
    """Given an assignment state, this function  will:

    - Select a variable using the most constrained variable heuristic,

    - Explore all possible values of the variable by:
       - Select a value using the least constraining variable heuristic,
       - Check if the assignment is still true
       - If true, update assignment state and recurse

    """
    if len(assignment) == numVariables:
        return assignment

    var = selectUnassignedVariable(domains, assignment, csp)

    orderedValues = orderValuesUsingLeastConstrainingValuesHeuristic(
        var, assignment, domains, csp
    )

    for num in orderedValues:
        # Modify this to reorder, checking for least constraining value
        if checkConstraint(var, num, assignment, csp):
            assignment[var] = num
            result = recursiveBacktracking(assignment, domains, csp)

            if result != "Failure":
                print(formatOutput(assignment, step[0], True))
                exit()  # Fix later; figure out why it keeps recursing even though it should be done
                # step[0] += 1
                # return result
        else:
            print(formatOutput(assignment, step[0], False))
            step[0] += 1
            del assignment[var]
    return "Failure"


def updateDomains(assignment: dict, domains: dict, csp: list):
    """
    1. Make list of relevant constraints
    2. Sort values by least constraining
    """

    relevant_constraints = []

    for variable in assignment:
        for constraint in csp:
            if variable not in constraint:
                continue

            # We want to skip if both variables in constraint are already in assignment
            constraint_valid = True
            for assigned_variable in assignment:
                if assigned_variable in constraint and assigned_variable != variable:
                    constraint_valid = False
                    break

            if not constraint_valid:
                continue

            # Now, update the domain
            var1, operator, var2 = constraint.split(" ")
            value = assignment[variable]  # Get assigned value for variable

            # Find other variable
            other_var = var1 if var1 != variable else var2

            # Make copy of domain so for loop works
            domain_copy = domains[other_var].copy()

            for other_var_value in domain_copy:
                # Determine correct order
                isValid = (
                    evaluate(other_var_value, operator, value)
                    if other_var == var1
                    else evaluate(value, operator, other_var_value)
                )

                if not isValid:
                    # Remove from domain
                    domains[other_var].remove(other_var_value)

    return domains


def recursiveForwardChecking(assignment: dict, domains: dict, csp: list):
    """Given an assignment state, this function  will:

    - Select a variable using the most constrained variable heuristic,

    - Explore all possible values of the variable by:
       - Select a value using the least constraining variable heuristic,
       - Check if the assignment is still true
       - If true, update assignment state, perform forward checking, and recurse

    """
    if len(assignment) == numVariables:
        return assignment

    var = selectUnassignedVariable(domains, assignment, csp)

    orderedValues = orderValuesUsingLeastConstrainingValuesHeuristic(
        var, assignment, domains, csp
    )

    for num in orderedValues:
        # Make a copy of domain here
        newDomains = copy.deepcopy(domains)

        if checkConstraint(var, num, assignment, csp):
            assignment[var] = num

            # Update domain here
            newDomains[var] = [num]

            # Check if domains work
            newDomains = updateDomains(assignment, newDomains, csp)  # type: ignore

            flagIG = True
            for v in newDomains:
                if len(newDomains[v]) == 0:
                    flagIG = False

                    break

            if flagIG:
                result = recursiveForwardChecking(assignment, newDomains, csp)

                if result != "Failure":
                    print(formatOutput(assignment, step[0], True))
                    exit()  # Fix later; figure out why it keeps recursing even though it should be done
                    # step[0] += 1
                    # return result

        print(formatOutput(assignment, step[0], False))
        step[0] += 1
        del assignment[var]
    return "Failure"


# Decide between backtracking & forwardchecking
if sys.argv[3] == "none":
    backtrackingSearch(domains=variablesDictionary, csp=constraintsArray)
elif sys.argv[3] == "fc":
    forwardCheckingSearch(domains=variablesDictionary, csp=constraintsArray)
else:
    print("Invalid arguments")
