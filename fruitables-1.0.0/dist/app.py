import random
from flask import Flask, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_session import Session  # Import Flask-Session
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import logging
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
# import bcrypt
# import jwt

app = Flask(__name__)
app.secret_key = "126945c1bdc73d55bb3d364aed2611f8"  # Secret key for session management
# app.config["SECRET_KEY"] = app.secret_key
# app.config["SESSION_TYPE"] = "filesystem"
# app.config["SESSION_PERMANENT"] = True
# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
# # #Configure session management
# # app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
# app.config["SESSION_TYPE"] = "filesystem"
# # app.config["SECRET_KEY"] = "your_secret_key"
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_USE_SIGNER"] = True

# Session(app)
# # Initialize Flask-Session
# Session(app)# Initialize Flask-Session

# Configure CORS to allow credentials and specific origins
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://127.0.0.1:1000"]}})
# CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins
# # Enforce HTTPS in Flask
# app.config["PREFERRED_URL_SCHEME"] = "https"

@app.before_request
def log_session_data():
    """
    Log session data for debugging purposes.
    """
    logging.debug(f"Session data before request: {dict(session)}")

def get_connection():
    """
    Establishes a connection to the MySQL database.
    Replace 'root' and 'Liku@123#' with your MySQL credentials.
    """
    try:
        connection = mysql.connector.connect(
            host="93.127.206.58",
            user="root",
            password="Lealava@123",
            database="Ecommerce"
        )
        cursor = connection.cursor(dictionary=True)
        print("Database connected!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

UPLOAD_FOLDER = "/var/www/html/BLINKIT/fruitables-1.0.0/dist/static/uploads"  # Updated path fruitables-1.0.0\Blink it\dashboard\dist\static\uploads      
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    """
    Serve a simple home page or message at the root endpoint.
    """
    return jsonify({"message": "Welcome to Blinkit API"})

@app.route('/login', methods=['POST'])
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
    
# Route to handle user logout
@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout route for users.
    Clears the session and redirects to the login page.
    """
    try:
        session.clear()  # Clear all session data
        return jsonify({"message": "Logout successful", "redirect": "index.html"}), 200
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500

# def login_required(func):
#     """
#     Decorator to protect routes. Redirects to the login page if the user is not logged in.
#     """
#     from functools import wraps

#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         if not session.get('logged_in'):
#             # User is not logged in, redirect to the login page
#             return jsonify({"error": "Unauthorized. Please log in.", "redirect": "/index.html"}), 401
#         return func(*args, **kwargs)

#     return decorated_function
# @app.route('/check-session', methods=['GET'])
# def check_session():
#     """
#     Checks if the user is logged in.
#     """
#     if session.get('logged_in'):
#         return jsonify({"logged_in": True}), 200
#     else:
#         return jsonify({"logged_in": False}), 401

@app.route('/save-category', methods=['POST'])
def save_category():
    """
    Save a new category to the database with a custom ID format (e.g., C01, C02).
    """
    conn = get_connection()
    cursor = conn.cursor()

    category_name = request.form.get('category-name')
    category_description = request.form.get('category-description')
    category_status = request.form.get('category-status')

    try:
        # Retrieve the highest category_id
        cursor.execute("SELECT category_id FROM Categories ORDER BY category_id DESC LIMIT 1")
        last_category = cursor.fetchone()

        # Generate the next custom ID
        if last_category:
            last_id_num = int(last_category[0][1:])  # Skip the 'C' prefix
            new_id_num = last_id_num + 1
        else:
            new_id_num = 1

        custom_category_id = f"C{new_id_num:02}"

        # Insert the new category
        sql = """
            INSERT INTO Categories (category_id, name, description, status) 
            VALUES (%s, %s, %s, %s)
        """
        values = (custom_category_id, category_name, category_description, category_status)
        cursor.execute(sql, values)
        conn.commit()

        return jsonify({"message": "Category added successfully", "category_id": custom_category_id}), 201

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/get-categories', methods=['GET'])
def get_categories():
    """
    Retrieve all categories from the database and return them as JSON.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT category_id, name, description, status FROM Categories")
        categories = cursor.fetchall()

        category_list = [
            {
                "category_id": row[0],
                "name": row[1],
                "description": row[2],
                "status": row[3],
            }
            for row in categories
        ]

        return jsonify({"categories": category_list}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/update-category/<category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Update an existing category in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    category_name = request.form.get('category-name')
    category_description = request.form.get('category-description')
    category_status = request.form.get('category-status')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    try:
        # Update the category in the database
        sql = """
            UPDATE Categories
            SET name = %s, description = %s, status = %s
            WHERE category_id = %s
        """
        values = (category_name, category_description, category_status, category_id)
        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Category not found"}), 404

        return jsonify({"message": "Category updated successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/delete-category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """
    Delete a category from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Delete the category from the database
        sql = "DELETE FROM Categories WHERE category_id = %s"
        cursor.execute(sql, (category_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Category not found"}), 404

        return jsonify({"message": "Category deleted successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/save-subcategory', methods=['POST'])
def save_subcategory():
    """
    Save a new subcategory to the database with a custom ID format (e.g., suc01, suc02),
    ensuring that the selected category_id exists in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Parse JSON data from the request body
    data = request.json  # Use `request.json` for JSON payloads
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    subcategory_name = data.get('sub-category-name')
    category_name = data.get('parent-category')  # Retrieve category name from the JSON payload
    subcategory_description = data.get('sub-category-description')
    subcategory_status = data.get('sub-category-status')
    subcategory_priority = data.get('sub-category-priority')

    if not subcategory_name or not category_name:
        return jsonify({"error": "Sub-category name and parent category are required"}), 400

    try:
        # Validate and retrieve the corresponding category_id for the given category_name
        cursor.execute("SELECT category_id FROM Categories WHERE category_id = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            return jsonify({"error": f"Category '{category_name}' not found in the database"}), 400

        category_id = category[0]  # Extract the category_id

        # Retrieve the highest subcategory_id currently in the table
        cursor.execute("SELECT subcategory_id FROM SubCategories ORDER BY subcategory_id DESC LIMIT 1")
        last_subcategory = cursor.fetchone()

        # Generate the next custom subcategory ID
        if last_subcategory:
            last_id_num = int(last_subcategory[0][3:])  # Skip the 'suc' prefix
            new_id_num = last_id_num + 1
        else:
            new_id_num = 1

        custom_subcategory_id = f"suc{new_id_num:02}"

        # Insert the new subcategory with the retrieved category_id
        sql = """
            INSERT INTO SubCategories (subcategory_id, category_id, name, description, priority_order, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (custom_subcategory_id, category_id, subcategory_name, subcategory_description, subcategory_priority, subcategory_status)
        cursor.execute(sql, values)
        conn.commit()

        return jsonify({
            "message": "Subcategory added successfully",
            "subcategory_id": custom_subcategory_id,
            "category_id": category_id
        }), 201

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/get-count', methods=['GET'])
def get_count():
    """
    For admin dashboard
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Products")
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM SubCategories")
        subcategories_count = cursor.fetchone()[0]

        return jsonify({
            "total_products": product_count,
            "total_categories": categories_count,
            "total_subcategories": subcategories_count
        })
    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/get-subcategories', methods=['GET'])
def get_subcategories():
    """
    Retrieve all subcategories from the database and return them as JSON.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT subcategory_id, category_id, name, description, priority_order, status FROM SubCategories")
        subcategories = cursor.fetchall()
        
        subcategory_list = [
            {
                "subcategory_id": row[0],
                "category_id": row[1],
                "name": row[2],
                "description": row[3],
                "priority_order": row[4],
                "status": row[5],
            }
            for row in subcategories
        ]
        
        return jsonify({"subcategories": subcategory_list}), 200
    
    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/update-subcategory/<subcategory_id>', methods=['PUT'])
def update_subcategory(subcategory_id):
    """
    Update an existing subcategory in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Parse JSON data from the request body
    data = request.json
    subcategory_name = data.get('sub-category-name')
    category_id = data.get('parent-category')
    subcategory_description = data.get('sub-category-description')
    subcategory_status = data.get('sub-category-status')
    subcategory_priority = data.get('sub-category-priority')

    if not subcategory_name or not category_id:
        return jsonify({"error": "Subcategory name and parent category are required"}), 400

    try:
        # Update the subcategory in the database
        sql = """
            UPDATE SubCategories
            SET name = %s, category_id = %s, description = %s, status = %s, priority_order = %s
            WHERE subcategory_id = %s
        """
        values = (subcategory_name, category_id, subcategory_description, subcategory_status, subcategory_priority, subcategory_id)
        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Subcategory not found"}), 404

        return jsonify({"message": "Subcategory updated successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/delete-subcategory/<subcategory_id>', methods=['DELETE'])
def delete_subcategory(subcategory_id):
    """
    Delete a subcategory from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Delete the subcategory from the database
        sql = "DELETE FROM SubCategories WHERE subcategory_id = %s"
        cursor.execute(sql, (subcategory_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Subcategory not found"}), 404

        return jsonify({"message": "Subcategory deleted successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


# Get the next product ID (p01, p02, ..., p10, ...)
def get_next_product_id(cursor):
    cursor.execute("SELECT product_id FROM Products ORDER BY product_id DESC LIMIT 1")
    last_id = cursor.fetchone()
    if last_id and last_id[0]:
        last_num = int(last_id[0][1:])  # Extract numeric part
        new_num = last_num + 1
        return f"p{new_num:02d}"  # Format as p01, p02, ..., p10
    return "p01"

# Get the next image ID (001, 002, ..., 010, ...)
def get_next_image_id(cursor):
    cursor.execute("SELECT image_id FROM ProductImages ORDER BY image_id DESC LIMIT 1")
    last_id = cursor.fetchone()
    if last_id and last_id[0]:
        last_num = int(last_id[0])
        new_num = last_num + 1
        return f"{new_num:03d}"  # Format as 001, 002, ..., 010
    return "001"

# **GET - Fetch All Products or Specific Product**
@app.route("/products", methods=["GET"])
def get_products():
    """
    Fetch all products, products filtered by category ID, or products searched by keyword.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    category_id = request.args.get("category_id")  # Get category_id from query params
    search_query = request.args.get("search")  # Get search keyword from query params
    max_price = request.args.get("max_price") 
    
    try:
        if max_price:
            # Filter products by maximum price
            cursor.execute("""
                SELECT p.*, c.name AS category_name, s.name AS subcategory_name
                FROM Products p
                JOIN SubCategories s ON p.subcategory_id = s.subcategory_id
                JOIN Categories c ON s.category_id = c.category_id
                WHERE p.price <= %s
            """, (max_price,))

        elif search_query and category_id:
            # Search products by name or description within a specific category
            cursor.execute("""
                SELECT p.*, c.name AS category_name, s.name AS subcategory_name
                FROM Products p
                JOIN SubCategories s ON p.subcategory_id = s.subcategory_id
                JOIN Categories c ON s.category_id = c.category_id
                WHERE c.category_id = %s AND (LOWER(p.name) LIKE %s OR LOWER(p.description) LIKE %s)
            """, (category_id, f"%{search_query.lower()}%", f"%{search_query.lower()}%"))
        elif search_query:
            # Search products by name or description (case-insensitive)
            cursor.execute("""
                SELECT p.*, c.name AS category_name, s.name AS subcategory_name
                FROM Products p
                JOIN SubCategories s ON p.subcategory_id = s.subcategory_id
                JOIN Categories c ON s.category_id = c.category_id
                WHERE LOWER(p.name) LIKE %s OR LOWER(p.description) LIKE %s
            """, (f"%{search_query.lower()}%", f"%{search_query.lower()}%"))
        elif category_id:
            # Filter products by category ID
            cursor.execute("""
                SELECT p.*, c.name AS category_name, s.name AS subcategory_name
                FROM Products p
                JOIN SubCategories s ON p.subcategory_id = s.subcategory_id
                JOIN Categories c ON s.category_id = c.category_id
                WHERE c.category_id = %s
            """, (category_id,))
        else:
            # Fetch all products
            cursor.execute("""
                SELECT p.*, c.name AS category_name, s.name AS subcategory_name
                FROM Products p
                JOIN SubCategories s ON p.subcategory_id = s.subcategory_id
                JOIN Categories c ON s.category_id = c.category_id
            """)

        products = cursor.fetchall()
        for product in products:
            cursor.execute("SELECT image_url FROM ProductImages WHERE product_id = %s AND is_primary = TRUE", (product["product_id"],))
            image = cursor.fetchone()
            if image and image["image_url"]:
                # Ensure the image URL is constructed correctly
                #product["image_url"] = f"http://localhost:1000/static/uploads/{image['image_url'].split('/')[-1]}"
                product["image_url"] = f"http://127.0.0.1:1000/static/uploads/{image['image_url'].split('/')[-1]}"
            else:
                product["image_url"] = None

        return jsonify({"products": products}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# **POST - Add New Product**
@app.route("/save-product", methods=["POST"])
def save_product():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Retrieve form data
        subcategory_id = request.form.get("product-sub-category")  # Use the correct field name
        name = request.form.get("product-name")
        description = request.form.get("product-description")
        price = request.form.get("product-price")
        discount = request.form.get("product-discount", 0)
        stock = request.form.get("product-stock")
        weight = request.form.get("product-weight")
        dimensions = request.form.get("product-dimensions")
        specifications = request.form.get("product-specifications")
        tags = request.form.get("product-tags")
        status = request.form.get("product-status")

        # Validate required fields
        if not subcategory_id or not name or not price or not stock:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the subcategory_id exists in the SubCategories table
        cursor.execute("SELECT subcategory_id FROM SubCategories WHERE subcategory_id = %s", (subcategory_id,))
        subcategory = cursor.fetchone()
        if not subcategory:
            return jsonify({"error": f"Subcategory ID '{subcategory_id}' does not exist"}), 400

        # Generate the next product ID
        product_id = get_next_product_id(cursor)

        # Insert product into the database
        cursor.execute("""
            INSERT INTO Products (product_id, subcategory_id, name, description, price, 
                                  discount_percentage, stock_quantity, weight, dimensions, 
                                  specifications, tags, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (product_id, subcategory_id, name, description, price, discount, stock, 
              weight, dimensions, specifications, tags, status))

        # Handle product image upload
        if "product-image" in request.files:
            file = request.files["product-image"]
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                # Generate the next image ID
                image_id = get_next_image_id(cursor)

                # Insert image details into the database (store only the image name)
                cursor.execute("""
                    INSERT INTO ProductImages (image_id, product_id, image_url, is_primary) 
                    VALUES (%s, %s, %s, %s)
                """, (image_id, product_id, filename, True))  # Store only the image name

        # Commit the transaction
        conn.commit()
        return jsonify({"success": True, "message": "Product saved successfully!", "product_id": product_id}), 201

    except mysql.connector.Error as db_err:
        conn.rollback()
        print("Database error:", db_err)  # Log the database error
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        conn.rollback()
        print("Unexpected error:", e)  # Log the unexpected error
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# **PUT - Update Product**
@app.route("/update-product/<product_id>", methods=["PUT"])
def update_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        data = request.form
        update_query = """
            UPDATE Products SET name=%s, description=%s, price=%s, discount_percentage=%s, 
                                stock_quantity=%s, weight=%s, dimensions=%s, specifications=%s, 
                                tags=%s, status=%s WHERE product_id=%s
        """
        cursor.execute(update_query, (
            data.get("product-name"),
            data.get("product-description"),
            data.get("product-price"),
            data.get("product-discount"),
            data.get("product-stock"),
            data.get("product-weight"),
            data.get("product-dimensions"),
            data.get("product-specifications"),
            data.get("product-tags"),
            data.get("product-status"),
            product_id,
        ))

        if "product-image" in request.files:
            file = request.files["product-image"]
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                cursor.execute("DELETE FROM ProductImages WHERE product_id = %s", (product_id,))
                image_id = get_next_image_id(cursor)

                cursor.execute("""
                    INSERT INTO ProductImages (image_id, product_id, image_url, is_primary) 
                    VALUES (%s, %s, %s, %s)
                """, (image_id, product_id, filename, True))


        conn.commit()
        return jsonify({"success": True, "message": "Product updated successfully!"}), 200

    except mysql.connector.Error as db_err:
        conn.rollback()
        return jsonify({"error": f"Database error: {db_err}"}), 500
    finally:
        cursor.close()
        conn.close()

# **DELETE - Remove Product**
@app.route("/delete-product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM ProductImages WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404

        conn.commit()
        return jsonify({"success": True, "message": "Product deleted successfully!"}), 200

    except mysql.connector.Error as db_err:
        conn.rollback()
        return jsonify({"error": f"Database error: {db_err}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get-product-tags', methods=['GET'])
def get_product_tags():
    """
    Retrieve all unique product tags from the database and return them as JSON.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Fetch unique tags from the Products table
        cursor.execute("SELECT DISTINCT tags FROM Products WHERE tags IS NOT NULL AND tags != ''")
        tags_data = cursor.fetchall()

        # Flatten and split tags into a unique list
        tags = set()
        for row in tags_data:
            tags.update(tag.strip() for tag in row[0].split(','))

        return jsonify({"tags": list(tags)}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# User Registration
# User Registration
# @app.route('/user/register', methods=['POST'])
# def user_register():
#     try:
#         data = request.json
#         name = data.get('name')
#         email = data.get('email')
#         mobile_no = data.get('mobile_no')
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')

#         if not (name and email and mobile_no and password and confirm_password):
#             return jsonify({"error": "All fields are required"}), 400

#         if password != confirm_password:
#             return jsonify({"error": "Passwords do not match"}), 400

#         conn = get_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed"}), 500
        
#         cursor = conn.cursor()
#         cursor.execute("SELECT email FROM Users WHERE email = %s", (email,))
#         if cursor.fetchone():
#             return jsonify({"error": "Email already registered"}), 409

#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#         cursor.execute(
#             "INSERT INTO Users (name, email, mobile_no, password_hash) VALUES (%s, %s, %s, %s)",
#             (name, email, mobile_no, hashed_password)
#         )
#         conn.commit()
#         return jsonify({"message": "Registration successful"}), 201
#     except mysql.connector.Error as db_err:
#         return jsonify({"error": f"Database error: {db_err}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Internal error: {e}"}), 500
#     finally:
#         if conn:
#             conn.close()

# # User Login
# @app.route('/user/login', methods=['POST'])
# def user_login():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         if not email or not password:
#             return jsonify({"error": "Email and password are required"}), 400

#         conn = get_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed"}), 500
        
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT user_id, name, password_hash, is_blocked FROM Users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if not user:
#             return jsonify({"error": "Invalid email or password"}), 401

#         if user['is_blocked']:
#             return jsonify({"error": "Your account is blocked. Please contact support."}), 403

#         if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
#             cursor.execute("UPDATE Users SET last_login = NOW() WHERE user_id = %s", (user['user_id'],))
#             conn.commit()

#             session.clear()
#             session['logged_in'] = True
#             session['user_email'] = email
#             session['user_name'] = user['name']
#             session['user_id'] = user['user_id']
            
#             return jsonify({
#                 "message": f"Welcome back, {user['name']}!",
#                 "user_id": user['user_id'],
#                 "user_name": user['name']
#             }), 200
#         else:
#             return jsonify({"error": "Invalid email or password"}), 401
#     except mysql.connector.Error as db_err:
#         return jsonify({"error": f"Database error: {db_err}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Internal error: {e}"}), 500
#     finally:
#         if conn:
#             conn.close()

# # **New Endpoint: Check Login Status**
# @app.route('/user/status', methods=['GET'])
# def check_login_status():
#     try:
#         if session.get('logged_in'):
#             return jsonify({
#                 "message": f"User is logged in as {session['user_name']}",
#                 "user_id": session['user_id'],
#                 "user_email": session['user_email']
#             }), 200
#         else:
#             return jsonify({"message": "User is not logged in."}), 401
#     except Exception as e:
#         return jsonify({"error": f"Internal error: {e}"}), 500

# #User Logout
# @app.route('/user/logout', methods=['POST'])
# def user_logout():
#     session.clear()
#     return jsonify({"message": "Logout successful"}), 200


# User Registration
# @app.route('/user/register', methods=['POST'])
# def user_register():
#     try:
#         data = request.json
#         name = data.get('name')
#         email = data.get('email')
#         mobile_no = data.get('mobile_no')
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')

#         if not all([name, email, mobile_no, password, confirm_password]):
#             return jsonify({"error": "All fields are required"}), 400

#         if password != confirm_password:
#             return jsonify({"error": "Passwords do not match"}), 400

#         conn = get_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed"}), 500
#         cursor = conn.cursor()
#         cursor.execute("SELECT email FROM Users WHERE email = %s", (email,))
#         if cursor.fetchone():
#             return jsonify({"error": "Email already registered"}), 409

#         hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#         cursor.execute("INSERT INTO Users (name, email, mobile_no, password_hash) VALUES (%s, %s, %s, %s)",
#                        (name, email, mobile_no, hashed_password))
#         conn.commit()
#         return jsonify({"message": "Registration successful"}), 201
#     finally:
#         if conn:
#             conn.close()

# @app.route('/user/login', methods=['POST'])
# def user_login():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         conn = get_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed"}), 500

#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT user_id, name, email, password_hash FROM Users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if not user or not bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
#             return jsonify({"error": "Invalid email or password"}), 401

#         token = jwt.encode(
#             {"user_id": user["user_id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
#             app.config["SECRET_KEY"], algorithm="HS256"
#         )

#         return jsonify({"message": f"Welcome, {user['name']}!", "token": token}), 200
#     finally:
#         if conn:
#             conn.close()

# @app.route('/user/info', methods=['GET'])
# def get_user_info():
#     token = request.headers.get("Authorization")
#     if not token:
#         return jsonify({"error": "Token is missing"}), 401

#     try:
#         decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
#         user_id = decoded_token["user_id"]

#         conn = get_connection()
#         if not conn:
#             return jsonify({"error": "Database connection failed"}), 500

#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT name, email FROM Users WHERE user_id = %s", (user_id,))
#         user = cursor.fetchone()
#         return jsonify(user), 200
#     except jwt.ExpiredSignatureError:
#         return jsonify({"error": "Token expired, please log in again"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"error": "Invalid token"}), 401
#     finally:
#         if conn:
#             conn.close()

#add to cart
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    """
    Adds a product to the user's cart. Updates quantity if already present.
    Removes the item if quantity is reduced to zero.
    """
    try:
        # Check if the user is logged in
        if not session.get('logged_in'):
            return jsonify({"error": "You must be logged in to add items to the cart."}), 403

        user_id = session.get('user_id')  # Get the logged-in user's ID
        data = request.json  # Parse JSON data from the request
        product_id = data.get('product_id')  # Get the product ID
        quantity = data.get('quantity', 1)  # Default quantity is 1

        # Validate product ID and quantity
        if not product_id or quantity < 0:
            return jsonify({"error": "Valid product ID and non-negative quantity are required."}), 400

        # Establish database connection
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection error"}), 500
        
        cursor = conn.cursor(dictionary=True)

        # Ensure the product exists in the Products table
        cursor.execute("SELECT stock_quantity FROM Products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Check if the requested quantity exceeds the available stock
        if quantity > product['stock_quantity']:
            return jsonify({"error": "Requested quantity exceeds available stock"}), 400

        # Ensure the user has a cart
        cursor.execute("SELECT cart_id FROM Carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if not cart:
            # Create a new cart for the user if it doesn't exist
            cursor.execute("INSERT INTO Carts (user_id) VALUES (%s)", (user_id,))
            conn.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart['cart_id']

        # Check if the product already exists in the cart
        cursor.execute("SELECT quantity FROM CartItems WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            # Update the quantity if the product is already in the cart
            new_quantity = cart_item['quantity'] + quantity

            if new_quantity <= 0:
                # Remove the product from the cart if the quantity is zero or less
                cursor.execute("DELETE FROM CartItems WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            else:
                # Update the quantity in the cart
                cursor.execute("UPDATE CartItems SET quantity = %s WHERE cart_id = %s AND product_id = %s",
                               (new_quantity, cart_id, product_id))
        else:
            # Add the product to the cart if it doesn't already exist
            if quantity > 0:
                cursor.execute("INSERT INTO CartItems (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
                               (cart_id, product_id, quantity))

        # Commit the changes to the database
        conn.commit()
        return jsonify({"message": "Cart updated successfully"}), 200

    except mysql.connector.Error as db_err:
        # Handle database errors
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        # Handle other errors
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        # Close the database connection
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

#  Get Cart Route (Unchanged)
@app.route('/get-cart', methods=['GET'])
def get_cart():
    """
    Fetches the cart items for the logged-in user.
    """
    try:
        if not session.get('logged_in'):
            return jsonify({"error": "You must be logged in to view your cart."}), 403

        user_id = session.get('user_id')
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT cart_id FROM Carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if not cart:
            return jsonify({"cartItems": []}), 200

        cart_id = cart['cart_id']

        # Fetch cart items with product details
        cursor.execute("""
            SELECT ci.product_id, p.name, p.price, ci.quantity, pi.image_url
            FROM CartItems ci
            JOIN Products p ON ci.product_id = p.product_id
            LEFT JOIN ProductImages pi ON p.product_id = pi.product_id AND pi.is_primary = TRUE
            WHERE ci.cart_id = %s
        """, (cart_id,))

        cart_items = cursor.fetchall()

        for item in cart_items:
            if item['image_url']:
                # item['image_url'] = f"http://localhost:1000/static/uploads/{item['image_url']}"
                item['image_url'] = f"http://127.0.0.1:1000/static/uploads/{item['image_url']}"

        return jsonify({"cartItems": cart_items}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


#  Update Item Quantity Route (New)
@app.route('/update-cart', methods=['POST'])
def update_cart():
    try:
        # Check if the user is logged in
        if not session.get('logged_in'):
            return jsonify({"error": "You must be logged in to update the cart."}), 403

        user_id = session.get('user_id')
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # Validate input
        if not product_id or quantity < 1:
            return jsonify({"error": "Invalid product ID or quantity."}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the product exists in the user's cart
        cursor.execute("SELECT * FROM CartItems WHERE product_id = %s AND cart_id = (SELECT cart_id FROM Carts WHERE user_id = %s)", (product_id, user_id))
        cart_item = cursor.fetchone()

        if not cart_item:
            return jsonify({"error": "Product not found in cart."}), 404

        # Update the quantity in the cart
        cursor.execute("UPDATE CartItems SET quantity = %s WHERE product_id = %s AND cart_id = (SELECT cart_id FROM Carts WHERE user_id = %s)", (quantity, product_id, user_id))
        conn.commit()

        return jsonify({"message": "Cart updated successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


#  Remove Item from Cart Route (Unchanged)
@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    """
    Removes a specific product from the user's cart.
    """
    try:
        if not session.get('logged_in'):
            return jsonify({"error": "You must be logged in to modify your cart."}), 403

        user_id = session.get('user_id')
        data = request.json
        product_id = data.get('product_id')

        if not product_id:
            return jsonify({"error": "Product ID is required."}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT cart_id FROM Carts WHERE user_id = %s", (user_id,))
        cart = cursor.fetchone()

        if not cart:
            return jsonify({"message": "Cart is empty"}), 200

        cart_id = cart['cart_id']

        cursor.execute("DELETE FROM CartItems WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
        conn.commit()

        return jsonify({"message": "Product removed from cart"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# # Fetch all users
# @app.route("/get-users", methods=["GET"])
# def get_users():
#     connection = get_connection()
#     if not connection:
#         return jsonify({"error": "Database connection failed"}), 500
    
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT user_id, name, email, is_blocked FROM Users")
#     users = cursor.fetchall()
#     connection.close()
    
#     # Convert is_blocked boolean to 'Active' or 'Blocked'
#     for user in users:
#         user["status"] = "Blocked" if user["is_blocked"] else "Active"
#         del user["is_blocked"]
    
#     return jsonify(users)

# # Update user status
# @app.route("/update-user-status", methods=["POST"])
# def update_user_status():
#     data = request.json
#     user_id = data.get("user_id")
#     new_status = data.get("status")
    
#     if user_id is None or new_status not in ["Active", "Blocked"]:
#         return jsonify({"error": "Invalid request data"}), 400
    
#     is_blocked = 1 if new_status == "Blocked" else 0
    
#     connection = get_connection()
#     if not connection:
#         return jsonify({"error": "Database connection failed"}), 500
    
#     cursor = connection.cursor()
#     cursor.execute("UPDATE Users SET is_blocked = %s WHERE user_id = %s", (is_blocked, user_id))
#     connection.commit()
#     connection.close()
    
#     return jsonify({"message": "User status updated successfully"})


# # -------------------- Signup Route --------------------
# @app.route("/user/signup", methods=["POST"])
# def signup_rps():
#     data = request.get_json()
#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")

#     if not (name and email and password):
#         return jsonify({"message": "All fields are required"}), 400

#     hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#     conn = get_connection()
#     if not conn:
#         return jsonify({"message": "Database connection error"}), 500
#     cursor = conn.cursor()

#     try:
#         cursor.execute("INSERT INTO Users (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, hashed_password))
#         conn.commit()
#         return jsonify({"message": "User registered successfully!"}), 201
#     except mysql.connector.IntegrityError:
#         return jsonify({"message": "Email already exists"}), 409
#     finally:
#         cursor.close()
#         conn.close()


# # # -------------------- Login Route --------------------
# @app.route("/user/login", methods=["POST"])
# def login_rps():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     conn = get_connection()
#     if not conn:
#         return jsonify({"message": "Database connection error"}), 500
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
#     user = cursor.fetchone()

#     if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
#         session["user_id"] = user["user_id"]
#         session["username"] = user["name"]
#         session["email"] = user["email"]
#         cursor.execute("UPDATE Users SET last_login = %s WHERE user_id = %s", (datetime.now(), user["user_id"]))
#         conn.commit()
#         return jsonify({
#             "message": "Login successful!",
#             "username": user["name"],
#             "redirect": "index.html"
#         }), 200
#     else:
#         return jsonify({"message": "Invalid email or password"}), 401
#     # finally:
#     #     cursor.close()
#     #     conn.close()



# # -------------------- Profile Route --------------------
# @app.route("/user/profile")
# def profile():
#     username = session.get("username")
#     if username:
#         return jsonify({"message": f"Hello, {username}!"})
#     else:
#         return jsonify({"message": "Not logged in"}), 401


# # -------------------- Logout Route --------------------
# @app.route("/user/logout")
# def logout():
#     session.clear()
#     return jsonify({"message": "Logged out successfully!"})

#Route for managing both GET (fetch contacts) and POST (add new contact)
@app.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if request.method == 'GET':
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT * FROM contacts")
            contacts = cursor.fetchall()
            return jsonify(contacts), 200
        except Exception as e:
            return jsonify({"error": f"Failed to fetch contacts: {str(e)}"}), 500
        finally:
            cursor.close()
            connection.close()

    # elif request.method == 'POST':
    #     data = request.get_json()
    #     name = data.get('name', '')
    #     email = data.get('email', '')
    #     phone = data.get('phone', '')
    #     message = data.get('message', '')

    #     if not name or not email or not phone:
    #         return jsonify({"error": "Missing required fields: name, email, or phone"}), 400

    #     connection = get_connection()
    #     cursor = connection.cursor()

    #     try:
    #         insert_query = """
    #             INSERT INTO contacts (name, email, phone, message)
    #             VALUES (%s, %s, %s, %s)
    #         """
    #         cursor.execute(insert_query, (name, email, phone, message))
    #         connection.commit()

    #         # send_email_notification(name, email, phone, message)

    #         return jsonify({"message": "Contact added successfully!"}), 201
    #     except Exception as e:
    #         return jsonify({"error": f"Failed to add contact: {str(e)}"}), 500
    #     finally:
    #         cursor.close()
    #         connection.close()
    elif request.method == 'POST':
        try:
            data = request.get_json(force=True)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            message = data.get('message', '').strip()

            if not name or not email or not phone:
                return jsonify({"error": "Missing required fields: name, email, or phone"}), 400

            connection = get_connection()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO contacts (name, email, phone, message)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, email, phone, message))
            connection.commit()

            return jsonify({"message": "Contact added successfully!"}), 201

        except Exception as e:
            return jsonify({"error": f"Failed to add contact: {str(e)}"}), 500
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'connection' in locals(): connection.close()

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
        contact_item = cursor.fetchone()

        if not contact_item:
            return jsonify({"error": "Contact not found!"}), 404

        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        connection.commit()

        return jsonify({"message": "Contact deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete contact: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()


# @app.route('/users/login', methods=['POST'])
# def login_user():
#     """
#     Login route for users.
#     """
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     data = request.json  # Get JSON data from request
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"error": "Email and password are required"}), 400

#     query = "SELECT user_id, name, email, password_hash, is_blocked FROM Users WHERE email = %s"
#     values = (email,)

#     try:
#         cursor.execute(query, values)
#         user = cursor.fetchone()

#         if not user:
#             return jsonify({"error": "Invalid email or password"}), 401

#         if user['is_blocked']:
#             return jsonify({"error": "Your account is blocked. Please contact support."}), 403

#         # Verify password hash
#         if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
#             session['logged_in'] = True
#             session['user_id'] = user['user_id']
#             session['user_email'] = user['email']

#             # Update last login timestamp
#             update_query = "UPDATE Users SET last_login = %s WHERE user_id = %s"
#             cursor.execute(update_query, (datetime.now(), user['user_id']))
#             conn.commit()

#             # Return the username and redirect URL
#             return jsonify({
#                 "message": "Login successful",
#                 "username": user['name'],  # Send the username
#                 "redirect": "index.html"  # Redirect to the homepage or dashboard
#             }), 200
#         else:
#             return jsonify({"error": "Invalid email or password"}), 401

#     except mysql.connector.Error as db_err:
#         return jsonify({"error": f"Database error: {db_err}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Internal error: {e}"}), 500
#     finally:
#         cursor.close()
#         conn.close()

# @app.route('/users/checkout', methods=['POST'])
# def save_billing_details():
#     """
#     Save the user's billing details and place the order.
#     """
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     data = request.json  # Get JSON data from request
#     user_id = session.get('user_id')  # Get user_id from the session
#     if not user_id:
#         return jsonify({"error": "User not logged in"}), 401  # Ensure user is logged in

#     # Extract fields from the request
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     company_name = data.get('company_name')
#     address = data.get('address')
#     city = data.get('city')
#     country = data.get('country')
#     postcode = data.get('postcode')
#     mobile = data.get('mobile')
#     email = data.get('email')
#     order_notes = data.get('order_notes', '')
#     cart_items = data.get('cart_items')  # List of products in the cart
#     total_amount = data.get('total_amount')  # Total amount for the order
#     delivery_address = address  # Assuming the address is the delivery address
#     contact_info = mobile  # Contact info is mobile here
#     delivery_time_preference = data.get('delivery_time_preference', 'No preference')

#     # Validate required fields
#     if not all([first_name, last_name, address, city, country, postcode, mobile, email, cart_items, total_amount]):
#         return jsonify({"error": "All required fields must be provided"}), 400

#     try:
#         # Step 1: Insert billing details into the BillingDetails table
#         query = """
#             INSERT INTO BillingDetails (
#                 user_id, first_name, last_name, company_name, address, city, country,
#                 postcode, mobile, email, order_notes
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             user_id, first_name, last_name, company_name, address, city, country,
#             postcode, mobile, email, order_notes
#         )
#         cursor.execute(query, values)
#         conn.commit()

#         billing_id = cursor.lastrowid  # Get the billing_id of the newly inserted record

#         # Step 2: Insert order details into the Orders table
#         query_order = """
#             INSERT INTO Orders (
#                 user_id, total_amount, delivery_address, contact_info, delivery_time_preference, billing_id
#             ) VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         values_order = (
#             user_id, total_amount, delivery_address, contact_info, delivery_time_preference, billing_id
#         )
#         cursor.execute(query_order, values_order)
#         conn.commit()

#         order_id = cursor.lastrowid  # Get the order_id of the newly inserted order

#         # Step 3: Insert order items into the OrderItems table
#         for item in cart_items:
#             query_item = """
#                 INSERT INTO OrderItems (order_id, product_id, quantity, price_at_purchase)
#                 VALUES (%s, %s, %s, %s)
#             """
#             cursor.execute(query_item, (order_id, item['product_id'], item['quantity'], item['price']))
        
#         conn.commit()

#         # Step 4: Return the order ID and success message
#         return jsonify({
#             "message": "Billing details saved and order placed successfully",
#             "order_id": order_id
#         }), 200

#     except mysql.connector.Error as db_err:
#         return jsonify({"error": f"Database error: {db_err}"}), 500
#     except Exception as e:
#         return jsonify({"error": f"Internal error: {e}"}), 500
#     finally:
#         cursor.close()
#         conn.close()


# -------------------- Fetch All Users --------------------
@app.route("/get-users", methods=["GET"])
def get_users():
    """Fetch all users from the database"""
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, is_blocked FROM Users")
    users = cursor.fetchall()
    conn.close()

    # Convert is_blocked boolean to 'Active' or 'Blocked'
    for user in users:
        user["status"] = "Blocked" if user["is_blocked"] else "Active"
        del user["is_blocked"]

    return jsonify(users)

# -------------------- Update User Status --------------------
@app.route("/update-user-status", methods=["POST"])
def update_user_status():
    """Update user status (Active/Blocked)"""
    data = request.json
    user_id = data.get("user_id")
    new_status = data.get("status")

    if not user_id or new_status not in ["Active", "Blocked"]:
        return jsonify({"error": "Invalid request data"}), 400

    is_blocked = 1 if new_status == "Blocked" else 0

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET is_blocked = %s WHERE user_id = %s", (is_blocked, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User status updated successfully"})


# -------------------- User Signup --------------------
@app.route("/user/signup", methods=["POST"])
def signup_rps():
    """User registration"""
    data = request.json
    name = data.get("name")
    email = data.get("email")
    mobile_no = data.get("mobile_no")  # Ensure mobile_no is included
    password = data.get("password")

    if not all([name, email, mobile_no, password]):
        return jsonify({"error": "All fields are required"}), 400

    # ✅ Use a strong hashing method explicitly
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (name, email, mobile_no, password_hash) VALUES (%s, %s, %s, %s)", 
                       (name, email, mobile_no, hashed_password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        cursor.close()
        conn.close()


# -------------------- User Login --------------------
## User Login
@app.route("/user/login", methods=["POST"])
def login_rps():
    """User login"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection error"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, name, email, password_hash, is_blocked FROM Users WHERE email = %s",
            (email,),
        )
        user = cursor.fetchone()

        if user:
            if user["is_blocked"]:
                conn.close()
                return jsonify({"error": f"{user['name']} is blocked by admin"}), 403
            # ✅ Ensure the password hash exists
            if not user["password_hash"]:
                conn.close()
                return jsonify({"error": "Invalid stored password hash"}), 500
            
            if check_password_hash(user["password_hash"], password):
                # Set session variables
                session["logged_in"] = True
                session["user_id"] = user["user_id"]
                session["username"] = user["name"]
                session["email"] = user["email"]

                # Update last login timestamp
                cursor.execute(
                    "UPDATE Users SET last_login = %s WHERE user_id = %s",
                    (datetime.now(), user["user_id"]),
                )
                conn.commit()

                conn.close()
                return jsonify({"message": "Login successful", "username": user["name"]}), 200
            else:
                conn.close()
                return jsonify({"error": "Invalid email or password"}), 401
        else:
            conn.close()
            return jsonify({"error": "Invalid email or password"}), 401

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500



# -------------------- User Profile --------------------
@app.route("/user/status", methods=["GET"])
def user_status():
    """Check if user is logged in"""
    if session.get("logged_in"):
        return jsonify({"username": session["username"]}), 200
    return jsonify({"username": None}), 200


# -------------------- User Logout --------------------
@app.route("/user/logout", methods=["POST"])
def logout_rps():
    """User logout"""
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# POST: Insert billing details
# @app.route('/billing', methods=['POST'])
# def add_billing():
#     data = request.json

#     # Validate required fields
#     required_fields = ["user_id", "first_name", "last_name", "address", "city", "country", "postcode", "mobile", "email"]
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return jsonify({'error': f'Missing required field: {field}'}), 400

#     connection = get_connection()
#     cursor = connection.cursor()

#     query = """
#         INSERT INTO BillingDetails (user_id, first_name, last_name, address, city, country, postcode, mobile, email, order_notes)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     values = (
#         data['user_id'], data['first_name'], data['last_name'], data['address'],
#         data['city'], data['country'], data['postcode'], data['mobile'], data['email'], data.get('order_notes', '')
#     )

#     try:
#         cursor.execute(query, values)
#         connection.commit()
#         return jsonify({'message': 'Billing details added successfully'}), 201
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()

@app.route('/users/checkout', methods=['POST'])
def save_billing_details():
    """
    Save the user's billing details and place the order.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "User not logged in"}), 401  # Ensure user is logged in

    user_id = session.get("user_id")  # Get user ID from session
    if not user_id:
        return jsonify({"error": "Session error: Unable to retrieve user details"}), 500

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        data = request.json  # Get JSON data from request
        
        # Extract required fields
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        address = data.get('address')
        city = data.get('city')
        country = data.get('country')
        postcode = data.get('postcode')
        mobile = data.get('mobile')
        email = data.get('email')
        order_notes = data.get('order_notes', '')  # Optional
        cart_items = data.get('cart_items')  # List of products in the cart
        total_amount = data.get('total_amount')  # Total order amount
        payment_method = data.get('payment_method')  # New field for payment method
        delivery_address = address  # Use billing address as delivery address
        contact_info = mobile  # Use mobile number as contact info
        delivery_time_preference = data.get('delivery_time_preference', 'No preference')

        # Validate required fields
        if not all([first_name, last_name, address, city, country, postcode, mobile, email, cart_items, total_amount, payment_method]):
            return jsonify({"error": "All required fields must be provided"}), 400

        # Start transaction
        conn.start_transaction()

        # Step 1: Insert billing details into the BillingDetails table
        query_billing = """
            INSERT INTO BillingDetails (
                user_id, first_name, last_name, address, city, country,
                postcode, mobile, email, order_notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_billing, (
            user_id, first_name, last_name, address, city, country,
            postcode, mobile, email, order_notes
        ))

        # Step 2: Generate a unique 5-digit Order ID
        custom_order_id = random.randint(10000, 99999)

        # Step 3: Insert order details into the Orders table
        query_order = """
            INSERT INTO Orders (
                order_id, user_id, total_amount, delivery_address, contact_info, 
                delivery_time_preference, payment_method, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
        """
        cursor.execute(query_order, (
            custom_order_id, user_id, total_amount, delivery_address, 
            contact_info, delivery_time_preference, payment_method
        ))

        # Step 4: Insert order items into the OrderItems table
        for item in cart_items:
            query_item = """
                INSERT INTO OrderItems (order_id, product_id, quantity, price_at_purchase)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_item, (custom_order_id, item['product_id'], item['quantity'], item['price']))
        
        # Commit transaction
        conn.commit()

         # Step 5: Insert payment details into Payments table
        payment_status = "Completed" if payment_method == "COD" else "Pending"
        transaction_id = "N/A" if payment_method == "COD" else f"TXN{random.randint(100000, 999999)}"

        query_payment = """
            INSERT INTO Payments (
                order_id, transaction_id, amount, payment_method, status, payment_date
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_payment, (
            custom_order_id, transaction_id, total_amount, payment_method, payment_status, datetime.now()
        ))

        # Commit transaction
        conn.commit()

        # Step 6: Return success response with the Order ID
        return jsonify({
            "message": "Billing details saved and order placed successfully",
            "order_id": custom_order_id
        }), 200

    except mysql.connector.Error as db_err:
        conn.rollback()  # Rollback transaction in case of DB error
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/users/checkout', methods=['GET'])
def get_checkout_details():
    """
    Retrieve the most recent checkout details for the logged-in user.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "User not logged in"}), 401

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Session error: Unable to retrieve user details"}), 500

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Step 1: Get the latest order by user_id
        cursor.execute("""
            SELECT * FROM Orders 
            WHERE user_id = %s 
            ORDER BY order_id DESC LIMIT 1
        """, (user_id,))
        order = cursor.fetchone()

        if not order:
            return jsonify({"message": "No orders found for this user"}), 404

        order_id = order['order_id']

        # Step 2: Get billing details
        cursor.execute("""
            SELECT * FROM BillingDetails 
            WHERE user_id = %s 
            ORDER BY billing_id DESC LIMIT 1
        """, (user_id,))
        billing = cursor.fetchone()

        # Step 3: Get order items with product images
        cursor.execute("""
            SELECT OI.*, P.name AS product_name, PI.image_url 
            FROM OrderItems OI
            JOIN Products P ON OI.product_id = P.product_id
            LEFT JOIN ProductImages PI ON OI.product_id = PI.product_id AND PI.is_primary = TRUE
            WHERE OI.order_id = %s
        """, (order_id,))
        items = cursor.fetchall()

        # Modify image URLs to include full path
        for item in items:
            # item['product_image'] = f"http://localhost:1000/static/uploads/{item['image_url']}" if item['image_url'] else "http://localhost:1000/static/uploads/default.jpg"
            item['product_image'] = f"http://127.0.0.1:1000/static/uploads/{item['image_url']}" if item['image_url'] else "http://127.0.0.1:1000/static/uploads/default.jpg"

        # Step 4: Get payment info
        cursor.execute("""
            SELECT * FROM Payments 
            WHERE order_id = %s
        """, (order_id,))
        payment = cursor.fetchone()

        # Step 5: Combine everything into a response
        return jsonify({
            "order_id": order_id,
            "billing_details": billing,
            "order": order,
            "items": items,
            "payment": payment
        }), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/admin/checkout', methods=['GET'])
def get_details():
    """
    Retrieve detailed checkout information for all users.
    Includes orders, order items, product details, and billing info.
    """
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection error"}), 500

    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                o.order_id,
                o.user_id,
                o.total_amount,
                o.status AS order_status,
                o.delivery_address,
                o.contact_info,
                o.delivery_time_preference,
                oi.product_id,
                p.name AS product_name,
                oi.quantity,
                oi.price_at_purchase,
                b.first_name,
                b.last_name,
                b.address AS billing_address,
                b.city,
                b.country,
                b.postcode,
                b.mobile,
                b.email,
                b.order_notes
            FROM Orders o
            JOIN OrderItems oi ON o.order_id = oi.order_id
            JOIN Products p ON oi.product_id = p.product_id
            JOIN BillingDetails b ON o.user_id = b.user_id
            ORDER BY o.order_date DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return jsonify({"message": "No checkout details available"}), 404

        # Group by order_id for better structure
        orders = {}
        for row in results:
            order_id = row["order_id"]
            if order_id not in orders:
                orders[order_id] = {
                    "order_id": order_id,
                    "user_id": row["user_id"],
                    "total_amount": row["total_amount"],
                    "order_status": row["order_status"],
                    "delivery_address": row["delivery_address"],
                    "contact_info": row["contact_info"],
                    "delivery_time_preference": row["delivery_time_preference"],
                    "billing_details": {
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "address": row["billing_address"],
                        "city": row["city"],
                        "country": row["country"],
                        "postcode": row["postcode"],
                        "mobile": row["mobile"],
                        "email": row["email"],
                        "order_notes": row["order_notes"]
                    },
                    "products": []
                }
            
            # Append each product in the order
            orders[order_id]["products"].append({
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "quantity": row["quantity"],
                "price_at_purchase": row["price_at_purchase"]
            })

        return jsonify(list(orders.values())), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
# # GET: Retrieve billing details for a specific user
# @app.route('/billing/<int:user_id>', methods=['GET'])
# def get_billing(user_id):
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     query = "SELECT * FROM BillingDetails WHERE user_id = %s"
#     cursor.execute(query, (user_id,))
#     result = cursor.fetchall()

#     cursor.close()
#     connection.close()

#     if result:
#         return jsonify(result), 200
#     return jsonify({'message': 'No billing details found'}), 404

@app.route('/payment_list', methods=['GET'])
def get_payment():
    """
    For admin dashboard - fetches all payment records.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # To get results as dictionaries
    try:
        cursor.execute("SELECT * FROM Payments")
        payments = cursor.fetchall()
        payment_list = []

        for payment in payments:
            payment_list.append({
                "payment_id": payment["payment_id"],
                "order_id": payment["order_id"],
                "transaction_id": payment["transaction_id"],
                "amount": float(payment["amount"]),
                "payment_method": payment["payment_method"],
                "status": payment["status"],
                "payment_date": payment["payment_date"].strftime("%Y-%m-%d %H:%M:%S") if payment["payment_date"] else None
            })

        return jsonify(payment_list), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/payment_list/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """
    Update a payment record by payment_id.
    Expected JSON body: any of the fields like amount, payment_method, status, payment_date
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Build update query dynamically
        fields = []
        values = []
        allowed_fields = ['amount', 'payment_method', 'status', 'payment_date']

        for field in allowed_fields:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])

        if not fields:
            return jsonify({"error": "No valid fields to update"}), 400

        values.append(payment_id)
        query = f"UPDATE Payments SET {', '.join(fields)} WHERE payment_id = %s"

        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No record found with the given payment_id"}), 404

        return jsonify({"message": "Payment updated successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/payment_list/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """
    Delete a payment record by payment_id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Payments WHERE payment_id = %s", (payment_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No record found with the given payment_id"}), 404

        return jsonify({"message": "Payment deleted successfully"}), 200

    except mysql.connector.Error as db_err:
        return jsonify({"error": f"Database error: {db_err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=1000)
