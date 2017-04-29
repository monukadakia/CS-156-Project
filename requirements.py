class Classes(object):
	classes = None
	grade = None

	def __init__(self):
		self.prereqs()

	def prereqs(self):
		self.classes = {
			"MATH30" : "MATH19",
			"MATH31" : "MATH30",
			"MATH32" : "MATH31",
			"MATH129A" : "MATH31",
			"MATH42" : "MATH19",
        	"CS46A" : "MATH19",
        	"CS46B" : "MATH30, CS46A",
        	"CS47" : "CS46B",
        	"CS100W" : "",
        	"CS146" : "MATH30, MATH42, CS46B",
        	"CS147" : "CS47, CMPE102",
        	"CS149" : "CS146, SE146",
        	"CS151" : "MATH42, CS46B, CS49J",
        	"CS152" : "CS151, CMPE135",
        	"CS154" : "MATH42, CS46B",
        	"CS160" : "CS146, CS151, CS100W",
			"CS156" : "CS146, CS151, CMPE135",
			"CS157A" : "CS146",
			"CS157B" : "CS157A",
			"CS158A" : "CS146, CS147, CMPE120",
			"CS158B" : "CS158A, CMPE148",
			"CS161" : "CS160",
			"CS166" : "CS146, CS47, CMPE102, CMPE120",
			"CS174" : "CS46B",
			"CS175" : "CS47",
			"CS185C" : "",
			"CS190" : "CS146",
			"CS190I" : "CS146",
			}
			
	def grades(self):
		self.grade = {
			"A+" : "4.0",
			"A" : "4.0",
			"A-" : "3.7",
			"B+" : "3.3",
			"B" : "3.0",
			"B-" : "2.7",
			"C+" : "2.3",
			"C" : "2.0",
			"C-" : "1.7",
			"D+" : "1.3",
			"D" : "1.0",
			"D-" : "0.7",
			"F" : "0",
			}


