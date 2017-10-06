import ast
import pandas
from sklearn import svm
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score, roc_curve, auc
from collections import defaultdict, Counter
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import numpy
#import matplotlib.pyplot as plt


random_state = numpy.random.RandomState(0)
file_path = '/home/shubhamjain/Desktop/db_click_classification/ad_data.csv'

class ClickClassification(object):
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

        # get corelation between columns and event_type.
        dd = pandas.get_dummies(self.data_frame[['event_type', 'ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        result = pandas.concat([dd, self.data_frame[['sesssion_id_click_count', 'sesssion_id_impression_count', 'story_id_click_count', 'story_id_impression_count']]], axis=1)
        print(result.describe())
        print(result.corr()[['event_type_impression']])

        
    def classify(self):
        """
        """
        X=pandas.get_dummies(self.data_frame[['category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        X.loc[:,'sesssion_id_click_count'] = self.data_frame.sesssion_id_click_count
        X.loc[:,'sesssion_id_impression_count'] = self.data_frame.sesssion_id_impression_count

        cv = StratifiedKFold(n_splits=6)

        y=pandas.get_dummies(self.data_frame[['event_type']], drop_first=True)
        #mysvm = svm.SVC(kernel='linear', class_weight={1: 1, 0: 3}, C=1).fit(X,y)
        #mysvm_pred = mysvm.predict(X)
        #print(confusion_matrix(mysvm_pred, y))
        #print(f1_score(y, mysvm_pred))
        #print(precision_score(y, mysvm_pred))
        #print(recall_score(y, mysvm_pred))


        classifier = classifier = svm.SVC(kernel='linear', probability=True,
                             random_state=random_state)
        tprs = []
        aucs = []
        mean_fpr = numpy.linspace(0, 1, 100)

        i = 0
        for X_train, X_test, y_train, y_test in train_test_split(X, y):
            probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)
            # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            
            aucs.append(roc_auc)
            #plt.plot(fpr, tpr, lw=1, alpha=0.3,
            #        label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

            i += 1
            print("{} {}".format(fpr, tpr)) 
        print(aucs)



def run():
    cc = ClickClassification()
    cc.get_data()
    cc.transform_data()
    cc.classify()



