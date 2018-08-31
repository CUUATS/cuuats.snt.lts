# sn-python
Python-based tool for calculating the Bike Level Traffic of Stress (BLTS),
Pedestrian Level Traffic of Stress (PLTS), Automobile Level of Stress (ALTS)
and aggreated destination accessibility score. The Sustainable Neighborhood
Toolkit uses CUUATS Datamodel, a light weight data access layer for ArcGIS,
to query, evaluate the data, and assign a score.

This analysis tool follows the documentation for Low-Stress Bicycling and
Network Connectivity Report from Mineta Transportation Institute and Bicycle
Level of Traffic Stress and Pedestrian Level of Traffic Stress from report of
Oregon Department of Transportation.

## Current Status
The sustianable neighborhood toolkit is still in the initial developing phrase
 of implementing both BLTS and PLTS analysis.

### Prerequisites
This script requires ArcGIS license and [CUUATS datamodel](https://github.com/CUUATS/cuuats.datamodel) to run.
```python
import arcpy
import cuuats.datamodel
```

## Development
To run the tests:
```
python -m unittest tests
```

## Upcoming Improvement
- More testing on BLTS and PLTS assessment
- Automobile Level of Traffic Stress
