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
                <!-- Logo and data Section -->
                <div class="bg-white rounded-lg shadow-md p-4">
                    <div class="flex flex-col items-start space-y-4">
                        <!-- Logo -->
                        <div class="w-48 h-48 p-2">
                            <img :src="currentApp.imagePath" :alt="currentApp.title"
                                class="w-full h-full object-contain">
                        </div>

                        <!-- Metadata -->
                        <div class="w-full space-y-3">
                            <div class="grid grid-cols-2 gap-4 text-sm">
                                <div class="text-gray-500 font-semibold">Title:</div>
                                <div class="text-gray-700">{{ currentApp.title || 'N/A' }}</div>

                                <div class="text-gray-500 font-semibold">Institution:</div>
                                <div class="text-gray-700">{{ currentApp.institution || 'N/A' }}</div>

                                <div class="text-gray-500 font-semibold">Description:</div>
                                <div class="text-gray-700">{{ currentApp.description || 'N/A' }}</div>

                                <div class="text-gray-500 font-semibold">URL:</div>
                                <div class="text-gray-700">{{ currentApp.url || 'N/A' }}</div>
                            </div>

                            <!-- Tags -->
                            <div v-if="currentApp.tags" class="pt-2 border-t">
                                <div class="flex flex-wrap gap-2">
                                    <span v-for="tag in currentApp.tags" :key="tag"
                                        class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
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
                    <p class="text-gray-600 leading-relaxed" style="white-space: pre-line">{{ currentApp.full_description }}</p>
                </div>
            </div>
        </main>
    </div>

    <!-- Loading State -->
    <div v-else class="min-h-screen flex items-center justify-center text-gray-500">
        Loading application details...
    </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const currentApp = ref({});
const error = ref(null);



const fetchAppData = async (id) => {
  try {
    console.log("Fetching app data for ID:", id);
    const response = await axios.get(`http://localhost:8000/api/usecases/${id}`);
    console.log("API Response:", response.data);
    currentApp.value = response.data;
  } catch (err) {
    console.error("API Error:", err.response ? err.response.data : err.message);
    error.value = 'Failed to load application details';
  }
};



// Fetch when component mounts or ID changes
onMounted(() => fetchAppData(route.params.id));
watch(() => route.params.id, (newId) => fetchAppData(newId));



</script>