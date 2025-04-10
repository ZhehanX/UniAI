import { ref } from 'vue';

/**
 * Composable for managing AI technologies data and API interactions
 * Provides functions to fetch all technologies and specific technology details
 */
export function useAiTechnologies() {
  // State variables
  const technologies = ref([]);  // Stores the list of all AI technologies
  const loading = ref(false);    // Tracks loading state during API calls
  const error = ref('');         // Stores error messages
  
  /**
   * Fetches all AI technologies from the API
   * @returns {Array} Array of AI technology objects
   */
  const fetchAllTechnologies = async () => {
    try {
      loading.value = true;
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/ai-technologies/`);

      if (!response.ok) throw new Error('Failed to fetch AI technologies');
      technologies.value = await response.json();
      return technologies.value;
    } catch (error) {
      error.value = 'Error fetching AI technologies';
      throw error;
    } finally {
      loading.value = false;
    }
  };
  
  /**
   * Fetches details for a specific AI technology by ID
   * @param {number|string} techId - The ID of the technology to fetch
   * @returns {Object|null} Technology details object or null if not found
   */
  const fetchTechnologyDetails = async (techId) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/ai-technologies/${techId}/`);

      if (!response.ok) throw new Error('AI technology not found');
      return await response.json();
    } catch (error) {
      console.error(`Error fetching AI technology ${techId}:`, error);
      return null;
    }
  };
  
  // Return state variables and methods for use in components
  return {
    technologies,
    loading,
    error,
    fetchAllTechnologies,
    fetchTechnologyDetails
  };
}