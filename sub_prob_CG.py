import pulp

import data


def sub_prob(dual):
    """ Solve sun problem and return new pattern and reduced cost"""
    x = {}
    for item in range(data.item_count):
        x[(item)] = pulp.LpVariable('x[{0}]'.format(item), 0, None, pulp.LpInteger)

    cs_prob = pulp.LpProblem("Sub Problem", pulp.LpMinimize)

    a = [x[(item)] * data.order_width[item] for item in range(data.item_count)]
    cs_prob += pulp.lpSum(a) <= data.bar_length
    a = [x[(item)]*dual[item] for item in range(data.item_count)]
    cs_prob += 1 - pulp.lpSum(a)
    cs_prob.writeLP("sub_problem_Model.lp")

    solver = pulp.getSolver('PULP_CBC_CMD', msg=False)
    cs_prob.solve(solver)

    model_status = str(pulp.LpStatus[cs_prob.status])
    obj_val = pulp.value(cs_prob.objective)
    print("sub problem Model Status = ", model_status," obj Val =",obj_val)
    new_pattern = []
    for i in x.keys():
        new_pattern.append(x[i].varValue)
    return new_pattern,obj_val

