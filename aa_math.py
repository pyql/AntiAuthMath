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
from reportlab.pdfbase.pdfmetrics import stringWidth
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
    Bases = None #


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

    def graph_paper(self,**kwargs):
        """put graph paper at current location
           TODO: Add base and stroke options scales """
        lines = kwargs.get('lines',50)
        color = kwargs.get('color',colors.Color(21/255., 67/255., 234/255.,0.08))
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        self.can.setStrokeColor(color)
        xlist = [x*(width/lines) for x in range(0,lines+1)]
        ylist = [x*(width/lines) for x in range(0,1+int(lines*height/width))]
        self.can.grid(xlist, ylist)


    def times_table(self,**kwargs):
        # layout a times table with options for prime grouping of dots, prime factors, ...
        size = kwargs.get('size',10)
        base = kwargs.get('base',10)
        width = kwargs.get('width',self.width)
        height = kwargs.get('height',self.height)
        show_products = kwargs.get('show_products',1) # set to between 0-1 for stroke alpha in the numbers
        x = 0; y = height-self.header_size
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
        font_size = 240/size
        font_size = max(12,font_size*base/10)
        self.can.setFont(self.normal_font, font_size)
        self.can.setFillColor( colors.Color(0,0,0,show_products))
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
                    dot_grid(self.can,r,c,size,size,dx-6,dy-6,
                             col_cuts=col_cuts,row_cuts=row_cuts,box=box,factors=factors)
                    self.can.restoreState()
                    if show_products: # or (1 in [c,r]):
                        p = c*r
                        if base!=10:
                            if not Bases:
                                raise Exception("`pip install bases.py` to use a base other than 10.")
                            p = Bases.toBase(p,base)
                        self.can.drawCentredString(cx,cy,"%s"%(p,))
                    xlist.append(cx+dx/2)
                ylist.append(cy-dy/2+font_size/2-2)

        self.can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,0.05))
        self.can.grid(xlist, ylist)

############ utilities ###################


def pythagoran(can,
               a=3,
               b=4,
               width=None,
               height=None,
):
    """A solved 3-4-5 followed by a pair of blank 17x17 grids.
"""
    margin=40
    can = canvas.Canvas('/home/jameyer/Write/Math/pythagoras.pdf', pagesize=letter)
    width,height = [x-2*margin for x in letter]
    can.setFont("Times-Roman", 30)
    y = height+margin
    x = margin
    can.drawCentredString(width/2,y,"Pythagorean Theorem")
    # define the color of the triangles from upper left clockwise
    ct1 = colors.Color(252/255., 108/255., 13/255.,1)
    ct2 = colors.Color(198/255., 252/255., 13/255.,1)
    ct3 = colors.Color(0/255., 174/255., 239/255.,1)
    ct4 = colors.Color(222/255., 61/255., 252/255.,1)
    y -= 40
    spacing = width/20
    sqwidth = (width-spacing)/2 # the width of a square, 2 across
    s = 7

    # start in upper left with a 3-4-5 proof
    # first column divides up in 3 and 4 squares
    can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,1))
    #can.setFillColor(colors.Color(21/255., 67/255., 234/255.,0.01))
    can.rect(x, y-sqwidth,sqwidth,sqwidth,stroke=1,fill=0) # outline the square
    # tone down the text
    can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,0.1))
    can.setFillColor(colors.Color(21/255., 67/255., 234/255.,0.1))
    xlist = [x+i*(sqwidth/s) for i in range(s+1)]
    ylist = [y-i*(sqwidth/s) for i in range(s+1)]
    can.grid(xlist, ylist)
    can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,1))
    can.line(x+3*(sqwidth/s),y,x+3*(sqwidth/s),y-7*sqwidth/s)
    can.line(x,y-3*(sqwidth/s),x+7*sqwidth/s,y-3*(sqwidth/s))

    # color triangles
    p = can.beginPath()
    p.moveTo(x+0*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+0*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+0*(sqwidth/s),y-7*(sqwidth/s))
    can.setFillColor(ct1)
    can.drawPath(p,fill=1,stroke=0)

    p = can.beginPath()
    p.moveTo(x+3*(sqwidth/s),y)
    p.lineTo(x+7*(sqwidth/s),y)
    p.lineTo(x+7*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y)
    can.setFillColor(ct2)
    can.drawPath(p,fill=1,stroke=0)

    p = can.beginPath()
    p.moveTo(x+0*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+0*(sqwidth/s),y-7*(sqwidth/s))
    can.setFillColor(ct3)
    can.drawPath(p,fill=1,stroke=0)

    p = can.beginPath()
    p.moveTo(x+3*(sqwidth/s),y)
    p.lineTo(x+7*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y)
    can.setFillColor(ct4)
    can.drawPath(p,fill=1,stroke=0)

    can.setFillColor(colors.Color(21/255., 67/255., 234/255.,0.1))
    n = 0
    for j in range(3):
        for i in range(3):
            n += 1
            can.drawCentredString(x+(i+0.5)*(sqwidth/s),y-(j+0.75)*(sqwidth/s), "%d"%n)
    n = 0
    for j in range(3,7):
        for i in range(3,7):
            n += 1
            can.drawCentredString(x+(i+0.5)*(sqwidth/s),y-(j+0.75)*(sqwidth/s), "%d"%n)
    # second column
    x += sqwidth + spacing
    can.rect(x, y-sqwidth,sqwidth,sqwidth,stroke=1,fill=0) # outline the square
    can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,0.1))
    xlist = [x+i*(sqwidth/s) for i in range(s+1)]
    ylist = [y-i*(sqwidth/s) for i in range(s+1)]
    can.grid(xlist, ylist)
    can.setStrokeColor( colors.Color(21/255., 21/255., 21/255.,1))
    can.line(x+3*(sqwidth/s),y,x+7*(sqwidth/s),y-3*sqwidth/s)
    can.line(x+7*(sqwidth/s),y-3*sqwidth/s,x+4*(sqwidth/s),y-7*sqwidth/s)
    can.line(x+4*(sqwidth/s),y-7*sqwidth/s,x+0*(sqwidth/s),y-4*sqwidth/s)
    can.line(x+0*(sqwidth/s),y-4*sqwidth/s,x+3*(sqwidth/s),y)
    # color triangles
    p = can.beginPath()
    p.moveTo(x,y)
    p.lineTo(x+3*(sqwidth/s),y)
    p.lineTo(x,y-4*(sqwidth/s))
    p.lineTo(x,y)
    can.setFillColor(ct1)
    can.drawPath(p,fill=1)

    p = can.beginPath()
    p.moveTo(x+3*(sqwidth/s),y)
    p.lineTo(x+7*(sqwidth/s),y)
    p.lineTo(x+7*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+3*(sqwidth/s),y)
    can.setFillColor(ct2)
    can.drawPath(p,fill=1)

    p = can.beginPath()
    p.moveTo(x+7*(sqwidth/s),y-3*(sqwidth/s))
    p.lineTo(x+7*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+4*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+7*(sqwidth/s),y-3*(sqwidth/s))
    can.setFillColor(ct3)
    can.drawPath(p,fill=1)

    p = can.beginPath()
    p.moveTo(x+4*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+0*(sqwidth/s),y-7*(sqwidth/s))
    p.lineTo(x+0*(sqwidth/s),y-4*(sqwidth/s))
    p.lineTo(x+4*(sqwidth/s),y-7*(sqwidth/s))
    can.setFillColor(ct4)
    can.drawPath(p,fill=1)

    can.saveState()
    can.translate(x+3*(sqwidth/s),y)
    can.rotate(-36.86989827)
    p = can.beginPath()
    p.moveTo(0,0)
    p.lineTo(5*(sqwidth/s),0)
    p.lineTo(5*(sqwidth/s),-5*(sqwidth/s))
    p.lineTo(0,-5*(sqwidth/s))
    p.lineTo(0,0)
    can.setStrokeColor( colors.Color(20/255., 21/255., 21/255.,0.1))
    can.setFillColor(colors.Color(255/255., 255/255., 255/255.,1))
    can.drawPath(p,fill=1)

    xlist = [i*(sqwidth/s) for i in range(6)]
    ylist = [-i*(sqwidth/s) for i in range(6)]
    can.grid(xlist, ylist)
    can.setFillColor(colors.Color(21/255., 67/255., 234/255.,0.1))
    n = 0
    for j in range(5):
        for i in range(5):
            n += 1
            can.drawCentredString(x*0+(i+0.5)*(sqwidth/s),y*0-(j+0.75)*(sqwidth/s), "%d"%n)
    can.restoreState()


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
    # TODO: superscript option
    for f in fs:
        for e in range(d[f]):
            s += '%sx'%f
    return s[:-1]

def dot_grid_delta(i,x):
    if x==1: return 0
    # group composite number in sets of largest prime
    group = sorted(prime_factors(x).keys())[-1]
    if group == 2:
        ret = -1 + 2*(i%2)
        if x >= 4:    ret +=  1*(i>4) - 1*(i<=4)
        if x >= 8:    ret +=  1*(i>8) - 1*(i<=8)
        return ret/2
    if group == 3:
        return {1:1,2:0,0:-1}[i%3]
    if group == 5:
        return {1:2,2:1,3:0,4:-1,0:-2}[i%5]
    if group == 7:
        ret = 2*(i>7) - 2*(i<=7)
        if x>14:
            ret = 2*(i>14) - 2*(i<=14)
        return ret
    return 0

def dot_grid(can,x=2,y=3,X=10,Y=10,w=40,h=40,col_cuts=0,row_cuts=0,box=0,factors=0):
    #  make as a large drawing, scale and place on canvas
    W = 180; H = 180
    draw = Drawing(W,H)
    dx = W/X
    dy = H/Y
    for j in range(1,Y+1):
        for i in range(1,X+1):
            if i<=x and j<=y:
                stroke_color =  colors.Color(21/255., 21/255., 21/255.,0.2)
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.4)
            else:
                stroke_color =  colors.Color(21/255., 21/255., 21/255.,0.05)
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.05)
            ddx = dot_grid_delta(i,x)*2
            ddy = dot_grid_delta(j,y)*2
            draw.add(Circle(i*dx-dx/2+ddx, -j*dy-ddy, max((dx/2-1), 1), fillColor=fill_color,strokeColor=None))
            if x>i>1 and col_cuts and sorted(prime_factors(x).keys())[-1] in prime_factors(i):
                draw.add(Line(i*dx+ddx/2,-j*dy-dy/2-1,i*dx+ddx/2,-j*dy+dy/2+1, strokeColor=stroke_color))
            if y>j>1 and row_cuts and  sorted(prime_factors(y).keys())[-1] in  prime_factors(j).keys():
                draw.add(Line(i*dx-dx,-j*dy-dy/2-ddy,i*dx,-j*dy-dy/2-ddy, strokeColor=stroke_color))
            if x>1 and box and  i == sorted(prime_factors(x).keys())[-1] and  y>1 and  j == sorted(prime_factors(y).keys())[-1]:
                fill_color =  colors.Color(21/255., 21/255., 21/255.,0.07)
                #can.setFillColor(fill_color)
                #can.rect(dx/6,-j*dy-dy/3,i*dx-dx/6,j*dy-dy/6,fill=1,stroke=0)
                draw.add(Rect(dx/12,-j*dy-dy/3,i*dx-dx/4,j*dy-dy/6-ddy, fillColor=fill_color,strokeColor=None))
    draw.scale(w/W,h/H)
    draw.wrapOn(can,w,h)
    draw.drawOn(can,0,0)

    if factors:
        fill_color =  colors.Color(21/255., 21/255., 21/255.,.7)
        can.setFillColor(fill_color)
        can.setFont("Times-Roman", 8)
        s = prime_factor_str(x*y)
        if len(s)==1: s= ''
        textWidth = stringWidth(s, fontName="Times-Roman", fontSize=8)
        can.drawString(w-textWidth,-h,s) # right

################### tests and demos #####################
def test_draw():
    sheet = Sheet('draw',margin=0,verbose=0)
    sheet.can.setFillColor('red')
    sheet.can.circle(0,200, 100, stroke=1,fill=1)
    d = Drawing(200, 200)
    d.add(Circle(0, 0, 100, fillColor=colors.yellow))
    d.add(String(150,100, 'Hello World', fontSize=18, fillColor=colors.red))
    #d.scale(0.5,0.5)
    d.wrapOn(sheet.can,200,200)
    d.drawOn(sheet.can,0,600)
    sheet.save()

def test():
    sheet = Sheet('graph_paper',margin=0,verbose=0)
    margin = 10
    sheet.can.saveState()
    sheet.can.translate(margin,margin)
    sheet.graph_paper(lines=50,width=sheet.width-2*margin,height=sheet.height-2*margin)
    sheet.graph_paper(lines=10,width=sheet.width-2*margin,height=sheet.height-2*margin)
    sheet.graph_paper(lines=5,width=sheet.width-2*margin,height=sheet.height-2*margin)
    sheet.can.restoreState()
    sheet.save()
    print("save gp")
    sheet = Sheet('times_table_v9',margin=margin,verbose=9)
    sheet.times_table()
    sheet.save()
    print("saved verbose 9 times_table to %s"%DOUT)
    sheet = Sheet('times_table_v3',margin=margin,verbose=3)
    sheet.times_table(size=12)
    sheet.save()
    print("saved verbose 3 times_table to %s"%DOUT)
    sheet = Sheet('times_table_empty',margin=margin)
    sheet.times_table(show_products=0.)
    sheet.save()
    print("saved empty times_table to %s"%DOUT)
    sheet = Sheet('times_table',margin=margin)
    sheet.times_table()
    sheet.save()
    print("saved verbose 0 times_table to %s"%DOUT)
    sheet = Sheet('times_table_b12',margin=margin)
    sheet.times_table(size=12,base=12)
    sheet.save()
    print("saved verbose 0 base 12 times_table to %s"%DOUT)


if __name__ == "__main__":
    # todo: use argparse
    import platform
    DOUT = "/home/jameyer/Write/Math"
    psystem = platform.system()
    #print("%s system detected"%psystem)
    if psystem == "Windows":
        DOUT = ''
    test()
    #test_draw()
