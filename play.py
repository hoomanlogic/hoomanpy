
import parsedatetime as pdt
cal = pdt.Calendar()
print cal.parse('5 hours after 12pm')

from hoomanlogic.querylist import

#cal.parse('5 hours before 12pm')
# todo: update date_add code to use timedeltas: target     = start + datetime.timedelta(days=offset)

# todo: outstanding parse issues below:
# testparse '5 days from tomorrow'
#           returns (time.struct_time(tm_year=2013, tm_mon=8, tm_mday=9, tm_hour=9, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=221, tm_isdst=-1), 1)
#           on 2013-08-02

# NLP TESTS
# testnlp at 8PM on August 5th i'm going to fly to Florida
# testnlp I'm so excited!! At 8PM on August 5th i'm going to fly to Florida. Then next Friday at 9PM i'm going to dog n bone!
# testnlp I'm so excited!! At 8PM on August 5th i'm going to fly to Florida. Then next Friday at 9PM i'm going to dog n bone! And in 5 minutes i'm going to eat some food!
# testnlp in 5 days from tomorrow i'll be 21

# PARSE TESTS
# print cal.parse('August 5 5pm')
# print cal.parse('25 August 2006')
# print cal.parse('22nd August 2008')
# print cal.parse('5pm 25 August, 2006')
# print cal.evalRanges("August 29 - September 2, 2006")
# print cal.parse("injunction")
# print cal.parse("jun 5th - 6th, 2013")
# print cal.parse("jun5th2013")
# print cal.parse("jun2013")
# print cal.parse("jun")
# print cal.parse("jun5th, 2013")
# print cal.parse("jun5th,2013")
# print cal.parse("jun 5th, 2013")
# print cal.parse("jun 5th,2013")
# print cal.parse("jun 5th 2013")
# print cal.parse("jun")

# NLP TESTS
# matches = cal.nlp("injunction")
# matches = cal.nlp("jun 5th - 6th, 2013")
# matches = cal.nlp("jun5th2013")
# matches = cal.nlp("jun2013")
# matches = cal.nlp("jun")
# matches = cal.nlp("jun5th, 2013")
# matches = cal.nlp("jun5th,2013")
# matches = cal.nlp("jun 5th, 2013")
# matches = cal.nlp("jun 5th,2013")
# matches = cal.nlp("jun 5th 2013")
# matches = cal.nlp("jun 2013")
# matches = cal.nlp("jun")


