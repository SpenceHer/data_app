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
comp_tab_variable_type_dict = {}
comp_tab_percent_type = ""
comp_tab_data_type = ""

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
def add_variable_to_comp_tab_variable_type_dict(tab_name, setting):
    global comp_tab_variable_type_dict
    comp_tab_variable_type_dict[tab_name] = setting

def get_comp_tab_variable_type_dict():
    return comp_tab_variable_type_dict


# COMPARISON TABLE PERCENT TYPE
def set_comp_tab_percent_type(variable):
    global comp_tab_percent_type
    comp_tab_percent_type = variable

def get_comp_tab_percent_type():
    return comp_tab_percent_type


# COMPARISON TABLE DATA SELECTION
def set_comp_tab_data_type(variable):
    global comp_tab_data_type
    comp_tab_data_type = variable

def get_comp_tab_data_selection():
    return comp_tab_data_type
#####################################################################
#####################################################################
#####################################################################

# REGRESSION MODEL MANAGEMENT

reg_tab_dep_var = None
reg_tab_ind_var_list = []

reg_tab_selected_regression = ""


# REGRESSION DEPENDENT VARIABLE
def set_reg_tab_dep_var(variable):
    global reg_tab_dep_var
    reg_tab_dep_var = variable

def get_reg_tab_dep_var():
    return reg_tab_dep_var


# REGRESSION INDEPENDENT VARIABLES LIST
def add_variable_to_reg_tab_ind_var_list(variable):
    global reg_tab_ind_var_list
    if variable not in reg_tab_ind_var_list:
        reg_tab_ind_var_list.append(variable)

def get_reg_tab_ind_var_list():
    return reg_tab_ind_var_list


# REGRESSION ANALYSIS TYPE
def set_reg_tab_selected_regression(variable):
    global reg_tab_selected_regression
    reg_tab_selected_regression = variable

def get_reg_tab_selected_regression():
    return reg_tab_selected_regression






reg_tab_log_reg_target_value_dict = {}
log_reg_var_type_dict = {}
log_reg_ref_dict = {}


# LOGISTIC REGRESSION TARGET VALUE
def add_variable_to_reg_tab_log_reg_target_value_dict(tab_name, setting):
    global reg_tab_log_reg_target_value_dict
    reg_tab_log_reg_target_value_dict[tab_name] = setting

def get_reg_tab_log_reg_target_value_dict():
    return reg_tab_log_reg_target_value_dict


# LOGISTIC REGRESSION INDEPENDENT VARIABLES DICT
def add_variable_to_log_reg_var_type_dict(variable, input_var):
    global log_reg_var_type_dict
    log_reg_var_type_dict[variable] = input_var

def get_log_reg_var_type_dict():
    return log_reg_var_type_dict


# LOGISTIC REGRESSION REFERENCES VARIABLES DICT
def add_variable_to_log_reg_ref_dict(ind_var, reference_value):
    global log_reg_ref_dict
    log_reg_ref_dict[ind_var] = reference_value

def get_log_reg_ref_dict():
    return log_reg_ref_dict







#####################################################################
#####################################################################
#####################################################################

# NON-NUMERIC INDEPENDENT VARIABLES DICT
non_numeric_ind_dict = {}


def add_variable_to_non_numeric_ind_dict(ind_var, value, input_var):
    global non_numeric_ind_dict
    
    # Check if ind_var exists in the dictionary, if not, create an empty dictionary
    if ind_var not in non_numeric_ind_dict:
        non_numeric_ind_dict[ind_var] = {}
    
    non_numeric_ind_dict[ind_var][value] = input_var

def get_non_numeric_ind_dict():
    return non_numeric_ind_dict




#####################################################################
#####################################################################
#####################################################################

mach_learn_tab_dep_var = None
mach_learn_tab_ind_var_list = []

mach_learn_tab_selected_model = None

# REGRESSION DEPENDENT VARIABLE
def set_mach_learn_tab_dep_var(variable):
    global mach_learn_tab_dep_var
    mach_learn_tab_dep_var = variable

def get_mach_learn_tab_dep_var():
    return mach_learn_tab_dep_var


# REGRESSION INDEPENDENT VARIABLES LIST
def add_variable_to_mach_learn_tab_ind_var_list(variable):
    global mach_learn_tab_ind_var_list
    if variable not in mach_learn_tab_ind_var_list:
        mach_learn_tab_ind_var_list.append(variable)

def get_mach_learn_tab_ind_var_list():
    return mach_learn_tab_ind_var_list


# REGRESSION ANALYSIS TYPE
def set_mach_learn_tab_selected_model(variable):
    global mach_learn_tab_selected_model
    mach_learn_tab_selected_model = variable

def get_mach_learn_tab_selected_model():
    return mach_learn_tab_selected_model







#####################################################################
#####################################################################
#####################################################################



create_var_tab_var_list = []

# REGRESSION INDEPENDENT VARIABLES LIST
def add_variable_to_create_var_tab_var_list(variable):
    global create_var_tab_var_list
    if variable not in create_var_tab_var_list:
        create_var_tab_var_list.append(variable)

def get_create_var_tab_var_list():
    return create_var_tab_var_list
