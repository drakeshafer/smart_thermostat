#-------------------------------------------------------------------------
#Program Name: main.py
#Author: Thomas Krenelka, Zach O'Toole
#------------------------------------------------------------------------
#Description:
#   This the main routine that calls all other subroutines.
#   Main entry point for the application.

#-----------------------------------------------------------------------

import bang_bang as bang_bang
import bounds as bounds
import thermostat_inputs as io
from learning import probability_present
import time, sched
import main_globals

# Main function of the project
def main():
    # Initialization
    main_globals.init() # TODO: get the user set point through the UI
    s = sched.scheduler(time.time, time.sleep)
    probability_present()
    print("Initialization complete. Entering main loop...")
    # Main Loop
    while True:
        # Get inputs (dt = 60sec)
        s.enter(5, 10, io.get_inside_temp)
#        s.enter(15, 9, io.get_outside_t)
        s.enter(10, 8, io.get_occ)

        # Get the probability present, then setpoint in the next delta t (dt = 15m)
        #s.enter(10*6, 3, probability_present)
        s.enter(10, 2, bounds.set_new)

        # Set the HVAC (dt = 1m)
        s.enter(5, 1, bang_bang.bang_bang)

        s.run()
        print("------------------------------------------------------ Cycle Complete ------------------------------------------------------")
        # UI Code (dt = 0)

if __name__ == "__main__ ":
    main()
main()
