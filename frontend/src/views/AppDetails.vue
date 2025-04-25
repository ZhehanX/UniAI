<template>
    <div class="min-h-screen bg-gray-50" v-if="currentApp">
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">{{ currentApp.title }}</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Overview
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- Metadata Section -->
                <div class="bg-white rounded-lg shadow-md p-6 col-span-1 lg:col-span-2">
                    <div class="flex flex-col items-start">
                        <!-- Metadata -->
                        <div class="w-full space-y-3">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 text-sm">
                                <div class="flex flex-col">
                                    <div class="text-gray-500 font-semibold mb-1">Title:</div>
                                    <div class="text-gray-700 break-words">{{ currentApp.title || 'N/A' }}</div>
                                </div>

                                <div class="flex flex-col">
                                    <div class="text-gray-500 font-semibold mb-1">Institution:</div>
                                    <div class="text-gray-700 break-words">
                                        <div v-if="institutionDetails">
                                            {{ institutionDetails.name }}
                                            <div class="text-gray-500 text-sm mt-1" v-if="hasLocation">
                                                {{ formatLocation(institutionDetails) }}
                                            </div>
                                        </div>
                                        <div v-else>Loading...</div>
                                    </div>
                                </div>

                                <div class="flex flex-col">
                                    <div class="text-gray-500 font-semibold mb-1">URL:</div>
                                    <div class="text-gray-700 break-all">
                                        <a v-if="currentApp.url" :href="currentApp.url" target="_blank" 
                                           class="text-blue-600 hover:underline">
                                            {{ currentApp.url }}
                                        </a>
                                        <span v-else>N/A</span>
                                    </div>
                                </div>

                                <div class="flex flex-col">
                                    <div class="text-gray-500 font-semibold mb-1">Short Description:</div>
                                    <div class="text-gray-700 break-words">{{ currentApp.short_description || 'N/A' }}</div>
                                </div>
                            </div>

                            <!-- Tags -->
                            <div v-if="currentApp.tags" class="pt-2 border-t mt-4">
                                <div class="text-gray-500 font-semibold mb-2">Tags:</div>
                                <div class="flex flex-wrap gap-2">
                                    <span v-for="tag in currentApp.tags" :key="tag"
                                        class="px-2.5 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                                        {{ tag }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Description -->
                <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
                    <h2 class="text-xl font-semibold mb-4">About this AI Tool</h2>
                    <p class="text-gray-600 leading-relaxed" style="white-space: pre-line">{{ currentApp.full_description ? currentApp.full_description.value : "" }}</p>
                </div>
            </div>
        </main>
    </div>

    <!-- Loading State -->
    <div v-else class="min-h-screen flex items-center justify-center text-gray-500">
        Loading application details...
    </div>

    <AppFooter />
</template>


<script setup>
import { onMounted, watch, ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProjects } from '@/composables/useProjects.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import AppFooter from '@/components/AppFooter.vue';

const route = useRoute();
const { currentProject, fetchUseProjectsById } = useProjects();
const { fetchInstitutionDetailsById } = useInstitutions();

const currentApp = currentProject;
const institutionDetails = ref(null);


const hasLocation = computed(() => {
    return institutionDetails.value && 
           (institutionDetails.value.city || 
            institutionDetails.value.state || 
            institutionDetails.value.country);
});

const formatLocation = (institution) => {
    const locationParts = [];
    if (institution.city) locationParts.push(institution.city);
    if (institution.state) locationParts.push(institution.state);
    if (institution.country) locationParts.push(institution.country);
    return locationParts.join(', ');
};

// Fetch institution details when currentApp changes
watch(currentApp, async () => {
    if (currentApp.value && currentApp.value.institution_id) {
        try {
            institutionDetails.value = await fetchInstitutionDetailsById(currentApp.value.institution_id);
        } catch (err) {
            console.error('Error fetching institution details:', err);
        }
    }
}, { immediate: true });

console.log("current app:", currentApp);

// Fetch when component mounts or ID changes
onMounted(() => {
    fetchUseProjectsById(route.params.id);
});
watch(() => route.params.id, (newId) => fetchUseProjectsById(newId));



</script>