class Classes(object):
	classes = None
	grade = None
	difficulty = None

	def __init__(self):
		self.prereqs()
		self.grades()
		self.difficulty()

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
        	"CS147" : "CS47",
        	"CS149" : "CS146",
        	"CS151" : "MATH42, CS46B, CS49J",
        	"CS152" : "CS151",
        	"CS154" : "MATH42, CS46B",
        	"CS160" : "CS146, CS151, CS100W",
			"CS156" : "CS146, CS151",
			"CS157A" : "CS146",
			"CS157B" : "CS157A",
			"CS158A" : "CS146, CS147",
			"CS158B" : "CS158A",
			"CS161" : "CS160",
			"CS166" : "CS146, CS47",
			"CS174" : "CS46B",
			"CS175" : "CS47",
			"CS190" : "CS146",
			"CS190I" : "CS146",
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

	def difficulty(self):
		self.difficulty = {
			"MATH19" : 1,
			"MATH30" : 1,
			"MATH31" : 2,
			"MATH32" : 3,
			"MATH129A" : 3,
			"MATH42" : 2,
        	"CS46A" : 1,
        	"CS46B" : 1,
        	"CS47" : 2,
        	"CS100W" : 3,
        	"CS146" : 3,
        	"CS147" : 2,
        	"CS149" : 2,
        	"CS151" : 3,
        	"CS152" : 2,
        	"CS154" : 2,
        	"CS160" : 3,
			"CS156" : 3,
			"CS157A" : 2,
			"CS157B" : 3,
			"CS158A" : 2,
			"CS158B" : 3,
			"CS161" : 3,
			"CS166" : 2,
			"CS174" : 2,
			"CS175" : 2,
			"CS185C" : 2,
			"CS190" : 1,
			"CS190I" : 1,
			}