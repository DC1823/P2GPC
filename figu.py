from libmat import *
from math import tan, pi, atan2, acos, sqrt

class Shape(object):
    def __init__(self, pos, mat):
        self.pos = pos
        self.mat = mat
        
    def rintrsct(self, ori, dir):
        return None

class Intercept(object):
    def __init__(self, dist, punto, norm, obj, txtucrds):
        self.dist = dist
        self.punto = punto
        self.norm = norm
        self.obj = obj
        self.txtucrds = txtucrds

class Plane(Shape):
    def __init__(self, pos, norm, mat):
        self.norm = norm
        super().__init__(pos, mat)

    def rintrsct(self, ori, dir):
        deno = prodpunto(dir, self.norm)
        if abs(deno) <=0.0001:
            return None
        nm = prodpunto(sv(self.pos, ori), self.norm)
        t= nm / deno
        if t < 0 :
            return None
        P = av(ori, escxv(dir, t))
        return Intercept(dist=t,punto=P,norm=self.norm,txtucrds=None,obj=self)
    
class Disk(Plane):
    def __init__(self, pos, norm, mat, radi):
        self.radi = radi
        super().__init__(pos, norm, mat)

    def rintrsct(self, ori, dir):
        rintrsct = super().rintrsct(ori, dir)
        if rintrsct is None:
            return None
        dist = magnv(sv(rintrsct.punto, self.pos))
        return None if dist > self.radi else Intercept(dist=rintrsct.dist,punto=rintrsct.punto,norm=rintrsct.norm,txtucrds=None,obj=self)

class AABB(Shape):
    def __init__(self, pos, tama, mat):
        self.tama = tama
        super().__init__(pos, mat)
        self.planos = []
        self.tama = tama
        izqPlane = Plane(av(pos, (-tama[0] / 2, 0, 0)), (-1, 0, 0), mat)
        derPlane = Plane(av(pos, (tama[0] / 2, 0, 0)), (1, 0, 0), mat)
        topPlane = Plane(av(pos, (0, tama[1] / 2, 0)), (0, 1, 0), mat)
        botPlane = Plane(av(pos, (0, -tama[1] / 2, 0)), (0, -1, 0), mat)
        frontPlane = Plane(av(pos, (0, 0, tama[2]/ 2)), (0, 0, 1), mat)
        backPlane = Plane(av(pos, (0, 0, -tama[2]/ 2)), (0, 0, -1), mat)
        self.planos.append(izqPlane)
        self.planos.append(derPlane)
        self.planos.append(topPlane)
        self.planos.append(botPlane)
        self.planos.append(frontPlane)
        self.planos.append(backPlane)
        self.limiMin =[0,0,0]
        self.limiMax =[0,0,0]
        bs = 0.0001
        for i in range(3):
            self.limiMin[i] = self.pos[i] - (self.tama[i] / 2 + bs)
            self.limiMax[i] = self.pos[i] + self.tama[i] / 2 + bs

    def rintrsct(self, ori, dir):
        intersect = None
        t = float("inf")
        u=0
        v=0
        for plane in self.planos:
            planeIntersect = plane.rintrsct(ori, dir)
            if planeIntersect is not None:
                planePoint = planeIntersect.punto
                if self.limiMin[0] < planePoint[0] < self.limiMax[0]:
                    if self.limiMin[1] < planePoint[1] < self.limiMax[1]:
                        if self.limiMin[2] < planePoint[2] < self.limiMax[2]:
                            if planeIntersect.dist < t:
                                t = planeIntersect.dist
                                intersect = planeIntersect
                                if abs(plane.norm[0])>0:
                                    u= (planePoint[1]-self.limiMin[1]) / (self.tama[1] + 0.002)
                                    v= (planePoint[2]-self.limiMin[2]) / (self.tama[2] + 0.002)
                                elif abs(plane.norm[1])>0:
                                    u= (planePoint[0]-self.limiMin[0]) / (self.tama[0] + 0.002)
                                    v= (planePoint[2]-self.limiMin[2]) / (self.tama[2] + 0.002)
                                elif abs(plane.norm[2])>0:
                                    u= (planePoint[0]-self.limiMin[0]) / (self.tama[0] + 0.002)
                                    v= (planePoint[1]-self.limiMin[1]) / (self.tama[1] + 0.002)
        return None if intersect is None else Intercept(dist=t,punto=intersect.punto,norm=intersect.norm,txtucrds=(u,v),obj=self)

class Sphere(Shape):
    def __init__(self, pos, radi, mat):
        self.radi = radi
        super().__init__(pos,mat)

    def rintrsct(self, ori, dir):
        L = sv(self.pos, ori)
        lenL = magnv(L)
        ta = prodpunto(L, dir)
        d = (lenL ** 2 - ta ** 2) ** 0.5
        if 0>lenL ** 2 - ta ** 2 or d > self.radi:
            return None
        tc = (self.radi ** 2 - d ** 2) ** 0.5
        t = ta - tc
        t1 = ta + tc
        if t < 0:
            t = t1
        if t < 0:
            return None
        punto = av(ori, escxv(dir, t))
        norm = sv(punto, self.pos)
        norm = nrv(norm)
        u = (atan2(norm[2], norm[0]) / (2 * pi)) + 0.5
        v = acos(norm[1]) / pi
        return Intercept(dist=t, punto=punto, norm=norm, txtucrds=(u, v),obj=self)

class Triangle(Shape):
        def __init__(self, vertices, mat):
            super().__init__(pos=vertices[0], mat=mat)
            self.vertices = vertices

        def rintrsct(self, ori, dir):
            v, v1, v2 = self.vertices
            edge1 = sv(v1, v)
            edge2 = sv(v2, v)
            norm = nrv(prodcruz(edge1, edge2))
            d = prodpunto(norm, v)
            deno = prodpunto(norm, dir)
            if abs(deno) < 0.0001:
                return None
            t = (d - prodpunto(norm, ori)) / deno
            if t < 0:
                return None
            punto = av(ori, escxv(dir,t))
            edge = sv(v, v2)
            edge2 = sv(v2, v1)
            if prodpunto(norm, prodcruz(edge, sv(punto, v2))) < 0:
                return None
            if prodpunto(norm, prodcruz(edge1, sv(punto, v))) < 0:
                return None
            if prodpunto(norm, prodcruz(edge2, sv(punto, v1))) < 0:
                return None
            c = prodpunto(edge, sv(punto, v2))
            c1 = prodpunto(edge1, sv(punto, v))
            c2 = prodpunto(edge2, sv(punto, v1))
            total = c + c1 + c2
            u = c1 / total
            v = c2 / total
            u *= 1.8
            v *= 1.3
            return Intercept(dist=t, punto=punto, norm=norm, txtucrds=(u, 1-v), obj=self)

class Pyramid(Shape):
    def __init__(self, pos, Width, Height, dp, rttn, mat):
        super().__init__(pos=pos, mat=mat)
        self.WI = Width
        self.He = Height
        self.dp = dp
        self.rttn = rttn

    def rintrsct(self, ori, dir):
        v = (-self.WI / 2, 0, -self.dp / 2)
        v1 = (-self.WI / 2, 0, self.dp / 2)
        v2 = (self.WI / 2, 0, self.dp / 2)
        v3 = (self.WI / 2, 0, -self.dp / 2)
        ax = (0, self.He, 0)
        v = rotate(v, self.rttn)
        v1 = rotate(v1, self.rttn)
        v2 = rotate(v2, self.rttn)
        v3 = rotate(v3, self.rttn)
        ax = rotate(ax, self.rttn)
        v = av(v, self.pos)
        v1 = av(v1, self.pos)
        v2 = av(v2, self.pos)
        v3 = av(v3, self.pos)
        ax = av(ax, self.pos)
        triangles = []
        triangles.append(Triangle((v, v1, v2), self.mat))
        triangles.append(Triangle((v, v2, v3), self.mat))
        triangles.append(Triangle((v, v1, ax), self.mat))
        triangles.append(Triangle((v1, v2, ax), self.mat))
        triangles.append(Triangle((v2, v3, ax), self.mat))
        triangles.append(Triangle((v3, v, ax), self.mat))
        cintersc = None
        for triangle in triangles:
            inter = triangle.rintrsct(ori, dir)
            if inter is not None:
                if cintersc is None or inter.dist < cintersc.dist:
                    cintersc = inter
        return Intercept(dist=cintersc.dist,punto=cintersc.punto,norm=cintersc.norm,txtucrds=cintersc.txtucrds,obj=self) if cintersc else None    
    
    
class Toroid(Shape):
    def __init__(self, pos, mat, mazradi, minradi, norm):
        super().__init__(pos, mat)
        self.mazradi = mazradi
        self.minradi = minradi
        self.norm = nrv(norm)

    def rintrsct(self, origin, direction):
        cplano = Plane(self.pos, self.norm, self.mat)
        cinterc = cplano.rintrsct(origin, direction)
        if cinterc is None:
            return None
        cpunto = sv(cinterc.punto, self.pos)
        dcen = magnv(cpunto)
        point = cinterc.punto
        if (dcen >= self.minradi and dcen <= self.mazradi + self.minradi):
            u = (1 + math.atan2(point[1], point[0]) / (2 * math.pi)) % 1
            v = (magnv(cpunto) - self.minradi) / (self.mazradi - self.minradi)
            return Intercept(distance=dcen,punto=cinterc.punto,norm=cinterc.norm,texcoords=(u,v),obj=self)
        else:
            return None
        