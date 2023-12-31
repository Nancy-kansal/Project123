from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def fetch_data():
    api_url = 'https://s3.amazonaws.com/open-to-cors/assignment.json'
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', {})

        sorted_products = sorted(products.items(), key=lambda x: int(
            x[1]['popularity']), reverse=True)
        sorted_product_list = []
        for product_id, product_details in sorted_products:
            sorted_product_list.append({
                "Product ID": product_id,
                "Popularity": product_details['popularity'],
                "Price": product_details['price'],
                "Subcategory": product_details['subcategory'],
                "Title": product_details['title']
            })

        return render_template('index.html', sorted_product_list=sorted_product_list)
        # If you want to return JSON data, use the line below instead
        # return jsonify(sorted_product_list)
    else:
        return jsonify({'error': f'Failed to fetch data. Status code: {response.status_code}'})

if __name__ == '__main__':
    # For local development, you can use the following line with debug=True
    # app.run(debug=True)
    
    # For production deployment, use the following line with debug=False
    app.run(host="0.0.0.0", port=int("5000"))
