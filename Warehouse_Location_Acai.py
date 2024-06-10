import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.datasets import make_blobs
import pandas as pd
import csv
# Load data from CSV
data = pd.read_excel('LocationForecastAll.xlsx')

#Making canvace
#plot_size   = 20
#plot_width  = 5
#plot_height = 5

#params = {'legend.fontsize': 'large',
#          'figure.figsize': (plot_width,plot_height),
#          'axes.labelsize': plot_size,
#          'axes.titlesize': plot_size,
#          'xtick.labelsize': plot_size*0.75,
#          'ytick.labelsize': plot_size*0.75,
#          'axes.titlepad': 25}
#plt.rcParams.update(params)
#center_box = (100, 200) 

#Number of towns
node = 772
transp_unit_cost = 1
capacity_unit_cost = 1
facil_capacities = 30*365    #Add warehouse cap 30 tonnes per day = 10 refrigerate warehouse
#281169 is demand for 2030 linear, 41677.823520 for S2 HoltWinter
#10 refrigerated warehouse with 1095 tonnes/year gives 350400

custm_demands = [data['Year 2016']] #Add Acai demand data
custm_dem_high = (max(data['Year 2016'])) #Add Max Acai demand


#Extract only town with Acai
custm_demands = []
Lon = []
Lat = []
Name = []

Fac_demands = []
Fac_Lon = []
Fac_Lat = []
Fac_Name = []



for _, row in data.iterrows():
        if row['Year 2016'] >= 0:
            custm_demands.append(row['Year 2016'])
            Lon.append(row['Longitude'])
            Lat.append(row['Latitude'])
            Name.append(row['City'])

for _, row in data.iterrows():
        if row['Year 2016'] > 1095: #1095 is from 3 tonnes per day as minimum requirement of production to fill a refrigerated factory
            Fac_demands.append(row['Year 2016'])
            Fac_Lon.append(row['Longitude'])
            Fac_Lat.append(row['Latitude'])
            Fac_Name.append(row['City'])

print("Factory total capacity " + str(len(Fac_Name)*facil_capacities))
print("Total demand " + str(sum(custm_demands)))
custm_demands = data['Year 2016'].to_numpy()
coord = np.column_stack((Lon, Lat))
Fac_coord = np.column_stack((Fac_Lon, Fac_Lat))

#Plot Scatter
#node_size = plot_size*10*((custm_demands/custm_dem_high)**2)
#node_size = 70

#plt.scatter(coord[:, 0], 
 #           coord[:, 1],  
  #          s=node_size , 
   #         cmap='viridis', 
    #        zorder=1500);

#plt.xticks(np.arange(-75, -40, 5))
#plt.yticks(np.arange(-20, 20, 5))

from scipy.spatial import distance

import pandas as pd

# Define the path to your Excel file
excel_file = 'RiverDistance.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file, header=None)

# Convert the DataFrame to a list of lists
dist = df.values.tolist()

# Now, 'data' contains all rows from the Excel file as lists
# You can convert it to a NumPy array if needed
import numpy as np

dist_matrix = np.array(dist)

# If you want to print the array, you can use:
print(dist_matrix)

from pulp import *

prob = LpProblem('prob', LpMinimize)

S = [('S'+str(i+1)) for i in range(len(Fac_Name))]
D = [('C'+str(i+1)) for i in range(len(Name))]

P = {facility:(facil_capacities) for j,facility in enumerate(S)}

transp_cost_matrix = dist_matrix * transp_unit_cost

t = {customer:{facility:(transp_cost_matrix[i][j]) for j,facility in enumerate(S)} for i,customer in enumerate(D)}

c = {facility:(facil_capacities*capacity_unit_cost) for j,facility in enumerate(S)}
Q = {customer:(custm_demands[i]) for i,customer in enumerate(D)}


n_min = 1
n_max = len(Name)

x = LpVariable.dicts('x', (D,S), lowBound = 0, cat = LpContinuous)
y = LpVariable.dicts('y', S, lowBound = 0, upBound = 1, cat = LpInteger)

prob += lpSum([lpSum([x[i][j]*t[i][j] for j in S]) for i in D]) + lpSum([c[j]*y[j] for j in S])

for i in D:
    prob += lpSum([x[i][j] for j in S]) == Q[i]

for j in S:
    prob += lpSum([x[i][j] for i in D]) <= P[j]*y[j]

prob += lpSum([y[j] for j in S]) >= n_min
prob += lpSum([y[j] for j in S]) <= n_max

status = prob.solve()

print(f'STATUS\n{LpStatus[status]}\n')


chosen_facil = []
for j,facility in enumerate(S):
    if y[facility].varValue == 1:
        chosen_facil.append(Fac_Name[j])
       
print(f'We will be establishing a facility in {chosen_facil}')

#Clustering
#dist_matrix= pd.read_csv('dist_matrix.csv')
#print(dist_matrix)
#array = dist_matrix.to_numpy()
