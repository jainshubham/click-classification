import ast
from collections import defaultdict, Counter

import numpy
import pandas
from sklearn import svm
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split

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
        dd = pandas.get_dummies(
            self.data_frame[['advertiser_name', 'cat_id', 'category', 'channel_id', 'communication_line']],
            drop_first=True)
        print(dd.corr())

        # drop advertiser_name and communication_line as perfectly corelated with category.
        self.data_frame = self.data_frame.drop('advertiser_name', 1)
        self.data_frame = self.data_frame.drop('communication_line', 1)

        # drop empty cat_id
        self.data_frame = self.data_frame.drop('cat_id', 1)

        # drop non-varying column plateform
        self.data_frame = self.data_frame.drop('plateform', 1)

        # convert time to 6 quarters
        self.data_frame.insert_time = pandas.Categorical(
            self.data_frame.insert_time.apply(lambda x: int(int(x[11:13]) / 4)))

        # transform session id to feature
        ctr = Counter(self.data_frame.sesssion_id)
        click_dict = defaultdict(int)
        impression_dict = defaultdict(int)
        for row in self.data_frame[['sesssion_id', 'event_type']].itertuples():
            if row.event_type == 'click':
                click_dict[row.sesssion_id] += 1
            if row.event_type == 'impression':
                impression_dict[row.sesssion_id] += 1
        self.data_frame.loc[:, 'sesssion_id_click_count'] = self.data_frame.sesssion_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:, 'sesssion_id_impression_count'] = self.data_frame.sesssion_id.apply(
            lambda x: ctr[x] - click_dict[x])

        # transform story_id to feature
        ctr = Counter(self.data_frame.story_id)
        click_dict = defaultdict(int)
        impression_dict = defaultdict(int)
        for row in self.data_frame[['story_id', 'event_type']].itertuples():
            if row.event_type == 'click':
                click_dict[row.story_id] += 1
            if row.event_type == 'impression':
                impression_dict[row.story_id] += 1
        self.data_frame.loc[:, 'story_id_click_count'] = self.data_frame.story_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:, 'story_id_impression_count'] = self.data_frame.story_id.apply(
            lambda x: ctr[x] - click_dict[x])

        # get corelation between columns and event_type.
        dd = pandas.get_dummies(
            self.data_frame[['event_type', 'ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        result = pandas.concat([dd, self.data_frame[
            ['sesssion_id_click_count', 'sesssion_id_impression_count', 'story_id_click_count',
             'story_id_impression_count']]], axis=1)
        print(result.describe())
        print(result.corr()[['event_type_impression']])

    def classify(self):
        """
        """
        # noinspection PyPep8Naming
        X = pandas.get_dummies(self.data_frame[['category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        X.loc[:, 'sesssion_id_click_count'] = self.data_frame.sesssion_id_click_count
        # X.loc[:,'sesssion_id_impression_count'] = self.data_frame.sesssion_id_impression_count
        y = pandas.get_dummies(self.data_frame[['event_type']], drop_first=True)
        for j in ['linear', 'rbf', 'poly']:
            degree_range = 3
            if j in 'poly':
                degree_range = 6
            for k in range(2, degree_range):
                for i in range(5):
                    # noinspection PyPep8Naming,PyPep8Naming
                    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=numpy.random.RandomState(0))
                    cc_svm = svm.SVC(kernel=j, class_weight={1: 1, 0: i}, C=1, degree=k, probability=True,
                                     random_state=numpy.random.RandomState(0)).fit(X_train, y_train)
                    probas = cc_svm.predict_proba(X_test)
                    fpr, tpr, thresholds = roc_curve(y_test, probas[:, 1])
                    roc_auc = auc(fpr, tpr)
                    cc_svm_pred = cc_svm.predict(X_test)
                    print("\n class weight: {} kernel: {} degree: {}".format(i, j, k))
                    print(confusion_matrix(cc_svm_pred, y_test))
                    print(roc_auc)


def run():
    cc = ClickClassification()
    cc.get_data()
    cc.transform_data()
    cc.classify()
