
inner_expr = {}
indexes = {}
count = 0
kb = []
proved_expr = set()
# pvr = ((p->F)->r)
# p^r = ((p->(r->F))->F)


def dfs(cur):
    s = inner_expr[cur]
    kb.append(s)
    if s[0].isdigit():
        dfs(int(s[0]))
    if s[3].isdigit():
        dfs(int(s[3]))


def rhs_dfs(cur):
    if len(cur) == 1:
        if cur[0].isalpha():
            kb.append(cur)
        else:
            next_expr = inner_expr[int(cur)]
            if next_expr[0].isalpha() and next_expr[3].isalpha():
                kb.append(next_expr)
            else:
                rhs_dfs(next_expr[0])
                rhs_dfs(next_expr[3])


def replace_or(expr):
    global count
    if expr[1] == 'v':
        inner_expr[count] = expr[0] + "->F"
        expr = str(count) + "->" + expr[len(expr)-1]
        count += 1
    return expr


def replace_and(expr):
    global count
    if expr[1] == '^':
        inner_expr[count] = expr[2] + "->F"
        inner_expr[count+1] = expr[0] + "->" + str(count)
        expr = str(count+1) + "->F"
        count += 2
    return expr


def replace_negation(expr):
    global count
    for i in range(2):
        pos = 0
        for c in expr:
            if c == '~':
                inner_expr[count] = expr[pos + 1:pos + 2] + "->F"
                expr = expr[:pos] + str(count) + expr[pos+2:]
                count += 1
                break
            pos += 1
    return expr


def update_expression(expr):
    expr = replace_negation(expr)
    expr = replace_or(expr)
    expr = replace_and(expr)
    return expr


def update_index():
    temp_set = set()
    for key, value in inner_expr.items():
        if value in temp_set:
            indexes[value].append(key)
        else:
            indexes[value] = [key]
            temp_set.add(value)


def deduction_theorem():
    flag = True
    while flag:
        flag = False
        for expr in kb:
            if len(expr) > 1 and str(expr[0]) in proved_expr and str(expr[3]) not in proved_expr:
                print(expr[3])
                if expr[3].isdigit():
                    nested_expr = inner_expr[int(expr[3])]
                    for i in indexes[nested_expr]:
                        proved_expr.add(str(i))
                else:
                    proved_expr.add(expr[3])
                flag = True
        if "F" in proved_expr:
            return True
    return False


def evaluate_expression():
    for expr in kb:
        if len(expr) == 1:
            proved_expr.add(expr)
    validity = deduction_theorem()
    if validity:
        print("Yippie!! It's a theorem")
    else:
        print("Need some help, senpai (*^*)\n Provide me some guidance senpai:-")


def parse(expr):
    start_pos = 0
    global count
    count = 0
    inner_expr.clear()
    kb.clear()
    proved_expr.clear()
    while not (expr[0] != '(' and expr[len(expr)-1] != ')'):
        pos = 0
        for c in expr:
            if c == '(':
                start_pos = pos
            if c == ')':
                temp = update_expression(expr[start_pos + 1:pos])
                inner_expr[count] = temp
                expr = expr[:start_pos] + str(count) + expr[pos+1:]
                count += 1
                break
            pos += 1

    if not expr.__eq__(str(count-1)):
        temp = update_expression(expr)
        inner_expr[count] = temp
        count += 1

    for i, j in inner_expr.items():
        print(i, j)

    if inner_expr[count-1][0].isdigit():
        #dfs(int(inner_expr[count-1][0]))
        kb.append(inner_expr[int(inner_expr[count - 1][0])])
    else:
        kb.append(inner_expr[count-1][0])

    rhs_dfs(inner_expr[count-1][3])
    last_expr = kb.pop()
    if len(last_expr) > 1:
        kb.append(str(last_expr[0]))
        inner_expr[count] = str(last_expr[0])
        count += 1
        last_expr = last_expr[3]
    if last_expr != "F":
        inner_expr[count] = last_expr + "->F"
        count += 1
        kb.append(last_expr + "->F")
    print()
    for i in kb:
        print(i, end=" ")
    print()
    for i, j in inner_expr.items():
        print(i, j)
    print()
    update_index()
    for key, value in indexes.items():
        print(key, end=": ")
        for j in value:
            print(j, end=" ")
        print()
    evaluate_expression()


def main():
    choice = "y"
    while choice.__eq__("y") or choice.__eq__("Y"):
        expression = input("Enter the complete expression: ")
        parse(expression)
        choice = input("Do you want to continue?(y/Y for yes): ")


if __name__ == '__main__':
    main()
