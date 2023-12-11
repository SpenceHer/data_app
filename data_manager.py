# DATAFRAME MANAGEMENT

df = None
df_dict = {}
df_name = None



# SET MAIN DATAFRAME
def set_dataframe(dataframe):
    global df
    df = df_dict[dataframe]

def get_dataframe():
    return df

# SET DATAFRAME NAME
def set_dataframe_name(dataframe_name):
    global df_name
    df_name = dataframe_name

def get_dataframe_name():
    return df_name


# ADD DATAFRAME TO DICTIONARY
def add_dataframe_to_dict(dataframe, dataframe_name):
    global df_dict
    df_dict[dataframe_name] = dataframe

def get_df_dict():
    return df_dict


#####################################################################
#####################################################################
#####################################################################

# TAB MANAGEMENT

tab_dict = {}

# ADD CURRENT SUB-TAB TO DICTIONARY
def add_tab_to_dict(tab_name, setting):
    global tab_dict
    tab_dict[tab_name] = setting

def get_tab_dict():
    return tab_dict


#####################################################################
#####################################################################
#####################################################################

# COMPARISON TABLE MANAGEMENT

comp_tab_dep_var = None
comp_tab_ind_var_list = []
comp_tab_ind_var_dict = {}


# COMPARISON TABLE DEPENDENT VARIABLE
def set_comp_tab_dep_var(variable):
    global comp_tab_dep_var
    comp_tab_dep_var = variable

def get_comp_tab_dep_var():
    return comp_tab_dep_var


# COMPARISON TABLE INDEPENDENT VARIABLES LIST
def add_variable_to_comp_tab_ind_var_list(variable):
    global comp_tab_ind_var_list
    if variable not in comp_tab_ind_var_list:
        comp_tab_ind_var_list.append(variable)

def get_comp_tab_ind_var_list():
    return comp_tab_ind_var_list


# COMPARISON TABLE INDEPENDENT VARIABLES DICT
def add_variable_to_comp_tab_ind_dict(tab_name, setting):
    global comp_tab_ind_var_dict
    comp_tab_ind_var_dict[tab_name] = setting

def get_comp_tab_ind_var_dict():
    return comp_tab_ind_var_dict

#####################################################################
#####################################################################
#####################################################################







#####################################################################
#####################################################################
#####################################################################








#####################################################################
#####################################################################
#####################################################################








#####################################################################
#####################################################################
#####################################################################
