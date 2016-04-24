"""
@author SodaPhish <sodaphish@protonmail.ch>
"""
class Version(object):
    """Version
    The Version class provides a basic class to handle software versions in the
    form of Major.Minor.Build/Bug.  Realistically, if your versioning system
    requires more than that, you've an unnecessarily complex versioning scheme.
    
    Seriously, I don't make a practice of preaching in comments, but version 
    numbers have gotten ABSURD.  -CJS
    """
    majorVersion = 0
    minorVersion = 0
    buildVersion = 0


    def __init__(self,maj=0,min=0,build=0):
        """__init__()
        constructor for the Version class.  Takes three integer arguments, and 
        has the necessary methods to support most logical operators (gt, eq, etc.)
        """
        if self.setMajor(maj) is not True or self.setMinor(min) is not True or self.setBuild(build) is not True:
            raise(Exception('type mismatch'))
        pass
    '''end __init__()'''


    def setMajor(self,major):
        if int(major) >= 0:
            self.majorVersion = int(major)
            return True
        else:
            return False
    '''end setMajor'''


    def setMinor(self,minor):
        if int(minor) >= 0:
            self.minorVersion = int(minor)
            return True
        else:
            return False
    '''end setMinor()'''


    def setBuild(self,build):
        if int(build) >= 0:
            self.buildVersion = build
            return True
        else:
            return False
    '''end setBuild()'''


    def __eq__(self,other):
        if self.majorVersion == other.majorVersion and self.minorVersion == other.minorVersion and self.buildVersion == other.buildVersion:
            return True
        return False
    '''end __eq__()'''


    def __lt__(self,other):
        if self.majorVersion > other.majorVersion:
            return False

        if self.minorVersion > other.minorVersion:
            return False

        if self.buildVersion > other.buildVersion:
            return False

        return True
    '''end __lt__()'''


    def __gt__(self,other):
        if self.majorVersion > other.majorVersion:
            return True
        elif self.majorVersion < other.majorVersion:
            return False

        if self.minorVersion > other.minorVersion:
            return True
        elif self.minorVersion < other.minorVersion:
            return False

        if self.buildVersion > other.buildVersion:
            return True
        elif self.buildVersion < other.buildVersion:
            return False

        return False
    '''end __gt__()'''


    def __repr__(self):
        return '%d.%d.%d' % (self.majorVersion,self.minorVersion,self.buildVersion)
    '''end __repr__()'''



if __name__ == '__main__':
    ver_a = Version(0,0,1)
    ver_b = Version(0,1,0)
    ver_c = Version(1,0,0)

    if ver_a > ver_b:
        print "%s is greater than %s" % (ver_a, ver_b)
    else:
        print "%s is greater than %s" % (ver_b, ver_a)

    if ver_b > ver_c:
        print "%s is greater than %s" % (ver_b, ver_c)
    else:
        print "%s is greater than %s" % (ver_c, ver_b)

    if ver_c < ver_a:
        print "%s is less than %s" % (ver_c, ver_a)
    else:
        print "%s is less than %s" % (ver_a, ver_c)

    if ver_b < ver_c:
        print "%s is less than %s" % (ver_c, ver_b)
    else:
        print "%s is less than %s" % (ver_b, ver_c)

""" ___EOF___ """
