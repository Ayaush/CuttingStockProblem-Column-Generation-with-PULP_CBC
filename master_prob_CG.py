import pulp
import  data

def master_prob(pattern,solver_type):
    """ solve mater problem  and return primal and Dual variable"""
    z = {}
    for pt in range(len(pattern)):
        if solver_type =="LP":
            z[(pt)] = pulp.LpVariable('z[{0}]'.format(pt), 0, None, pulp.LpContinuous)
        elif solver_type == "MILP":
            z[(pt)] = pulp.LpVariable('z[{0}]'.format(pt), 0, None, pulp.LpInteger)

    cs_prob = pulp.LpProblem("Master Problem", pulp.LpMinimize)

    for item in range(len(data.order_quantity)):
        a = [pattern[pt][item] * z[(pt)] for pt in range(len(pattern))]
        cs_prob += pulp.lpSum(a) >= data.order_quantity[item]
    a = [z[(pt)] for pt in range(len(pattern))]
    cs_prob += pulp.lpSum(a)
    cs_prob.writeLP("Model.lp")

    solver = pulp.getSolver('PULP_CBC_CMD', msg=False)
    cs_prob.solve(solver)

    model_status = str(pulp.LpStatus[cs_prob.status])
    obj_val = pulp.value(cs_prob.objective)
    print("master Problem Model Status = ", model_status," objective val :  ",obj_val)
    dual = []
    for name, c in list(cs_prob.constraints.items()):
        dual.append(c.pi)

    return dual,obj_val,z

if __name__ == '__main__':
    main()
