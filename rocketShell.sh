####################################################################
# This is the shell script to run the Rocket Simulation            #
# The script assumes you have a usable STL file, and generates     #
#    the mesh and output in a separate rocketShell.out file        #
# Inputs                                                           #
#   Source: STL file                                               #
# Outputs                                                          #
####################################################################

# Initalizing counters
ctr=200

# This is the maximum number of STLs you have available.
#   So, if you have 5 STLs, max = 5, and the files should be 
#     rocket_0, rocket_1, rocket_2, rocket_3, rocket_4
max=201

# Setting start time
date
start=`date +%s`

while [ $ctr -lt $max ]
do

  # Step 1: Scaling the file down to 50%, while copying to triSurface (destination location)
  echo "*************************** Step 1: Scaling down source STL and copying to triSurface ***********************"
  source_file=rocket_$ctr.stl
  echo "Running Simulation for " $source_file
  surfaceConvert ../allSTL/$source_file ./constant/triSurface/motorBike.stl -clean -scale 0.5
  echo "*************************** Step 1: surfaceConvert completed ************************************************"

  echo "*************************** Step 2: Starting blockMesh ***********************"
  blockMesh
  echo "*************************** Step 2: blockMesh Completed ***********************"

  echo "*************************** Step 3: surfaceFeatureExtract started ***********************"
  surfaceFeatureExtract
  echo "*************************** Step 3: surfaceFeatureExtract Completed ***********************"

  echo "*************************** Step 4: Starting snappyHexhMesh in serial mode ***********************"
  snappyHexMesh -overwrite
  echo "*************************** Step 4: snappyHexMesh in serial mode completed ***********************"

  echo "*************************** Step 5: Starting simpleFoam and generating fluid dynamics parameters ***********************"
  simpleFoam
  echo "*************************** Step 5: simpleFoam completed ***********************"

  # increment counter- moving to the next file
  ctr=`expr $ctr + 1`
done

echo "****************************** All simulations completed, and ready for analysis *****************************************"

# Setting end time
date
end=`date +%s`

runtime=$((end-start))
echo "Total runtime is "$runtime" seconds"