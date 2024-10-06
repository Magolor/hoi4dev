# %%
from hoi4dev import *

# %%
# Uprise
print(get_num_days("0999.11.11", "1001.02.01") // 7)
# Changeling Retaliation
print(get_num_days("0999.11.11", "1001.04.06") // 7)
# Appleloosa Trade Agreement
print(get_num_days("0999.11.11", "1001.06.01") // 7)
# Crystal Empire Truce
print(get_num_days("0999.11.11", "1001.09.01") // 7)
# Canterlot Pact
print(get_num_days("1001.06.01", "1001.12.01") // 7)
print(get_num_days("1001.09.01", "1001.12.01") // 7)
print(get_num_days("1001.04.06", "1001.12.01") // 7)
print(get_num_days("0999.11.11", "1001.12.01") // 7)
# Cozy Glow Coronation
print(get_num_days("1001.12.01", "1002.06.24") // 7)
print(get_num_days("0999.11.11", "1002.06.25") // 7)
# Jahr Null
print(get_num_days("0999.11.11", "1002.12.25") // 7)

# Second Ponyvile Election
print(get_end_date("1002.12.01", 1298))

# %%