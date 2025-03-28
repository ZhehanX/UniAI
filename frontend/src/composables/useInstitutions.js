import { ref } from 'vue';

export function useInstitutions() {
    const institutions = ref([]);
    const loading = ref(false);
    const error = ref('');

    const fetchInstitutions = async () => {
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

    return {
        institutions,
        loading,
        error,
        fetchInstitutions,
        fetchInstitutionDetailsById,
        updateInstitution,
        createInstitution
    };
}