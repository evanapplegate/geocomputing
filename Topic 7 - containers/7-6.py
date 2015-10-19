rects = [(5,2), (7,13), (9,4), (17,4)]

def calculate_areas(a):
    area_list = []
    for a, b in rects:
        area_of_rectangle = a*b
        area_list.append(area_of_rectangle)
    return area_list

areas_to_sort = calculate_areas(rects)
areas_to_sort.sort(reverse=True)
print areas_to_sort