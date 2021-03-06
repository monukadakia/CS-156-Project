class Classes(object):
	classes = None
	grade = None
	difficulty = None

	def __init__(self):
		self.prereqs()
		self.grades()

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
        	"CS146" : "MATH30, MATH42, CS46B",
        	"CS147" : "CS47",
        	"CS149" : "CS146",
        	"CS151" : "MATH42, CS46B",
        	"CS152" : "CS151",
        	"CS154" : "MATH42, CS46B",
        	"CS160" : "CS146, CS151, CS100W",
			"CS156" : "CS146, CS151",
			"CS157A" : "CS146",
			"CS157B" : "CS157A",
			"CS158A" : "CS146, CS147",
			"CS166" : "CS146, CS47",
			"CS174" : "CS46B",
			"CS190" : "CS146",
			"CS100W": "CS146",
			"PHIL134": "CS100W"
			}

	def grades(self):
		self.grade = {
			"A+" : 4.0,
			"A" : 4.0,
			"A-" : 3.7,
			"B+" : 3.3,
			"B" : 3.0,
			"B-" : 2.7,
			"C+" : 2.3,
			"C" : 2.0,
			"C-" : 1.7,
			"D+" : 1.3,
			"D" : 1.0,
			"D-" : 0.7,
			"F" : 0,
			}
