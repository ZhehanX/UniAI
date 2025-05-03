import axios from 'axios';

const API_URL = 'http://localhost:8000/api/search';

export const searchProjects = async (query) => {
  try {
    const response = await axios.get(`${API_URL}?q=${encodeURIComponent(query)}`);
    return response.data;
  } catch (error) {
    console.error('Error searching projects:', error);
    throw error;
  }
};