from django.core.paginator import Paginator
from django.core.cache import cache
from .glt import GltAPI
from .utils.glt import formate_all_products_glt
from shop.models import WishlistItem


def format_tour_response(data):
    glt = data["formatted_glt"]
    filtered_data = glt[:16]

    for idx, item in enumerate(filtered_data, start=1):
        item["id"] = idx

    return {"status": True, "data": filtered_data}

def format_filter_tour_response(
    data,
    sort="title",
    page=1,
    category=None,
    search=None,
):
    page_size = 12
    filtered_data = data["formatted_glt"]

    # Filter by category (if provided)
    if category:
        filtered_data = [
            item
            for item in filtered_data
            if item.get("category") and category.lower() in item["category"].lower()
        ]

    # Filter by search term (if provided)
    print(search)
    if search:
        filtered_data = [
            item
            for item in filtered_data
            if item.get("title") and search.lower() in item["title"].lower()
        ]

    # Sort the data
    sort_options = {
        "asc": lambda x: x["id"],
        "desc": lambda x: -x["id"],
        "name-asc": lambda x: x["title"].lower() if x.get("title") else "",
        "name-desc": lambda x: -ord(x["title"][0].lower()) if x.get("title") else 0,
        "price-asc": lambda x: x.get("price", 0),
        "price-desc": lambda x: -x.get("price", 0),
    }
    if sort in sort_options:
        filtered_data.sort(key=sort_options[sort])

    # Paginate the data
    paginator = Paginator(filtered_data, page_size)
    result_page = paginator.get_page(page)

    # Update IDs for the current page
    for idx, item in enumerate(
        result_page, start=(result_page.number - 1) * page_size + 1
    ):
        item["id"] = idx

    return {
        "status": True,
        "data": list(result_page),
        "pagination": {
            "total_pages": paginator.num_pages,
            "current_page": result_page.number,
            "total_items": paginator.count,
            "page_size": page_size,
        },
    }

def format_tour_detail_response(data={}, api_type=None, id=None, request=None):
    if api_type:
        is_favorite = False

        if request.user.is_authenticated:
            try:
                WishlistItem.objects.get(
                    api_category=api_type.upper(),
                    product_id=id,
                    wishlist__user=request.user,
                )
                is_favorite = True
            except WishlistItem.DoesNotExist:
                is_favorite = False

        data["is_favorite"] = is_favorite
        return {
            "status": True,
            "data": data,
        }
    return {
        "status": True,
        "data": data,
    }


class BaseAPI:
    @staticmethod
    def get_all_tours(request=None):
        glt = GltAPI.get_tours(request)
        popular = GltAPI.get_popular_products()
        reels = GltAPI.get_reels(request)
        blogs = GltAPI.get_blogs(request)
        formatted_glt = formate_all_products_glt(glt, request)
        formatted_popular_products = formate_all_products_glt(popular, request)

        data = {
            "formatted_glt": formatted_glt,
        }

        return {
            "tours": format_tour_response(data),
            "popular_products": formatted_popular_products,
            "reels": reels,
            "blogs": blogs,
        }

    @staticmethod
    def get_filter_tours(
        search=None,
        sort=None,
        page=None,
        request=None,
        category=None,
    ):
        # cache_key = f"all-filter2-{category}"
        # cached_data = cache.get(cache_key)

        # if cached_data is not None:
            # return format_filter_tour_response(
            #     cached_data,
            #     sort,
            #     page,
            #     search,
            #     category,
            # )

        glt = GltAPI.get_tours()
        formatted_glt = formate_all_products_glt(glt, request)

        data = {
            "formatted_glt": formatted_glt,
        }
 
        # cache.set(cache_key, data, 60 * 15)

        return format_filter_tour_response(data, sort, page, category, search)

    @staticmethod
    def get_tour_detail(api_type, id, request=None):
        data = {}

        if api_type.upper() == "G":
            data = GltAPI.get_tour_detail(id, request=request)

        return format_tour_detail_response(data, api_type, request=request, id=id)

    @staticmethod
    def check_availability(api_type, id, data=None):
        if api_type.upper() == "G":
            data = GltAPI.check_availability(api_type, id, data)
        return format_tour_detail_response(data)

    @staticmethod
    def create_booking(api_type, data=None):
        result = {}

        if api_type.upper() == "G":
            result = GltAPI.create_booking(data=data)

        return format_tour_detail_response(result)

    @staticmethod
    def get_detail_booking(api_type, booking_id=None):
        data = {}

        if api_type.upper() == "G":
            data = GltAPI.get_detail_booking(booking_id)

        return format_tour_detail_response(data)

    @staticmethod
    def update_detail_booking(api_type, booking_id=None):
        data = {}

        if api_type.upper() == "G":
            data = GltAPI.update_detail_booking(booking_id)

        return format_tour_detail_response(data)
