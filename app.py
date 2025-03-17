from flask import Flask, render_template 
app = Flask(__name__) 
 
products = [{'id': 1, 'name': 'Telefon', 'price': 1000}, {'id': 2, 'name': 'Laptop', 'price': 5000}] 
 
cart = [] 
@app.route('/add/<int:product_id>') 
def add_to_cart(product_id): 
    product = next((p for p in products if p['id'] == product_id), None) 
    if product: 
        cart.append(product) 
        return f"{product['name']} sepete eklendi!" 
    return "Ürün bulunamadı."
 
@app.route('/') 
def home(): 
    return render_template('index.html', products=products) 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)