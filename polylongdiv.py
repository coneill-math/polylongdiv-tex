import argparse
import os.path


__author__ = "Christopher O'Neill"
__version__ = "$0.1a $"
__date__ = "$Date: 2019/03/31 14:00:00 $"
__copyright__ = "Copyright (c) 2019 Christopher O'Neill"
__license__ = "MIT"




#######################################
########## Class definitions ##########
#######################################

class PolyLongDiv:
	def __init__(self, ax, bx, N):
		if N <= 1:
			raise ValueError("Invalid input!  Modular base n must be at least 2.")

		if ax == [] or ax == [0] or bx == [] or bx == [0]:
			raise ValueError("Invalid input!  Polynomials must be nonzero.")
		
		self.ax = ax
		self.bx = bx
		self.N = N
		
		self.ax = [i % self.N for i in self.ax]
		self.bx = [i % self.N for i in self.bx]
		self.ax = PolyLongDiv.prunepoly(self.ax)
		self.bx = PolyLongDiv.prunepoly(self.bx)
		
		self.divide()
	
	# performs division
	# stores results in mathlines
	def divide(self):
		
		self.da = len(self.ax) - 1
		self.db = len(self.bx) - 1
		
		blanks = ["" for i in self.ax]
		self.mathlines = [blanks[:]]
		self.mathlines = self.mathlines + [self.ax]
		
		invs = [i for i in range(N) if (i*self.bx[0]) % N == 1]
		if invs == []:
			raise ValueError("Error: leading coefficent of g is not a unit!")
		invleadcoef = invs[0]
		
		lpos = 0
		while lpos < len(self.mathlines[-1]) - self.db:
			coef = (invleadcoef*self.mathlines[-1][lpos]) % N
			self.mathlines[0][lpos] = coef
			
			self.mathlines = self.mathlines + [blanks[:]]
			self.mathlines = self.mathlines + [blanks[:]]
			for i in range(len(self.bx)):
				self.mathlines[-2][lpos+i] = (coef*self.bx[i]) % N
				
				if self.mathlines[-3][lpos+i] == "":
					self.mathlines[-3][lpos+i] = self.mathlines[1][lpos+i]
				
				self.mathlines[-1][lpos+i] = (self.mathlines[-3][lpos+i] - self.mathlines[-2][lpos+i]) % N
			
			while lpos < len(self.mathlines[-1]) - self.db and (self.mathlines[-1][lpos] == 0 or self.mathlines[-1][lpos] == ""):
				lpos = lpos + 1
		
		self.mathlines = [[(i if i != "" else 0) for i in l] for l in self.mathlines]
		
		self.qx = PolyLongDiv.prunepoly(self.mathlines[0][:(self.da-self.db+1)])
		self.rx = PolyLongDiv.prunepoly(self.mathlines[-1])
	
	def latexoutput(self, polyvar = "x"):
		strlines = []
		strlines = strlines + ["\\begin{array}{" + (self.db*"r@{}l@{}c@{}") + "rc@{}" + (self.da*"r@{}l@{}c@{}") + "r@{}}"]
		strlines = strlines + [(self.db*"&&&") + "&& " + PolyLongDiv.polytolatex(self.mathlines[0], self.db, polyvar=polyvar) + "\\\\"]
		strlines = strlines + ["\\cline{" + str(3*self.db + 2) + "-" + str(3*self.db + 3*self.da + 3) + "}\\rule{0pt}{2.5ex}"]
		# strlines = strlines + [(self.db*"&&&") + " & ".join([(("{}-{}" if l[i] < 0 else "{}+{}") + " & " + str(abs(l[i])) + " & x^" + str()) if l[i] == 0 else "" for i in range(len(l))]) + "\\\\"]
		
		for li in range(1,len(self.mathlines)):
			l = self.mathlines[li]
			
			if li % 2 == 1 and li > 1:
				startzeros = 0
				while startzeros < len(self.mathlines[li-1]) and self.mathlines[li-1][startzeros] == 0:
					startzeros = startzeros + 1
				
				endzeros = len(l)-1
				while endzeros > startzeros and self.mathlines[li-1][endzeros] == 0:
					endzeros = endzeros - 1
				
				startzeros = 3*startzeros
				endzeros = 3*endzeros
				
				if startzeros == 0:
					startzeros = startzeros + 0
				if endzeros == 3*(len(l) - 1):
					endzeros = endzeros - 1
				
				strlines = strlines + ["\\cline{" + str(3*self.db + startzeros + 3) + "-" + str(3*self.db + endzeros + 4) + "}\\rule{0pt}{2.5ex}"]
			
			strline = ""
			strline = strline + (PolyLongDiv.polytolatex(self.bx, polyvar=polyvar) + " & \\multicolumn{1}{|l@{}}{} " if li == 1 else ((self.db*"&&&") + " & "))
			
			# if li % 2 == 0 and li > 1:
			# 	strline = strline + "-"
			
			strline = strline + " & " + PolyLongDiv.polytolatex(l, polyvar=polyvar)
			# strline = strline + ((("" if l[0] == 1 else ("-" if l[0] == -1 else str(l[0]))) + " & x^" + str(len(l)-1)) if l[0] != 0 else " & ") + " & "
			# strline = strline + " & ".join([(("{}-{}" if l[i] < 0 else "{}+{}") + " & " + str(abs(l[i]) if abs(l[i]) != 1 else "") + " & " + ("x^" + str(len(l)-1-i) if i != len(l) - 2 else "x")) if l[i] != 0 else " &  & " for i in range(1,len(l))])
			strline = strline + " \\\\"
			strlines = strlines + [strline]
		
		strlines = strlines + ["\\end{array}"]
		
		return strlines
	
	# prune leading 0's from polynomial
	@staticmethod
	def prunepoly(mf):
		while len(mf) > 1 and mf[0] == 0:
			mf = [mf[i] for i in range(1,len(mf))]
		return mf
	
	# create regular print of polynomial
	@staticmethod
	def polytoprettystr(l, polyvar = "x"):
		def lcoefstr(l,i):
			return ("" if l[i] == 1 else ("-" if l[i] == -1 else str(l[i])))
		
		def coefstr(l,i):
			if all([j==0 for j in l]) and i == len(l) - 1:
				return "0"
			elif i == len(l) - 1:
				return str(abs(l[i])) if l[i] != 0 else ""
			else:
				return (str(abs(l[i])) if abs(l[i]) != 1 else "") if l[i] != 0 else ""
		
		def powstr(l,i):
			expon = len(l)-1-i
			return (polyvar + "^" + str(expon) if expon != 1 else polyvar) if l[i] != 0 and expon != 0 else ""
		
		def signstr(l,i):
			return (" - " if l[i] < 0 else (" + " if l[i] > 0 else ""))
		
		strout = ""
		
		j = 0
		while j < len(l)-1 and l[j] == 0:
			j = j + 1
		
		if j < len(l) - 1:
			strout = strout + lcoefstr(l,j) + powstr(l,j)
			if j < len(l) - 2:
				strout = strout + "".join([signstr(l,i) + coefstr(l,i) + powstr(l,i) for i in range(j+1,len(l)-1)])
			strout = strout + signstr(l,len(l)-1) + coefstr(l,len(l)-1)
		else:
			strout = strout + coefstr(l,len(l)-1)
		
		return strout
	
	# create LaTeX for polynomial
	# powadj is for shifting variable powers on intermediate steps
	@staticmethod
	def polytolatex(l, powadj = 0, polyvar = "x"):
		def lcoefstr(l,i):
			return ("" if l[i] == 1 else ("-" if l[i] == -1 else str(l[i])))
		
		def coefstr(l,i):
			if all([j==0 for j in l]) and i == len(l) - 1:
				return "0"
			elif i + powadj == len(l) - 1:
				return str(abs(l[i])) if l[i] != 0 else ""
			else:
				return (str(abs(l[i])) if abs(l[i]) != 1 else "") if l[i] != 0 else ""
		
		def powstr(l,i):
			expon = len(l)-1-i-powadj
			return (polyvar + "^" + str(expon) if expon != 1 else polyvar) if l[i] != 0 and expon != 0 else ""
		
		def signstr(l,i):
			return ("{}-{}" if l[i] < 0 else ("{}+{}" if l[i] > 0 else ""))
		
		strout = ""
		
		j = 0
		while j < len(l)-1 and l[j] == 0:
			strout = strout + " &  &  & "
			j = j + 1
		
		if j < len(l) - 1:
			strout = strout + lcoefstr(l,j) + " & " + powstr(l,j)
			if j < len(l) - 2:
				strout = strout + " & " + " & ".join([signstr(l,i) + " & " + coefstr(l,i) + " & " + powstr(l,i) for i in range(j+1,len(l)-1)])
			strout = strout + " & " + signstr(l,len(l)-1) + " & " + coefstr(l,len(l)-1)
		else:
			strout = strout + coefstr(l,len(l)-1)
		
		return strout




#######################################
########## Argument handling ##########
#######################################

parser = argparse.ArgumentParser(description='Perform polynomial long division using modular arithmetic')

# parser.add_argument('-a', type=str, help='coefficients of a(x), separated by "," or ";"')
# parser.add_argument('-b', type=str, help='coefficients of b(x), separated by "," or ";"')
parser.add_argument('-a', '--a-coeffs', action='store', type=int, nargs="+", help='coefficients of a(x)')
parser.add_argument('-b', '--b-coeffs', action='store', type=int, nargs="+", help='coefficients of b(x)')
parser.add_argument('-n', action='store', type=int, help='modular base')

parser.add_argument('-o', '--output-file', nargs="?", action='store', type=str, help='output file name')
parser.add_argument('-V', '--variable', action='store', default='x', help='polynomial variable')

parser.add_argument('-t', '--latex', action='store_true', help='output formatted LaTeX')
parser.add_argument('-v', '--verbose', action='count', help='increase verbosity')

# parser.add_argument('--noreduce-inputs', action='store_true', help='don\'t reduce input polynomials modulo n in output')

# # samples
# parser.add_argument('-z', '--zaxis', choices=['up', 'out', 'right'], default='out', help='direction for the z-axis')
# parser.add_argument('-cf', '--front-color', action='store', default='#bebebe', help='color of front faces')

args = parser.parse_args()




#######################################
############## Main body ##############
#######################################

# main inputs from arguments
ax = args.a_coeffs  # [1, 3, -7, 0, 5, 4]
bx = args.b_coeffs  # [2, 1, 5]
N = args.n  # 11
var = args.variable

polydiv = PolyLongDiv(ax, bx, N)

# if args.noreduce_inputs:
# 	polydiv.reduceinputs()


# create the output
outputlines = []
if args.latex:
	outputlines = polydiv.latexoutput(polyvar = var)
else:
	outputlines = []
	outputlines = outputlines.append("a(" + var + ") = q(" + var + ")b(" + var + ") + r(" + var + ")")
	outputlines = outputlines.append("")
	outputlines = outputlines.append("a(" + var + ") = " + PolyLongDiv.polytoprettystr(polydiv.ax, polyvar = var))
	outputlines = outputlines.append("b(" + var + ") = " + PolyLongDiv.polytoprettystr(polydiv.bx, polyvar = var))
	outputlines = outputlines.append("q(" + var + ") = " + PolyLongDiv.polytoprettystr(polydiv.qx, polyvar = var))
	outputlines = outputlines.append("r(" + var + ") = " + PolyLongDiv.polytoprettystr(polydiv.rx, polyvar = var))


# write the output
if args.output_file != None:
	fout = open(args.output_file, 'w')
	for l in outputlines:
		fout.write(l + "\n")
	fout.close()
else:
	print ""
	for l in outputlines:
		print l
	print ""



