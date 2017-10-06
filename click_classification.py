import ast
from collections import defaultdict, Counter

import numpy
import pandas
from sklearn import svm
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import train_test_split

file_path = '/home/shubhamjain/Desktop/db_click_classification/ad_data.csv'
DEGREE_RANGE = 12
CLASS_WEIGHT_RANGE = 5


class ClickClassification(object):
    """Principal class for click classification

    This class uses pandas dataframes for data loading and analysis and
    support vector machines from sklearn for training.

    """

    def __init__(self):
        """Initializes the dataframe data object.

        """
        self.data_frame = pandas.DataFrame()

        # Display related parameters.
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

    def get_click_through_rates(self, column_name):
        """ generates click through rate for a given columns in pandas.

        :return: click through and impression through rate.

        TODO: Test if we need impression through rate. Looks like we dont.
        """
        click_dict = defaultdict(int)
        for row in self.data_frame[[column_name, 'event_type']].itertuples():
            column_key = eval("row.{}".format(column_name))
            if row.event_type == 'click':
                click_dict[column_key] += 1
        return click_dict

    def transform_data(self):
        """Analyzes and prepares data for classification.

        Performs steps like spelling correction, feature reduction, click rate feature creation, binarization of
        category labels.

        """

        # print(data_frame.describe())
        # fix spelling mistake in advertiser_name.
        self.data_frame.advertiser_name = self.data_frame.advertiser_name.replace('FirstWall', 'firstwall')

        # Get correlation between columns to identify redundant columns
        data_frame_slice = pandas.get_dummies(
            self.data_frame[['advertiser_name', 'cat_id', 'category', 'channel_id', 'communication_line']],
            drop_first=True)
         # print(data_frame_slice.corr())

        # drop advertiser_name and communication_line as these are perfectly correlated with category.
        self.data_frame = self.data_frame.drop('advertiser_name', 1)
        self.data_frame = self.data_frame.drop('communication_line', 1)

        # drop empty cat_id
        self.data_frame = self.data_frame.drop('cat_id', 1)

        # drop non-varying column plateform
        self.data_frame = self.data_frame.drop('plateform', 1)

        # convert time to 6 quarters.
        self.data_frame.insert_time = pandas.Categorical(
            self.data_frame.insert_time.apply(lambda x: int(int(x[11:13]) / 4)))

        # transform session id to feature
        ctr = Counter(self.data_frame.sesssion_id)

        click_dict = self.get_click_through_rates('sesssion_id')
        self.data_frame.loc[:, 'sesssion_id_click_count'] = self.data_frame.sesssion_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:, 'sesssion_id_impression_count'] = self.data_frame.sesssion_id.apply(
            lambda x: ctr[x] - click_dict[x])

        # transform story_id to feature
        ctr = Counter(self.data_frame.story_id)
        click_dict = self.get_click_through_rates('story_id')
        self.data_frame.loc[:, 'story_id_click_count'] = self.data_frame.story_id.apply(lambda x: click_dict[x])
        self.data_frame.loc[:, 'story_id_impression_count'] = self.data_frame.story_id.apply(
            lambda x: ctr[x] - click_dict[x])

        # get correlation between columns and event_type.
        data_frame_slice = pandas.get_dummies(
            self.data_frame[['event_type', 'ad_id', 'category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        result = pandas.concat([data_frame_slice, self.data_frame[
            ['sesssion_id_click_count', 'sesssion_id_impression_count', 'story_id_click_count',
             'story_id_impression_count']]], axis=1)
        # print(result.describe())
        print(result.corr()[['event_type_impression']])

    def model_validation(self):
        """Validate svm model to the click data.

        The function cross-validates svm for the given data for degree, kernel and class weights.
        The metrics used are confusion matrix and Area Under the ROC curve.
        """
        X = pandas.get_dummies(self.data_frame[['category', 'channel_id', 'insert_time', 'title']], drop_first=True)
        X.loc[:, 'sesssion_id_click_count'] = self.data_frame.sesssion_id_click_count
        y = pandas.get_dummies(self.data_frame[['event_type']], drop_first=True)
        for j in ['linear', 'rbf', 'poly']:
            degree_range = 3
            if j in 'poly':
                degree_range = DEGREE_RANGE
            for k in range(2, degree_range):
                for i in range(CLASS_WEIGHT_RANGE):
                    X_train, X_test, y_train, y_test = train_test_split(X, y)
                    classifier = svm.SVC(kernel=j, class_weight={1: 1, 0: i}, C=1, degree=k, probability=True
                                         ).fit(X_train, y_train)
                    probas = classifier.predict_proba(X_test)
                    fpr, tpr, thresholds = roc_curve(y_test, probas[:, 1])
                    roc_auc = auc(fpr, tpr)
                    classifier_pred = classifier.predict(X_test)
                    print("\n class weight: {} kernel: {} degree: {} \n Confusion Matrix \n {} \n AUC {}".format(
                        i, j, k, confusion_matrix(classifier_pred, y_test), roc_auc))

def run():
    cc = ClickClassification()
    cc.get_data()
    cc.transform_data()
    cc.model_validation()
