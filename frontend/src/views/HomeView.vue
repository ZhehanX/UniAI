<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">AI Tools Directory</h1>
                <div class="flex space-x-2">
                    <button v-if="!isLoggedIn" @click="router.push('/login')"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        Login
                    </button>
                    <button v-else @click="handleLogout"
                        class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        Logout
                    </button>
                    <button v-if="isAdmin" @click="router.push('/admin/review')"
                        class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        Admin Review
                    </button>
                    <button @click="handleSubmitCase"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        Submit a Case
                    </button>
                </div>
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
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router'; 
import axios from 'axios';
import AppCard from '@/components/AppCard.vue';
import { getUserRole } from '@/utils/auth.js';

const router = useRouter();
const route = useRoute();

// Check if user is logged in
const isLoggedIn = computed(() => !!localStorage.getItem('authToken'));
// Check if user is an admin
const isAdmin = computed(() => getUserRole() === 'admin');

// Add auth check function
const checkAuthState = () => {
    isLoggedIn.value;  // Trigger computed update
};

watch(() => localStorage.getItem('authToken'), () => {
    checkAuthState()
})

const handleLogout = () => {
    localStorage.removeItem('authToken')
    router.push({ path: '/login', replace: true })
    checkAuthState()
}
const useCases = ref([]);
const loading = ref(true);
const error = ref(null);


const handleSubmitCase = () => {
    if (localStorage.getItem('authToken')) {
        router.push('/submit-case');
    } else {
        router.push('/login');
    }
};

// Fetch data from backend
/*
const fetchUseCases = async () => {
    try {
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
*/

// Navigation to detail page
const navigateToDetail = (caseId) => {
    router.push({ name: 'AppDetail', params: { id: caseId } });
};

// Fetch data when component mounts
import { watch } from 'vue'




// Update mount hook
onMounted(() => {
    checkAuthState()
    //fetchUseCases()
})
</script>