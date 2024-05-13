import os

import usermodel, doctormodel, statemodel, statsmodel

print(os.getcwd())
tcw_db_name=f"{os.getcwd()}/tcwDB.db"
print(tcw_db_name)
usermodel.User(tcw_db_name).initialize_users_table()
doctormodel.Doctor(tcw_db_name).initialize_doctors_table()
#statemodel.State(tcw_db_name).initialize_states_table()
statsmodel.Stat(tcw_db_name).initialize_stats_table()