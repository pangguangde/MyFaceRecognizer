from facepp import API


API_KEY = 'e0e5b6989cf28bd24682d025d9946d21'
API_SECRET = 'cgh0KpSOnTqO1nYlyANtoG529JxNDAGk'
api = API(API_KEY, API_SECRET)

api.group.delete(group_name = 'family')
persons = [
	'pangguangde_0',
'pangguangde_1',
'pangguangde_2',
'pangguangde_3',
'pangguangde_4',
'wengwenxia_0',
'wengwenxia_1',
'wengwenxia_2',
# 'wengwenxia_3',
# 'wengwenxia_4',
# 'lianglixia_0',
# 'lianglixia_1',
# 'lianglixia_2',
# 'lianglixia_3',
# 'lianglixia_4',
# 'pangxianfu_0',
# 'pangxianfu_1',
# 'pangxianfu_2',
# 'pangxianfu_3',
# 'pangxianfu_4'
]
for item in persons:
	api.person.delete(person_name = item)