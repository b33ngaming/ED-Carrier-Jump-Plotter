import pyodbc
import numpy as np

# Enter the name of your database here
serverName = ''  

# Enter the name of your database here
databaseName = ''

# Enter your start and end points here
start = 'Lamaku'
end = 'Colonia'

currsys = [] 										# Var used in the while loop
distance = 999999999 								# Arbitrary Var for distance, it only needs to be greater than the carrier jump range.
jumps = 0 											# Var for the print statements
filename = f"{start}_to_{end}_Jump_Route.txt"		# Filename for the output text file
filename = filename.replace('*', '')				# Removes the special char for Sag A
filename = filename.replace(' ', '-')
file = open(filename, 'w+')							# Creates the file, or overwrites if it exists already

# Queries the database for the start coordinates
startquery = f"""
SELECT a.x, a.y, a.z
FROM {databaseName} as a
WHERE a.[name] = '{start}'"""

# Queries the database for the end coordinates
endquery = f"""
SELECT a.x, a.y, a.z
FROM {databaseName} as a
WHERE a.[name] = '{end}'"""

# create a connection to your database
cnxn = pyodbc.connect(f'DSN={serverName};Trusted_Connection=Yes')
cursor = cnxn.cursor()

# Grab starting coordinates from system in line 11, and print to console
print(f"Gathering coordinates for {start} system")
cursor.execute(startquery)
startCoord = np.array(cursor.fetchall())
print(f"{start} system coordinates, x:{startCoord[0, 0]} y:{startCoord[0, 1]} z:{startCoord[0, 2]}")

# Grab end coordinates from system in line 12, and print to console
print(f"\nGathering coordinates for {end} system")
cursor.execute(endquery)
endCoord = np.array(cursor.fetchall())
print(f"{end} system coordinates, x:{endCoord[0, 0]} y:{endCoord[0, 1]} z:{endCoord[0, 2]}\n")

print(f"Plotting a course from '{start}' to '{end}'\n")

# Loop will cycle through all the systems and write to the text file as well as print it out on the console
while currsys != end:

    systemsQuery = f"""
    SELECT TOP 1
    a.name,
    SQRT(POWER((a.x-({endCoord[0, 0]})),2) + POWER((a.y-({endCoord[0, 1]})),2) + POWER((a.z-({endCoord[0, 2]})),2)) 'Distance',
    a.x,
    a.y,
    a.z    
    
    FROM
    {databaseName} as a
    
    WHERE
    SQRT(POWER((a.x-({startCoord[0, 0]})),2) + POWER((a.y-({startCoord[0, 1]})),2) + POWER((a.z-({startCoord[0, 2]})),2)) < 500 AND
    SQRT(POWER((a.x-({endCoord[0, 0]})),2) + POWER((a.y-({endCoord[0, 1]})),2) + POWER((a.z-({endCoord[0, 2]})),2)) < SQRT(POWER((({endCoord[0, 0]})-({startCoord[0, 0]})),2) + POWER((({endCoord[0, 1]})-({startCoord[0, 1]})),2) + POWER((({endCoord[0, 2]})-({startCoord[0, 2]})),2))
    
    ORDER BY
    SQRT(POWER((a.x-({endCoord[0, 0]})),2) + POWER((a.y-({endCoord[0, 1]})),2) + POWER((a.z-({endCoord[0, 2]})),2))"""

    if float(distance) < 500:
        currsys = end
        jumps = jumps + 1
        print(f"Jump {jumps} is to {end}.\n\nScript completed successfully")
        with open(filename, 'a+') as fa:
            fa.write(f"Jump {jumps} is to {end}.\n\nScript completed successfully")

    else:
        cursor = cnxn.cursor()

        cursor.execute(systemsQuery)
        results = np.array(cursor.fetchall())

        currsys = results[0, 0]
        distance = results[0, 1]
        startCoord[0, 0] = results[0, 2]
        startCoord[0, 1] = results[0, 3]
        startCoord[0, 2] = results[0, 4]

        jumps = jumps + 1
        print(f"""Jump {jumps} is to {currsys}, only {round(float(distance),2)}ly to go!""")
        with open(filename, 'a+') as fa:
            fa.write(f"""Jump {jumps} is to {currsys}, only {round(float(distance),2)}ly to go!\n""")

cnxn.close()

