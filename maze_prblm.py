from pymaze import maze,COLOR,agent,textLabel
from random import *

def rand_gene():
    a=[]
    for i in range(population):
        a= [randint(1,row) for j in range(col)]
        rand_pop.append(a)
        rand_pop[i][0]= 1
        rand_pop[i][col-1]=row

def path_turns(gene):

    turns=0
    for i in range(1,col):
        if (abs(rand_pop[gene][i-1]-rand_pop[gene][i]))!=0:
            turns+=2

    return turns

def path_steps(gene):

    steps=0
    for i in range(1,col):
        steps+=(abs(rand_pop[gene][i-1]-rand_pop[gene][i]))
        steps+=1

    return steps

def obstacles(gene):

    inf_step=0
    c=1
    for i in range(1,col):
        
        if(rand_pop[gene][i]>rand_pop[gene][i-1]):
            for j in range(rand_pop[gene][i-1],rand_pop[gene][i]):
                if (map[(j,c)]['S']==0):
                    inf_step+=1
            if(map[rand_pop[gene][i],c]['E'])==0:
                inf_step+=1
        else:
            for k in range(rand_pop[gene][i-1],rand_pop[gene][i],-1):
                if(map[(k,c)]['N'])==0:
                    inf_step+=1
            if(map[rand_pop[gene][i],c]['E'])==0:
                inf_step+=1
        c+=1

    return inf_step

def maxVal():

    global max_turn
    global min_turn
    global max_inf_step
    global min_inf_step
    global max_len
    global min_len

    for i in range(population):
        if max_len < path_steps(i):
            max_len = path_steps(i)
        if min_len > path_steps(i):
            min_len = path_steps(i)
        if max_turn < path_turns(i):
            max_turn = path_turns(i)
        if min_turn > path_turns(i):
            min_turn = path_turns(i)
        if max_inf_step < obstacles(i):
            max_inf_step = obstacles(i)
        if min_inf_step > obstacles(i):
            min_inf_step = obstacles(i)

def fitness_fn(gene):
    weight_f = 50
    weight_l = 1
    weight_t = 1

    fit_inf_step = (float)(1 - ((obstacles(gene) - min_inf_step) / (max_inf_step - min_inf_step)))
    fit_len = (float)(1 - ((path_steps(gene) - min_len) / (max_len - min_len)))
    fit_turns = (float)(1 - ((path_turns(gene) - min_turn) / (max_turn - min_turn)))

    f = (float)((weight_f * fit_inf_step) + (weight_l * fit_len) + (weight_t * fit_turns))

    return f

def bubble_sorting():
    for p in range(population-1):
        for i in range(population-1):
            if fitness_fn(i+1)>fitness_fn(i):
                temp= rand_pop[i]
                rand_pop[i]=rand_pop[i+1]
                rand_pop[i+1]=temp

def cross_over():
    cut_point=randint(2,col-2)
    for i in range(int(population/2)):
        for j in range(cut_point):
            rand_pop[i+int(population/2)][j]=rand_pop[i][j]
        for j in range(cut_point,col-1):
            rand_pop[i+int(population/2)][j]=rand_pop[i+1][j]

def mutation():
    rand_index=0
    for i in range(0,population,2):
        rand_index= randint(1,col-2)
        rand_pop[i][rand_index]=randint(1,row)

def display():
    path=[]
    f_step=(row,row)
    for i in range(1,col):
        if((rand_pop[0][i])>(rand_pop[0][i-1])):
            for j in range(rand_pop[0][i-1],(rand_pop[0][i])+1):
                newStep=(j,i)
                path.append(newStep)
        else:
            for j in range(rand_pop[0][i-1],(rand_pop[0][i])-1,-1):
                newStep=(j,i)
                path.append(newStep)
    path.append(f_step)
    return path

# Main Programe

max_len = 0
min_len = 100
max_inf_step = 0
min_inf_step = 100
max_turn = 0       
min_turn = 100

row=10
col=10
population=100

m=maze(row,col)
m.CreateMaze(row,col,pattern='v',loopPercent=100)
a=agent(m,1,1,footprints=True)
map=m.maze_map

rand_pop=[]
path=[]
rand_gene()  

for i in range(1,1000):
    maxVal()
    bubble_sorting()
    if min_inf_step==0:
        break
    cross_over()
    mutation()
    
    print(f'iterations = {i} / inf_step = {min_inf_step}')

path=display()
print()
print(rand_pop[0])
print()
print(path)

m.tracePath({a:path}, delay=50)
l1=textLabel(m,'Total Cells',m.rows*m.cols)
l1=textLabel(m,'Syed Zain-ul-Aabideen',86)
m.run()
