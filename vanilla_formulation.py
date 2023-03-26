import pulp
import  data

def main():
    no_of_bars = sum(data.order_quantity)
    x,y ={},{}
    for item in range(data.item_count):
        for bar in range(no_of_bars):
            x[(item, bar)] = pulp.LpVariable('x[{0}_{1}]'.format(item, bar), 0,None,pulp.LpInteger)
            y[(bar)] = pulp.LpVariable('y[{0}]'.format(bar),0,1,pulp.LpBinary)

    cs_prob = pulp.LpProblem("cutting stock problem", pulp.LpMinimize)

    for bar in range(no_of_bars):
        a = [data.order_width[item]* x[(item,bar)] for item in range(data.item_count) ]
        cs_prob += pulp.lpSum(a)<= data.bar_length*y[(bar)]

    for item in range(data.item_count):
        a = [x[(item, bar)] for bar in range(no_of_bars)]
        cs_prob += pulp.lpSum(a) >= data.order_quantity[item]
    a =[y[(bar)] for bar in range(no_of_bars)]
    cs_prob += pulp.lpSum(a)
    #cs_prob.writeLP("Model.lp")

    try:
        solver =pulp.CPLEX_CMD(path=path_to_cplex,timeLimit=300,gapRel=0.001, msg=True)
        cs_prob.solve(solver)
    except:
        solver = pulp.getSolver('PULP_CBC_CMD', msg=True)
        cs_prob.solve(solver)

    model_status = str(pulp.LpStatus[cs_prob.status])
    print("Model Status = ",model_status)
    print("Objective Value", pulp.value(cs_prob.objective))
    pattern_list = {}
    for i in range(len(y)):
        if y[(i)].varValue > 0 :
            pattern =str([x[(item,i)].varValue for item in range(data.item_count)])
            pattern_list.setdefault(pattern, 0)
            pattern_list[pattern]+=1
    for i in pattern_list.keys():
        print("pattern ", i, "= ",pattern_list[i])


if __name__ == '__main__':
    main()
