<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">AI Tools Directory</h1>
                <router-link to="/submit-case"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                    Submit a Case
                </router-link>
            </div>
        </header>

        <!-- App Grid -->
        <main class="container mx-auto px-6 py-8">
            <div class="space-y-6">
                <AppCard v-for="useCase in useCases" :key="useCase.id" :app="useCase"
                    @click="navigateToDetail(useCase.id)" />
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import AppCard from '@/components/AppCard.vue';

const router = useRouter();
const useCases = ref([]);
const loading = ref(true);
const error = ref(null);





// Fetch data from backend
const fetchUseCases = async () => {
    try {
        console.log("API URL:");
        console.log("API URL:", import.meta.env.VITE_API_URL);
        const response = await axios.get(
            `${import.meta.env.VITE_API_URL}/api/usecases/` // Use environment variable
        );
        useCases.value = response.data;
    } catch (err) {
        error.value = 'Failed to load use cases. Please try again later.';
    } finally {
        loading.value = false;
    }
};

// Navigation to detail page
const navigateToDetail = (caseId) => {
    router.push({ name: 'AppDetail', params: { id: caseId } });
};

// Fetch data when component mounts
onMounted(fetchUseCases);
</script>