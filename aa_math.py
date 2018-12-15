"""
TODO Sheet Ideas:
    a line intersecting parallel lines to table of polygon angles
    functions, slopes to equation of line, present higher order curves and ask for slope(x): make a table, graph.
    fast math tables and proofs
    rotate, reflect, and resize
    sums to areas as integrals
    root 2 is irrational graphically and algebraically
    measures: how large the earth, how far the star, how tall the tree
"""

import random
import math
import os
import reportlab
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.charts.axes import XValueAxis,YValueAxis
from reportlab.graphics.shapes import Line, Rect, Polygon, Drawing, Group, String, Circle, Wedge
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle, Image, PageBreak, Frame
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch,cm

try:
    import bases
    Bases = bases.Bases()
except:
    Bases = None
#bases.toAlphabet(11, '0123456789XY')

GRID_COLOR = colors.Color(21/255., 67/255., 234/255.,0.03)
LINE_COLOR = colors.Color(21/255., 67/255., 234/255.,1)

MODULES = {}
MODULES["What is a Proof"] = """
Rectangle bar of gold cut in 3 triangles (write as equation)
Pythagorean Theorem
Sum of the first N counting numbers (folding solution)
Xeno's paradox
Fast math rules: n5*n5 = n(n+1)|25
Exercise: make data tables of above equations
"""
MODULES["Angles and Polygons"] = """
Parallel line intersected by a third line: match angles
Interior angles of a triangle add to 180
Interior angles of various polygon: make a table, find equation.
Rotate a vector (or shape) about the origin: make a table by measurement and find the equation
"""
MODULES["What is a Function"] = """
Sample table mappings to equations
Equations to data tables
PyQL.org Barely Rational database
Plotting
Slopes
Derivatives
e^x = A + Bx + Cx^2 + ....
"""
MODULES["Fundamental Rule of Algebra"] = """
Prime bunnies story
Sieve of Eratosthenes
Fundamental Rule of Arithmatic
Multiplying numbers adds exponents: 2^3*2^2 = 2^5
Negative exponents: 1/2 == 2^(-1): what is 4^0?
Exercise: write compound numbers in Sieve as product of primes
Exercise: reduce fractions like 16*6/4*3, and with variables like 8x^2/16x
"""
MODULES["Different Bases"] = """
familiar 10x times table (with background base 2 values)
times table in base 2 (with background base 2 values)
exercise: write the times table for table for base 3
exercise: what time is it 135 minutes after 11:35AM?
exercise: what is 320 + 60 degrees
multiplication and long divison in base 2
log
"""


class Sheet(object):
    def __init__(self,fout='aa_math.pdf',**kwargs):
        """ Init a Canvas and set defaults.
            Add content to instance and then save."""
        self.margin = kwargs.get('margin',50)
        self.verbose = kwargs.get('verbose',0) # verbose is from 0-9 with 9 most solved
        # kind of patched in here for windows systems. needs fix.
        if DOUT:   fout = os.path.join(DOUT,'%s'%(fout,))
        if not fout.lower().endswith('.pdf'): fout += ".pdf"
        self.can = canvas.Canvas(fout, pagesize=letter)
        self.width, self.height = [x-2*self.margin for x in letter]
        if self.margin:
            self.can.translate(self.margin,-self.margin) # make room at the top
        self.set_style(**kwargs)

    def save(self):
        self.can.save()

    def set_style(self,**kwargs):
        self.header_font, self.header_size = "Helvetica-Bold", 30
        self.normal_font, self.normal_size = "Helvetica", 10

    def sharing_brownies(self,**kwargs):
        margin = kwargs.get('margin',self.margin)
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        rcolor =colors.Color(0/255., 0/255., 0/255., kwargs.get('alpha',1)) # the rectangle
        scolor =colors.Color(0/255., 0/255., 0/255., kwargs.get('alpha',0.5)) # the cuts
        fcolor =colors.Color(0/255., 0/255., 0/255., kwargs.get('alpha',0.05)) # the fill
        gcolor =colors.Color(0/255., 0/255., 0/255., kwargs.get('alpha',.2))
        x = 0; y = height
        self.can.setFont(self.header_font,self.header_size)
        self.can.drawCentredString(width/2, y, "Sharing Brownies")
        y -= self.header_size+160
        self.can.setFillColor(fcolor)
        rect_height = 120
        rect_width = 240
        xspace = (width - 2* rect_width) / 3
        for Y in range(4):
            if Y: y -= xspace + rect_height
            for X in range(2):
                x = xspace + X*( xspace +  rect_width)
                self.can.setStrokeColor(scolor)
                self.can.setStrokeColor(rcolor)
                self.can.rect(x,y,rect_width,rect_height, stroke=1, fill=1)
                if Y == 0: # first row
                    self.can.setStrokeColor(gcolor)
                    N = 2
                    gsize = rect_height / N
                    self.can.grid([x+i*gsize for i in range(1+N*int(rect_width/rect_height))],
                                 [y+i*gsize for i in range(N+1)])
                    tx,ty = x+rect_width*(.5+X/4.),y
                    rx,ry = x,y+rect_height
                    lx,ly = x+rect_width,y+rect_height
                    self.can.setStrokeColor(scolor)
                    self.can.line(tx,ty,rx,ry)
                    self.can.line(tx,ty,lx,ly)
                if Y == 1: # second row
                    self.can.setStrokeColor(gcolor)
                    N = 2
                    gsize = rect_height / N
                    self.can.grid([x+i*gsize for i in range(1+N*int(rect_width/rect_height))],
                                 [y+i*gsize for i in range(N+1)])
                    tx,ty = x+rect_width*(7/8.+X/8.),y
                    rx,ry = x,y+rect_height
                    lx,ly = x+rect_width,y+rect_height
                    self.can.setStrokeColor(scolor)
                    self.can.line(tx,ty,rx,ry)
                    self.can.line(tx,ty,lx,ly)
                if Y == 2:
                    self.can.setStrokeColor(gcolor)
                    N = 4
                    gsize = rect_height / N
                    self.can.grid([x+i*gsize for i in range(1+N*int(rect_width/rect_height))],
                                 [y+i*gsize for i in range(N+1)])

                    if X:
                        tx,ty = x+rect_width*4/8.,y
                        rx,ry = x+rect_width*1/8.,y+rect_height
                        lx,ly = x+rect_width,y+rect_height-rect_width*1/8
                    else:
                        tx,ty = x+rect_width*2/8.,y+rect_width*1/8
                        rx,ry = x+X*rect_width*1/8.,y+rect_height-rect_width*1/8
                        lx,ly = x+rect_width,y+rect_height-rect_width*1/8
                    self.can.setStrokeColor(scolor)
                    self.can.line(tx,ty,rx,ry)
                    self.can.line(tx,ty,lx,ly)
                if Y > 2:
                    self.can.setStrokeColor(gcolor)
                    N = Y*2
                    gsize = rect_height / N
                    self.can.grid([x+i*gsize for i in range(1+N*int(rect_width/rect_height))],
                                 [y+i*gsize for i in range(N+1)])

    def graph_paper(self,**kwargs):
        """put graph paper at current location"""
        lines = kwargs.get('lines',50)
        color = kwargs.get('color',colors.Color(21/255., 67/255., 234/255.,0.08))
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        self.can.setStrokeColor(color)
        xlist = [x*(width/lines) for x in range(0,lines+1)]
        ylist = [x*(width/lines) for x in range(0,1+int(lines*height/width))]
        self.can.grid(xlist, ylist)

    def prime_bunnies(self,**kwargs):
        # number line with prime bunny hops as bezier
        size = kwargs.get('size',12)
        width = kwargs.get('width',self.width+self.margin) # go all the way to right edge
        height = kwargs.get('height',self.height+self.margin)
        hop = (1.*height/size)
        alpha = .5
        self.can.setFont(self.header_font,self.header_size)
        self.can.rotate(90)
        self.can.drawCentredString(height/2, -2*self.header_size, "The Prime Bunnies")
        y = -2*self.header_size-10
        self.can.setFillColor(colors.Color(0,0,0,.2))
        start = 10+1*hop
        self.can.circle(start,-width+2*self.header_size, hop/2, stroke=0,fill=1)
        self.can.setStrokeColor(colors.Color(0,0,0,.1))
        # bottom circles for filling in prime numbers / prime factors
        for i in range(0,size+10):
            self.can.circle(i*hop+start,-width+2*self.header_size, hop/2, stroke=1,fill=0)
        self.can.setLineWidth(1)
        self.can.setStrokeColor(colors.Color(0,0,0,alpha))
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                  37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                  79, 83, 89, 97, 101, 103, 107, 109, 113,
                  127, 131, 137, 139, 149, 151, 157, 163,
                  167, 173, 179, 181, 191, 193, 197, 199]:
            if p>size*2:
                break
            self.can.setDash([1,2])
            #  dash breaks down for large p
            #  self.can.setDash([1,1]*p+[p,1])
            phop = p*hop
            for i in range(0,size+1):
                self.can.bezier(i*phop+start ,-width+2*self.header_size+hop/2,
                            (i+.25)*phop+start ,-width+2*self.header_size+hop/2+phop*.9,
                            (i+.75)*phop+start ,-width+2*self.header_size+hop/2+phop*.9,
                            (i+1)*phop+start ,-width+2*self.header_size+hop/2)


    def times_table(self,**kwargs):
        # layout a times table with options for prime grouping of dots, prime factors, ...
        size = kwargs.get('size',10)
        base = kwargs.get('base',10)
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height+self.margin)
        font_alpha = kwargs.get('font_alpha',1) # set to between 0-1 for stroke alpha in the numbers
        font_alpha_top = kwargs.get('font_alpha_top',font_alpha) # set to between 0-1 for stroke alpha in the top numbers
        x = 0; y = height
        self.can.setFont(self.header_font,self.header_size)
        self.can.drawCentredString(width/2, y, "Ye Olde Times Table")
        y -= self.header_size-10
        if self.verbose:
            self.can.setFont(self.header_font, self.header_size-10)
            self.can.drawCentredString(width/2, y, "and prime factorization")
            y -= self.header_size-20
            self.can.setFont(self.normal_font, self.normal_size)
            dyl = self.normal_size + 2
            prompts = ["Look for patterns.",
                       "Circle all of the prime numbers.",
                       "Shade in all of the numbers that are the product of 2 primes.",
                       "Play 'cut out a prime factor.' ",
                       "How interesting! The perfect squares seem to be separated by the odd integers.",
                       "Write each number as the product of primes."]
            for prompt in prompts:
                y-=dyl
                self.can.drawString(x+width/10,y,prompt)
        font_size = 220/size
        font_size = max(12,font_size*base/10)
        self.can.setFont(self.normal_font, font_size)
        dx = dy = width/(size+1)
        x += dx
        ylist = [y-dy/2+font_size/2-2]
        for c in range(1,size+1):
            cy = y-c*dy
            xlist=[x-dx/2]
            for r in range(1,1+size):
                cx = x+(r-1)*dx
                if r<=size and c<=size:
                    self.can.saveState()
                    self.can.translate(cx-dx/2+3,cy+dy/2+font_size/2-3)
                    row_cuts = col_cuts = box = factors = 0
                    if random.randint(1,9)<=self.verbose:  box=1
                    else:  box = 0
                    if random.randint(1,9)<=self.verbose:  row_cuts=col_cuts=1
                    else:  row_cuts=col_cuts = 0
                    if random.randint(1,9)<=self.verbose:  factors=1
                    else: factors = 0
                    #dot_grid(self.can,r,c,size,size,dx-6,dy-6,col_cuts=col_cuts,row_cuts=row_cuts,box=box,factors=factors)
                    DotGrid(self.can,r,c,size,size,dx-6,dy-6,col_cuts=col_cuts,row_cuts=row_cuts,box=box,factors=factors,base=base)
                    self.can.restoreState()
                    if font_alpha or font_alpha_top:
                        p = c*r
                        if base!=10:
                            if not Bases:
                                raise Exception("`pip install bases.py` to use a base other than 10.")
                            p = Bases.toBase(p,base)
                        if r == 1 or c == 1:
                            self.can.setFillColor( colors.Color(0,0,0,font_alpha_top))
                        else:
                            self.can.setFillColor( colors.Color(0,0,0,font_alpha))

                        self.can.drawCentredString(cx,cy,"%s"%(p,))
                    xlist.append(cx+dx/2)
                ylist.append(cy-dy/2+font_size/2-2)

        self.can.setStrokeColor(colors.Color(21/255., 21/255., 21/255.,0.05))
        self.can.grid(xlist, ylist)

    def counting_table(self,**kwargs):
        size = kwargs.get('size',10)
        base = kwargs.get('base',10)
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        height = kwargs.get('height',self.height)
        font_alpha = kwargs.get('font_alpha',1) # set to between 0-1 for stroke alpha in the numbers
        font_alpha_top = kwargs.get('font_alpha_top',1) # set to between 0-1 for stroke alpha in top numbers
        x = 0; y = height-self.header_size
        self.can.setFont(self.header_font,self.header_size)
        self.can.drawCentredString(width/2, y, "Counting Numbers")
        y -= self.header_size*1/2.

        font_size = 240/size
        font_size = max(12,font_size*base/10)
        #if base == 2: font_size/=2

        self.can.setFont(self.header_font,font_size)
        dx = dy = width/(size+1)
        x += dx
        xlist=[x-dx/2]
        for c in range(1,size+1):
            cx = x+(c-1)*dx
            ylist = [y-dy/2+font_size/2-2]
            xlist.append(cx+dx/2)
            for r in range(0,size):
                cy = y-(r+1)*dy
                p = size*r+c
                if base!=10:
                    if not Bases:
                        raise Exception("`pip install bases.py` to use a base other than 10.")
                    p = Bases.toBase(p,base)
                if r == 0:
                    self.can.setFillColor( colors.Color(0,0,0,font_alpha_top))
                else:
                    self.can.setFillColor( colors.Color(0,0,0,font_alpha))

                self.can.drawCentredString(cx,cy,"%s"%(p,))
                ylist.append(cy-dy/2+font_size/2-2)

        self.can.setStrokeColor(colors.Color(21/255., 21/255., 21/255.,0.1))
        self.can.grid(xlist, ylist)

    def pythagorean_theorem(self,**kwargs):
        a = kwargs.get('a',3)
        b = kwargs.get('b',4)
        a2 = kwargs.get('a2',5)
        b2 = kwargs.get('b2',12)

        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        x = 0; y = height-self.header_size
        self.can.setFont(self.header_font,self.header_size)
        self.can.drawCentredString(width/2, y, "The Pythagorean Theorem")
        y -= self.header_size*1/2.
        self.can.setFont(self.normal_font, self.normal_size)
        if self.verbose:
            dyl = self.normal_size + 2
            prompts = ["Behold!",
                       "Make and match the triangles.",
                       "Make up labels and write an algebraic proof.",
                       "Find and draw the Pythagorean triplet that fits in the lower grids.",
            ]
            for prompt in prompts:
                y-=dyl
                self.can.drawString(x+self.margin,y,prompt)
        swidth = self.width/2.-self.margin/2
        pythag = PythagoreanTheorem(a,b,size=swidth)
        drawing = pythag.ab_square(show_grid=1,count_squares=1)
        y -= width/2 + self.header_size/2
        drawing.drawOn(self.can,x,y)
        drawing = pythag.c_square(show_grid=1,count_squares=1)
        x = width/2 + self.margin/2
        drawing.drawOn(self.can,x,y)


class CountingTable(reportlab.platypus.flowables.Flowable):

    def __init__(self,xoffset=0,N=10,base=10,size=800,font = "Helvetica-Bold",font_size=None):
        self.xoffset = xoffset
        self.N = N
        self.base = base
        self.size = size
        self.font = font
        self.font_size = font_size or 24

    def wrap(self,w,h):
        return (self.size, self.size)

    def draw(self):
        x = self.xoffset
        y = self.size
        self.canv.setFont(self.font,self.font_size)
        dx = dy = 1.*self.size/self.N
        for c in range(1,self.N+1):
            cx = x+(c-1)*dx + dx/2
            for r in range(0,self.N):
                cy = y-(r+1)*dy + dy/2 - self.font_size/2.
                p = self.N*r+c
                if self.base!=10:
                    if not Bases:
                        raise Exception("`pip install bases.py` to use a base other than 10.")
                    p = Bases.toBase(p,self.base)
                self.canv.drawCentredString(cx,cy,"%s"%(p,))

        self.canv.setStrokeColor(colors.Color(21/255., 21/255., 21/255.,0.05))
        glist = [x*dx for x in range(self.N+1)]
        self.canv.grid(glist, glist)


############ utilities ###################

class PythagoreanTheorem(object):
    def __init__(self,a,b,size,
                 grid_color =  colors.Color(236/255., 236/255., 236/255.,1),
                 stroke_color =  colors.Color(20/255., 20/255., 20/255.,1),
                 fill_color =  colors.Color(255/255., 255/255., 255/255.,0)):
        self.a = a
        self.b = b
        self.size = size
        self.grid_color = grid_color
        self.stroke_color = stroke_color
        self.fill_color = fill_color

    def ab_square(self,**kwargs):
        """return a drawing  the a^2+b^2 part of the pythagorean"""
        show_grid = kwargs.get('show_grid',0)
        count_squares = kwargs.get('count_squares',0)
        drawing = Drawing(self.size,self.size)
        apb = self.a + self.b
        step = 1.*self.size / apb
        if show_grid:
            for i in range(1,apb):
                drawing.add(Line(0,i*step,self.size,i*step, strokeColor=self.grid_color))
                drawing.add(Line(i*step,0,i*step,self.size, strokeColor=self.grid_color))
        drawing.add(Line(0,self.b*step,self.size,self.b*step, strokeColor=self.stroke_color))
        drawing.add(Line(self.a*step,0,self.a*step,self.size, strokeColor=self.stroke_color))
        drawing.add(Rect(0,0,self.size,self.size, fillColor=self.fill_color,strokeColor=self.stroke_color))
        return drawing

    def c_square(self,**kwargs):
        """return a drawing  the a^2+b^2 part of the pythagorean"""
        show_grid = kwargs.get('show_grid',0)
        count_squares = kwargs.get('count_squares',0)
        drawing = Drawing(self.size,self.size)
        angle = math.atan(1.*self.a/self.b) * 180 / math.pi
        print("fotate:",angle)
        drawing.rotate(angle)
        c = math.pow(self.a*self.a+self.b*self.b,0.5)
        print("c:",c)
        step = 1.*self.size / (self.a+self.b)
        if show_grid:
            i = 1
            while i <= c:
                drawing.add(Line(0,i*step,self.size,i*step, strokeColor=self.grid_color))
                drawing.add(Line(i*step,0,i*step,self.size, strokeColor=self.grid_color))
                i += 1
        drawing.add(Rect(self.a,0,c,c, fillColor=self.fill_color,strokeColor=self.stroke_color))
        #drawing.rotate(-angle)
        drawing.add(Rect(0,0,self.size,self.size, fillColor=self.fill_color,strokeColor=self.stroke_color))
        return drawing

class PrimeFactors(object):
    def __init__(self,num,base=10):
        self.base = base
        self.factors = {}
        n = 2
        while num > 1:
            while num % n == 0:
                num /= n
                if n in self.factors:
                    self.factors[n] += 1
                else:
                    self.factors[n] = 1
            n += 1

    def __str__(self):
        fs = list(self.factors.keys())
        fs.sort()
        s = ''
        # TODO: superscript option
        for f in fs:
            for e in range(self.factors[f]):
                if self.base!=10:
                    if not Bases:
                        raise Exception("`pip install bases.py` to use a base other than 10.")
                    fb = Bases.toBase(f,self.base)
                else:
                    fb = f
                s += '%s,'%fb
        return s[:-1]


class DotGrid(object):
    def __init__(self,can,x,y,X,Y,w,h,**kwargs): #row_cuts=0,col_cuts=0,box=0,factors=0):
        #print "dg:",x,y,X,Y
        col_cuts = kwargs.get('col_cuts',0)
        row_cuts = kwargs.get('row_cuts',0)
        factors = kwargs.get('factors',0)
        box = kwargs.get('box',0)
        base = kwargs.get('base',10)
        self.W = 1.*w; self.H = 1.*h
        self.dx = self.W/X
        self.dy = self.H/Y
        drawing = self.add_dots(x,y,X,Y,row_cuts=row_cuts,col_cuts=col_cuts,box=box)
        #drawing.scale(w/self.W,h/self.H)
        drawing.wrapOn(can,w,h)
        drawing.drawOn(can,0,0)
        if factors:
            self.add_factors(can,x,y,w,h,base)

    def add_dots(self,x,y,X,Y,row_cuts,col_cuts,box):
        dx = self.dx
        dy = self.dy

        drawing = Drawing(self.W,self.H)

        for j in range(1,Y+1):
            for i in range(1,X+1):
                if i<=x and j<=y:
                    stroke_color =  colors.Color(211/255., 211/255., 211/255.,1)
                    fill_color =  colors.Color(180/255., 180/255., 180/255.,1)
                else:
                    stroke_color =  colors.Color(241/255., 241/255., 241/255.,1)
                    fill_color =  colors.Color(241/255., 241/255., 241/255.,1)
                ddx = self.dot_grid_delta(i,x)*1
                ddy = self.dot_grid_delta(j,y)*1
                #drawing.add(Circle(i*dx-dx/2+ddx, -j*dy-ddy, max((dx/2-1), 1), fillColor=fill_color,strokeColor=None))
                drawing.add(Circle(i*dx-dx/2+ddx, -j*dy-ddy+int(dy)/2, max((dx/2-1), 1), fillColor=fill_color,strokeColor=None))

                if x>i>1 and col_cuts and sorted(PrimeFactors(x).factors.keys())[-1] in PrimeFactors(i).factors:
                    drawing.add(Line(i*dx+ddx/2,-j*dy-dy/2-1,i*dx+ddx/2,-j*dy+dy/2+1, strokeColor=colors.white))
                    drawing.add(Line(i*dx+ddx/2,-j*dy-dy/2-1,i*dx+ddx/2,-j*dy+dy/2+1, strokeColor=stroke_color))
                if y>j>1 and row_cuts and  sorted(PrimeFactors(y).factors.keys())[-1] in  PrimeFactors(j).factors.keys():
                    drawing.add(Line(i*dx-dx,-j*dy-dy/2-ddy/2,i*dx,-j*dy-dy/2-ddy/2, strokeColor=colors.white))
                    drawing.add(Line(i*dx-dx,-j*dy-dy/2-ddy/2,i*dx,-j*dy-dy/2-ddy/2, strokeColor=stroke_color))

        if box and x>1 and y>1:
            i = sorted(PrimeFactors(x).factors.keys())[-1]
            j = sorted(PrimeFactors(y).factors.keys())[-1]
            fill_color =  colors.Color(21/255., 21/255., 21/255.,0.05)
            drawing.add(Rect(0,-dy/2,i*dx-dx/4,-j*dy, fillColor=fill_color,strokeColor=None))
        return drawing

    def add_factors(self,can,x,y,w,h,base):
        fill_color =  colors.Color(21/255., 21/255., 21/255.,.7)
        can.setFillColor(fill_color)
        can.setFont("Times-Roman", 8)
        s = '%s'%PrimeFactors(x*y,base)
        if len(s)==1: s= ''
        textWidth = stringWidth(s, fontName="Times-Roman", fontSize=8)
        can.drawString(w-textWidth+self.dx-1,-h-self.dy,s) # right

    def dot_grid_delta(self,i,x):
        if x==1: return 0
        # group composite number in sets of largest prime
        group = sorted(PrimeFactors(x).factors.keys())[-1]
        if group == 2:
            ret = -1 + 2*(i%2)
            if x >= 4:    ret +=  1*(i>4) - 1*(i<=4)
            if x >= 8:    ret +=  1*(i>8) - 1*(i<=8)
            if x >= 12:   ret +=  1*(i>12) - 1*(i<=12)
            return ret/2
        if group == 3:
            return {1:1,2:0,0:-1}[i%3]
        if group == 5:
            return {1:2,2:1,3:0,4:-1,0:-2}[i%5]
        if group == 7:
            ret = (i>7) - (i<=7)
            if x>=14:
                ret += (i>14) - (i<=14)
            return ret
        if group == 11:
            ret = (i>11) - (i<=11)
            if x>11:  ret += (i>11) - (i<=11)
            return ret
        if group == 13:
            ret = (i>13) - (i<=13)
            if x>13:  ret += (i>13) - (i<=13)
            return ret
        return 0

################### tests and demos #####################
def test_flow_canvas():

    canv = canvas.Canvas('test_flow_canvas.pdf', pagesize=letter)
    w,h = letter
    styles = reportlab.lib.styles.getSampleStyleSheet()

    ptext = "<font size=14 color='#FF00FF'>Test Flow</font>"
    head = reportlab.platypus.Paragraph(ptext, styles["Normal"])
    head.wrapOn(canv,w,h)
    head.drawOn(canv,10,h-100)
    t7 = CountingTable(N=7,size=7*inch/2.,font_size=0.01)
    tw7,th7 = t7.wrapOn(canv,w,h)
    y = h-360-th7
    x = 10
    t7.drawOn(canv,x,y)

    t3 = CountingTable(N=3,size=3*inch/2.)
    tw3,th3 = t3.wrapOn(canv,w,h)
    y = h-360-th3
    x = 10
    t3.drawOn(canv,x,y)

    t4 = CountingTable(N=4,size=4*inch/2.)
    tw4, th4 = t4.wrapOn(canv,w,h)
    y = h-360-th7
    x = 10+tw3
    t4.drawOn(canv,x,y)

    y = h-360-th3
    x = 10+th3
    angle = math.atan(4./3) * 180 / math.pi
    canv.saveState()
    canv.translate(x,y)
    t7.drawOn(canv,0,0)
    canv.restoreState()
    canv.saveState()
    x = 10+th7
    canv.translate(x,y)
    canv.rotate(angle)
    canv.setFillColor(colors.white)
    canv.rect(0, 0,5*inch/2.,5*inch/2.,stroke=0,fill=1)
    t5 = CountingTable(N=5,size=5*inch/2.)
    canv.setFillColor(colors.black)
    tw5,th5 = t5.wrapOn(canv,w,h)
    t5.drawOn(canv,0,0)
    canv.restoreState()
    ptext = "<font size=14 color='#FF00FF'>Test Flow</font>"
    foot = reportlab.platypus.Paragraph(ptext, styles["Normal"])
    foot.wrapOn(canv,w,h)
    foot.drawOn(canv,100,10)
    canv.save()

def test_flow():
    elements=[]
    doc = reportlab.platypus.SimpleDocTemplate("test_flow.pdf",pagesize=letter,topMargin=10,leftMargin=10)
    styles = reportlab.lib.styles.getSampleStyleSheet()
    spacer = reportlab.platypus.Spacer(0, 0.25*inch)

    ptext = "<font size=12 color='#FF00FF'>Test Flow</font>"
    elements.append(reportlab.platypus.Paragraph(ptext, styles["Normal"]))
    elements.append(spacer)

    t = CountingTable(N=7,size=2*inch)
    elements.append(t)
    t = CountingTable(N=8,size=3*inch,xoffset=3*inch)
    elements.append(t)
    elements.append(spacer)

    ptext = "<font size=12>Done with Test</font>"
    elements.append(reportlab.platypus.Paragraph(ptext, styles["Normal"]))

    doc.build(elements)

def test_draw():
    sheet = Sheet('draw',margin=0,verbose=0)
    sheet.can.setFillColor('red')
    sheet.can.circle(0,200, 100, stroke=1,fill=1)
    d = Drawing(200, 200)
    d.add(Rect(100, 0, 100, 120, fillColor=colors.yellow,strokeColor=None))
    d.rotate(-45)
    d.add(Rect(100, 105, 120, 130,fillColor=colors.blue,strokeColor=None))
    #d.rotate(45)
    d.add(String(150,100, 'Hello World', fontSize=18, fillColor=colors.red))
    #d.scale(0.5,0.5)
    d.wrapOn(sheet.can,200,200)
    d.drawOn(sheet.can,0,600)
    sheet.save()

def test():
    #sheet = Sheet('brownies',margin=20,verbose=0)
    #sheet.sharing_brownies()
    #sheet.save()
    #return
    sheet = Sheet('pythagorean',margin=20,verbose=0)
    sheet.pythagorean_theorem(a=3,b=4)
    sheet.save()
    print("saved verbose 9 pythagorean to %s"%DOUT)

def times_tables():
    for s in [2,4,6,8,10,12,16]:
        font_alpha=0.0
        font_alpha_top=0.3
        fout = 'times_table_s%s_b%s_fa%0.1f_fat%0.1f'%(s,s,font_alpha,font_alpha_top)
        sheet = Sheet(fout,verbose=0)
        sheet.times_table(size=s,base=s,font_alpha=font_alpha,font_alpha_top=font_alpha_top)
        sheet.save()
        print("saved to %s/%s"%(DOUT,fout))

def counting():
    for b in [2,4,6,8,10,12,16]:
        if b == 2:
            s = 4
        else:
            s = b
        font_alpha=0.3
        font_alpha_top=0.3
        fout = 'counting_s%s_b%s_fa%0.1f_fat%0.1f'%(s,b,font_alpha,font_alpha_top)
        sheet = Sheet(fout,verbose=0)
        sheet.counting_table(size=s,base=b,font_alpha=font_alpha,font_alpha_top=font_alpha_top)
        sheet.save()
        print("saved to %s/%s"%(DOUT,fout))

def bunnies():
    for N in [10,25,50,100]:
        sheet = Sheet('prime_bunnies_%d'%N,verbose=9,margin=10)
        sheet.prime_bunnies(size=N)
        sheet.save()
        print("saved prime bunnues %d to %s"%(N,DOUT))



if __name__ == "__main__":
    # todo: use argparse
    DOUT = "/home/jameyer/Write/Math"
    test()
    #times_tables()
    #counting()
    #bunnies()
    #test_draw()
    #test_flow_canvas()
