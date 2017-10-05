import ast


data = []

with open('Desktop/ad_data.csv') as f:
	for line in f:
		data.append(ast.literal_eval(line)) 

df = pandas.DataFrame(data)

"""
len(df.columns)
12


'ad_id', 'advertiser_name'2, 'cat_id'11, 'category'2, 'channel_id'3,
       'communication_line'2, 'event_type', 'insert_time'8, 'plateform'2,
       'sesssion_id-', 'story_id', 'title'
