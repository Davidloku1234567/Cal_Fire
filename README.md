# Cal_Fire
Study of California Wildfires using seven years of CalFire Data


1. [ Introduction. ](#intro)
2. [ Problem statement. ](#statement)
3. [ Cleaning. ](#cleaning)
4. [ Data Dictionary. ](#data_dictionary)
5. [ EDA. ](#eda)
6. [ Modeling. ](#modeling)
7. [ Flask App. ](#flask)
8. [ Conclusions. ](#conclusion)

<a name="intro"></a>
## 1. Introduction

Living in California, I am no stranger to fires and the damage they cause. The fire season of 2019 may cost the state as much as $80 billion in lost property and economic activity. This is not a problem that is getting better. I personally had to drive through a major fire zone just to commute to work in 2017. People lose homes, national parks close and the economy is disrupted for millions of Californians. I believe that data can help anticipate when fires are going occur and where they will burn the longest. 

<a name="statement"></a>
## 2. Problem Statement


Using historical fire data, I will attempt to predict the burn duration of a fire given a location within the state of California. 
For these purposes "burn duration" is defined as time from fire ignition to 100% fire containment as reported by the local fire officials. For those unfamiliar with fire terminology, "containment" is how fire officials define that a fire will no longer spread past fire defenses such as fire breaks. 

I will also attempt to predict the frequency of fire occurances in the state of California. 


<a name="data_dictionary"></a>
## 3. Data Dictionary
| Title                                      | Data Type | Description            |
|-------------|-----------|----------------------------------------------------------------------------------------------|
| index                                      | int       | Default index number. Describes initial dataframe order       |
| fire_department_identification_number_fdid | int       | Identification number of fire department involved in incident |
| fire_department_name                       | str       | Name of fire department involved in incident                  |
| incident_number                            | int       | Identifying number for incident                               |
| exposure_number                            | int       | Should represent number of structures exposed to fire incident- this number is inconsistent  |
| nfirs_incidenttype_code_and_description    | str       | Code and description of fire type                             |
| type_and_description  | str       | extracted description of fire without nfirs code                      |
| incident_name                              | str       | Name of fire incident if named                                |
| year                                       | int       | year incident occurred                                        |
| start_date                                 | datetime  | Date fire started                                             |
| containment_date                           | datetime  | Date fire declared contained                                  |
| burn_duration.                             | int       | time from start to containment in minutes                                |
| county                                     | str       | County of incident                                            |
| street_address                             | str       | Street address of incident                                    |
| city                                       | str       | City where incident took place                              |
| state                                      | str       | State where incident took place                             |
| zip                                          | int      | Zip code where fire took place                             |
| cross_streets_or_directions_or_national_grid | str      | Description of fire location if near landmark              |
| latitude                                     | int      | Latitude of fire origin                                    |
| longitude                                    | int      | Longitude of fire origin                                   |
| total_injuries                               | int      | Number of people injured by fire                           |
| total_fatalities                             | int      | Number of people killed by fire                            |
| estimated_property_or_contents_loss          | str      | dollar amounts or structures quantity lost - inconsistent  |
| total_acres_burned                           | str      | Total acres burned by fire                                 |


<a name="cleaning"></a>
## 4. Cleaning

Getting data was initially a challenge for this project, but I was able to make a contact at the US Geological survey who gave me access to their data set. 

The data came somewhat fragmented and was compiled together from 626 different fire departments spread over 58 counties. While there was clearly a standard template for the data, a lot of cleaning was needed to get servicable models out of it. 

The two major issues were inconsistancies and missing data. Inconsistancies were primarily in string-type cells or in the way that date/times were recorded. For date/time inconsistancies, I had to use the `coerce` feature when setting date/time and then convert those date times again as they were calculated down to nanoseconds. 

Missing data was much trickier. Most fire incidents were missing either containment time, latitude/longitude or additional address data. As may be expected, most fires were not named as the vast majority of fire incidents are small. 

Missing data in string features were simply replaced by strings such as "not provided".

In order to deal with the large amount of missing data from various features sets, I broke the data frame up into smaller data frames that had specialized aspects. For example, the `coords_df` is a dataframe that was created specifically from all fires that had existing lat/long coordinates. 

<a name="eda"></a>
## 5. EDA

I was very excited to get my hands on the data set and immediatly start plotting fires geographically. The initial data set with with Lat/Long revieled some interesting trends. 

![Burn Duration Graph](./Cal_Fire/images/burn_duration_graph.png)

There is a clear gap in a good deal of the longitude/latitude data, specifically in the areas of Los Angeles, Malibu and Riverside. So the accuracy of the coordinates is much better reported in the north of the state. It should be noted that I also had to limit the lat/long params of the graph as many of the coordinates placed fires outside of the state of California and as far away as Africa or placed fires in the middle of oceans. 


<a name="modeling"></a>
## 6. Modeling

I dropped a good deal of the features that were mostly missing data such as `incident_name` and all of the address columns for the 37,000 entries that had lat/long that fell within the state of California. I ran a `DBSCAN` and attempted to sort the fires into clusters by burn duration. I dummied out `fire_department_name`, `cause`, and `type_description` features. This was over 2,000 features, so I ran `PCA` (Principle Component Analysis) to settle on `146` features that had the most weight.

I ran `LinearRegerssion`, `RandomForestRegressor` and `KNeighborsRegressor` models and was unable to yield an R2 score above -0.0015. 


After which, I log tranformed my $y$ variable and ran my models again. My after all of that, here are the best results:

| Model                 | Transformed $y$? | Train/Test | R2      |
|-----------------------|----------------|------------|---------|
| LinearRegression      | yes            | Train      | 0.0149  |
| LinearRegression      | yes            | Test       | -0.0043 |
| RandomForestRegressor | yes            | Train      | 0.8369  |
| RandomForestRegressor | yes            | Test       | -0.1315 |
| KNeighborsRegressor   | yes            | Train      | 0.20667 |
| KNeighborsRegressor   | yes            | Test       | -0.1716 |


From these results it was beginning to become clear that I was nowhere close to predicting burn durations. I shifted gears to the second objective - predicting number of fires. 

Modeling this was much easier. Every fire had a date, which means that I could focus more on the modeling and less on the missing data. I used a `.count` function to give my a dataframe with only two features. `start_date` and `count` This gave me about 134,000 events to model a time series with. 

Initially I looked for and found some pretty stark seasonality. I then used `OLS` to model monthly, quartly and yearly lags in that date.

![Seasonality Modeling](../Cal_Fire/Images/2013_to_2020.png)

I then took my dataset and reduced it so  and ran it through `ARIMA`, `SARIMA` and `SARIMAX` models. 

The `SARIMAX` model output an 'MSE' of '20.25' and I was able to model it out over the course of the next year. The model eventualy defaulted to the mean, but predicted all the way through October. 

![Seasonality Modeling](../Cal_Fire/Images/12_mo_preds.png)

<a name="flask"></a>
## 7. Flask App

I created a simple flask app to model the predictionsusing Python and HTML. The `SARIMAX` model was enourmous when running (48GB) and would have slowed the app down, so I simply printed all of 2020s predictions into a `.csv` and had the app read off that. This saved a lot of processing power and still gave off the desired result. 

<a name="conclusion"></a>
## 8. Conclusions

While it turns out that wildfires are difficult to predict, I hope that even being able to predict the number of fires expected on any given day of the year would be useful to Cal Fire. It is my hope that efforts like this can help allocate resources in the future so that lives and properties are saved. 

I would like to return to this project in the future and attempt to isolate predictions by county or even attempt again at burn durations through the use of a neural network. 
