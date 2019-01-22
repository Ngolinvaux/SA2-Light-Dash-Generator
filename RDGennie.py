import math
import struct

class SetObject(object):
    def _init_(self,objId,xRot,yRot,zRot,x,y,z,v1,v2,v3):
        pass


class SetFile(object):
    def _init_(self):
        #init empty setfile
        pass

    def write_to_file(self,objects):
        with open("light.bin",'wb') as setfile:
            setfile.write(struct.pack('I',len(objects)))
            #print(len(objects))
            for i in range(1,8):
                #print(i)
                setfile.write(struct.pack('I',0))
            for obj in objects:
                setfile.write(struct.pack('H',obj.objId))
                setfile.write(struct.pack('H',obj.xRot))
                setfile.write(struct.pack('H',obj.yRot))
                setfile.write(struct.pack('H',obj.zRot))
                setfile.write(struct.pack('f',obj.x))
                setfile.write(struct.pack('f',obj.y))
                setfile.write(struct.pack('f',obj.z))
                setfile.write(struct.pack('f',obj.v1))
                setfile.write(struct.pack('f',obj.v2))
                setfile.write(struct.pack('f',obj.v3))
        pass


def getDist(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])+(p1[2]-p2[2])*(p1[2]-p2[2]))


def lineRDG(idd,space):
    objects = []
    i = 0
    distBetween = space
    numOfRings = 1
    dashSize = distBetween*numOfRings

    while (i < numOfPoints - 1):
        dist = getDist(points[i],points[i+1])
        t = dist/dashSize
                       
        iteration = 0;
        while(dist > 0):
                       
            x1 = points[i][0]
            x2 = points[i+1][0]         
            y1 = points[i][1]
            y2 = points[i+1][1]
            z1 = points[i][2]
            z2 = points[i+1][2]
                       
            obj = SetObject()
            obj.objId = idd
            obj.xRot = 0
            obj.yRot = 0
            obj.zRot = 0
            obj.x = x1 + (iteration * (x2-x1)/t)
            obj.y = y1 + (iteration * (y2-y1)/t)
            obj.z = z1 + (iteration * (z2-z1)/t)
            obj.v1 = distBetween
            obj.v2 = 0
            obj.v3 = numOfRings
            objects.append(obj)
            dist = dist - dashSize
            iteration += 1
            print(iteration, obj.x,obj.y,obj.z)
        i += 1

    #1,xAngle,yAngle,zAngle,x1,y1,z1,distBetween,69,numOfRings)
    #print(zAngle,yAngle,xAngle)
    print("Done")


    set.write_to_file(objects)


def spiralRDG(plane,idd,space,ri,r,offset):
    objects = []
    i = 0
    distBetween = space
    numOfRings = 1
    dashSize = distBetween*numOfRings

    while (i < numOfPoints - 1):
        dist = getDist(points[i],points[i+1])
        t = dist/dashSize
        theta = math.radians(270)
        #theta = 0
        iteration = 0;
        its = 360 / dashSize
        while(iteration < ri):
                       
            x1 = points[i][0]
            x2 = points[i+1][0]         
            y1 = points[i][1]
            y2 = points[i+1][1]
            z1 = points[i][2]
            z2 = points[i+1][2]
                       
            obj = SetObject()
            obj.objId = idd
            obj.xRot = 0
            obj.yRot = 0
            obj.zRot = 0
            useThisTheta = math.radians((iteration*space)+offset)
            if(plane == 'y'):
                obj.x = x1 + r* math.cos(useThisTheta) + (iteration * (x2-x1)/ri)
                obj.z = z1 + r* math.sin(useThisTheta) + (iteration * (z2-z1)/ri)
                obj.y = y1 + (iteration * (y2-y1)/ri)
            if(plane == 'z'):
                obj.x = x1 + r* math.cos(useThisTheta) + (iteration * (x2-x1)/ri) 
                obj.y = y1 + r* math.sin(useThisTheta) + (iteration * (y2-y1)/ri)
                obj.z = z1 + (iteration * (z2-z1)/ri)
            if(plane == 'x'):
                obj.y = y1 + r* math.cos(useThisTheta) + (iteration * (y2-y1)/ri)
                obj.z = z1 + r* math.sin(useThisTheta) + (iteration * (z2-z1)/ri)
                obj.x = x1 + (iteration * (x2-x1)/ri)
                
            obj.v1 = distBetween
            obj.v2 = 0
            obj.v3 = numOfRings
            objects.append(obj)
            dist = getDist([obj.x,obj.y,obj.z],points[i+1])
            #print(dist)
            iteration += 1
            print(iteration, obj.x,obj.y,obj.z)
        i += 1


    print("Done")


    set.write_to_file(objects)



set = SetFile()
points = []
with open("input.txt",'r') as inputF:
    line = inputF.readline().strip().lower()
    if(line == "line"):
        idd = int(inputF.readline().strip())
        space = float(inputF.readline().strip())
        numOfPoints = int(inputF.readline().strip())
        for i in range(0,numOfPoints):
            points.append([])
            points[i] = [float(c.strip()) for c in inputF.readline().strip().split(',')]
        lineRDG(idd,space)

    elif(line == "spiral"):      
        plane = inputF.readline().strip()
        idd = int(inputF.readline().strip())
        space = float(inputF.readline().strip())
        r = float(inputF.readline().strip())
        ri = int(inputF.readline().strip())
        offset = float(inputF.readline().strip())
        numOfPoints = 2
        for i in range(0,numOfPoints):
            points.append([])
            points[i] = [float(c.strip()) for c in inputF.readline().strip().split(',')]
        spiralRDG(plane,idd,space,ri,r,offset)
