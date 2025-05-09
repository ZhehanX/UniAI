import { ref } from 'vue';
import axios from 'axios';

/**
 * Composable for managing projects data and API interactions
 * Provides functions to fetch, update, approve, and reject projects
 */
export function useProjects() {
    // State variables
    const projects = ref([]);              // Stores the list of all projects
    const currentProject = ref({});        // Stores the currently selected project
    const loading = ref(false);         // Tracks loading state during API calls
    const errorMessage = ref('');       // Stores error messages
    const successMessage = ref('');     // Stores success messages

    /**
     * Fetches all projects from the API
     * @returns {Array} Array of project objects
     */
    const fetchAllProjects = async () => {
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/api/projects/` // Use environment variable
            );
            projects.value = response.data;
            return projects.value;
        } catch (err) {
            errorMessage.value = 'Failed to load projects. Please try again later.';
            return [];
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches a specific project by ID
     * @param {number} id - The ID of the project to fetch
     * @returns {Object|null} project object or null if not found
     */
    const fetchProjectById = async (id) => {
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/projects/${id}`);
            currentProject.value = response.data;
            return currentProject.value;
        } catch (err) {
            console.error("API Error:", err.response ? err.response.data : err.message);
            errorMessage.value = 'Failed to load application details';
            return null;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches all projects submitted by a specific user
     * @param {number} userId - The ID of the user whose projects to fetch
     * @returns {Array} Array of project objects submitted by the user
     */
    const fetchProjectsByUserId = async (userId) => {
        try {
            loading.value = true;
            const token = localStorage.getItem('authToken');
            // Using the main endpoint with a query parameter for user_id
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/user/${userId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
      
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch user projects');
            }
      
            return await response.json();
        } catch (error) {
            console.error('Error in fetchProjectsByUserId:', error);
            errorMessage.value = 'Failed to load your projects. Please try again later.';
            throw error;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Fetches all pending projects that need review
     * @returns {Array} Array of pending project objects
     */
    const fetchPendingProjectsWithDetails = async () => {
        try {
            loading.value = true;
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/?status=pending`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) throw new Error('Failed to fetch projects');
            projects.value = await response.json();

            return projects.value;
        } catch (error) {
            errorMessage.value = 'Error loading projects';
            throw error;
        } finally {
            loading.value = false;
        }
    };
    // Search projects
    const searchProjects = async (query) => {
        loading.value = true;
        errorMessage.value = null;
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Search failed');
            
            const data = await response.json();
            return data;
        } catch (err) {
            console.error('Search error:', err);
            errorMessage.value = 'Search failed. Please try again later.';
            return [];
        } finally {
            loading.value = false;
        }
    };

    /**
     * Approves a pending project
     * @param {number} projectId - The ID of the project to approve
     * @returns {boolean} True if approval was successful
     */
    const approveProject = async (projectId) => {
        try {
            const token = localStorage.getItem('authToken');
            
            // First, get the current project data
            const getResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${projectId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!getResponse.ok) throw new Error('Failed to fetch project data');
            const projectData = await getResponse.json();
            
            // Update only the status field
            projectData.status = "approved";
            
            // Send the complete updated project data
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${projectId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(projectData)
            });
    
            if (!response.ok) throw new Error('Approval failed');
            successMessage.value = 'Project approved successfully';
            return true;
        } catch (error) {
            errorMessage.value = 'Approval failed. Please try again.';
            throw error;
        }
    };

    /**
     * Rejects a pending project
     * @param {number} projectId - The ID of the project to reject
     * @returns {boolean} True if rejection was successful
     */
    const rejectProject = async (projectId) => {
        try {
            const token = localStorage.getItem('authToken');
            
            // First, get the current project data
            const getResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${projectId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!getResponse.ok) throw new Error('Failed to fetch project data');
            const projectData = await getResponse.json();
            
            // Update only the status field
            projectData.status = "rejected";
            
            // Send the complete updated project data
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${projectId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(projectData)
            });

            if (!response.ok) throw new Error('Rejection failed');
            successMessage.value = 'Project rejected successfully';
            return true;
        } catch (error) {
            errorMessage.value = 'Rejection failed. Please try again.';
            throw error;
        }
    };

    /**
     * Updates an existing project
     * @param {number} projectId - The ID of the project to update
     * @param {Object} projectData - New project data
     * @returns {Object} Updated project object
     */
    const updateProject = async (projectId, projectData) => {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${projectId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(projectData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || JSON.stringify(errorData) || 'Failed to update project');
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    };

    // Return state variables and methods for use in components
    return {
        projects,
        currentProject,
        loading,
        errorMessage,
        successMessage,
        fetchAllProjects,
        fetchProjectById,
        fetchProjectsByUserId,
        fetchPendingProjectsWithDetails,
        searchProjects,
        approveProject,
        rejectProject,
        updateProject
    };
}