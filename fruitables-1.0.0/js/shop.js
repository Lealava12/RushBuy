document.addEventListener("DOMContentLoaded", () => {
    const API_BASE_URL = "http://lealavaecommerce.com/api"; // Backend API URL
    const productContainer = document.querySelector(".row.g-4.justify-content-center");
    const categoryList = document.querySelector(".fruite-categorie");
    const searchInput = document.querySelector("input[type='search']");
    const sortSelect = document.getElementById("fruits");
    const priceRange = document.getElementById("rangeInput");
    const additionalFilters = document.querySelectorAll("input[name='Categories-1']");

    // Fetch and display products
    async function fetchProducts(filters = {}) {
        try {
            let query = new URLSearchParams(filters).toString();
            const response = await fetch(`${API_BASE_URL}/products?${query}`);
            if (!response.ok) throw new Error("Failed to fetch products");

            const data = await response.json();
            productContainer.innerHTML = "";

            if (data.products.length === 0) {
                productContainer.innerHTML = `<p class="text-center">No products found.</p>`;
                return;
            }

            data.products.forEach(product => {
                productContainer.innerHTML += `
                    <div class="col-md-6 col-lg-4 col-xl-3">
                        <div class="rounded position-relative fruite-item">
                            <div class="fruite-img">
                                <img src="${product.image_url || 'img/default.jpg'}" class="img-fluid w-100 rounded-top" alt="${product.name}">
                            </div>
                            <div class="text-white bg-secondary px-3 py-1 rounded position-absolute" style="top: 10px; left: 10px;">${product.category_name}</div>
                            <div class="p-4 border border-secondary border-top-0 rounded-bottom">
                                <h4>${product.name}</h4>
                                <p>${product.description || "No description available."}</p>
                                <div class="d-flex justify-content-between flex-lg-wrap">
                                    <p class="text-dark fs-5 fw-bold mb-0">${product.price} ₹</p>
                                    <button class="btn border border-secondary rounded-pill px-3 text-primary add-to-cart"><i class="fa fa-shopping-bag me-2 text-primary"></i> Add to cart</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
        } catch (error) {
            console.error("Error fetching products:", error);
            productContainer.innerHTML = `<p class="text-center text-danger">Failed to load products. Please try again later.</p>`;
        }
    }

    // Fetch and display categories
    async function fetchCategories() {
        try {
            const response = await fetch(`${API_BASE_URL}/get-categories`);
            if (!response.ok) throw new Error("Failed to fetch categories");

            const data = await response.json();
            categoryList.innerHTML = "";

            data.categories.forEach(category => {
                categoryList.innerHTML += `
                    <li>
                        <div class="d-flex justify-content-between fruite-name">
                            <label>
                                <input type="checkbox" class="category-filter me-2" value="${category.category_id}">
                                ${category.name}
                            </label>
                        </div>
                    </li>
                `;
            });

            // Add event listeners to category checkboxes
            document.querySelectorAll(".category-filter").forEach(checkbox => {
                checkbox.addEventListener("change", applyFilters);
            });
        } catch (error) {
            console.error("Error fetching categories:", error);
            categoryList.innerHTML = `<p class="text-danger">Failed to load categories.</p>`;
        }
    }

    // Apply filters
    function applyFilters() {
        const filters = {};

        // Search filter
        const searchValue = searchInput.value.trim();
        if (searchValue) filters.search = searchValue;

        // Sorting filter
        const sortValue = sortSelect.value;
        if (sortValue !== "volvo") filters.sort = sortValue;

        // Price filter
        const priceValue = priceRange.value;
        if (priceValue) filters.max_price = priceValue;

        // Additional filters
        const selectedAdditionalFilter = Array.from(additionalFilters).find(filter => filter.checked);
        if (selectedAdditionalFilter) filters.additional = selectedAdditionalFilter.value;

        // Category filters
        const selectedCategories = Array.from(document.querySelectorAll(".category-filter:checked")).map(cb => cb.value);
        if (selectedCategories.length > 0) filters.categories = selectedCategories.join(",");

        fetchProducts(filters);
    }

    // Event listeners
    searchInput.addEventListener("input", applyFilters);
    sortSelect.addEventListener("change", applyFilters);
    priceRange.addEventListener("input", applyFilters);
    additionalFilters.forEach(filter => filter.addEventListener("change", applyFilters));

    // Initial load
    fetchCategories();
    fetchProducts();
});
