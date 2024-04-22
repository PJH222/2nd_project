from now_geo import current_location
from geo import get_location
from address import get_address

location = current_location()
print(get_address(location['lat'],location['lng']))
print(location)

# 37.4926 126.92