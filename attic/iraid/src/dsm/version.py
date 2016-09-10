class Version():
	major=None
	minor=None
	patch=None

	def __init__(self,major=0,minor=0,patch=0):
		self.major=major
		self.minor=minor
		self.patch=patch

	def __repr__(self):
		return "%d.%d.%d" % (self.major,self.minor,self.patch)

	def __eq__(self,target):
		if self.major == target.major and self.minor==target.minor and self.patch==target.patch:
			return True
		return False

	def __gt__(self,target):
		if self.major > target.major:
			return True
		if self.minor > target.minor:
			return True
		if self.patch > target.patch:
			return True
		return False

	def __lt__(self,target):
		if self.major < target.major:
			return True
		if self.minor < target.minor:
			return True
		if self.patch < target.patch:
			return True
		return False







if __name__ == '__main__':
	print "debugging..."
	myver = Version(1,3,0)
	yourver = Version(2,0,7544)

	if myver > yourver:
		print "myver is bigger"
	else:
		print "yourver is bigger"

	yourver=Version(1,3,0)

	if myver == yourver:
		print "version are same"
	else:
		print "yourver is bigger"
