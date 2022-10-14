import datetime
# prev_time="2022-09-21 12:48:12.274862"
# converted_prev_time= datetime.datetime.strptime(prev_time, '%Y-%m-%d %H:%M:%S.%f')
# print(converted_prev_time)
#
# time_now=datetime.datetime.now()
# print(time_now)
# print(type(time_now))
#
# diff=time_now - converted_prev_time
# print("Diff ", diff.total_seconds())

# regex = "^\+254\d{9}"
# import re
# if re.match(regex,  "+254729225710"):
#     print("Ok")
# else:
#     print("Not Ok")
#

import re

def solve(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False