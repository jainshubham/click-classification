import ast
import pandas
from sklearn import svm
from sklearn.metrics import confusion_matrix

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


    def data_preparation(self):
        """
        """
        # fix spelling mistake in advertiser_name.
        self.data_frame.advertiser_name = self.data_frame.advertiser_name.replace('FirstWall', 'firstwall')
        
        # get correlation between similar looking columns
        dd = pandas.get_dummies(self.data_frame[['advertiser_name', 'cat_id', 'category', 'channel_id', 'communication_line']], drop_first=True)
        print(dd.corr())
        
        # drop advertiser_name and communication_line as perfectly corelated with category.
        self.data_frame = self.data_frame.drop('advertiser_name', 1)
        self.data_frame = self.data_frame.drop('communication_line', 1)
        
        # drop empty cat_id
        self.data_frame = self.data_frame.drop('cat_id', 1)
        
        # drop non-varying column plateform
        self.data_frame = self.data_frame.drop('plateform', 1)
        
        # convert time to 6 quaters
        self.data_frame.insert_time = pandas.Categorical(self.data_frame.insert_time.apply(lambda x: int(int(x[11:13])/4)))
        
        # sesssion_id story_id
        dd = pandas.get_dummies(self.data_frame[['event_type', 'ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        print(dd.corr())        

        
    def classify(self):
        """
        """
        X=pandas.get_dummies(self.data_frame[['ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        y=pandas.get_dummies(self.data_frame[['event_type']], drop_first=True)

        mysvm = svm.SVC(kernel='rbf').fit(X,y)
        mysvm_pred = mysvm.predict(X)
        print(confusion_matrix(mysvm_pred, y))
