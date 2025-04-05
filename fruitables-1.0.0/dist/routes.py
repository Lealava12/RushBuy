from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_connection
import mysql.connector
from functools import wraps
from werkzeug.utils import secure_filename
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

user_routes = Blueprint('user_routes', __name__)
@user_routes.route('/admin/login', methods=['POST'])
def login():
    """
    Login route for users.
    """
    conn = get_connection()
    cursor = conn.cursor()

    data = request.json  # Use JSON instead of form data
    email = data.get('email')
    password = data.get('password')

    query = "SELECT * FROM admin WHERE email = %s AND password = %s"
    values = (email, password)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            session['admin_email'] = email
            conn.close()
            return jsonify({"message": "Login successful", "redirect": "dashboard.html"}), 200
        else:
            conn.close()
            return jsonify({"error": "Invalid email or password"}), 401

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500

# Route to save category
# @user_routes.route('/save-category', methods=['POST'])
# def save_category():
#     conn = get_connection()
#     cursor = conn.cursor()

#     category_name = request.form['category-name']
#     category_description = request.form.get('category-description', '')
#     category_status = request.form['category-status']

#     query = "INSERT INTO Categories (name, description, status) VALUES (%s, %s, %s)"
#     values = (category_name, category_description, category_status)

#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Category saved successfully!"})

# # Route to save subcategory
# @user_routes.route('/save-subcategory', methods=['POST'])
# def save_subcategory():
#     conn = get_connection()
#     cursor = conn.cursor()

#     subcategory_name = request.form['sub-category-name']
#     parent_category = request.form['parent-category']
#     subcategory_description = request.form.get('sub-category-description', '')
#     subcategory_status = request.form['sub-category-status']

#     # Get category_id from Categories table based on parent category name
#     cursor.execute("SELECT category_id FROM Categories WHERE name = %s", (parent_category,))
#     category_result = cursor.fetchone()
#     if category_result:
#         category_id = category_result[0]
#     else:
#         return jsonify({"error": "Parent category not found!"}), 404

#     query = "INSERT INTO SubCategories (category_id, name, description) VALUES (%s, %s, %s)"
#     values = (category_id, subcategory_name, subcategory_description)

#     cursor.execute(query, values)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Sub-Category saved successfully!"})

# # Route to save product
# @user_routes.route('/save-product', methods=['POST'])
# def save_product():
#     conn = get_connection()
#     cursor = conn.cursor()

#     product_name = request.form['product-name']
#     product_description = request.form.get('product-description', '')
#     product_category = request.form['product-category']
#     product_sub_category = request.form['product-sub-category']
#     product_price = request.form['product-price']
#     product_discount = request.form.get('product-discount', 0)
#     product_stock = request.form['product-stock']
#     product_weight = request.form.get('product-weight', None)
#     product_status = request.form['product-status']
#     product_tags = request.form.get('product-tags', '')
#     product_dimensions = request.form.get('product-dimensions', '')
#     product_specifications = request.form.get('product-specifications', '')

#     # Fetch subcategory_id based on the sub-category name
#     cursor.execute("SELECT subcategory_id FROM SubCategories WHERE name = %s", (product_sub_category,))
#     subcategory_result = cursor.fetchone()
#     if subcategory_result:
#         subcategory_id = subcategory_result[0]
#     else:
#         return jsonify({"error": "Sub-category not found!"}), 404

#     query = """INSERT INTO Products (subcategory_id, name, description, price, discount_percentage, stock_quantity, 
#                weight, status, tags, dimensions, specifications) 
#                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#     values = (subcategory_id, product_name, product_description, product_price, product_discount,
#               product_stock, product_weight, product_status, product_tags, product_dimensions, product_specifications)

#     cursor.execute(query, values)
#     product_id = cursor.lastrowid

#     # Handle product image if uploaded
#     if 'product-image' in request.files:
#         product_image = request.files['product-image']
#         image_filename = product_image.filename
#         # Assuming you save images in a static folder
#         image_path = os.path.join('static/images', image_filename)
#         product_image.save(image_path)

#         # Save image details in ProductImages table
#         query_image = "INSERT INTO ProductImages (product_id, image_url, is_primary) VALUES (%s, %s, %s)"
#         cursor.execute(query_image, (product_id, image_path, True))

#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Product saved successfully!"})
