import { ref } from 'vue';
import axios from 'axios';

export function useCases() {
    const cases = ref([]);
    const currentCase = ref({});
    const loading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');

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

    return {
        cases,
        currentCase,
        loading,
        errorMessage,
        successMessage,
        fetchAllUseCases,
        fetchUseCasesById,
        fetchPendingCasesWithDetails,
        approveCase,
        rejectCase,
        updateCase
    };
}