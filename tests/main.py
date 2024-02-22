from varainterface import *
import unittest



class TestSum(unittest.TestCase):
        
    def test_query(self):
        account = Account()
        service_functions = ServiceFunctions(account)
        num_dt = service_functions.chainstate_query("GearGas", "Allowance")
        print(num_dt)
    
    def test_send_msg(self):

        def callback(data):
            if data["message"]["payload"] == "PONG":
                print("DONE")

        account = Account()
        subscriber = Subscriber(account, SubEvent.UserMessageSent, subscription_handler=callback)

        account = Account(seed="water plug remind fame match spin ridge float butter safe bean uphold", remote_ws="wss://testnet.vara.network")
        service_functions = ServiceFunctions(account, return_block_num=True)
        hash_e = service_functions.extrinsic("Gear", "send_message", {"destination": "0xaa33d8cffb97646a16a73509b6f78bfb33c25351517652d4fbd9ac725e35e07c", "payload": "PING", "gas_limit": 10_000_000_000, "value": 0, "keep_alive": False})
        print(hash_e)
        subscriber.cancel()

if __name__ == '__main__':
    unittest.main()