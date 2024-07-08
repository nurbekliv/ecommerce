from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        """
        Initialize the cart with the session and request data.
        """
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        """
        Add a product to the cart in the database.
        """
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass  # Product is already in the cart
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            # Update user's cart in the database if authenticated
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=carty)

    def add(self, product, quantity):
        """
        Add a product to the cart and update the session.
        """
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass  # Product is already in the cart
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            # Update user's cart in the database if authenticated
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=carty)

    def cart_total(self):
        """
        Calculate the total price of the items in the cart.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            value = int(value)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total

    def __len__(self):
        """
        Get the number of items in the cart.
        """
        return len(self.cart)

    def get_prods(self):
        """
        Get all products in the cart.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        """
        Get the quantities of each product in the cart.
        """
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        """
        Update the quantity of a product in the cart.
        """
        product_id = str(product)
        product_qty = str(quantity)
        self.cart[product_id] = product_qty
        self.session.modified = True

        if self.request.user.is_authenticated:
            # Update user's cart in the database if authenticated
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=carty)

        return self.cart

    def delete(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        if self.request.user.is_authenticated:
            # Update user's cart in the database if authenticated
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace("'", "\"")
            current_user.update(old_cart=carty)
