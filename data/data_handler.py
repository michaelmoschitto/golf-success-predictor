"""
This script will preprocess our dataset and return a formatted, Pandas dataframe object aht our 
machine learning models can use.

Author: Keon Roohparvar
Date: November 14, 2022
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def import_dataset(path_to_csv, split_train_test=True):
    """
    This will import the golf dataset, preprocess it, and return Dataframe objects.

    Inputs:
        path_to_csv (string): The location of our .csv file with our golf data
        split_train_test (boolean): True if we want to do a 80/20 split on our data, and False if 
            we do not want to perform this split.
        
    Returns:
        if split_train_test -> 
            (np.array, np.array, np.array, np.array) : Train X, Test X, Train Y, Test Y data in numpy arrays
        else ->
            (np.array, np.array) : All X data, all Y data 
    """
    # Load in data
    if not os.path.exists(path_to_csv):
        print('ERROR - Csv path does not exist')
        exit(-1)
    df = pd.read_csv(path_to_csv)
    
    # Remove most of the dummy data where player data is not recorded
    df.dropna(subset=['Avg Distance', 'Points'], inplace=True)

    # Fill in 0's for Nan's in our predictor variable and remove commas
    df.fillna(0, inplace=True)
    df.replace(',', '', regex=True, inplace=True)


    # Split predictor from the rest of the data
    Y = df['Top 10']
    X = df.drop(['Top 10'], axis=1)

    # Remove unneeded columns
    X.drop(['Year', 'Money'], axis=1, inplace=True)
    

    # Split data if needed
    if split_train_test:
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

        # Z-score normalize data
        scaler = StandardScaler()

        cols_to_scale = ['Rounds', 'Fairway Percentage', 'Avg Distance',
            'gir', 'Average Putts', 'Average Scrambling', 'Average Score', 'Points',
            'Wins', 'Average SG Putts', 'Average SG Total', 'SG:OTT', 'SG:APR',
            'SG:ARG']
        
        X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
        X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

        return X_train.to_numpy(), X_test.to_numpy(), Y_train.to_numpy(), Y_test.to_numpy()
    
    else:
        # Z-score normalize data
        scaler = StandardScaler()

        cols_to_scale = ['Rounds', 'Fairway Percentage', 'Avg Distance',
            'gir', 'Average Putts', 'Average Scrambling', 'Average Score', 'Points',
            'Wins', 'Average SG Putts', 'Average SG Total', 'SG:OTT', 'SG:APR',
            'SG:ARG']
        
        X[cols_to_scale] = scaler.fit_transform(X[cols_to_scale])

        return X.to_numpy(), Y.to_numpy()

    

if __name__ == '__main__':
    import_dataset('pgaTourData.csv', True)
