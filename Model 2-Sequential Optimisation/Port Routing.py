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

# Read all sheets from the Excel file
results = pd.read_excel('results_MinCostTime.xlsx', sheet_name=None)

# Access the 'Chosen Facilities' sheet
transportation_results_sheet = results['Transportation Results']
chosen_facilities_sheet = results['Chosen Facilities']
network_sheet = results['Network']

chosen_facilities = chosen_facilities_sheet['Chosen Facilities'].to_numpy()



Quantity_Facilities = []
for i in range(len(chosen_facilities)):
    Quantity = 0
    for _, row in transportation_results_sheet.iterrows():
      if row['Destination'] == chosen_facilities[i]:
         Quantity += float(row['Quantity'])
    Quantity_Facilities.append(float(Quantity))
    

Factory = []
for i in range(len(chosen_facilities)):
    Factory.append(chosen_facilities[i])
    
    
Port_Name = ['Manaus','São Luís']
Port = []
for i in range(len(Port_Name)):
    loc = (np.where(Name == Port_Name[i]))
    Port.append(loc[0].item())
    
towns_to_skip = []
Town = []
for i in range(len(Factory)):
    skip = (np.where(Name == Factory[i]))
    Town.append(skip[0].item())
    
TotalTown = list(range(767))
rows_to_skip = [item for item in TotalTown if item not in Town]
# Load distance matrices (/1000 to be km)
dist_matrix_River = (pd.read_excel('RiverDistance.xlsx', usecols = Port, skiprows = rows_to_skip, header=None).values / 1000)
dist_matrix_Road = (pd.read_excel('RoadDistance.xlsx', usecols = Port,skiprows = rows_to_skip, header=None).values / 1000)
dist_matrix_Rail = (pd.read_excel('RailDistance.xlsx', usecols = Port,skiprows = rows_to_skip, header=None).values / 1000)
    
    
# Define transportation modes and their properties
#Mode = ['Freezer Boat', 'Ferry with Freezer', 'Mid Size ferry', 'Large ferry', 'River Barges', 'Voadeiras', 'Refrigerator truck', 'Pickup Truck', 'Vans', 'Normal Truck']
Mode = ['Ferry with Freezer', 'Mid Size ferry', 'Large ferry', 'River Barges', 'Refrigerator truck','Normal Truck','Standard Cargo Train','Refrigerated Cargo Train']

# Mode Capacity in tonnes
#mode_capacity = [32, 125, 150, 900, 3500, 0.3, 18, 1.25, 5, 22.5]
mode_capacity = [125, 150, 900,3500, 18, 22.5,7000,7000]

# Mode fix cost ($/vehicle)
#mode_fcost = [3790000, 600000, 2000000, 4000000, 1250000, 17500, 150000, 32500, 30000, 100000]
mode_fcost = [600000, 2000000,4000000,1250000, 150000, 100000,2000000,5000000]

# Mode variable cost (Per tonne per km)
#mode_vcost = [0.04350, 0.125, 0.0435, 0.0435, 0.03, 0.3, 3, 2.5, 1.25, 1.75]
mode_vcost = [ 0.125, 0.0435, 0.0435, 0.03, 3, 1.75, 0.02, 0.035]
# Mode speed (km/h)
#mode_speed = [18.4, 20, 21, 21, 12, 34, 80, 65, 70, 80]
mode_speed = [20, 21, 21, 12, 80, 80, 60, 60]
    
Port 
# Define decision variable
S = ['S' + str(i + 1) for i in range(len(Port))]  # Port
D = ['D' + str(i + 1) for i in range(len(Factory))]  # Factory
M = ['M' + str(i + 1) for i in range(len(Mode))]  # Mode
   
print('Defining Parameters')
# Define parameters

print('Define QF')
# Quantity for each facility
QF = {customer: Quantity_Facilities[i] for i, customer in enumerate(D)}

print('Define d')
# Customer-Facility distance based on mode
d = {customer: {facility: {mode: (dist_matrix_River[i, j] if k < 4 else dist_matrix_Road[i, j] if k >= 4 and k < 6 else dist_matrix_Rail[i,j] )
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
                math.ceil(QF[customer] / m[mode]) * mode_fcost[k] * (d[customer][facility][mode] if int(d[customer][facility][mode]) == 0 else 1) +
                (d[customer][facility][mode]) * mode_vcost[k] * QF[customer] * math.ceil(QF[customer] / m[mode]))
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
z = LpVariable.dicts('z', (D, S, M), lowBound=0, upBound=1, cat=LpInteger)  # Route.mode used open or not

# Define Objective function options
print('Setting Obj function')
def objective_function(option):
    if option == 1:  # Minimise cost for initial investment and 1 day operation
        return lpSum([mc[i][j][k] * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ])
    elif option == 2:  # Minimise time
        return lpSum([(d[i][j][k] / s[k]) * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
                    ])
    elif option == 3:  # Minimise cost and time
        return lpSum([mc[i][j][k] * x[i][j][k]
                    for i in D
                    for j in S
                    for k in M
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
    prob += lpSum([x[i][j][k] for j in S for k in M]) == QF[i]
    
print('Setting prob Prevent trip with zero distance')
# Prevent trip with zero distance
for i in D:
    for j in S:
        for k in M:
            if d[i][j][k] == 0 and i != j:
                prob += x[i][j][k] == 0
                
print('Setting prob Travel time constraint: time must be less than 24')
# Travel time constraint: time must be less than 24 hours
for i in D:
    for j in S:
        for k in M:
            if k not in ['M1', 'M5','M8']:
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
                if mode_index < 4:
                    distance_matrix = "River"
                    distance = dist_matrix_River[int(i[1:]) - 1, int(j[1:]) - 1]
                elif mode_index >= 4 and mode_index < 6:
                    distance_matrix = "Road"
                    distance = dist_matrix_Road[int(i[1:]) - 1, int(j[1:]) - 1]
                else:
                    distance_matrix = "Rail"
                    distance = dist_matrix_Rail[int(i[1:]) - 1, int(j[1:]) - 1]
                # Calculate travel time based on the chosen mode
                travel_time = distance / s[k]
                num_vehicles = math.ceil(x[i][j][k].varValue / m[k])
                route_cost = mc[i][j][k]
                totalcost += route_cost
                totaltime += travel_time * num_vehicles  # Sum travel time for all vehicles
                print(f"Customer {i} ({Factory[int(i[1:]) - 1]}) to Facility {j} ({Port_Name[int(j[1:]) - 1]}) using {Mode[mode_index]}")
                print(f"  Quantity: {x[i][j][k].varValue}")
                print(f"  Number of vehicles: {num_vehicles}")
                print(f"  Travel time: {travel_time} hours per vehicle")
                print(f"  Total travel time for all vehicles: {travel_time * num_vehicles} hours")
                print(f"  Cost for this route: {route_cost}")
                print(f"  Distance matrix used: {distance_matrix}")
                print(f"  Distance: {distance} km")


print(f"Network total transportation cost: {totalcost}")
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
                if mode_index < 4:
                    distance_matrix = "River"
                    distance = dist_matrix_River[int(i[1:]) - 1, int(j[1:]) - 1]
                elif mode_index >= 4 and mode_index < 6:
                    distance_matrix = "Road"
                    distance = dist_matrix_Road[int(i[1:]) - 1, int(j[1:]) - 1]
                else:
                    distance_matrix = "Rail"
                    distance = dist_matrix_Rail[int(i[1:]) - 1, int(j[1:]) - 1]

                travel_time = distance / s[k]
                num_vehicles = math.ceil(x[i][j][k].varValue / m[k])
                route_cost = mc[i][j][k]   
                results_data.append([
                    Factory[int(i[1:]) - 1],
                    Port_Name[int(j[1:]) - 1],
                    Mode[mode_index],
                    x[i][j][k].varValue,
                    num_vehicles,
                    travel_time,
                    travel_time * num_vehicles,
                    route_cost,
                    distance_matrix,
                    distance
                ])

# Convert lists to DataFrame
results_df = pd.DataFrame(results_data, columns=[
    'Origin', 'Destination', 'Mode', 'Quantity', 'Number of Vehicles', 
    'Travel Time (hrs/vehicle)', 'Total Travel Time (hrs)', 
    'Cost for this Route', 'Distance Matrix Used', 'Distance (km)' 
])

AllCost = totalcost + network_sheet['Echelon1 Cost']
AllTime = totaltime + network_sheet['Echelon1 Time']
network_data = [[totalcost,totaltime,
    float(AllCost[0]),
    float(AllTime[0])]
]
network_df = pd.DataFrame(network_data, columns=['Echelon2 Cost', 'Echelon2 Time','Network Cost','Network Time'])

# Save to Excel
with pd.ExcelWriter('results_MinCost_MinCost.xlsx') as writer:
    results_df.to_excel(writer, sheet_name='Transportation Results', index=False)
    network_df.to_excel(writer, sheet_name='Network', index=False)


