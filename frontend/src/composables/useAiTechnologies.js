import { ref } from 'vue';

export function useAiTechnologies() {
  const technologies = ref([]);
  const loading = ref(false);
  const error = ref('');
  
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
  
  return {
    technologies,
    loading,
    error,
    fetchAllTechnologies,
    fetchTechnologyDetails
  };
}