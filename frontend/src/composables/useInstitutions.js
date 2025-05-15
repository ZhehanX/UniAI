import { ref } from 'vue';

/**
 * Composable for managing institution data and API interactions
 * Provides functions to fetch, create, and update institution records
 */
export function useInstitutions() {
    // State variables
    const institutions = ref([]); // Stores the list of all institutions
    const loading = ref(false);   // Tracks loading state during API calls
    const error = ref('');        // Stores error messages

    /**
     * Fetches all institutions from the API
     * @returns {Array} Array of institution objects
     */
    const fetchAllInstitutions = async () => {
        try {
            loading.value = true;
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/institutions/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch institutions');
            institutions.value = await response.json();
            return institutions.value;
        } catch (error) {
            errorMessage.value = 'Error fetching institutions';
            throw error;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches details for a specific institution by ID
     * @param {number} institutionId - The ID of the institution to fetch
     * @returns {Object} Institution details object
     */
    const fetchInstitutionDetailsById = async (institutionId) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/institutions/${institutionId}/`,
                {
                    headers: { 'Authorization': `Bearer ${token}` }
                }
            );

            if (!response.ok) throw new Error('Institution not found');
            return await response.json();
        } catch (error) {
            error.value = 'Could not fetch institution details';
            throw error;
        }
    };

    /**
     * Updates an existing institution's data
     * @param {number} institutionId - The ID of the institution to update
     * @param {Object} institutionData - New institution data
     * @returns {Object} Updated institution object
     */
    const updateInstitution = async (institutionId, institutionData) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/institutions/${institutionId}/`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(institutionData)
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to update institution');
            }
            
            return await response.json();
        } catch (error) {
            throw error;
        }
    };

    /**
     * Creates a new institution
     * @param {Object} institutionData - Institution data to create
     * @returns {Object} Newly created institution object
     */
    const createInstitution = async (institutionData) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/api/institutions/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(institutionData)
                }
            );

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create institution');
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    };

    // Return state variables and methods for use in components
    return {
        institutions,
        loading,
        error,
        fetchAllInstitutions,
        fetchInstitutionDetailsById,
        updateInstitution,
        createInstitution
    };
}