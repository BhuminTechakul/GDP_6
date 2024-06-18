import numpy as np
import pandas as pd
from pulp import *
import math
from scipy.sparse import csr_matrix
print('Getting demand data')
# Load data from CSV
data = pd.read_excel('LocationForecastAll.xlsx')

# Extract all towns in the Amazon region
#Lon = data['Longitude'].to_numpy()
#Lat = data['Latitude'].to_numpy()

 
Name = data['City'].to_numpy()
custm_demands = data['Weighted Production'].to_numpy()

# Define facility demands and coordinates based on demand threshold
facil_threshold = 1.65 # Minimum production requirement to fill a refrigerated factory
Fac_demands = data[data['Weighted Production'] > facil_threshold]['Weighted Production'].to_numpy()
Fac_Name = data[data['Weighted Production'] > facil_threshold]['City'].to_numpy()
Factory = []
for i in range(len(Fac_Name)):
    loc = (np.where(Name == Fac_Name[i]))
    Factory.append(loc[0].item())
    
print('Defining properties')
# Define transportation modes and their properties
#Mode = ['Freezer Boat', 'Ferry with Freezer', 'Mid Size ferry', 'Large ferry', 'River Barges', 'Voadeiras', 'Refrigerator truck', 'Pickup Truck', 'Vans', 'Normal Truck']
Mode = ['Ferry with Freezer', 'Mid Size ferry', 'Refrigerator truck','Normal Truck']

# Mode Capacity in tonnes
#mode_capacity = [32, 125, 150, 900, 3500, 0.3, 18, 1.25, 5, 22.5]
mode_capacity = [125, 150, 18, 22.5]

# Mode fix cost ($/vehicle)
#mode_fcost = [3790000, 600000, 2000000, 4000000, 1250000, 17500, 150000, 32500, 30000, 100000]
mode_fcost = [600000, 2000000, 150000, 100000]

# Mode variable cost (Per tonne per km)
#mode_vcost = [0.04350, 0.125, 0.0435, 0.0435, 0.03, 0.3, 3, 2.5, 1.25, 1.75]
mode_vcost = [ 0.125, 0.0435, 3, 1.75]
# Mode speed (km/h)
#mode_speed = [18.4, 20, 21, 21, 12, 34, 80, 65, 70, 80]
mode_speed = [20, 21, 80, 80]

print('loading OD')

# Load distance matrices (/1000 to be km)
dist_matrix_River = (pd.read_excel('RiverDistance.xlsx', usecols = Factory, header=None).values / 1000)
dist_matrix_Road = (pd.read_excel('RoadDistance.xlsx', usecols = Factory,header=None).values / 1000)



print('Defining decision variables')
ODpair = 10 #All is 767
# Define decision variable
S = ['S' + str(i + 1) for i in range(len(Factory))]  # Factory
D = ['D' + str(i + 1) for i in range(767)]  # Town
M = ['M' + str(i + 1) for i in range(len(Mode))]  # Mode

print('Defining Parameters')
# Define parameters

# Facility Capacities
facil_capacities = 150  # 800 tonnes
capacity_unit_cost = 4627500  # $ per facility open
print('Define P')
P = {facility: facil_capacities for facility in S}
print('Define c')
# Facility Cost
c = {facility: capacity_unit_cost for facility in S}
print('Define Q')
# Customer demands
Q = {customer: custm_demands[i] for i, customer in enumerate(D)}
print('Define d')
# Customer-Facility distance based on mode
d = {customer: {facility: {mode: (dist_matrix_River[i, j] if k < 2 else dist_matrix_Road[i, j])
            for k, mode in enumerate(M)
        }
        for j, facility in enumerate(S)
    }
    for i, customer in enumerate(D)
}
print('Define m')
# Mode capacity
m = {mode: mode_capacity[k] for k, mode in enumerate(M)}
print('Define mc')
# Mode total Cost (Sum of fix cost(Customer demand * mode fix cost/mode capacity) and variable cost(distance for ij route using k mode * customer demand * mode variable cost))
mc = {customer: {facility: {mode: (
                math.ceil(Q[customer] / m[mode]) * mode_fcost[k] * (d[customer][facility][mode] if int(d[customer][facility][mode]) == 0 else 1) +
                (d[customer][facility][mode]) * mode_vcost[k] * Q[customer] * math.ceil(Q[customer] / m[mode]))
                for k, mode in enumerate(M)
        }
        for j, facility in enumerate(S)
    }
    for i, customer in enumerate(D)
}
print('Define s')
# Mode Speed
s = {mode: mode_speed[k] for k, mode in enumerate(M)}

print('Define decision variables')
# Decision variables
x = LpVariable.dicts('x', (D, S, M), lowBound=0, cat=LpContinuous)  # Quantity on route D to S using M
y = LpVariable.dicts('y', S, lowBound=0, upBound=1, cat=LpInteger)  # Facility open or not
z = LpVariable.dicts('z', (D, S, M), lowBound=0, upBound=1, cat=LpInteger)  # Route.mode used open or not

# Define Objective function options
print('Setting Obj function')
def objective_function(option):
    if option == 1:  # Minimise cost for initial investment and 1 day operation
        return lpSum([mc[i][j][k] * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ]) + lpSum([c[j] * y[j]
                    for j in S
                    ])
    elif option == 2:  # Minimise time
        return lpSum([(d[i][j][k] / s[k]) * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ])
    elif option == 3:  # Minimise cost and time
        return lpSum([(mc[i][j][k]/10000) * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ]) + lpSum([c[j] * y[j]
                    for j in S
                    ]) + lpSum([(d[i][j][k] / s[k]) * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ])


# Set the objective function (option 1, 2, or 3)
objective_option = 1

print('Setting prob Obj function')
prob = LpProblem('prob', LpMinimize)
prob += objective_function(objective_option)

# Define constraints
print('Setting prob Each customers product must be delivered')
# Each customer's product must be delivered
for i in D:
    prob += lpSum([x[i][j][k] for j in S for k in M]) == Q[i]
print('Setting prob Ensure that a facility is open if it is used')
# Ensure that a facility is open if it is used
for i in D:
    for j in S:
        prob += lpSum([z[i][j][k] for k in M]) <= y[j]
print('Setting prob Prevent trip with zero distance')
# Prevent trip with zero distance
for i in D:
    for j in S:
        for k in M:
            if d[i][j][k] == 0 and i != j:
                prob += z[i][j][k] == 0
print('Setting prob Each facilitys capacity must not be exceeded')
# Each facility's capacity must not be exceeded
for j in S:
    prob += lpSum([x[i][j][k] for i in D for k in M]) <= P[j] * y[j]
print('Setting prob At least n_min and at most n_max facilities should be used')
# At least n_min and at most n_max facilities should be used
n_min = 1
n_max = len(Factory)
prob += lpSum([y[j] for j in S]) >= n_min
prob += lpSum([y[j] for j in S]) <= n_max
print('Setting prob Only one mode is used for each customer-facility pair')
# Only one mode is used for each customer-facility pair
for i in D:
    for j in S:
        prob += lpSum([z[i][j][k] for k in M]) <= 1
print('Setting prob Each customer is assigned to only one facility')
# Each customer is assigned to only one facility
for i in D: 
    prob += lpSum([z[i][j][k] for j in S for k in M]) == 1
print('Setting prob z and x relationship')
# z and x relationship
for i in D:
    for j in S:
        for k in M:
            prob += x[i][j][k] <= Q[i] * z[i][j][k]
            prob += z[i][j][k] <= y[j]
print('Setting prob Travel time constraint: time must be less than 24')
# Travel time constraint: time must be less than 24 hours
for i in D:
    for j in S:
        for k in M:
            if k not in ['M1', 'M3']:
                prob += (d[i][j][k] / s[k]) * z[i][j][k] <= 24
                

print('Start solving')
# Solve the problem
status = prob.solve()
print('Done solving')
# Output the results
totalcost = 0
totaltime = 0
chosen_facilities = []
for i in D:
    for j in S:
        for k in M:
            if x[i][j][k].varValue > 0:
                # Determine which distance matrix is used
                mode_index = int(k[1:]) - 1
                if mode_index < 2:
                    distance_matrix = "River"
                    distance = dist_matrix_River[int(i[1:]) - 1, int(j[1:]) - 1]
                else:
                    distance_matrix = "Road"
                    distance = dist_matrix_Road[int(i[1:]) - 1, int(j[1:]) - 1]

                # Calculate travel time based on the chosen mode
                travel_time = distance / s[k]
                num_vehicles = math.ceil(x[i][j][k].varValue / m[k])
                route_cost = mc[i][j][k]
                totalcost += route_cost
                totaltime += travel_time * num_vehicles  # Sum travel time for all vehicles
                print(travel_time)
                print(f"Customer {i} ({Name[int(i[1:]) - 1]}) to Facility {j} ({Fac_Name[int(j[1:]) - 1]}) using {Mode[mode_index]}")
                print(f"  Quantity: {x[i][j][k].varValue}")
                print(f"  Number of vehicles: {num_vehicles}")
                print(f"  Travel time: {travel_time} hours per vehicle")
                print(f"  Total travel time for all vehicles: {travel_time * num_vehicles} hours")
                print(f"  Cost for this route: {route_cost}")
                print(f"  Distance matrix used: {distance_matrix}")
                print(f"  Distance: {distance} km")

for j in S:
    if y[j].varValue > 0:
        chosen_facilities.append(Fac_Name[int(j[1:]) - 1])
        print(f"\nFacility {j} ({Fac_Name[int(j[1:]) - 1]}) used")

FacCount = len(chosen_facilities)
FacCost = FacCount * capacity_unit_cost
NetworkTotalCost = FacCost + totalcost
print(f"Chosen facilities: {chosen_facilities}")
print(f"Network total transportation cost: {totalcost}")
print(f"Network total cost: {NetworkTotalCost}")
print(f"Network total time: {totaltime} hours")
print(f'STATUS\n{LpStatus[status]}\n')

# Initialize lists to store data
results_data = []
facility_data = []

# Iterate over the decision variables to collect results
for i in D:
    for j in S:
        for k in M:
            if x[i][j][k].varValue > 0:
                mode_index = int(k[1:]) - 1
                if mode_index < 2:
                    distance_matrix = "River"
                    distance = dist_matrix_River[int(i[1:]) - 1, int(j[1:]) - 1]
                else:
                    distance_matrix = "Road"
                    distance = dist_matrix_Road[int(i[1:]) - 1, int(j[1:]) - 1]

                travel_time = distance / s[k]
                num_vehicles = math.ceil(x[i][j][k].varValue / m[k])
                route_cost = mc[i][j][k]   
                results_data.append([
                    Name[int(i[1:]) - 1],
                    Fac_Name[int(j[1:]) - 1],
                    Mode[mode_index],
                    x[i][j][k].varValue,
                    num_vehicles,
                    travel_time,
                    travel_time * num_vehicles,
                    route_cost,
                    distance_matrix,
                    distance
                ])
# Append chosen facilities data
for j in S:
    if y[j].varValue > 0:
        facility_data.append(Fac_Name[int(j[1:]) - 1])

# Convert lists to DataFrame
results_df = pd.DataFrame(results_data, columns=[
    'Origin', 'Destination', 'Mode', 'Quantity', 'Number of Vehicles', 
    'Travel Time (hrs/vehicle)', 'Total Travel Time (hrs)', 
    'Cost for this Route', 'Distance Matrix Used', 'Distance (km)' 
])
network_data = [[
    NetworkTotalCost,
    totaltime
]]


facility_df = pd.DataFrame({'Chosen Facilities': facility_data})
network_df = pd.DataFrame(network_data, columns=['Echelon1 Cost', 'Echelon1 Time'])
# Save to Excel
with pd.ExcelWriter('results_MinCost.xlsx') as writer:
    results_df.to_excel(writer, sheet_name='Transportation Results', index=False)
    facility_df.to_excel(writer, sheet_name='Chosen Facilities', index=False)
    network_df.to_excel(writer, sheet_name='Network', index=False)


