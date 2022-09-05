from enum import Enum
import pandas as pd

class Nation(Enum):
	USA = 'USA'
	GERMANY = 'Germany'
	USSR = 'USSR'
	UK = 'Great Britain'
	JAPAN = 'Japan'
	CHINA = 'China'
	ITALY = 'Italy'
	FRANCE = 'France'
	SWEDEN = 'Sweden'
	ISRAEL = 'Israel'

class Class(Enum):
	LIGHT = 'Light tank'
	MEDIUM = 'Medium tank'
	HEAVY = 'Heavy tank'
	DESTROYER = 'Tank destroyer'
	SPAA = 'SPAA'

class Category(Enum):
	NON_PREMIUM = 'Researchable'
	PREMIUM_EAGLES = 'Premium - Golden Eagles'
	PREMIUM_GIFT = 'Premium - Bundle or Gift'
	SQUADRON = 'Squadron'

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])

class Tank:
	name_: None
	nation: Nation = None
	class_: Class = None
	rank: None
	category: Category = None
	battle_rating: None

	def to_dataframe(self) -> pd.DataFrame:
		return pd.DataFrame({
		'Name':[self.name_],
		'Nation':[self.nation], 
		'Class':[self.class_],
		'Rank':[self.rank],
		'Category':[self.category],
		'BR':[self.battle_rating]
		})