# Creates points to be written to the database
# Measurement name = light name, which should be pointDict key
class Points:

	def __init__(self, inputDict, tagNames = []):
		self.pointsDict = inputDict
		for i in self.pointsDict.keys():
			point = dict()
			fields = self.pointsDict[i]
			point["measurement"] = i
			tags = dict()
			for j in tagNames:
				try:
					tags[j] = point["fields"][j]
				except KeyError:
					tags[j] = None
			point["tags"] = tags
			point["fields"] = self.getFields(fields)
			self.pointsDict[i] = point

	def getFields(self, fields, fieldPrefix = ''):
		fieldSet = dict()
		for i in fields:
			if not isinstance(fields[i], dict): # Base case
				if isinstance(fields[i], bool):
					fields[i] = 1 if fields[i] else 0
					fieldSet[fieldPrefix + i] = fields[i]
				elif isinstance(fields[i], int) or isinstance(fields[i], float):
					fieldSet[fieldPrefix + i] = fields[i]
				else:
					fieldSet[fieldPrefix + i] = str(fields[i])
			else: # Recursive case
				fieldPrefix = fieldPrefix + str(i) + "_"
				fieldSet.update(self.getFields(fields[i], fieldPrefix))
				fieldPrefix = ''
		return fieldSet

	def get(self):
		values = list()
		for i in self.pointsDict.values():
			values.append(i)
		return values