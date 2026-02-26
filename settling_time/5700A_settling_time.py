import pyvisa
from datetime import datetime
import time
import pandas as pd
import logging

VISA_3458A = 'GPIB0::25::INSTR'
VISA_5700A = 'GPIB0::1::INSTR'
SECONDS_TO_PREP = 60*3
SECONDS_TO_CAPTURE = 60*3
NPLC = 10
VOLTAGE_START = 1.0
VOLTAGE_STEP = 6.0

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
rm = pyvisa.ResourceManager()

def setup_3458a(addr):
    inst = rm.open_resource(addr)
    inst.clear()
    inst.write("RESET")
    inst.write("END ALWAYS")
    inst.write("OFORMAT ASCII")
    inst.write("BEEP")
    inst.write("DCV 10")
    inst.write("NPLC "+str(NPLC))
    inst.write("TARM HOLD")
    logging.info("ID? -> "+inst.query("ID?"))
    return inst
    
def setup_5700a(addr):
    inst = rm.open_resource(addr)
    inst.clear()
    inst.write("*RST")
    inst.write("*CLS")
    inst.write("STBY") 
    inst.write("OUT 10 V, 0 Hz")
    inst.write("RANGELCK ON")
    inst.write("OUT 0 V, 0 Hz")
    inst.write("OPER")
    logging.info("ID? -> "+inst.query("*IDN?"))
    return inst

def run_settling_test():
    results = []
    
    dmm = setup_3458a(VISA_3458A)
    calibrator = setup_5700a(VISA_5700A)
    
    logging.info(f"Setting Calibrator to {VOLTAGE_START}V baseline...")
    calibrator.write(f"OUT {VOLTAGE_START}")
    calibrator.write("OPER")
    start_time = time.perf_counter()
    
    while (time.perf_counter() - start_time) < SECONDS_TO_PREP:
        dmm.query("TARM SGL")
    
    logging.info(f"Stepping to {VOLTAGE_STEP}V and capturing...")
    calibrator.write(f"OUT {VOLTAGE_STEP}")
    start_time = time.perf_counter()
    
    while (time.perf_counter() - start_time) < SECONDS_TO_CAPTURE:
        elapsed = time.perf_counter() - start_time
        val = float(dmm.query("TARM SGL"))
        results.append((elapsed, val))
        
    return results
    
settling_data = run_settling_test()
df_settle = pd.DataFrame(settling_data, columns=['Elapsed_Time', 'Voltage'])
timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
output_filename = "csv/settling_test_"+str(NPLC)+"NPLC_"+""+str(SECONDS_TO_CAPTURE)+"capture_"+timestr+".csv"
df_settle.to_csv(output_filename, index=False)