import sys
import os
sys.path.append(os.path.abspath("..") +"/src/account")
class testAccount:
    def testCreate(self):
        from account import account;
        account = account();
        ret = account.create();
        return ret


testAccount = testAccount();
ret = testAccount.testCreate();
print ret
exit;
