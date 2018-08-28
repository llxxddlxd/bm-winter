import sys
import os
sys.path.append(os.path.abspath("..") + "/src/account")
from account import account;
account = account();
# account.randomByRandom();
ret = account.create();
print ret
exit;
