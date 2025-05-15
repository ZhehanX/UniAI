<template>
    <div v-if="userRole === 'admin'" class="min-h-screen bg-gray-100">
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-2xl font-bold text-gray-900">Admin Review Panel</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Overview
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-semibold mb-6">Projects Requiring Validation</h2>

                <!-- Loading/error states remain same -->

                <div v-if="projects.length" class="space-y-6">
                    <div v-for="projectItem in projects" :key="projectItem.id"
                        class="border rounded-lg p-6 hover:shadow-sm transition-all">
                        <!-- Header Section -->
                        <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
                            <div class="space-y-2 flex-1 min-w-[300px]">
                                <div class="flex items-center gap-3">
                                    <h3 class="text-lg font-semibold text-gray-900">
                                        {{ projectItem.title }}
                                    </h3>
                                    <span :class="statusBadge(projectItem.status)" class="text-sm">
                                        {{ projectItem.status }}
                                    </span>
                                </div>
                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Institution</label>
                                    <div v-if="projectItem.institution">
                                        <p class="font-medium text-gray-800">{{ projectItem.institution.name }}</p>
                                        <p class="text-gray-600">
                                            {{ [projectItem.institution.city, projectItem.institution.state,
                                                projectItem.institution.country].filter(Boolean).join(', ') }}
                                        </p>
                                        <p class="text-gray-500 text-xs mt-1">
                                            Coordinates: {{ projectItem.institution.latitude !== undefined ?
                                            projectItem.institution.latitude : 'N/A' }},
                                            {{ projectItem.institution.longitude !== undefined ?
                                            projectItem.institution.longitude : 'N/A' }}
                                        </p>
                                    </div>
                                    <span v-else class="text-gray-400">No institution associated</span>
                                </div>
                            </div>

                            <div class="flex gap-3">
                                <button @click="openEditModal(projectItem)"
                                    class="text-blue-600 hover:text-blue-800 flex items-center gap-1">
                                    <PencilIcon class="w-5 h-5" />
                                    <span class="text-sm">Edit</span>
                                </button>
                            </div>
                        </div>

                        <!-- Main Content Grid -->
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 text-sm">
                            <!-- Left Column: contact, url, project initiation date and AI Technologies-->
                            <div class="space-y-4">
                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Contact</label>
                                    <a :href="`mailto:${projectItem.contact}`"
                                        class="text-blue-600 hover:underline break-all">
                                        {{ projectItem.contact || 'Not provided' }}
                                    </a>
                                </div>

                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Project URL</label>
                                    <a :href="projectItem.url" target="_blank"
                                        class="text-blue-600 hover:underline break-all">
                                        {{ projectItem.url || 'Not provided' }}
                                    </a>
                                </div>
                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Project Initiation Date</label>
                                    <p class="text-gray-800">
                                        {{ projectItem.project_initiation_date || 'Not provided' }}
                                    </p>
                                </div>
                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">AI Technologies</label>
                                    <div v-if="projectItem.aiTechDetails && projectItem.aiTechDetails.length"
                                        class="flex flex-wrap gap-2">
                                        <span v-for="(tech, index) in projectItem.aiTechDetails" :key="index"
                                            class="px-2.5 py-1 bg-blue-50 text-blue-800 rounded-full text-xs">
                                            {{ tech.name }}
                                        </span>
                                    </div>
                                    <div v-else-if="projectItem.ai_technologies && projectItem.ai_technologies.length"
                                        class="flex flex-wrap gap-2">
                                        <span v-for="(techId, index) in projectItem.ai_technologies" :key="index"
                                            class="px-2.5 py-1 bg-gray-50 text-gray-600 rounded-full text-xs flex items-center">
                                            <span class="animate-pulse mr-1">⟳</span> Loading...
                                        </span>
                                    </div>
                                    <span v-else class="text-gray-400">None specified</span>
                                </div>
                            </div>

                            <!-- Right Column: short description + full description -->
                            <div class="space-y-4">
                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Short Description</label>
                                    <p class="text-gray-800 whitespace-pre-wrap leading-relaxed">
                                        {{ projectItem.short_description }}
                                    </p>
                                </div>

                                <div>
                                    <label class="text-gray-500 font-medium block mb-1">Full Description</label>
                                    <p
                                        class="text-gray-800 whitespace-pre-wrap leading-relaxed max-h-[200px] overflow-y-auto">
                                        {{ projectItem.full_description?.value || 'No description provided' }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Action Footer -->
                        <div class="mt-6 pt-4 border-t flex flex-wrap gap-4 justify-end">
                            <button @click="rejectProject(projectItem.id)"
                                class="px-4 py-2 text-red-700 bg-red-50 hover:bg-red-100 rounded-md flex items-center gap-2">
                                <XMarkIcon class="w-5 h-5" />
                                <span>Reject Project</span>
                            </button>
                            <button @click="approveProject(projectItem.id)"
                                class="px-4 py-2 text-green-700 bg-green-50 hover:bg-green-100 rounded-md flex items-center gap-2">
                                <CheckIcon class="w-5 h-5" />
                                <span>Approve Project</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div v-if="!projects.length && !loading" class="text-center text-gray-500 py-4">
                    No projects requiring validation
                </div>
            </div>
        </main>
    </div>

    <div v-else class="text-center mt-8 text-red-600">
        You don't have permission to access this page
    </div>

    <!-- Update the modal backdrop styling -->
    <div v-if="showEditModal"
        class="fixed inset-0 backdrop-blur-sm bg-white/30 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-semibold">Edit Project</h2>
                    <button @click="closeEditModal" class="text-gray-500 hover:text-gray-700">
                        <XMarkIcon class="w-6 h-6" />
                    </button>
                </div>

                <div v-if="editError" class="mb-4 p-3 bg-red-50 text-red-700 rounded-md">
                    {{ editError }}
                </div>

                <form @submit.prevent="saveEditedProject" class="space-y-4">
                    <div>
                        <label for="editProjectTitle" class="block text-gray-700 font-medium mb-1">Title</label>
                        <input id="editProjectTitle" v-model="editForm.title" type="text" required
                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>

                    <div>
                        <label class="block text-gray-700 font-medium mb-1">Institution Details</label>
                        <div class="border rounded-md p-4 bg-gray-50">
                            <div class="space-y-3">
                                <div>
                                    <label for="editInstitutionName"
                                        class="block text-gray-600 text-sm mb-1">Name</label>
                                    <input id="editInstitutionName" v-model="editForm.institution_name" type="text"
                                        class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                </div>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <div>
                                        <label for="editInstitutionCity"
                                            class="block text-gray-600 text-sm mb-1">City</label>
                                        <input id="editInstitutionCity" v-model="editForm.institution_city" type="text"
                                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    </div>
                                    <div>
                                        <label for="editInstitutionCountry"
                                            class="block text-gray-600 text-sm mb-1">Country</label>
                                        <input id="editInstitutionCountry" v-model="editForm.institution_country"
                                            type="text"
                                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    </div>
                                </div>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <div>
                                        <label for="editInstitutionLatitude"
                                            class="block text-gray-600 text-sm mb-1">Latitude</label>
                                        <input id="editInstitutionLatitude" v-model="editForm.institution_latitude"
                                            type="text"
                                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    </div>
                                    <div>
                                        <label for="editInstitutionLongitude"
                                            class="block text-gray-600 text-sm mb-1">Longitude</label>
                                        <input id="editInstitutionLongitude" v-model="editForm.institution_longitude"
                                            type="text"
                                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div>
                        <label class="block text-gray-700 font-medium mb-1">AI Technologies</label>
                        <div v-if="allAiTechnologies.length"
                            class="border rounded-md p-3 max-h-[200px] overflow-y-auto">
                            <div v-for="tech in allAiTechnologies" :key="tech.id" class="flex items-center mb-2">
                                <input type="checkbox" :id="`tech-${tech.id}`" :value="tech.id"
                                    v-model="editForm.ai_technologies" class="mr-2">
                                <label :for="`tech-${tech.id}`" class="text-gray-700">{{ tech.name }}</label>
                            </div>
                        </div>
                        <div v-else class="text-sm text-gray-500 mt-1">
                            Loading AI technologies...
                        </div>
                    </div>

                    <div>
                        <label for="editShortDescription" class="block text-gray-700 font-medium mb-1">Short
                            Description</label>
                        <textarea id="editShortDescription" v-model="editForm.short_description" required rows="2"
                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>

                    <div>
                        <label for="editFullDescription" class="block text-gray-700 font-medium mb-1">Full
                            Description</label>
                        <textarea id="editFullDescription" v-model="editForm.full_description" rows="5"
                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label for="editProjectUrl" class="block text-gray-700 font-medium mb-1">Project URL</label>
                            <input id="editProjectUrl" v-model="editForm.url" type="url"
                                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>

                        <div>
                            <label for="editContactEmail" class="block text-gray-700 font-medium mb-1">Contact
                                Email</label>
                            <input id="editContactEmail" v-model="editForm.contact" type="email"
                                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                    </div>

                    <!-- Add project initiation date field -->
                    <div>
                        <label for="editProjectDate" class="block text-gray-700 font-medium mb-1">Project Initiation
                            Date</label>
                        <input id="editProjectDate" v-model="editForm.project_initiation_date" type="date"
                            class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>

                    <div class="flex justify-end gap-3 pt-4 border-t">
                        <button type="button" @click="closeEditModal"
                            class="px-4 py-2 border rounded-md hover:bg-gray-50">
                            Cancel
                        </button>
                        <button type="submit" :disabled="editLoading"
                            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                            <span v-if="editLoading">Saving...</span>
                            <span v-else>Save Changes</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUserRole } from '@/utils/auth.js';
import { PencilIcon, CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import { useProjects } from '@/composables/useProjects.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';

const router = useRouter();
const userRole = getUserRole();

const {
    projects,
    loading,
    successMessage,
    fetchPendingProjectsWithDetails,
    approveProject: approveProjectAction,
    rejectProject: rejectProjectAction
} = useProjects();

const {
    institutions,
    fetchInstitutionDetailsById,
    fetchAllInstitutions
} = useInstitutions();

const {
    technologies: allAiTechnologies,
    fetchAllTechnologies,
    fetchTechnologyDetails
} = useAiTechnologies();

// Local state
const aiTechnologies = ref({});
const showEditModal = ref(false);
const editingProject = ref(null);
const editForm = ref({});
const editLoading = ref(false);
const editError = ref('');


// Load institution details for each project
const loadInstitutionDetails = async (projectItem) => {
    if (!projectItem.institution_id) return;

    try {
        const institutionData = await fetchInstitutionDetailsById(projectItem.institution_id);
        if (institutionData) {
            // Update the project item with institution details
            projectItem.institution = institutionData;
        }
    } catch (error) {
        console.error('Error loading institution details:', error);
    }
};

// Fetch projects with details
const loadProjectsWithDetails = async () => {
    try {
        const projectsData = await fetchPendingProjectsWithDetails();

        // Load institution details for each project
        for (const projectItem of projectsData) {
            if (projectItem.institution_id) {
                await loadInstitutionDetails(projectItem);
            }

            // Load AI technology details
            if (projectItem.ai_technologies && projectItem.ai_technologies.length) {
                projectItem.aiTechDetails = [];
                for (const techId of projectItem.ai_technologies) {
                    // Check if we already have this tech in our cache
                    if (!aiTechnologies.value[techId]) {
                        const techDetails = await fetchTechnologyDetails(techId);
                        if (techDetails) {
                            aiTechnologies.value[techId] = techDetails;
                        }
                    }

                    if (aiTechnologies.value[techId]) {
                        projectItem.aiTechDetails.push(aiTechnologies.value[techId]);
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error loading projects with details:', error);
    }
};

// Approve project wrapper
const approveProject = async (projectId) => {
    try {
        await approveProjectAction(projectId);
        await loadProjectsWithDetails();
    } catch (error) {
        console.error('Error approving project:', error);
    }
};

// Reject project wrapper
const rejectProject = async (projectId) => {
    try {
        await rejectProjectAction(projectId);
        await loadProjectsWithDetails();
    } catch (error) {
        console.error('Error rejecting project:', error);
    }
};

onMounted(() => {
    if (userRole === 'admin') {
        loadProjectsWithDetails();
        fetchAllTechnologies();
    } else {
        router.push('/');
    }
});

// Status badge styling
const statusBadge = (status) => ({
    'px-3 py-1 rounded-full text-sm font-medium': true,
    'bg-amber-100 text-amber-800': status === 'pending',
    'bg-emerald-100 text-emerald-800': status === 'approved',
    'bg-rose-100 text-rose-800': status === 'rejected'
});


const openEditModal = (projectItem) => {
    editingProject.value = projectItem;

    // Format the date for the input field (YYYY-MM-DD format)
    // The date input field in HTML requires the YYYY-MM-DD format to work properly, even though we are displaying dates in DD-MM-YYYY format to users
    let formattedDate = null;
    if (projectItem.project_initiation_date) {
        try {
            const date = new Date(projectItem.project_initiation_date);
            if (!isNaN(date.getTime())) {
                formattedDate = date.toISOString().split('T')[0]; // Format as YYYY-MM-DD for the input field
            } else {
                // If invalid but we have a string, keep the original value
                formattedDate = projectItem.project_initiation_date;
            }
        } catch (e) {
            // If parsing fails, use the original string
            formattedDate = projectItem.project_initiation_date;
        }
    }

    // Create a copy of the project data for editing
    editForm.value = {
        title: projectItem.title,
        short_description: projectItem.short_description,
        full_description: projectItem.full_description?.value || '',
        url: projectItem.url || '',
        contact: projectItem.contact || '',
        ai_technologies: [...(projectItem.ai_technologies || [])],
        institution_id: projectItem.institution_id,
        project_initiation_date: formattedDate
    };

    // Add institution details if available
    if (projectItem.institution) {
        editForm.value.institution_name = projectItem.institution.name;
        editForm.value.institution_city = projectItem.institution.city;
        editForm.value.institution_country = projectItem.institution.country;
        editForm.value.institution_latitude = projectItem.institution.latitude;
        editForm.value.institution_longitude = projectItem.institution.longitude;
    }

    // Fetch institutions and AI technologies if not already loaded
    if (institutions.value.length === 0) {
        fetchAllInstitutions();
    }

    if (allAiTechnologies.value.length === 0) {
        fetchAllTechnologies();
    }

    showEditModal.value = true;
};

const saveEditedProject = async () => {
    if (!editingProject.value) return;

    try {
        editLoading.value = true;
        editError.value = '';

        const token = localStorage.getItem('authToken');

        // First, update institution if needed
        if (editingProject.value.institution_id) {
            // Update existing institution
            const institutionData = {
                name: editForm.value.institution_name,
                city: editForm.value.institution_city,
                country: editForm.value.institution_country,
                latitude: editForm.value.institution_latitude,
                longitude: editForm.value.institution_longitude
            };

            const institutionResponse = await fetch(
                `${import.meta.env.VITE_API_URL}/api/institutions/${editingProject.value.institution_id}/`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(institutionData)
                }
            );

            if (!institutionResponse.ok) {
                const errorData = await institutionResponse.json();
                throw new Error(errorData.detail || 'Failed to update institution');
            }
        } else if (editForm.value.institution_name) {
            // Create new institution
            const institutionData = {
                name: editForm.value.institution_name,
                city: editForm.value.institution_city,
                country: editForm.value.institution_country,
                latitude: editForm.value.institution_latitude,
                longitude: editForm.value.institution_longitude
            };

            const institutionResponse = await fetch(
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

            if (!institutionResponse.ok) {
                const errorData = await institutionResponse.json();
                throw new Error(errorData.detail || 'Failed to create institution');
            }

            // Get the new institution ID
            const newInstitution = await institutionResponse.json();
            editForm.value.institution_id = newInstitution.id;
        }

        // Format the date to dd-mm-yyyy before sending to API
        let formattedDate = null;
        if (editForm.value.project_initiation_date) {
            try {
                const date = new Date(editForm.value.project_initiation_date);
                if (!isNaN(date.getTime())) {
                    const day = String(date.getDate()).padStart(2, '0');
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const year = date.getFullYear();
                    formattedDate = `${day}-${month}-${year}`;
                } else {
                    // If invalid but we have a string, pass it through
                    formattedDate = editForm.value.project_initiation_date;
                }
            } catch (e) {
                // If parsing fails, use the original string
                formattedDate = editForm.value.project_initiation_date;
            }
        }

        // Then update the project
        const projectData = {
            title: editForm.value.title,
            short_description: editForm.value.short_description,
            full_description: { value: editForm.value.full_description },
            url: editForm.value.url || null,
            contact: editForm.value.contact || null,
            ai_technologies: editForm.value.ai_technologies || [],
            institution_id: editForm.value.institution_id || null,
            project_initiation_date: formattedDate
        };


        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/projects/${editingProject.value.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(projectData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error response:', errorData);
            throw new Error(errorData.detail || JSON.stringify(errorData) || 'Failed to update project');
        }

        successMessage.value = 'Project updated successfully';
        closeEditModal();
        await fetchPendingProjectsWithDetails(); // Refresh the projects list
    } catch (error) {
        console.error('Error in saveEditedProject:', error);
        editError.value = error.message || 'Error updating project';
    } finally {
        editLoading.value = false;
    }
};

const closeEditModal = () => {
    showEditModal.value = false;
    editingProject.value = null;
    editForm.value = {};
    editError.value = '';
};
</script>
