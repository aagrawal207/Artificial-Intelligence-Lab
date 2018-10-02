def replace_or(expr, inner_expr, count):
    if expr[1] == 'v':
        inner_expr[count] = (expr[0], "F")
        expr = str(count) + "->" + expr[len(expr)-1]
        count += 1
    return expr, inner_expr, count


def replace_and(expr, inner_expr, count):
    if expr[1] == '^':
        inner_expr[count] = (expr[2], "F")
        inner_expr[count+1] = (expr[0], str(count))
        expr = str(count+1) + "->F"
        count += 2
    return expr, inner_expr, count


def replace_negation(expr, inner_expr, count):
    for i in range(2):
        pos = 0
        for c in expr:
            if c == '~':
                inner_expr[count] = (expr[pos + 1:pos + 2], "F")
                expr = expr[:pos] + str(count) + expr[pos+2:]
                count += 1
                break
            pos += 1
    return expr, inner_expr, count


def update_expression(expr, inner_expr, count):
    expr, inner_expr, count = replace_negation(expr, inner_expr, count)
    expr, inner_expr, count = replace_or(expr, inner_expr, count)
    expr, inner_expr, count = replace_and(expr, inner_expr, count)
    return expr, inner_expr, count


def simplify_expr(expr, inner_expr, count):
    temp, inner_expr, count = update_expression(expr, inner_expr, count)
    inner_expr[count] = (temp.split("->")[0], temp.split("->")[1])
    count += 1
    return inner_expr, count


def rhs_dfs(cur, kb, inner_expr):
    next_expr = inner_expr[int(cur)]
    if next_expr[0].isdigit():
        kb.append(inner_expr[int(next_expr[0])])
    else:
        kb.append(next_expr[0])
    if next_expr[1].isdigit():
        rhs_dfs(next_expr[1], kb, inner_expr)
    else:
        kb.append(next_expr[1])


def dfs(expr, inner_expr):
    if len(expr) == 1:
        return expr
    left_side_expression = dfs(inner_expr[int(expr[0])], inner_expr) if expr[0].isdigit() else expr[0]
    right_side_expression = dfs(inner_expr[int(expr[1])], inner_expr) if expr[1].isdigit() else expr[1]
    return "(" + left_side_expression + "->" + right_side_expression + ")"


def update_index(inner_expr, indexes, parsed_help_expr={}, kb=[]):
    temp_set = set()
    for key, value in inner_expr.items():
        if value in temp_set:
            indexes[value].append(str(key))
        else:
            indexes[value] = [str(key)]
            temp_set.add(value)
    flag = True
    temp_map = {}
    while flag:
        flag = False
        temp_map.clear()
        temp_set.clear()
        for key, value in indexes.items():
            if len(value) == 1:
                continue
            x = value[0]
            for key1, value1 in inner_expr.items():
                value2 = (x if value1[0] in value else value1[0], x if value1[1] in value else value1[1])
                if value1 != value2:
                    flag = True
                    if value2 in temp_set:
                        temp_map[value2].append(str(key1))
                    else:
                        temp_map[value2] = [str(key1)]
                        temp_set.add(value2)
                    if value1 in kb:
                        kb.append(value2)
                inner_expr[key1] = value2
                if key1 in parsed_help_expr.keys():
                    parsed_help_expr[key1] = value2

            if flag:
                indexes[key] = [value[0]]
                break
        for key, value in indexes.items():
            if key in temp_map.keys():
                temp_map[key].extend(value)
        indexes.update(temp_map)
    return indexes


def modus_ponens(expr, proved_expr, indexes, inner_expr, results):
    if str(expr[0]) in proved_expr and str(expr[1]) not in proved_expr:
        if expr[1].isdigit():
            proved_expr.add(str(indexes[inner_expr[int(expr[1])]][0]))
        else:
            proved_expr.add(expr[1])
        lhs = dfs(inner_expr[int(expr[0])], inner_expr) if expr[0].isdigit() else expr[0]
        rhs = dfs(inner_expr[int(expr[1])], inner_expr) if expr[1].isdigit() else expr[1]
        results.append("Modus Ponens: ")
        results.append(lhs)
        results.append(lhs + "->" + rhs)
        results.append(rhs)
        return True
    return False


def deduction_theorem(indexes, inner_expr, kb, proved_expr):
    flag = True
    results = []
    while flag:
        flag = False
        for expr in kb:
            if len(expr) == 1:
                continue
            flag |= modus_ponens(expr, proved_expr, indexes, inner_expr, results)
        if "F" in proved_expr:
            return True, results
    return False, results


def evaluate_expression(indexes, inner_expr, kb):
    proved_expr = set()
    for expr in kb:
        if len(expr) == 1:
            proved_expr.add(expr)
        elif str(expr[0]).isalpha() and str(expr[1]).__eq__("F"):
            proved_expr.add(str(indexes[expr][0]))
    return deduction_theorem(indexes, inner_expr, kb, proved_expr)


def query_ans(result_found, results=[]):
    if not result_found:
        print("Looks like it didn't work out this time between us. Sorry!")
    else:
        print("We did it! It's a theorem")
        for expr in results:
            print(expr)


def parse(expr, count):
    start_pos = 0
    inner_expr = {}
    kb = []
    while not (expr[0] != '(' and expr[len(expr)-1] != ')'):
        pos = 0
        for c in expr:
            if c == '(':
                start_pos = pos
            if c == ')':
                inner_expr, count = simplify_expr(expr[start_pos + 1:pos], inner_expr, count)
                expr = expr[:start_pos] + str(count-1) + expr[pos+1:]
                break
            pos += 1

    if expr != str(count-1):
        inner_expr, count = simplify_expr(expr, inner_expr, count)

    x = inner_expr[count-1][0]
    flag = False
    while x.isdigit() and inner_expr[int(x)][0].isdigit() and inner_expr[int(x)][1] == 'F':
        x = inner_expr[int(x)][0]
        flag = True
    if flag:
        kb.append((x, 'F'))
    else:
        kb.append(inner_expr[int(x)] if x.isdigit() else x)
    if inner_expr[count-1][1].isalpha():
        kb.append(inner_expr[count-1][1])
    else:
        rhs_dfs(inner_expr[count-1][1], kb, inner_expr)
    last_expr = kb.pop()
    if str(last_expr) != "F":
        kb.append((last_expr, 'F'))
        inner_expr[count] = (last_expr, 'F')
        count += 1
    return inner_expr, list(set(kb)), count


def main(expression, cnt):
    inner_expr, kb, count = parse(expression, cnt)
    indexes = {}
    indexes = update_index(inner_expr, indexes)
    validity, results = evaluate_expression(indexes, inner_expr, kb)
    if validity:
        query_ans(True, results)
    else:
        print("Help me!! senpai (*^*)\n")
        extra_expr = input("Give me some extra expression to ease the task(say 'no' if you don't want to help): ")
        if extra_expr.__eq__("no"):
            query_ans(False)
            return
        parsed_help_expr, dummy1, dummy2 = parse(extra_expr, count)
        inner_expr.update(parsed_help_expr)
        indexes.clear()
        indexes = update_index(inner_expr, indexes, parsed_help_expr, kb)
        kb.extend(parsed_help_expr.values())
        kb = list(set(kb))
        validity, results = evaluate_expression(indexes, inner_expr, kb)
        query_ans(True, results) if validity else query_ans(False)


if __name__ == '__main__':
    choice = "y"
    while choice.__eq__("y") or choice.__eq__("Y"):
        expression = input("Enter the complete expression: ")
        cnt = 0
        main(expression, cnt)
        choice = input("Do you want to continue?(y/Y for yes): ")
