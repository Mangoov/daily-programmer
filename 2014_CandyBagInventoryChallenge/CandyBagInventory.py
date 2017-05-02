#! python3.4
__author__ = 'Julien Lapointe'

#DailyProgrammer Challenge #186 (Halloween special)
#Get statistics of Halloween candies  from a trick or treater's bag
#http://www.reddit.com/r/dailyprogrammer/comments/2kwfqr/10312014_challenge_186_special_code_or_treat/

def open_candy_bag(candy_bag_Location):
    candy_bag = open(candy_bag_Location, 'r')
    candy_list = dict()
    candy_count = 0
    for candy in candy_bag:
        candy_list[candy] = candy_list.get(candy, 0) + 1
        candy_count += 1
    return candy_list, candy_count


candyList, totalCandy = open_candy_bag("candyBag.txt")
for candy in candyList:
    percentage = candyList[candy] / totalCandy * 100
    percentage = format(percentage, '.1f').rstrip('.')
    print(candy.rstrip('\n') + ": ", percentage, "%")


