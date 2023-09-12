
df = None
df_dict = {}
df_name = None


def set_dataframe_name(dataframe_name):
    global df_name
    df_name = dataframe_name


def get_dataframe_name():
    return df_name





def add_dataframe_to_dict(dataframe, dataframe_name):
    global df_dict
    df_dict[dataframe_name] = dataframe

def get_df_dict():
    return df_dict





def set_dataframe(dataframe_name):
    global df
    df = df_dict[dataframe_name]

def get_dataframe():
    return df
