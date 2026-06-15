import math
import time
import string
PI = 3.1415926535897931
RADEG = 180.0 / PI
DEGRAD = PI / 180.0
INV360 = 1.0 / 360.0

def __daysSince2000Jan0(y, m, d):
    '''A macro to compute the number of days elapsed since 2000 Jan 0.0
       (which is equal to 1999 Dec 31, 0h UT)'''
    return (367 * y - 7 * (y + (m + 9) / 12) / 4) + 275 * m / 9 + d - 730530


def __sind(x):
    '''Returns the sin in degrees'''
    return math.sin(x * DEGRAD)


def __cosd(x):
    '''Returns the cos in degrees'''
    return math.cos(x * DEGRAD)


def __acosd(x):
    '''Returns the arc cos in degrees'''
    return math.acos(x) * RADEG


def __atan2d(y, x):
    '''Returns the atan2 in degrees'''
    return math.atan2(y, x) * RADEG


def __sunRiseSet(year, month, day, lon, lat):
    """
    This macro computes times for sunrise/sunset.
    Sunrise/set is considered to occur when the Sun's upper limb is
    35 arc minutes below the horizon (this accounts for the refraction
    of the Earth's atmosphere).
    """
    return __sunriset__(year, month, day, lon, lat, -35.0 / 60.0, 1)


def __sunriset__(year, month, day, lon, lat, altit, upper_limb):
    """
    Note: year,month,date = calendar date, 1801-2099 only.
          Eastern longitude positive, Western longitude negative
          Northern latitude positive, Southern latitude negative
          The longitude value IS critical in this function!
          altit = the altitude which the Sun should cross
                  Set to -35/60 degrees for rise/set, -6 degrees
                  for civil, -12 degrees for nautical and -18
                  degrees for astronomical twilight.
                  upper_limb: non-zero -> upper limb, zero -> center
                  Set to non-zero (e.g. 1) when computing rise/set
                  times, and to zero when computing start/end of
                  twilight.
          *rise = where to store the rise time 
          *set  = where to store the set  time 
                  Both times are relative to the specified altitude,
                  and thus this function can be used to compute
                  various twilight times, as well as rise/set times
    Return value:  0 = sun rises/sets this day, times stored at
                       *trise and *tset.
                  +1 = sun above the specified 'horizon' 24 hours.
                       *trise set to time when the sun is at south,
                       minus 12 hours while *tset is set to the south
                       time plus 12 hours. 'Day' length = 24 hours 
                  -1 = sun is below the specified 'horizon' 24 hours
                       'Day' length = 0 hours, *trise and *tset are
                       both set to the time when the sun is at south.
    """
    d = __daysSince2000Jan0(year, month, day) + 0.5 - lon / 360.0
    sidtime = __revolution(__GMST0(d) + 180.0 + lon)
    res = __sunRADec(d)
    sRA = res[0]
    sdec = res[1]
    sr = res[2]
    tsouth = 12.0 - __rev180(sidtime - sRA) / 15.0
    sradius = 0.2666 / sr
    if upper_limb:
        altit = altit - sradius
    
    cost = (__sind(altit) - __sind(lat) * __sind(sdec)) / (__cosd(lat) * __cosd(sdec))
    if cost >= 1.0:
        rc = -1
        t = 0.0
    elif cost <= -1.0:
        rc = 1
        t = 12.0
    else:
        t = __acosd(cost) / 15.0
    return (tsouth - t, tsouth + t)


def __sunpos(d):
    """
    Computes the Sun's ecliptic longitude and distance 
    at an instant given in d, number of days since     
    2000 Jan 0.0.  The Sun's ecliptic latitude is not  
    computed, since it's always very near 0.           
    """
    M = __revolution(356.04700000000003 + 0.98560025849999999 * d)
    w = 282.94040000000001 + 4.7093499999999999e-05 * d
    e = 0.016709000000000002 - 1.1510000000000001e-09 * d
    E = M + e * RADEG * __sind(M) * (1.0 + e * __cosd(M))
    x = __cosd(E) - e
    y = math.sqrt(1.0 - e * e) * __sind(E)
    r = math.sqrt(x * x + y * y)
    v = __atan2d(y, x)
    lon = v + w
    if lon >= 360.0:
        lon = lon - 360.0
    
    return (lon, r)


def __sunRADec(d):
    ''
    res = __sunpos(d)
    lon = res[0]
    r = res[1]
    x = r * __cosd(lon)
    y = r * __sind(lon)
    obl_ecl = 23.439299999999999 - 3.5629999999999998e-07 * d
    z = y * __sind(obl_ecl)
    y = y * __cosd(obl_ecl)
    RA = __atan2d(y, x)
    dec = __atan2d(z, math.sqrt(x * x + y * y))
    return (RA, dec, r)


def __revolution(x):
    '''
    This function reduces any angle to within the first revolution 
    by subtracting or adding even multiples of 360.0 until the     
    result is >= 0.0 and < 360.0
    
    Reduce angle to within 0..360 degrees
    '''
    return x - 360.0 * math.floor(x * INV360)


def __rev180(x):
    '''
    Reduce angle to within +180..+180 degrees
    '''
    return x - 360.0 * math.floor(x * INV360 + 0.5)


def __GMST0(d):
    '''
    This function computes GMST0, the Greenwich Mean Sidereal Time  
    at 0h UT (i.e. the sidereal time at the Greenwhich meridian at  
    0h UT).  GMST is then the sidereal time at Greenwich at any     
    time of the day.  I\'ve generalized GMST0 as well, and define it 
    as:  GMST0 = GMST - UT  --  this allows GMST0 to be computed at 
    other times than 0h UT as well.  While this sounds somewhat     
    contradictory, it is very practical:  instead of computing      
    GMST like:                                                      
                                                                    
     GMST = (GMST0) + UT * (366.2422/365.2422)                      
                                                                    
    where (GMST0) is the GMST last time UT was 0 hours, one simply  
    computes:                                                       
                                                                    
     GMST = GMST0 + UT                                              
                                                                    
    where GMST0 is the GMST "at 0h UT" but at the current moment!   
    Defined in this way, GMST0 will increase with about 4 min a     
    day.  It also happens that GMST0 (in degrees, 1 hr = 15 degr)   
    is equal to the Sun\'s mean longitude plus/minus 180 degrees!    
    (if we neglect aberration, which amounts to 20 seconds of arc   
    or 1.33 seconds of time)
    '''
    sidtim0 = __revolution(818.98753999999997 + 0.98564735199999998 * d)
    return sidtim0


def calcSunRiseSet(lon, lat, date = None):
    if date is None:
        date = time.gmtime(time.time())
    
    times = __sunRiseSet(date[0], date[1], date[2], lon, lat)
    currTime = time.localtime(time.mktime(date))
    if currTime[8] == 1:
        timeDiff = time.altzone / 3600
    else:
        timeDiff = time.timezone / 3600
    sunRST = []
    for t in times:
        localTime = list(date)
        (min, hour) = math.modf(t)
        localTime[3] = int(hour - timeDiff)
        localTime[4] = int(min * 60)
        sunRST.append(localTime)
    
    return sunRST

