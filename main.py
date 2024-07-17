import requests
import json
import geojson
 

south_coast = {"SE": "54.768088, -129.096165",
"SW": "51.288725, -178.524441",
"NW": "60.965413, -173.427755",
"NE": "62.000697, -136.186531"}

example_json_data = '''
{
"type": "Feature",
"properties": {
	"name": "Example Feature"
},
"geometry": {
	"type": "Point",
	"coordinates": [0, 0]
}
}
'''

def convert_json_to_geojson(json_data):
	#Parsing JSON data
    print (json_data)
    parsed_json = json_data #json.loads(json_data)
    for i in parsed_json:
        # Converting to GeoJSON feature
        feature = geojson.Feature(geometry=i["geometry"], properties=i["object_value"])

	#Create a GeoJSON FeatureCollection
	# feature_collection = geojson.FeatureCollection([feature])kill
    # return feature_collection
    return feature

 
def check_len(data: dict)->bool:
    """Checks if the length of data is less than 2000. Returns True if less than 2000 features are returned, otherwise False."""
    length = len(data.get("data"))
    print("The length is " + str(length))
    if length >= 2000:
        return False
    else:
        return True

def get_images(bounding_box="12.967,55.597,13.008,55.607"):
    api_endpoint = 'https://graph.mapillary.com/images'
 
    # Parameters for searching images
    params = {
    'access_token': client_token,
    'fields': 'id,thumb_1024_url',
    'bbox': bounding_box,  # Bounding box coordinates
    'limit': 2,  # Limit the number of results
    }
 
    # Make the GET request
    response = requests.get(api_endpoint, params=params)
    return parse_response(response)

 
def parse_response(response: requests.Response):
    # Check the response status
    if response.status_code == 200:
    # Parse and print the response JSON data
        print(json.dumps(json.loads(response.text), indent=2))
        data = json.loads(response.text)
        return data
    else:
        print("An error occured:" + response.text)
    # Handle errors
        return f'Error: {response.status_code} - {response.text}' 

def get_map_features(bounding_box="-178.525, 51.289, -129.097, 62.001")->dict:
    api_endpoint = "https://graph.mapillary.com/map_features"

    params = {
        "access_token": client_token,
        "fields": "id, object_value, geometry",
        "bbox": bounding_box,
        "object_values": "regulatory-*, *traffic-sign*",
    }

    response = requests.get(api_endpoint, params=params, timeout=30)
    return parse_response(response)

# def get_map_feature_id(feature_id:str)->dict:
#     api_endpoint = f"https://graph.mapillary.com/{feature_id}"

#     params = {
#         "access_token": client_token,
#         "fields": "aligned_direction, last_seen_at, object_value, object_type, geometry",
#     }

#     response = requests.get(api_endpoint, params=params)
#     return parse_response(response)

# map_features = get_map_features(bounding_box='-178.525, 51.289, -129.097, 62.001')
# feature = get_map_feature_id("25641511085497366")
# feature2 = get_map_feature_id("25641511095497365")

partitionx = 4
partitiony = 4
level = 0
i=0
feature_collection = geojson.FeatureCollection([])


def check_for_features(west_most, north_most, east_most, south_most):
    global i, level, partitionx, partitiony, feature_collection
    stepx = (west_most - east_most) / partitionx
    stepy = (north_most - south_most) / partitiony
    print ("stepx is " + str(stepx) + " and stepy is " + str(stepy))
    for x in range(partitionx): 
        for y in range(partitiony):
            #print ("x is " + x + " and y is " + y)
            i = i + 1
            boundingboxX = west_most - stepx*x 
            boundingboxY = north_most - stepy*y
            boundingboxXend = boundingboxX - stepx
            boundingboxYend = boundingboxY - stepy
            south_coast_quadrant = f"{boundingboxX}, {boundingboxYend}, {boundingboxXend}, {boundingboxY}"
            print (str(i) + ": The bounding box is " + south_coast_quadrant + ". LEVEL is " + str(level))
            feature_list = get_map_features(south_coast_quadrant)
            #print ("The feature list is " + str(feature_list))
            if (not check_len(feature_list)):
                level = level + 1
                check_for_features(boundingboxX, boundingboxY, boundingboxXend, boundingboxYend)
                level = level - 1
            else:
                if len(feature_list.get("data")) > 0:
                    for features,value in feature_list.items():
                        #print ("Value is " + str(value))
                        for z in value:
                            # Converting to GeoJSON feature
                            feature = geojson.Feature(geometry=z["geometry"], properties=z["object_value"])
                            feature_collection.features.append(feature)
                        #feature_collection.features.append(convert_json_to_geojson(value))
                        #convert_json_to_geojson(value)


farthest_west = -178.525
farthest_east = -129.097
farthest_north = 62.001
farthest_south = 51.289
check_for_features(farthest_west, farthest_north, farthest_east, farthest_south)
with open("south_coast.geojson", 'w') as outfile:
      geojson.dump(feature_collection, outfile)


print("This was successful!")
print(len(feature_collection))

# Converting JSON to GeoJSON
#geojson_result = convert_json_to_geojson(example_json_data)
 
#Printing the GeoJSON result.
#print(geojson.dumps(geojson_result, indent=2))




        
