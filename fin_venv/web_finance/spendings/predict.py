import datetime, calendar
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.nn.functional as F



def predict(spendings):

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(5, 125)
            self.fc2 = nn.Linear(125, 25)
            self.fc3 = nn.Linear(25, 1)
            
        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    spendings_by_category = []
    for k in set([x['category_id'] for x in spendings]):
        spendings_by_category.append([x for x in spendings if x['category_id'] == k])

    day_prediction = []
    month_prediction = []

    for cat in spendings_by_category:
        
        df = pd.DataFrame(cat)
        #  drop useless info
        df_prep = df.drop(['id', 'user_id', 'category_id'], axis = 1)

        # add features in data frame 
        df_prep['Day'] = [elem.day for elem in df_prep['date'].to_list()]
        df_prep['Month'] = [elem.month for elem in df_prep['date'].to_list()]
        df_prep['Hour'] = [elem.hour for elem in df_prep['date'].to_list()]
        df_prep['Minute'] = [elem.minute for elem in df_prep['date'].to_list()]
        df_prep['Weekday'] = [elem.weekday() for elem in df_prep['date'].to_list()]
        df_prep = df_prep.drop(['date'], axis = 1)

        # df for fit MinMaxScaler
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        dict_scaler = {"Day": list(range(1,calendar.monthrange(year, month)[1]+1)),
               "Month" : [i+1 for i in range(12)], 
               "Hour": [i for i in range(24)],
               "Minute": [i for i in range(60)],
               "Weekday": [i for i in range(7)],
               "amount": [0, df["amount"].max()]}
        df_scaler = pd.DataFrame.from_dict(dict_scaler, orient='index')
        df_scaler = df_scaler.transpose()
        df_scaler = df_scaler.fillna(1)
        df_scaler[["Day", "Month", "Hour", "Minute", "Weekday"]] = df_scaler[["Day", "Month", "Hour", "Minute", "Weekday"]].astype('int64')

        # Scalers for better prediction
        scaler = MinMaxScaler()
        scaler_test = MinMaxScaler()
        scaler_amount = MinMaxScaler()
        scaler.fit(df_scaler[["Day", "Month", "Hour", "Minute", "Weekday", "amount"]])
        scaler_test.fit(df_scaler[["Day", "Month", "Hour", "Minute", "Weekday"]])
        scaler_amount.fit(df_scaler["amount"].to_numpy().reshape(-1, 1))

        # transform input data frame 
        df_prep[["Day", "Month", "Hour", "Minute", "Weekday", "amount"]] = scaler.transform(df_prep[["Day", "Month", "Hour", "Minute", "Weekday", "amount"]])

        train_inputs = torch.tensor(df_prep[["Day", "Month", "Hour", "Minute", "Weekday"]].values, dtype=torch.float32)
        train_labels = torch.tensor(df_prep["amount"].values.reshape(-1,1), dtype=torch.float32)

        # Initialize the model, loss function (mean squared error), and optimizer (stochastic gradient descent)
        model = Net()
        criterion = nn.MSELoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

        # Train the model
        for epoch in range(1000):
            # Forward pass
            outputs = model(train_inputs)
            loss = criterion(outputs, train_labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # preparing data for prediction
        dict_df = {"Day" : [], "Month" : [], "Hour" : [], "Minute" : [], "Weekday" : []}
        dict_df['Day'].append(datetime.datetime.now().day)
        dict_df['Month'].append(datetime.datetime.now().month)
        dict_df['Hour'].append(datetime.datetime.now().hour)
        dict_df['Minute'].append(datetime.datetime.now().minute)
        dict_df['Weekday'].append(datetime.datetime.now().weekday())

        test_day_df = pd.DataFrame(data=dict_df)
        test_day_df[["Day", "Month", "Hour", "Minute", "Weekday"]] = scaler_test.transform(test_day_df[["Day", "Month", "Hour", "Minute", "Weekday"]])
        test_day_inputs = torch.tensor(test_day_df[["Day", "Month", "Hour", "Minute", "Weekday"]].values, dtype=torch.float32)

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        num_days = calendar.monthrange(year, month)[1]
        dict_month_df = {"Day" : [], "Month" : [], "Hour" : [], "Minute" : [], "Weekday" : []}

        for i in range(num_days):
            dict_month_df["Day"].append(i+1)
            dict_month_df['Weekday'].append(datetime.datetime(year, month, i+1).weekday())
            dict_month_df["Month"].append(month)
            dict_month_df['Hour'].append(datetime.datetime.now().hour)
            dict_month_df['Minute'].append(datetime.datetime.now().minute)

        test_month_df = pd.DataFrame(data=dict_month_df)
        test_month_df[["Day", "Month", "Hour", "Minute", "Weekday"]] = scaler_test.transform(test_month_df[["Day", "Month", "Hour", "Minute", "Weekday"]])
        test_month_inputs = torch.tensor(test_month_df[["Day", "Month", "Hour", "Minute", "Weekday"]].values, dtype=torch.float32)

        # Set the model to evaluation mode
        model.eval()

        # predicition by categories in a day
        with torch.no_grad():
            test_day_outputs = model(test_day_inputs).numpy()
            test_month_outputs = model(test_month_inputs).numpy()

        day_prediction.append(float(scaler_amount.inverse_transform(test_day_outputs)))
        month_prediction.append(scaler_amount.inverse_transform(test_month_outputs).sum())

    return day_prediction, month_prediction