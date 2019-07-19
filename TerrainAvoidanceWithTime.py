import time

# Excessive Descent Rate
def TerrainAvoidance (radar_Altimeter, barometric_Altimeter):
    pull_Up_Line = (2500/5500)
    sink_Rate_Line = (2500/3000)
    ba = [2000,1950,1900,1800,5000]
    
        
    # descendRate (feet per minute)
    for i in range (1,len(ba)):
        descend_Rate = (ba[i]-ba[i-1]) * 60
        ad = abs(ba[i]/descend_Rate)
        
        EDRAlarm = "No Alarm"

        while(ba[i] < 2500 and descend_Rate < 0):
            if (pull_Up_Line <= ad < sink_Rate_Line):
                EDRAlarm = "SINKRATE"
                break
            elif (ad < sinkRateLine):
                EDRAlarm = "PULL UP!"
                break
        print(EDRAlarm)
        time.sleep(1)

        



EDR(5000,1000)