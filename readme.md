
#### Click classifier 

A support vector machine based click classifier.

##### Data Analysis Steps

A. After the data is loaded, the first step is to look for the number and types of features available. 

B. It looks like a few of the features may be redundant. Co-relation analysis as below tells us that 
   1.  Communication_line_Adda.com is perfectly correlated to negative of advertiser_name_firstwall. This implies that all the missing values in communication_line are firstwall.
   2. Communication_line, category and communication_line line are correlated therefore dropping advertiser_name and communication_line.

C. insert_time is a continous feature. We are converting insert_time into 6 categories of 4 hour each. There could be certain times of the day when people would be more likely to click. 
 
D. session_id corresponds to user behaviour. Some users are more likely to click on ads than other. We categorize users based on number of past clicks and impressions. If a new user belongs to high clickers he is more likely to click again. This looks like a good replacement of click through rate. 

E. We could calculate click through rate for specific adds. This may help reduce the false positives. I could not implement this for the lack of time.

E. Similar to session_id a profile based on past clicks and impression of story_ids are converted into categorical features. 

F. Get co-relations between event_type and all the features.
   1. ad_id and story_id have co-relations very close to 0 and therefore we will not be including these two columns in our analysis.

##### Train Classifier

A. Run a svm classification with different parameters. I use svm because it just works for me most of the times. Run cross validation for class weights, degree and kernel. 
   1. class weight: 3, kernel: linear give the best results for our model.
   2. Some literature also mentions use of log-loss for analysis. This needs to be worked out. 

##### Result Summary

A. For a test case of 25000 items, our model has been able to predict almost all clicks while also predicting a similar number of false positives. 

Confusion Matrix 

    |162    |     215    |
    |0         |    24623|


AUC: 0.995903578646419


##### Future Work
   1. Make the algorithm online.
   2. Try tree based methods or deep-learning.
