

A. After the data is loaded, the first step is to look for the number and types of features available. 
    i.   We see that there are 12 features available to us. 
    ii.  The advertiser_name has an obvious spelling mistake that we correct to contain only firstwall and no FirstWall.
    iii. Cat_id and plateform have only one class type each and hence of no value for classificaiton, hence dropping these two columns.

               ad_id advertiser_name  cat_id  category channel_id communication_line  event_type           insert_time plateform sesssion_id   story_id                                              title
count         100000          100000  100000    100000     100000             100000      100000                100000    100000      100000     100000                                             100000
unique             8               3       1         2          2                  3           2                 20134         1       81531       4909                                                  8
top     138209154678        Adda.com          Adda.com        521           Adda.com  impression  2017-08-22T06:16:06Z       wap              120151885  10 मिनट में 6 डिजिट कैश प्राइज़ जीतने के लिए ख...
freq           18996           85645  100000     85645      86092              85645       99370                    38    100000          60      14651                                              18996


B. It looks like a few of the features may be redundant. Co-relation analysis as below tells us that 
	i.  Communication_line_Adda.com is perfectly corelated to negative of advertiser_name_firstwall. This implies that all the missing values in communication_line are firstwall.
	ii. Communication_line, category and communication_line line are corelated therefore dropping advertiser_name and communication_line.

 
                              advertiser_name_firstwall  category_firstwall  channel_id_521  communication_line_Adda.com  communication_line_Firstwall
advertiser_name_firstwall                      1.000000            1.000000       -0.981749                    -1.000000                      0.163673
category_firstwall                             1.000000            1.000000       -0.981749                    -1.000000                      0.163673
channel_id_521                                -0.981749           -0.981749        1.000000                     0.981749                      0.026933
communication_line_Adda.com                   -1.000000           -1.000000        0.981749                     1.000000                     -0.163673
communication_line_Firstwall                   0.163673            0.163673        0.026933                    -0.163673                      1.000000

C. insert_time is a continous feature. We are converting insert_time into 6 categories of 4 hour each. There could be certain times of the day when people would be more likely to click.
 

D. session_id corresponds to user behaviour. Some users are more likely to click on ads than other. We categorize users based on number of past clicks and impressions. If a new user belongs to high clickers he is more likely to click again. A useful way would be to also include click impression ratio, but it proved difficult to evolve a metric for this.

E. Similar to session_id a profile based on past clicks and impression of story_ids are converted into categorical features. 

F. Get co-relations between event_type and all the features.

                                                    event_type_impression
event_type_impression                                            1.000000
ad_id_138209024889                                              -0.006032
ad_id_138209116249                                               0.007216
ad_id_138209154384                                               0.008372
ad_id_138209154678                                               0.014394
ad_id_138209169641                                               0.008436
ad_id_138209171096                                               0.012242
ad_id_138209171162                                               0.009843
category_firstwall                                              -0.060399
channel_id_521                                                   0.060039
insert_time_1                                                    0.040965
insert_time_2                                                   -0.027901
insert_time_3                                                   -0.027526
insert_time_4                                                   -0.006620
insert_time_5                                                   -0.010066
title_22 साल की ये लड़की जैसे ही जेल में गई कैद...              -0.060039
title_?????? ?? ???? ?? ??????, ?????? ???? Add...               0.000252
title_अमीर बनिए- मेहनत कीजिए या स्मार्ट खेलिए                    0.009843
title_अमीरों के क्लब से जुड़िए, ज्वाइन करें Add...               0.008370
title_पोकर खेलिए और जीतिए अपनी सैलरी से कहीं ज्...               0.007216
title_पोकर खेलें और जीती राशि को अपने बैंकखाते ...               0.007105
title_मैंने चुना 10 मिनट में 10,000 रुपए बनाना                   0.012242
sesssion_id_click_count                                         -0.632950
sesssion_id_impression_count                                     0.001761
story_id_click_count                                             0.001015
story_id_impression_count                                        0.008744

ad_id and story_id have co-relations very close to 0 and therefore we will not be including these two columns in our analysis.

G. Run a linear classification 

To do


learning curve 
roc curve
crossvalidation
log-loss
correct cost function
see if click count and impression count can be exchanged
