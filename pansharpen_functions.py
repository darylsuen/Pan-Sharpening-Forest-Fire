import planetary_computer
import pystac_client
from pystac.extensions.eo import EOExtension as eo


def print_collections(catalog: pystac_client.Client):
    """
    Get a list of collections in the catalog and print the list. get_collections()
    returns a generator which isn't stored in memory so it must be converted to a
    list to be printed. Call this function to get the exact syntax of the collection
    for the 'collections' variable.
    """
    collections = [collection.to_dict() for collection in catalog.get_collections()]
    print(len(collections))
    for collection in collections:
        print(collection['id'])

def search(
        catalog: pystac_client.Client, collection: list, bbox: list, 
        time_of_interest: str, cloud_cover: dict
        ) -> dict: 
    """
    Search the Microsoft Planetary Computer catalog for a specific collection
    of satellite images. The search is filtered by a bounding box, time range,
    and cloud cover percentage. The search results are returned as a Python
    dictionary.
    """
    # Connect to the catalog. A STAC catalog is a JSON file of links that can be 
    # searched with a query to find specific assets. The open() method creates an 
    # instance of the Client class, which is used to interact with the catalog. The 
    # 'modifier' parameter is used to authenticate the request to the catalog.
    catalog = pystac_client.Client.open(
        catalog, modifier=planetary_computer.sign_inplace
        )
    search = catalog.search(
        collections=collection,
        bbox=bbox,
        datetime=time_of_interest,
        query=cloud_cover
    )
    items = search.item_collection()
    return items

def get_least_cloudy(items: dict) -> dict:
    """
    Get the least cloudy image from the search results. The least cloudy image
    is determined by the 'eo:cloud_cover' property in the metadata.
    """
    # The 'key' parameter uses a lambda to apply eo.ext() to each item in items
    # which extracts item properties, one of which is cloud_cover.
    selected_item = min(items, key=lambda item: eo.ext(item).cloud_cover)
    # .datetime is a property of the selected item and date() is a method of the
    # datetime object that returns the date in the format 'YYYY-MM-DD'.
    print(
    f"Choosing {selected_item.id} from {selected_item.datetime.date()}"
    + f" with {selected_item.properties['eo:cloud_cover']}% cloud cover"
    )
    return selected_item


