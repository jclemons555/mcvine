
import units
radian = units.angle.radian
def toRadians( angles ):
    ret = []
    for angle in angles:
        try:
            # test if angle is with appropriate unit
            angle + radian
            angle /= radian
        except Exception, err:
            if angle == 0 or isinstance(angle,float):
                pass
            else:
                raise ValueError , "Not an angle: %s(type=%s). %s:%s" % (
                    angle, type(angle), err.__class__, err)
        ret.append( angle )
        continue
    return ret



