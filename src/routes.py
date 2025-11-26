from flask import Blueprint, request, jsonify

from scraper.driver_manager import driver_manager
from scraper.scraper import Scraper

api = Blueprint('api', __name__)

@api.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    if not query:
        return jsonify({"error": "query required"}), 400
    
    try:
        driver = driver_manager.get_driver()
        scraper = Scraper(driver)
        result = scraper.search(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/product', methods=['GET'])
def product():
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({"error": "url required"}), 400
    
    try:
        driver = driver_manager.get_driver()
        scraper = Scraper(driver)
        result = scraper.get_product(url)

        if result is None:
            return jsonify({
                "error": "Product not found",
                "url": url
            }), 404

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "driver_connected": driver_manager.driver is not None
    })
