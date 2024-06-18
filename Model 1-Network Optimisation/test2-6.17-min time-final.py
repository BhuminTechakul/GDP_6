#!/usr/bin/env python
# coding: utf-8

# test: 
# 1. 1 fac_type (max_q<cap<total_q)
# 2. min time 
# 3. 
# 4. potential location: top 30 production

# In[1]:


# define the optimisation problem

from pulp import *

prob1 = LpProblem('prob1', LpMinimize)


# In[2]:


# define parameters

import pandas as pd
import numpy as np

# sources and production

df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Weighted Production')
s = df['Source'].tolist()                        #list of sources of products
q = df['Weighted Production'].tolist()           #weighted production of each sorce

S = [('S'+str(k+1)) for k in range(len(s))]
Q = {source:(q[k]) for k,source in enumerate(S)}

Q


# In[3]:


# location and type of factories

df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Town-test')
t = df['Town'].tolist()  

T = [('T'+str(i+1)) for i in range(len(t))]      #list of potential location of factories

T


# In[4]:


df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Factory Type-test2')
f = df['Fac_Type'].tolist()
cap_fac = df['Capacity'].tolist()
c_fac = df['Cost'].tolist()

F = [('F'+str(j+1)) for j in range(len(f))]   #set of factory types
Cap_F = {factype:(cap_fac[j]) for j,factype in enumerate(F)}
C_F = {factype:(c_fac[j]) for j,factype in enumerate(F)}

Cap_F
C_F


# In[5]:


# export sites

df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Export Site')

p = df['Location'].tolist()
E = [('E'+str(l+1)) for l in range(len(p))]    #set of export sites

E


# In[6]:


# modes

df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Mode 1')

mode1 = df['Mode'].tolist()
M = [('M'+str(m+1)) for m in range(len(mode1))]     #set of modes from sources to factories

c_m1_int = df['Initial Cost'].tolist()
c_m1_ship = df['Shippment Cost'].tolist()
c_m1_cat = df['Category'].tolist()
c_m1_cap = df['Capacity'].tolist()
C_M_INT = {mode:(c_m1_int[m]) for m,mode in enumerate(M)}
C_M_SHIP = {mode:(c_m1_ship[m]) for m,mode in enumerate(M)}


v_m1 = df['Speed'].tolist()

df = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','Mode 2')

mode2 = df['Mode'].tolist()
N = [('N'+str(n+1)) for n in range(len(mode2))]     #set of modes from sources to factories

c_m2_int = df['Initial Cost'].tolist()
c_m2_ship = df['Shippment Cost'].tolist()
c_m2_cat = df['Category'].tolist()
c_m2_cap = df['Capacity'].tolist()
C_N_INT = {mode:(c_m2_int[n]) for n,mode in enumerate(N)}
C_N_SHIP = {mode:(c_m2_ship[n]) for n,mode in enumerate(N)}

v_m2 = df['Speed'].tolist()

C_N_SHIP


# In[7]:


dis_sf_water = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-SF-Water').iloc[0:, 1:].values.tolist()
dis_sf_road = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-SF-Road').iloc[0:, 1:].values.tolist()

dis_sf = np.zeros((len(s), len(t), len(f), len(mode1)))

print(len(s))
print(len(t))
print(len(f))
print(len(mode1))

print(len(dis_sf_water))
print(len(dis_sf_water[0]))
print(len(dis_sf_road))
print(len(dis_sf_road[0]))

print(len(dis_sf))
print(len(dis_sf[0]))
print(len(dis_sf[0][0]))
print(len(dis_sf[0][0][0]))


# In[8]:


for k in range(len(s)):
    for i in range(len(t)):
        for j in range(len(f)):
            for m in range (len(mode1)):
                if c_m1_cat[m] == 'Water':
                    dis_sf[k][i][j][m] = dis_sf_water[k][i]
                if c_m1_cat[m] == 'Road':
                    dis_sf[k][i][j][m] = dis_sf_road[k][i]
                    

T_SF = {
    source: {
        town: {
            factype: {
                mode: dis_sf[k][i][j][m]/(1000*v_m1[m]) 
                for m, mode in enumerate(M)
            } 
            for j, factype in enumerate(F)
        } 
        for i, town in enumerate(T)
    } 
    for k, source in enumerate(S)
}

print(f"T_SF: {str(T_SF)[:1000]}")

D_SF = {
    source: {
        town: {
            factype: {
                mode: dis_sf[k][i][j][m]/1000 
                for m, mode in enumerate(M)
            } 
            for j, factype in enumerate(F)
        } 
        for i, town in enumerate(T)
    } 
    for k, source in enumerate(S)
}


# In[9]:


dis_fe_water = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-FE-Water').iloc[0:, 1:].values.tolist()
#dis_fe_road = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-FE-Road').iloc[0:, 1:].values.tolist()
#dis_fe_air = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-FE-Air').iloc[0:, 1:].values.tolist()
dis_fe_rail = pd.read_excel('/Users/kouchenlu/Desktop/Transport Strategy.xlsx','OD Matrix-FE-Rail').iloc[0:, 1:].values.tolist()

dis_fe = np.zeros((len(t), len(f), len(p), len(mode2)))

for i in range(len(t)):
    for j in range(len(f)):
        for l in range(len(p)):
            for n in range (len(mode2)):
                if c_m2_cat[n] == 'Water':
                    dis_fe[i][j][l][n] = dis_fe_water[i][l]
                if c_m2_cat[n] == 'Road':
                    #dis_fe[i][j][l][n] = dis_fe_road[i][l]
                    dis_fe[i][j][l][n] = 9999999999
                if c_m2_cat[n] == 'Air':
                    #dis_fe[i][j][l][n] = dis_fe_air[i][l]
                    dis_fe[i][j][l][n] = 9999999999
                if c_m2_cat[n] == 'Rail':
                    dis_fe[i][j][l][n] = dis_fe_rail[i][l]

T_FE = {
    town: {
        factype: {
            export: {
                mode: dis_fe[i][j][l][n]/(1000*v_m2[n]) 
                for n, mode in enumerate(N)
            } 
            for l, export in enumerate(E)
        } 
        for j, factype in enumerate(F)
    } 
    for i, town in enumerate(T)
}

print(f"T_FE: {str(T_FE)[:1000]}")

D_FE = {
    town: {
        factype: {
            export: {
                mode: dis_fe[i][j][l][n]/1000 
                for n, mode in enumerate(N)
            } 
            for l, export in enumerate(E)
        } 
        for j, factype in enumerate(F)
    } 
    for i, town in enumerate(T)
}


# In[10]:


# define decision varibles

x = LpVariable.dicts('x', (T,F), lowBound = 0, upBound = 1, cat = LpInteger)      # is there a factory of type j in town i
y = LpVariable.dicts('y', (S,T,F,M), lowBound = 0, upBound = 1, cat = LpInteger)  # whether products collected from source k are transported to a type j factory in town i by mode m
z = LpVariable.dicts('z', (T,F,E,N), lowBound = 0, upBound = 1, cat = LpInteger)  # whether products processed in a type j factory in town i are transported to an export site l by mode n


# In[11]:


# define the objective function

# min time 
prob1 += lpSum([y[k][i][j][m]*T_SF[k][i][j][m] for m in M for j in F for i in T for k in S]) + \
         lpSum([z[i][j][l][n]*T_FE[i][j][l][n] for n in N for l in E for j in F for i in T])


# In[12]:


# define constraints

# factory construction - no more than 1 factory in a town
for i in T:
    prob1 += lpSum([x[i][j] for j in F]) <= 1

# source and factory distribution - it is possible for y to = 1 only if x = 1 -- change
for i in T:
    for j in F:
        for k in S:
            for m in M:
                prob1 += y[k][i][j][m] <= x[i][j]

# factory and export site distribution - it is possible for z to = 1 only if x = 1 -- change
for i in T:
    for j in F:
        for l in E:  
            for n in N:
                prob1 += z[i][j][l][n] <= x[i][j]
        
# ensure that products from each source are transported to 1 factory using 1 mode -- delete
for k in S:
    prob1 += lpSum([y[k][i][j][m] for j in F for i in T for m in M]) == 1


# ensure that products from each factory are transported to 1 export site using 1 mode -- delete and add * x[i][j]
for i in T:
    for j in F:
        prob1 += lpSum([z[i][j][l][n] for l in E for n in N]) == 1 * x[i][j]

# factory capacity constraint
for i in T:
    for j in F:
        prob1 += lpSum(y[k][i][j][m] * Q[k] for k in S for m in M) <= x[i][j] * Cap_F[j]


# In[13]:


# solution

status = prob1.solve()

print("STATUS\n" + LpStatus[status])


# In[28]:


import math

total_fac = 0

# Output values of x
print("Location of factories:")
for i in T:
    for j in F:
        if x[i][j].varValue == 1:
            index_i = int(i[1:]) - 1
            index_j = int(j[1:]) - 1
            total_fac += 1
            print(f"Factory {f[index_j]} located in: {t[index_i]}")
            #print(f"{t[index_i]}")

print(f"Total number of factories: {total_fac}")
            
# Output values of y
print("\nFactory assignment:")

output_s =[]
output_s_q = []
output_fac_sf = []
output_mode1 = []
output_mode1_n = []
output_dis_sf = []
output_cost_sf = []
output_time_sf = []

for k in S:
    for i in T:
        for j in F:
            for m in M:
                if y[k][i][j][m].varValue == 1:
                    index_k = int(k[1:]) - 1
                    index_i = int(i[1:]) - 1
                    index_j = int(j[1:]) - 1
                    index_m = int(m[1:]) - 1
                    print(f"Source {s[index_k]} --> {mode1[index_m]} --> Factory {t[index_i]} -- {f[index_j]}")
                    #wirte to excel
                    output_s.append(s[index_k])
                    output_s_q.append(q[index_k])
                    output_fac_sf.append(t[index_i])
                    output_mode1.append(mode1[index_m])
                    output_mode1_n.append(math.ceil(q[index_k]/c_m1_cap[index_m]))
                    output_dis_sf.append(dis_sf[index_k][index_i][index_j][index_m])
                    output_cost_sf.append(math.ceil(q[index_k]/c_m1_cap[index_m])*c_m1_int[index_m] + dis_sf[index_k][index_i][index_j][index_m]*c_m1_ship[index_m])
                    output_time_sf.append(dis_sf[index_k][index_i][index_j][index_m]/(1000*v_m1[index_m]))
                   
 # Output values of z
print("\nPort assignment:")

output_fac_fe = []
output_p = []
output_mode2 = []
output_mode2_cap = []
output_mode2_n = []
output_mode2_int = []
output_mode2_ship = []
output_dis_fe = []
output_cost_fe = []
output_time_fe = []

for i in T:
    for j in F:
        for l in E:
            for n in N:
                if z[i][j][l][n].varValue == 1:
                    index_i = int(i[1:]) - 1
                    index_j = int(j[1:]) - 1
                    index_l = int(l[1:]) - 1
                    index_n = int(n[1:]) - 1
                    print(f"Port {p[index_l]} <-- {mode2[index_n]} <-- Factory {t[index_i]} -- {f[index_j]}")
                    #wirte to excel
                    output_fac_fe.append(t[index_i])
                    output_p.append(p[index_l])
                    output_mode2.append(mode2[index_n])
                    output_mode2_cap.append(c_m2_cap[index_n])
                    output_mode2_int.append(c_m2_int[index_n])
                    output_mode2_ship.append(c_m2_ship[index_n])
                    output_mode2_n.append(0)
                    output_dis_fe.append(dis_fe[index_i][index_j][index_l][index_n])
                    output_cost_fe.append(0)
                    output_time_fe.append(dis_fe[index_i][index_j][index_l][index_n]/(1000*v_m2[index_n]))
                   
                    
# Output of total cost
print("\nTotal cost:")

total_cost = 0

for i in T:
    for j in F:
        total_cost += x[i][j].varValue * C_F[j]

for k in S:
    for i in T:
        for j in F:
            for m in M:
                total_cost += (y[k][i][j][m].varValue * D_SF[k][i][j][m] * C_M_SHIP[m]) + C_M_INT[m]

for i in T:
    for j in F:
        for l in E:
            for n in N:
                total_cost += (z[i][j][l][n].varValue * D_FE[i][j][l][n] * C_N_SHIP[n]) + C_N_INT[n]

print(f"{total_cost} dollars")

# Output of total time
print("\nTotal time:")
print(f"{prob1.objective.value()} hours")


# In[29]:


# Output

df_sf = pd.DataFrame({'Source': output_s, 'Production': output_s_q, 'Factory': output_fac_sf, 'Mode': output_mode1, 'Num of Veh': output_mode1_n, 
                  'Distance': output_dis_sf, 'Time': output_time_sf, 'Transport Cost': output_cost_sf})

df_fe = pd.DataFrame({'Factory': output_fac_fe, 'Port': output_p, 'Mode': output_mode2, 'Capacity': output_mode2_cap, 'Num of Veh': output_mode2_n, 
                  'Distance': output_dis_fe, 'Time': output_time_fe, 'Initial Cost': output_mode2_int, 'Shippment Cost': output_mode2_ship, 'Transport Cost': output_cost_fe})

filename = 'Output_Min_Time.xlsx'

sheet_name_sf = 'Sheet_SF'
sheet_name_fe = 'Sheet_FE'

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    df_sf.to_excel(writer, sheet_name=sheet_name_sf, index=False)  
    df_fe.to_excel(writer, sheet_name=sheet_name_fe, index=False)  


# In[ ]:




