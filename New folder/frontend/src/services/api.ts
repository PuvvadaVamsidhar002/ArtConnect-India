import axios from 'axios';

// Base URL for API requests
const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor to include auth token in requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Product API services
export const productService = {
  // Get all products with pagination
  getProducts: async (page = 1, perPage = 20) => {
    try {
      const response = await apiClient.get(`/products?page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  // Get product by ID
  getProductById: async (productId) => {
    try {
      const response = await apiClient.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching product ${productId}:`, error);
      throw error;
    }
  },

  // Get products by category
  getProductsByCategory: async (categoryId, page = 1, perPage = 20) => {
    try {
      const response = await apiClient.get(`/products/category/${categoryId}?page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching products for category ${categoryId}:`, error);
      throw error;
    }
  },

  // Search products
  searchProducts: async (query, page = 1, perPage = 20) => {
    try {
      const response = await apiClient.get(`/products/search?q=${encodeURIComponent(query)}&page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error(`Error searching products with query "${query}":`, error);
      throw error;
    }
  }
};

// Artisan API services
export const artisanService = {
  // Get all artisans with pagination
  getArtisans: async (page = 1, perPage = 20) => {
    try {
      const response = await apiClient.get(`/artisans?page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching artisans:', error);
      throw error;
    }
  },

  // Get artisan by ID
  getArtisanById: async (artisanId) => {
    try {
      const response = await apiClient.get(`/artisans/${artisanId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching artisan ${artisanId}:`, error);
      throw error;
    }
  }
};

// Partner API services
export const partnerService = {
  // Get all partners with pagination
  getPartners: async (page = 1, perPage = 20) => {
    try {
      const response = await apiClient.get(`/partners?page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching partners:', error);
      throw error;
    }
  },

  // Get partners for a specific product
  getPartnersByProduct: async (productId) => {
    try {
      const response = await apiClient.get(`/partners/product/${productId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching partners for product ${productId}:`, error);
      throw error;
    }
  }
};

// QR Code API services
export const qrCodeService = {
  // Get QR code for a product
  getProductQRCode: async (productId) => {
    try {
      // This returns the URL to the QR code image
      return `${API_BASE_URL}/qrcode/product/${productId}`;
    } catch (error) {
      console.error(`Error getting QR code for product ${productId}:`, error);
      throw error;
    }
  },

  // Get transparency data for a product
  getTransparencyData: async (productId) => {
    try {
      const response = await apiClient.get(`/transparency/${productId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching transparency data for product ${productId}:`, error);
      throw error;
    }
  }
};

// Authentication API services
export const authService = {
  // Register a new user
  register: async (userData) => {
    try {
      const response = await apiClient.post('/auth/register', userData);
      if (response.data.access_token) {
        localStorage.setItem('accessToken', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
      }
      return response.data;
    } catch (error) {
      console.error('Error registering user:', error);
      throw error;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await apiClient.post('/auth/login', credentials);
      if (response.data.access_token) {
        localStorage.setItem('accessToken', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
      }
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    return true;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('accessToken');
  }
};

// Order API services
export const orderService = {
  // Get user orders
  getUserOrders: async (page = 1, perPage = 10) => {
    try {
      const response = await apiClient.get(`/orders?page=${page}&per_page=${perPage}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user orders:', error);
      throw error;
    }
  },

  // Get order details
  getOrderById: async (orderId) => {
    try {
      const response = await apiClient.get(`/orders/${orderId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching order ${orderId}:`, error);
      throw error;
    }
  },

  // Create new order
  createOrder: async (orderData) => {
    try {
      const response = await apiClient.post('/orders', orderData);
      return response.data;
    } catch (error) {
      console.error('Error creating order:', error);
      throw error;
    }
  }
};

export default {
  productService,
  artisanService,
  partnerService,
  qrCodeService,
  authService,
  orderService
};
