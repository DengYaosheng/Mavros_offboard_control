import sys
import math
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from math import radians, cos, sin, tan, asin, atan, acos, sqrt, fabs

print 'Start Script'

startRunning=True

def b_time(dist, vel):
	return dist/vel

def haverdist(X_ua, Y_ua, X_dest, Y_dest):
	lat_ua, lng_ua, lat_dest, lng_dest = map(radians, [X_ua, Y_ua, X_dest, Y_dest])

	dlat = lat_ua - lat_dest
	dlon = lng_ua - lng_dest
	a = sin(dlat/2)**2 + cos(lat_ua) * cos(lat_dest) * sin(dlon/2)**2
	d = 12756274 * asin(sqrt(a))
	return d

def angle2points(lat_ua, long_ua, lat_dest, long_dest):
	angle_unmodified = 57.295779513082323 * atan(fabs((long_dest - long_ua) / (lat_dest - lat_ua)))

	if (lat_ua >= lat_dest and long_ua >= long_dest):
		angle_modified = angle_unmodified
	elif (lat_ua >= lat_dest and long_ua < long_dest):
		angle_modified = 360 - angle_unmodified
	elif (lat_ua < lat_dest and long_ua < long_dest):
		angle_modified = 180 + angle_unmodified
	elif (lat_ua < lat_dest and long_ua >= long_dest):
		angle_modified = 180 - angle_unmodified

	return angle_modified

def addCoords(lng, lat, arr):
	arr.append([lng, lat])

def getangle(Ax, Ay, Bx, By, Cx, Cy):
	hd1 = haverdist(Ax, Ay, Bx, By)
	hd2 = haverdist(Bx, By, Cx, Cy)
	hd3 = haverdist(Cx, Cy, Ax, Ay)
	return acos((hd1 * hd1 + hd3 * hd3 - hd2 * hd2) / (2 * hd1 * hd3))

class locate_point:
	def __init__(self, Vertices, Geoheight, UA_lat, UA_long, UA_alt):
		self.Vertices = Vertices
		self.Geoheight = Geoheight
		self.UA_lat = UA_lat
		self.UA_long = UA_long
		self.UA_alt = UA_alt

		self.Vtx = []
		self.Shortdist_xy = []
		self.Auxangle = []
		self.State = []

		self.Shortdist_plane = 0
		self.Shortdist_z = 0
		self.Shortdist = 0
		self.Inclined_ang = 0
		self.Pt = 0

	def sort_array(self):
		for i in range(0, len(self.Vertices), 2):
			addCoords(self.Vertices[i], self.Vertices[i+1], self.Vtx)

	def locate_xy(self):
		minX = self.Vtx[0][1]
		maxX = self.Vtx[0][1]
		minY = self.Vtx[0][0]
		maxY = self.Vtx[0][0]

		for i in range(0, len(self.Vtx)):
			minX = min(self.Vtx[i][1], minX)
			maxX = max(self.Vtx[i][1], maxX)
			minY = min(self.Vtx[i][0], minY)
			maxY = max(self.Vtx[i][0], maxY)

		if(self.UA_lat < minX or self.UA_lat > maxX or self.UA_long < minY or self.UA_long > maxY):
			return False

		inside = False
		j = len(self.Vtx) - 1
		for i in range(0, len(self.Vtx)):
			if((self.Vtx[i][0] > self.UA_long) != (self.Vtx[j][0] > self.UA_long) and self.UA_lat < (self.Vtx[j][1] - self.Vtx[i][1]) * (self.UA_long - self.Vtx[i][0]) / (self.Vtx[j][0] - self.Vtx[i][0]) + self.Vtx[i][1]):
				inside = not inside

			j=i

		return inside

	def locate(self):
		stt = False

		if(self.locate_xy()):
			if(self.UA_alt < self.Geoheight):
				stt = True

		return stt

	def short_dist_xy(self):
		if (self.locate_xy() == False):
			dist1 = 0
			angUA_ptA = 0
			angUA_ptB = 0
			angUA_pt2A = 0
			angUA_pt2B = 0

			for i in range(0, len(self.Vtx)):
				dist1 = haverdist(self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

				if (i == 0):
					angUA_ptA = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[1][1], self.Vtx[1][0])
					angUA_ptB = getangle(self.Vtx[1][1], self.Vtx[1][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					angUA_pt2A = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[len(self.Vtx) - 1][1], self.Vtx[len(self.Vtx) - 1][0])
					angUA_pt2B = getangle(self.Vtx[len(self.Vtx) - 1][1], self.Vtx[len(self.Vtx) - 1][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					if((angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966) and (angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966)):
						dist1 = dist1*min(sin(angUA_ptA), sin(angUA_pt2A))
						self.Auxangle.append(min(angUA_ptA, angUA_pt2A)*(57.295779513082323))
						if (angUA_ptA <= angUA_pt2A):
							self.State.append(1)
						else:
							self.State.append(2)
					elif(angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966):
						dist1 = dist1*sin(angUA_ptA)
						self.Auxangle.append(angUA_ptA * 57.295779513082323)
						self.State.append(1)
					elif(angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966):
						dist1 = dist1*sin(angUA_pt2A)
						self.Auxangle.append(angUA_pt2A * 57.295779513082323)
						self.State.append(2)
					else:
						self.Auxangle.append(0)
						self.State.append(0)

				elif (i == len(self.Vtx) - 1):
					angUA_ptA = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[0][1], self.Vtx[0][0])
					angUA_ptB = getangle(self.Vtx[0][1], self.Vtx[0][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					angUA_pt2A = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[i - 1][1], self.Vtx[i - 1][0])
					angUA_pt2B = getangle(self.Vtx[i - 1][1], self.Vtx[i - 1][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					if ((angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966) and (angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966)):                    
						dist1 = dist1 * min(sin(angUA_ptA), sin(angUA_pt2A))
						self.Auxangle.append(min(angUA_ptA, angUA_pt2A) * 57.295779513082323)
						if (angUA_ptA <= angUA_pt2A):
							self.State.append(1)                        
						else:                        
							self.State.append(2)                        

					elif (angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966):                   
						dist1 = dist1 * sin(angUA_ptA)
						self.Auxangle.append(angUA_ptA * 57.295779513082323)
						self.State.append(1)

					elif (angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966):                   
						dist1 = dist1 * sin(angUA_pt2A)
						self.Auxangle.append(angUA_pt2A * 57.295779513082323)
						self.State.append(2)

					else:
						self.Auxangle.append(0)
						self.State.append(0)

				else:
					angUA_ptA = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[i + 1][1], self.Vtx[i + 1][0])
					angUA_ptB = getangle(self.Vtx[i + 1][1], self.Vtx[i + 1][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					angUA_pt2A = getangle(self.Vtx[i][1], self.Vtx[i][0], self.UA_lat, self.UA_long, self.Vtx[i - 1][1], self.Vtx[i - 1][0])
					angUA_pt2B = getangle(self.Vtx[i - 1][1], self.Vtx[i - 1][0], self.UA_lat, self.UA_long, self.Vtx[i][1], self.Vtx[i][0])

					if ((angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966) and (angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966)):                 
						dist1 = dist1 * min(sin(angUA_ptA), sin(angUA_pt2A))
						self.Auxangle.append(min(angUA_ptA, angUA_pt2A) * 57.295779513082323)
						if (angUA_ptA <= angUA_pt2A):
							self.State.append(1)                      
						else:                 
							self.State.append(2)                      

					elif (angUA_ptA < 1.5707963267948966 and angUA_ptB < 1.5707963267948966):                  
						dist1 = dist1 * sin(angUA_ptA)
						self.Auxangle.append(angUA_ptA * 57.295779513082323)
						self.State.append(1)

					elif (angUA_pt2A < 1.5707963267948966 and angUA_pt2B < 1.5707963267948966):                 
						dist1 = dist1 * sin(angUA_pt2A)
						self.Auxangle.append(angUA_pt2A * 57.295779513082323)
						self.State.append(2)

					else:                   
						self.Auxangle.append(0)
						self.State.append(0)

				self.Shortdist_xy.append(dist1)

			self.Shortdist_plane = min(self.Shortdist_xy)

		else:
			self.Shortdist_plane = 0

		return self.Shortdist_plane

	def short_dist_z(self):
		if(self.UA_alt <= self.Geoheight):
			self.Shortdist_z = 0
		else:
			self.Shortdist_z = self.UA_alt - self.Geoheight

		return self.Shortdist_z

	def short_dist(self):
		self.Shortdist = sqrt(self.short_dist_xy()**2 + self.short_dist_z()**2)
		
		if(self.short_dist_xy() != 0):
			self.Inclined_ang = 57.295779513082323 * atan(self.short_dist_z() / self.short_dist_xy())
		else:
			self.Inclined_ang = 90

		return self.Shortdist

	def inc_ang(self):
		return self.Inclined_ang

	def point_tied(self):
		if(self.locate_xy() == False):
			self.Pt = self.Shortdist_xy.index(min(self.Shortdist_xy))
		else:
			self.Pt = 0

		return self.Pt

	def aux_ang(self):
		if(self.locate_xy() == False):
			return self.Auxangle[self.Pt]
		else:
			return 0

	def st(self):
		if(self.locate_xy() == False):
			return self.State[self.Pt]
		else:
			return 0

class calculate:
	def __init__(self, lat_ua, long_ua, alt_ua, G_vert, G_height, B3_vert, B3_height, B2_vert, B2_height, B1_vert, B1_height):
		self.UA_lat = lat_ua
		self.UA_long = long_ua
		self.UA_alt = alt_ua

		self.G_vert = G_vert
		self.G_height = G_height
		self.B3_vert = B3_vert
		self.B3_height = B3_height
		self.B2_vert = B2_vert
		self.B2_height = B2_height
		self.B1_vert = B1_vert
		self.B1_height = B1_height

		self.shrtd = 0
		self.p_tied = 0
		self.incang = 0
		self.auxang = 0
		self.stat = 0
		self.polylat = 0
		self.polylong = 0
	
	def pt_state(self):
		gf = locate_point(self.G_vert, self.G_height, self.UA_lat, self.UA_long, self.UA_alt)
		gf.sort_array()

		b3 = locate_point(self.B3_vert, self.B3_height, self.UA_lat, self.UA_long, self.UA_alt)
		b3.sort_array()

		b2 = locate_point(self.B2_vert, self.B2_height, self.UA_lat, self.UA_long, self.UA_alt)
		b2.sort_array()

		b1 = locate_point(self.B1_vert, self.B1_height, self.UA_lat, self.UA_long, self.UA_alt)
		b1.sort_array()

		pos = 0

		if (gf.locate() and b3.locate() and b2.locate() and b1.locate()):
			pos = 4
		elif (b3.locate() and b2.locate() and b1.locate()):
			pos = 3
		elif (b2.locate() and b1.locate()):
			pos = 2
		elif (b1.locate()):
			pos = 1

		if (pos == 0):
			self.shrtd = b1.short_dist()
			self.p_tied = b1.point_tied()
			self.incang = b1.inc_ang()
			self.auxang = b1.aux_ang()
			self.stat = b1.st()
			self.polylong = self.B1_vert[self.p_tied*2]
			self.polylat = self.B1_vert[(self.p_tied*2) + 1]

		elif (pos == 1):
			self.shrtd = b2.short_dist()
			self.p_tied = b2.point_tied()
			self.incang = b2.inc_ang()
			self.auxang = b2.aux_ang()
			self.stat = b2.st()
			self.polylong = self.B2_vert[self.p_tied*2]
			self.polylat = self.B2_vert[(self.p_tied*2) + 1]

		elif (pos == 2):
			self.shrtd = b3.short_dist()
			self.p_tied = b3.point_tied()
			self.incang = b3.inc_ang()
			self.auxang = b3.aux_ang()
			self.stat = b3.st()
			self.polylong = self.B3_vert[self.p_tied*2]
			self.polylat = self.B3_vert[(self.p_tied*2) + 1]

		elif (pos == 3):
			self.shrtd = gf.short_dist()
			self.p_tied = gf.point_tied()
			self.incang = gf.inc_ang()
			self.auxang = gf.aux_ang()
			self.stat = gf.st()
			self.polylong = self.G_vert[self.p_tied*2]
			self.polylat = self.G_vert[(self.p_tied*2) + 1]

		elif (pos == 4):
			self.shrtd = 0
			self.p_tied = 0
			self.incang = 0
			self.auxang = 0
			self.stat = 0

		return pos

	def buffer_dist(self):
		return self.shrtd

	def pt_tied(self):
		return self.p_tied

	def state(self):
		return self.stat

while True:

	lat_ua = cs.lat;
	long_ua = cs.lng;
	alt_ua = cs.alt;

	gf_vert = [103.74862, 1.35123, 103.74954, 1.35096, 103.74935, 1.35031, 103.74986, 1.34942, 103.74887, 1.35025, 103.74805, 1.35004]
	gf_height = 10
	b3_vert = [103.74850, 1.35144, 103.74982, 1.35108, 103.74959, 1.35034, 103.75022, 1.34898, 103.74882, 1.35002, 103.74771, 1.34978]
	b3_height = 20
	b2_vert = [103.74839, 1.35177, 103.75012, 1.35125, 103.74982, 1.35031, 103.75063, 1.34854, 103.74875, 1.34973, 103.74729, 1.34944]
	b2_height = 30
	b1_vert = [103.74827, 1.35207, 103.75050, 1.35140, 103.75017, 1.35030, 103.75117, 1.34790, 103.74870, 1.34941, 103.74681, 1.34906]
	b1_height = 40

	c = calculate(lat_ua, long_ua, alt_ua, gf_vert, gf_height, b3_vert, b3_height, b2_vert, b2_height, b1_vert, b1_height)
	print("State = %s and Distance = %s m" % (c.pt_state(), c.buffer_dist()))

	time.sleep(1.2)
