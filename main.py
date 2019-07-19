import time as t
import struct
import socket

Level0 = 'No Warning\0'
Level1 = 'Sinkrate\0'
Level2 = 'Terrain Terrain\0'
Level3 = 'Pullup\0'


class Altimeter:
    def __init__(self, update_fun, start_time):
        self.__update_fun = update_fun
        self.altitude = self.__update_fun(start_time)
        self.altitude_prev = self.__height

    def get_altitude(self):
        return self.altitude

    def get_altitudeprev(self):
        return self.altitude_prev

    def update(self, time):
        self.altitude_prev = self.altitude
        self.altitude = self.__update_fun(time)


def updateBarometricAltimeter(x):
    return 2.58082070417806E-30*x**9.0 - \
           1.43998087080294E-25*x**8.0 + \
           3.23090472761222E-21*x**7.0 - \
           3.76627663625449E-17*x**6.0 + \
           2.45542473711697E-13*x**5.0 - \
           8.91555498884083E-10*x**4.0 + \
           1.60596436776688E-6*x**3.0 - \
           5.60114120783000E-4*x**2.0 - \
           1.88123150516033*x + \
           6000.00000004435


def updateRadarAltimeter(x):
    return -3.51267870846810E-22*x**7.0 + \
           1.31621594470521E-17*x**6.0 - \
           1.94360705290089E-13*x**5.0 + \
           1.44017725303852E-9*x**4.0 - \
           5.64335394646106E-6*x**3.0 + \
           1.10545660156682E-2*x**2.0 - \
           7.66353503641428*x + \
           1999.99999999998


def status(distance, altitude, terrainClosureRate, descentRate):
    # Mode 2
    if 2000.0 < terrainClosureRate <= 3500.0 and distance < terrainClosureRate - 2000.0:
        return Level3
    elif terrainClosureRate > 3500.0 and distance < 0.14286 * terrainClosureRate + 1000.0:
        return Level3
    elif 2000.0 < terrainClosureRate <= 3500.0 and distance < terrainClosureRate - 1500.0:
        return Level2
    elif terrainClosureRate > 3500.0 and distance < 0.14286 * terrainClosureRate + 1500.0:
        return Level2
		# Mode 1
		if descentRate > 1800.0 and altitude < 0.45 * descentRate - 700.0:
			return PULLUP
		elif descentRate > 1800.0 and altitude < 0.6 * descentRate - 600.0:
			return Level1
		return Level0


def terrainAvoidance(RadarAltimeter, barometricAltimeter):
    altitude = barometricAltimeter.get_altitude()
    altitude_prev = barometricAltimeter.getaAltitudePrev()
    distance = altitude - RadarAltimeter.get_altitude()
    distance_prev = altitude_prev - RadarAltimeter.getaAltitudePrev()

    descentRate = (altitude_prev - altitude) * 60
    terrainClosureRate = (distance_prev - distance) * 60

    return status(descentRate, distance, altitude, terrainClosureRate)


def main():
    ip_adress = "127.0.0.1"
    udp_port = 5555
    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    packer = struct.Struct('f I 16s f f f f f')

    start_time = 0.0
    end_time = 2000.0
    step_size = 1.0
    time = start_time
    version = 3.1
    size = 44

    barometricAltimeter = Altimeter(updateBarometricAltimeter, start_time)
    RadarAltimeter = Altimeter(updateRadarAltimeter, start_time)

    while time <= end_time:
        message = (
            version,
            size,
            terrainAvoidance(RadarAltimeter, barometricAltimeter).encode(),
            time,
            barometricAltimeter.get_altitude(),
            RadarAltimeter.get_altitude(),
            (barometricAltimeter.getaAltitudePrev() - barometricAltimeter.get_altitude()) * 60,
            (RadarAltimeter.getaAltitudePrev() - RadarAltimeter.get_altitude()) * 60
        )
        print(message)

        time += step_size
        RadarAltimeter.update(time)
        barometricAltimeter.update(time)

        sock.sendto(packer.pack(*message), (ip_adress, udp_port))
        t.sleep(step_size)


if __name__ == '__main__':
    main()
