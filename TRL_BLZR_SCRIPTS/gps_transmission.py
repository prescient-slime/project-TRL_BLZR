from pymavlink import mavutil
import time

def main():
    connection_string = 'udpin:0.0.0.0:14550'  #IMPORTANT: replace with actual drone connection port

    master = mavutil.mavlink_connection(connection_string)
    master.wait_heartbeat()  # is drone connection established?

    try:
        while True:  # loop for GPS coordinates
            msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

            if msg is not None:
                lat = msg.lat / 1e7
                lon = msg.lon / 1e7
                alt = msg.alt / 1000
                direction = msg.hdg / 100  

                print(f'Latitude: {lat}, Longitude: {lon}, Altitude: {alt}, direction: {direction} degrees')
            else:
                print("No Connection, Aborting.")
            time.sleep(1)  # slows down readings

    finally:
        if 'master' in locals():
            master.close()
            print("Connection Closed.")

if __name__ == "__main__":
    main()