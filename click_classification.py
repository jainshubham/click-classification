import ast
import pandas
from sklearn import svm
from sklearn.metrics import confusion_matrix, f1_score
from collections import defaultdict, Counter

file_path = '/home/shubhamjain/Desktop/db_click_classification/ad_data.csv'

class click_classification(object):
    """
    """
    def __init__(self):
        self.data_frame = pandas.DataFrame()
        pandas.set_option('display.width', 1000)
        pandas.set_option('display.max_columns', 1000)        

    def get_data(self):
        """ The function loads the data from the given file to a pandas 
        dataframe
        
        """
        data = []
        with open(file_path) as f:
            for line in f:
                data.append(ast.literal_eval(line)) 
        self.data_frame = pandas.DataFrame(data)


    def transform_data(self):
        """
        """
        # fix spelling mistake in advertiser_name.
        self.data_frame.advertiser_name = self.data_frame.advertiser_name.replace('FirstWall', 'firstwall')
        
        # get correlation between similar looking columns
        dd = pandas.get_dummies(self.data_frame[['advertiser_name', 'cat_id', 'category', 'channel_id', 'communication_line']], drop_first=True)
        # print(dd.corr())
        
        # drop advertiser_name and communication_line as perfectly corelated with category.
        self.data_frame = self.data_frame.drop('advertiser_name', 1)
        self.data_frame = self.data_frame.drop('communication_line', 1)
        
        # drop empty cat_id
        self.data_frame = self.data_frame.drop('cat_id', 1)
        
        # drop non-varying column plateform
        self.data_frame = self.data_frame.drop('plateform', 1)
        
        # convert time to 6 quaters
        self.data_frame.insert_time = pandas.Categorical(self.data_frame.insert_time.apply(lambda x: int(int(x[11:13])/4)))
       
        # transform session id to feature
        ctr = Counter(self.data_frame.sesssion_id) 
        click_dict = defaultdict(int)
        impression_dict = defaultdict(int)
        for row in self.data_frame[['sesssion_id', 'event_type']].itertuples():
            if row.event_type == 'click':
                click_dict[row.sesssion_id] += 1
            if row.event_type == 'impression':
                impression_dict[row.sesssion_id] += 1
        self.data_frame.sesssion_id_click_count = self.data_frame.sesssion_id.apply(lambda x: click_dict[x])
        self.data_frame.sesssion_id_impression_count = self.data_frame.sesssion_id.apply(lambda x: ctr[x]-click_dict[x])


        # transform session id to feature
        ctr = Counter(self.data_frame.sesssion_id) 
        click_dict = defaultdict(int)
        impression_dict = defaultdict(int)
        for row in self.data_frame[['sesssion_id', 'event_type']].itertuples():
            if row.event_type == 'click':
                click_dict[row.sesssion_id] += 1
            if row.event_type == 'impression':
                impression_dict[row.sesssion_id] += 1
        self.data_frame.loc[:,'sesssion_id_click_count'] = self.data_frame.sesssion_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:,'sesssion_id_impression_count'] = self.data_frame.sesssion_id.apply(lambda x: ctr[x]-click_dict[x])

        # transform story_id to feature
        ctr = Counter(self.data_frame.story_id) 
        click_dict = defaultdict(int)
        impression_dict = defaultdict(int)
        for row in self.data_frame[['story_id', 'event_type']].itertuples():
            if row.event_type == 'click':
                click_dict[row.story_id] += 1
            if row.event_type == 'impression':
                impression_dict[row.story_id] += 1
        self.data_frame.loc[:,'story_id_click_count'] = self.data_frame.story_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:,'story_id_impression_count'] = self.data_frame.story_id.apply(lambda x: ctr[x]-click_dict[x])

        # sesssion_id story_id are still not included in out analysis.
        dd = pandas.get_dummies(self.data_frame[['event_type', 'ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        print(dd.corr()[['event_type_impression']])
        # quite low correlation coefficients for everything.      

        
    def classify(self):
        """
        """
        X=pandas.get_dummies(self.data_frame[['ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        X.loc[:,'sesssion_id_click_count'] = self.data_frame.sesssion_id_click_count
        X.loc[:,'sesssion_id_impression_count'] = self.data_frame.sesssion_id_impression_count
        #X.loc[:,'story_id_click_count'] = self.data_frame.story_id_click_count
        #X.loc[:,'story_id_impression_count'] = self.data_frame.story_id_impression_count
        print(X.columns)
        y=pandas.get_dummies(self.data_frame[['event_type']], drop_first=True)
        mysvm = svm.SVC(kernel='linear', class_weight={1: 1, 0: 100}, C=1).fit(X,y)
        mysvm_pred = mysvm.predict(X)
        print(confusion_matrix(mysvm_pred, y))
        print(f1_score(y, mysvm_pred))


def run():
    cc = click_classification()
    cc.get_data()
    cc.transform_data()
    cc.classify()
