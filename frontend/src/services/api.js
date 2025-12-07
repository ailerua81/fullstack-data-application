const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

class ApiService {
  constructor() {
    this.baseURL = API_URL;
  }

  getToken() {
    return localStorage.getItem('token');
  }

  setToken(token) {
    localStorage.setItem('token', token);
  }

  clearToken() {
    localStorage.removeItem('token');
  }

  async request(endpoint, options = {}) {
    const token = this.getToken();
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `HTTP Error: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Auth
  async login(username, password) {
    const data = await this.request('/auth/token', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setToken(data.access_token);
    return data;
  }

  logout() {
    this.clearToken();
  }

  // Users
  async createUser(userData) {
    return this.request('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getAllUsers() {
    return this.request('/users/');
  }

  // Fiches Lapin
  async getAllFiches() {
    return this.request('/ficheslapin/');
  }

  async getFicheById(id) {
    return this.request(`/ficheslapin/${id}`);
  }

  async createFiche(ficheData) {
    return this.request('/ficheslapin/', {
      method: 'POST',
      body: JSON.stringify(ficheData),
    });
  }

  async updateFiche(id, updates) {
    return this.request(`/ficheslapin/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteFiche(id) {
    return this.request(`/ficheslapin/${id}`, {
      method: 'DELETE',
    });
  }

  // Posts
  async getAllPosts() {
    return this.request('/posts/');
  }

  async createPost(postData) {
    return this.request('/posts/', {
      method: 'POST',
      body: JSON.stringify(postData),
    });
  }

  async createPostForFiche(ficheId, postData) {
    return this.request(`/posts/fiches/${ficheId}/posts`, {
      method: 'POST',
      body: JSON.stringify(postData),
    });
  }

  async deletePost(id) {
    return this.request(`/posts/${id}`, {
      method: 'DELETE',
    });
  }
}

export default new ApiService();