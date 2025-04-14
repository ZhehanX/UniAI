import { ref } from 'vue';
import axios from 'axios';

/**
 * Composable for managing use cases data and API interactions
 * Provides functions to fetch, update, approve, and reject use cases
 */
export function useCases() {
    // State variables
    const cases = ref([]);              // Stores the list of all use cases
    const currentCase = ref({});        // Stores the currently selected use case
    const loading = ref(false);         // Tracks loading state during API calls
    const errorMessage = ref('');       // Stores error messages
    const successMessage = ref('');     // Stores success messages

    /**
     * Fetches all use cases from the API
     * @returns {Array} Array of use case objects
     */
    const fetchAllUseCases = async () => {
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/api/use-cases/` // Use environment variable
            );
            cases.value = response.data;
            return cases.value;
        } catch (err) {
            errorMessage.value = 'Failed to load use cases. Please try again later.';
            return [];
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches a specific use case by ID
     * @param {number|string} id - The ID of the use case to fetch
     * @returns {Object|null} Use case object or null if not found
     */
    const fetchUseCasesById = async (id) => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/use-cases/${id}`);
            currentCase.value = response.data;
            return currentCase.value;
        } catch (err) {
            console.error("API Error:", err.response ? err.response.data : err.message);
            errorMessage.value = 'Failed to load application details';
            return null;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches all use cases submitted by a specific user
     * @param {number|string} userId - The ID of the user whose cases to fetch
     * @returns {Array} Array of use case objects submitted by the user
     */
    const fetchCasesByUserId = async (userId) => {
        try {
            loading.value = true;
            const token = localStorage.getItem('authToken');
            // Using the main endpoint with a query parameter for user_id
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/?user_id=${userId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
      
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch user cases');
            }
      
            return await response.json();
        } catch (error) {
            console.error('Error in fetchCasesByUserId:', error);
            errorMessage.value = 'Failed to load your cases. Please try again later.';
            throw error;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches all pending use cases that need review
     * @returns {Array} Array of pending use case objects
     */
    const fetchPendingCasesWithDetails = async () => {
        try {
            loading.value = true;
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/?status=pending`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch cases');
            cases.value = await response.json();

            return cases.value;
        } catch (error) {
            errorMessage.value = 'Error loading cases';
            throw error;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Approves a pending use case
     * @param {number|string} caseId - The ID of the use case to approve
     * @returns {boolean} True if approval was successful
     */
    const approveCase = async (caseId) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/${caseId}/approve/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error('Approval failed');
            successMessage.value = 'Case approved successfully';
            return true;
        } catch (error) {
            errorMessage.value = 'Approval failed. Please try again.';
            throw error;
        }
    };

    /**
     * Rejects a pending use case
     * @param {number|string} caseId - The ID of the use case to reject
     * @returns {boolean} True if rejection was successful
     */
    const rejectCase = async (caseId) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/${caseId}/reject/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error('Rejection failed');
            successMessage.value = 'Case rejected successfully';
            return true;
        } catch (error) {
            errorMessage.value = 'Rejection failed. Please try again.';
            throw error;
        }
    };

    /**
     * Updates an existing use case
     * @param {number|string} caseId - The ID of the use case to update
     * @param {Object} caseData - New use case data
     * @returns {Object} Updated use case object
     */
    const updateCase = async (caseId, caseData) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/use-cases/${caseId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(caseData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || JSON.stringify(errorData) || 'Failed to update case');
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    };

    // Return state variables and methods for use in components
    return {
        cases,
        currentCase,
        loading,
        errorMessage,
        successMessage,
        fetchAllUseCases,
        fetchUseCasesById,
        fetchCasesByUserId,
        fetchPendingCasesWithDetails,
        approveCase,
        rejectCase,
        updateCase
    };
}