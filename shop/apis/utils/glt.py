import os
from shop.models import WishlistItem


def formate_all_products_glt(data, request):
    api_name = "GLT"
    api_type = "G"
    response_data = []
    discount_percent = 0

    for product in data:
        product_name = product.get("title", "")
        category = product.get("category", "")
        product_image = product.get("product_image", "")
        total_reviews = product.get("total_reviews", 0)
        avg_rating = product.get("avg_rating", 0)
        product_id = product.get("id", "")
        images = product.get("images", [])
        price = product.get("basePrice", 0)
        is_favorite = False

        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0.0

        if request.user.is_authenticated:
            try:
                wishlist_item = WishlistItem.objects.get(
                    api_category="G", product_id=product_id, wishlist__user=request.user
                )
                if wishlist_item:
                    is_favorite = True
            except WishlistItem.DoesNotExist:
                pass

        if product_image:
            image = product_image
        else:
            image = (
                os.environ.get("API_URL", "http://gt.codecanvascreation.com")
                + images[0].get("image", "")
                if images
                else ""
            )

        product_response = {
            "api": {
                "api_type": api_type,
                "api_name": api_name,
                "id": product_id,
            },
            "title": product_name,
            "image": image,
            "country": product.get("country", ""),
            "duration": product.get("duration", ""),
            "price": price,
            "category": category,
            "discounted_price": price,
            "discount_percent": discount_percent,
            "is_favorite": is_favorite,
            "total_reviews": total_reviews,
            "avg_rating": avg_rating,
        }

        response_data.append(product_response)

    return response_data
