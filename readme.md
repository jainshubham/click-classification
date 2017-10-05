

A. pd.describe()
               ad_id advertiser_name  cat_id  category channel_id communication_line  event_type           insert_time plateform sesssion_id   story_id                                              title
count         100000          100000  100000    100000     100000             100000      100000                100000    100000      100000     100000                                             100000
unique             8               3       1         2          2                  3           2                 20134         1       81531       4909                                                  8
top     138209154678        Adda.com          Adda.com        521           Adda.com  impression  2017-08-22T06:16:06Z       wap              120151885  10 मिनट में 6 डिजिट कैश प्राइज़ जीतने के लिए ख...
freq           18996           85645  100000     85645      86092              85645       99370                    38    100000          60      14651                                              18996

advertiser_name is corrected to contain only firstwall and none FirstWall.

B. Co-relation 
                              advertiser_name_firstwall  category_firstwall  channel_id_521  communication_line_Adda.com  communication_line_Firstwall
advertiser_name_firstwall                      1.000000            1.000000       -0.981749                    -1.000000                      0.163673
category_firstwall                             1.000000            1.000000       -0.981749                    -1.000000                      0.163673
channel_id_521                                -0.981749           -0.981749        1.000000                     0.981749                      0.026933
communication_line_Adda.com                   -1.000000           -1.000000        0.981749                     1.000000                     -0.163673
communication_line_Firstwall                   0.163673            0.163673        0.026933                    -0.163673                      1.000000


1. Communication_line_Adda.com is perfectly corelated to negative of advertiser_name_firstwall. This implies that all the missing values in communication_line are firstwall.
2. communication_line, category and communication_line line are corelated therefore dropping advertiser_name and communication_line.
3. Cat_id is empty hence dropping.
4. Plateform is a constant hence dropping.

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
