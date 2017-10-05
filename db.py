import ast
import pandas


def get_data():
    """ The function loads the data from the given file to a pandas 
    dataframe
    
    """
    data = []
    with open('/home/shubhamjain/Desktop/db_click_classification/ad_data.csv') as f:
        for line in f:
            data.append(ast.literal_eval(line)) 
    return pandas.DataFrame(data)


def basic_analysis(df):
    """
    """
    pandas.set_option('display.width', 1000)
    df.describe()


def data_preparation():
    """
    """
    
def classify():
    """
    """
    
    
