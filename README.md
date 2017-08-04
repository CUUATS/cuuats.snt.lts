# sn-python
Python-based tool for calculating the Bike Level Traffic of Stress (BLTS), 
Pedestrian Level Traffic of Stress (PLTS), automobile level of stress, 
transit level of stress and aggreated destination accessibility score. The 
tools uses arcpy library and calculate each scoring category and aggregate 
the score into an overall score for each road segment.

## Overview
This analysis tool follows the documentation for Low-Stress Bicycling and 
Network Connectivity Report from Mineta Transportation Institute and Bicycle 
Level of Traffic Stress and Pedestrian Level of Traffic Stress from report of 
Oregon Department of Transportation.  

## Current Status
The sustianable neighborhood toolkit is still in the initial developing phrase
 of implementing both BLTS and PLTS analysis.  

## Bicycle Level of Traffic Stress
This tool uses the street center line from Champaign County GIS Consortium 
and all the data is stored as fields in the feature class in a geodatabase.  
First step is to initiate a BLTS object pointing to the correct file 
geodatabase and the future class.  
```python
blts = BLTS_Analaysis(GDB_PATH, FC_NAME)
```
Once the object is initialized, analysis can be perform.

####  Bike Lane *with* Parking Lane Score
Using the following method from blts, score can be assigned to a new field in
 the feature class.
 ```python
blts.assingBLwithPkLaneScore("lpd", "SPEED", "Comb_ParkBike_width", 
"HasParkingLane")
```
The parameters are the names of the fields required to complete this part of 
scoring

####  Bike Lane *without* Parking Lane Score
This method assign the bike lane without parking lane score to a new field in
 the feature class.
 
```python
blts.assignBLwithoutPkLaneScore("lpd", "SPEED", "Width", "HasParkingLane")
```
The parameters are the names of the fields required to complete this part of 
scoring

#### Mix Traffic Score
This method assign the mix traffic score to a new field in the feature class.

```python
blts.assignMixTrafficScore("SPEED", "lpd")
```

The parameters are the names of the fields required to complete this part of 
scoring

#### Aggregate Segment Score
After calculating the bike lane with parking lane score, bike lane without 
parking lane score, and the mix traffic score, this method should be run to 
aggregate the above three scores and generate an overall segment score.  The 
aggregation uses the minimum of the three to reflect the a present of either 
of these facilities will lower the stress level of biking.

```python
blts.aggregateSegmentScore()
```

This method does not take any input and uses the pre-determined score fields 
to aggregate the score

#### Right Turn Lane Criteria Score
This method assign the right turn lane score to a new field in the feature 
class.
```python
blts.assignRightTurnLaneScore("RTL_Conf_", "RTL_Len_", "bike_AA_")
```
The parameters are the names of the fields required to complete this part of 
scoring.  Currently the data, is stored as four directional data in the 
feature class, this method automatically chooses the four direction and 
select the one with the highest score(more stress)and represent the whole 
semgnet.

#### Left Turn Lane Criteria Score
This method assign the left turn lane score to a new field in the feature class.

```python
blts.assignLeftTurnLaneScore("SPEED", "LTL_Conf_", "LTL_lanescrossed_")
```

The parameters are the names of the fields required to complete this part of 
scoring.  Currently the data, is stored as four directional data in the 
feature class, this method automatically chooses the four direction and 
select the one with the highest score(more stress)and represent the whole 
semgnet.

#### Unsignalized Crossing with *No* Median Present Score
This method assign the unsiganalized crossing with no median present to a new 
field in the feature class.
```python
blts.assignUnsignalizedNoMedianScore("med_present", "SPEED","TotalLanes_EW_12", 
                                        "TotalLanes_NS", "Control_Type")
```
The parameters are the names of the fields required to complete this part of 
scoring.  

#### Unsignalized Crossing *With* Median Present Score
The parameters are the names of the fields required to complete this part of 
scoring.
```python
blts.assignUnsignalizedHasMedianScore("med_present", "SPEED",
                                        "through_lane_EW", "through_lane_NS",
                                        "Control_Type")
```
The parameters are the names of the fields required to complete this part of 
scoring.

#### Aggregating the Overall Score
After calculating all the previous individual score, this method combine all 
the previous score by selecting the most stress of score for each segment.  
```python
blts.aggregateOverallScore(["segmentScore",
                                "rtlScore",
                                "ltlScore",
                                "unsignalized_NoMedian"])
```
The paramter is a list of fields that is input for aggregation.  

### Configuration of Scoring
In the config.py file a list of scoring criteria, user can adjust the scores 
in the corresponding list to adjust the score of the BLTS analysis.  The 
lists are based on the table in the documentation and should be used along 
side with the report.

## Pedestrian Level of Traffic Stress
This tool uses the sidewalk feature class geometry as the base for the 
assessment and attribute associated with the sidewalk to perform PLTS 
analysis. Similar to the BLTS analysis, first the PLTS object must be 
initiated with the path to the geodatabase and the name of the feature class. 

```python
plts = PLTS_Analysis(GDB_PATH, FC_NAME)
```

#### Sidewalk Condition Score
Once the plts object has been initiated, the side walk condition score method
 can be called to calculate the score based on the input field. 
 
 ```python
plts.assignSidewalkCondScore(sw_cond = "CondScoreCat", sw_width = "Width")
```

Based on the width and the condition, the score is calculated in written in a
 new field in the future class. 
 
#### Buffer Type Score
A buffer type score can be calculated using the following method
```python
plts.assignBufferTypeScore(buff_type, speed)
```

#### Buffer Width Score
Buffer width score is also calculated using the following method
```python
plts.assignBufferWidthScore(buff_width, total_lanes)
```

#### Aggregate Overall Score
After the calcuation of sidewalk condition score, buffer type score, buffer 
width score, an aggregation of these score can be calculated.

```python
plts.aggregateScore(method = "MAX")
```

The method is optional parameter, and the default is "MAX", which aggregate 
the score by selecting the highest score (highest stress level). 


## Upcoming Improvement
+ Customize the input data type and domain
