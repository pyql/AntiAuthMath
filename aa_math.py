"""
Sheet Ideas:
    a line intersecting parallel lines to table of polygon angles
    functions, slopes to equation of line, present higher order curves and ask for slope(x): make a table, graph.
    fast math tables and proofs
    rotate, reflect, and resize
    sums to areas as integrals
    root 2 is irrational graphically and algebraically
    measures: how large the earth, how far the star, how tall the tree
"""

import math
import os
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.graphics.shapes import Line, Rect, Polygon, Drawing, Group, String, Circle, Wedge
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Table,TableStyle, Image, PageBreak, Frame
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch


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
    def __init__(self,flavor='graph_paper',**kwargs):
        """ Init a Canvas, set defaults and dispatch."""
        self.margin = kwargs.get('margin',50)
        self.verbose = kwargs.get('verbose',0) # verbose is from 0-9 with 9 most solved
        fout=kwargs.get('fout',flavor)
        if self.verbose: fout += '_k%s'%self.verbose
        if DOUT:   fout = os.path.join(DOUT,'%s'%(fout,))
        fout += '.pdf'
        self.can = canvas.Canvas(fout, pagesize=letter)
        self.width, self.height = [x-2*self.margin for x in letter]
        self.x_center = self.margin + self.width/2
        self.x, self.y = self.margin, self.height + self.margin
        self.set_style(**kwargs)
        self.dispatch(flavor,**kwargs)
        self.can.save()

    def set_style(self,**kwargs):
        self.header_font, self.header_size = "Helvetica-Bold", 30
        self.normal_font, self.normal_size = "Helvetica", 10

    def dispatch(self,flavor='graph_paper',**kwargs):
        if flavor == 'graph_paper':
            return self.graph_paper(**kwargs)
        if flavor == 'times_table':
            return self.times_table(**kwargs)


    def graph_paper(self,**kwargs):
        """TODO: Add scales for levels of verbose"""
        num_lines = kwargs.get('num_lines',50)
        # make a stroke every 10
        self.can.setStrokeColor( colors.Color(21/255., 67/255., 234/255.,0.08))
        #self.can.setStrokeColor( colors.Color(1, 0, 0, 1) )
        xlist = [self.margin+x*(self.width/num_lines) for x in range(0,num_lines+1,10)]
        ylist = [self.margin+x*(self.width/num_lines) for x in range(0,1+int(num_lines*(self.height/self.width)),10)]
        self.can.grid(xlist, ylist)
        # make a stroke every 5
        self.can.setStrokeColor( colors.Color(21/255., 67/255., 234/255.,0.04))
        xlist = [self.margin+x*(self.width/num_lines) for x in range(0,num_lines+1,5)]
        ylist = [self.margin+x*(self.width/num_lines) for x in range(0,1+int(num_lines*(self.height/self.width)),5)]
        self.can.grid(xlist, ylist)
        # make a stroke every 1
        self.can.setStrokeColor( colors.Color(21/255., 67/255., 234/255.,0.1))
        xlist = [self.margin+x*(self.width/num_lines) for x in range(0,num_lines+1)]
        ylist = [self.margin+x*(self.width/num_lines) for x in range(1+int(num_lines*(self.height/self.width)))]
        self.can.grid(xlist, ylist)


    def times_table(self,**kwargs):
        # layout a times table with options for prime grouping of dots, prime factors, ...
        size = kwargs.get('size',10)
        x, y = self.x, self.y
        self.can.setFont(self.header_font,self.header_size)
        self.can.drawCentredString(self.x_center, self.y, "Ye Olde Times Table")
        if 0<self.verbose: # include all prompts for any verbose level
            y -= self.header_size-10
            self.can.setFont(self.header_font, self.header_size-10)
            self.can.drawCentredString(self.x_center, y, "and prime factorization")
            y -= self.header_size
            self.can.setFont(self.normal_font, self.normal_size)
            dyl = self.normal_size + 2
            self.can.drawString(self.margin,y,"Look for patterns.")
            y-=dyl
            self.can.drawString(self.margin,y,"Circle all of the prime numbers.")
            y-=dyl
            self.can.drawString(self.margin,y,"Play 'cut out a prime factor and write it down'. ")
            y-=dyl
            self.can.drawString(self.margin,y," As shown: Cut any of the 12 dots in half to get 2 copies of a 2 by 3 prime grid. And behold: 12 is prime factored as 2x2x3")
            y-=dyl
            self.can.drawString(self.margin,y," Also shown: The 16 dot square takes 2 cuts to get 2x2 copies of a 2 by 2 grid. And behold: 16 is prime factored as 2x2x2x2.")
            y-=dyl
            self.can.drawString(self.margin,y,"Shade in all of the numbers that are the products of 2 primes as shown for 15.")
            y-=dyl
            self.can.drawString(self.margin,y,"How interesting! The perfect squares seem to be separated by the odd integers!")
            y-=dyl
            self.can.drawString(self.margin,y,"Write each compound number as the product of primes.")

        else:
            y -= self.margin
        font_size = 240/size
        self.can.setFont(self.normal_font, font_size)
        dx = dy = self.width/(size-1)
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
                    #if master and r in [2,3,5,7] and c in [2,3,5,7]:  box=1
                    if self.verbose and r*c in [15]:  box=1
                    else:
                        box = 0
                    if self.verbose and  ((r == 6 and c == 2) or (r==4 and c==3) or (r==c==4)):  col_cuts=1
                    else: col_cuts = 0
                    if self.verbose and  ((r == 2 and c == 6) or (r==3 and c==4) or (r==c==4)):  row_cuts=1
                    else: row_cuts = 0
                    if self.verbose and  r*c==40:  factors=1
                    if self.verbose > 5: factors = 1
                    else: factors = 0
                    dot_grid(self.can,r,c,size,size,dx-6,dy-6,
                             col_cuts=col_cuts,row_cuts=row_cuts,box=box,factors=factors)
                    self.can.restoreState()
                    self.can.drawCentredString(cx,cy,"%d"%(c*r))
                    xlist.append(cx+dx/2)
                ylist.append(cy-dy/2+font_size/2-2)

        self.can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,0.1))
        self.can.grid(xlist, ylist)


def prime_factors(num):
    factors = {}
    n = 2
    while num != 1:
        while num % n == 0:
            num /= n
            if n in factors:
                factors[n] += 1
            else:
                factors[n] = 1
        n += 1
    return factors


def prime_factor_str(n):
    if n==1: return ''
    d = prime_factors(n)
    fs = list(d.keys())
    fs.sort()
    s = ''
    for f in fs:
        for e in range(d[f]):
            s += '%sx'%f
    return s[:-1]

def dot_grid_delta(i,x):
    if x==1: return 0
    # group composite number in sets of largest prime
    group = sorted(prime_factors(x).keys())[-1]
    if group == 2: # odd number move right, even right
        if x == 8: # ad = hoc
            return {1:0,2:-2,3:-1,4:-3,5:1,6:-1,7:0,8:-2,9:2,10:1}.get(i,0)
        else:
            return -1 + 2*(i%2)
    if group == 3:
        return {1:1,2:0,0:-1}[i%3]
    if group == 5:
        return {1:2,2:1,3:0,4:-1,0:-2}[i%5]
    return 0

def dot_grid(can,x=2,y=3,X=10,Y=10,w=40,h=40,col_cuts=0,row_cuts=0,box=0,factors=0):
    # make at a large scale and then shrink for antialiasing?
    dx = w/X
    dy = h/Y
    for j in range(1,Y+1):
        for i in range(1,X+1):
            if i<=x and j<=y:
                stroke_color =  colors.Color(21/255., 21/255., 21/255.,0.2)
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.4)
            else:
                stroke_color =  colors.Color(21/255., 21/255., 21/255.,0.05)
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.05)
            ddx = dot_grid_delta(i,x)
            ddy = dot_grid_delta(j,y)
            can.setStrokeColor(stroke_color)
            can.setFillColor(fill_color)
            can.circle(i*dx-dx/2+ddx, -j*dy-ddy, (dx/2-1) or 1, stroke=0,fill=1)
            if x>i>1 and col_cuts and sorted(prime_factors(x).keys())[-1] in prime_factors(i):
                can.setStrokeColor(colors.white)
                can.line(i*dx+ddx+dx/4,-j*dy-dy/2-1,i*dx+ddx+dx/4,-j*dy+dy/2+1)
                can.setStrokeColor(stroke_color)
                can.line(i*dx+ddx+dx/4,-j*dy-dy/2-1,i*dx+ddx+dx/4,-j*dy+dy/2+1)
            if y>j>1 and row_cuts and  sorted(prime_factors(y).keys())[-1] in  prime_factors(j).keys():
                can.setStrokeColor(colors.white)
                can.line(i*dx-dx,-j*dy-3*dy/4-ddy,i*dx,-j*dy-3*dy/4-ddy)
                can.setStrokeColor(stroke_color)
                can.line(i*dx-dx,-j*dy-3*dy/4-ddy,i*dx,-j*dy-3*dy/4-ddy)

            if x>1 and box and  i == sorted(prime_factors(x).keys())[-1] and  y>1 and  j == sorted(prime_factors(y).keys())[-1]:
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.07)
                can.setFillColor(fill_color)
                can.rect(dx/6,-j*dy-dy/3,i*dx-dx/6,j*dy-dy/6,fill=1,stroke=0)

    if factors:
        fill_color =  colors.Color(21/255., 21/255., 21/255.,.7)
        can.setFillColor(fill_color)
        can.setFont("Times-Roman", 8)
        s = prime_factor_str(x*y)
        textWidth = stringWidth(s, fontName="Times-Roman", fontSize=8)
        can.drawString(w-textWidth,-h-dy/2,s) # right


################### tests and demos #####################

def test():
    sheet = Sheet('times_table',verbose=0)
    print("saving times_table to %s"%DOUT)
    sheet = Sheet('times_table',verbose=9)
    print("saving verbose times_table to %s"%DOUT)
    sheet = Sheet('graph_paper')
    print("saving graph_paper to %s"%DOUT)

if __name__ == "__main__":
    # todo: use argparse
    import platform
    DOUT = "/home/jameyer/Write/Math"
    psystem = platform.system()
    print("%s system detected"%psystem)
    if psystem == "Windows":
        DOUT = ''
    test()
