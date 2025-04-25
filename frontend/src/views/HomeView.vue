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
                    <button v-if="isLoggedIn" @click="router.push('/my-projects')"
                        class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        My Projects
                    </button>
                    <button @click="$router.push('/graphs')"
                        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2">
                        <span>View Analytics</span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                            <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                        </svg>
                    </button>
                    <button @click="handleSubmitProject"
                        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                        Submit a Project
                    </button>
                </div>
            </div>
        </header>

        <!-- App Grid -->
        <main class="container mx-auto px-6 py-8">
            <!-- Loading state -->
            <div v-if="loading" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-2 text-gray-600">Loading AI tools...</p>
            </div>
            
            <!-- Projects list -->
            <div v-else class="space-y-6">
                <div v-for="project in allProjects" :key="project.id" 
                     tabindex="0"
                     role="button"
                     class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 rounded-lg"
                     @click="navigateToDetail(project.id)"
                     @keydown.enter="navigateToDetail(project.id)"
                     @keydown.space="navigateToDetail(project.id)">
                    <AppCard :app="project" />
                </div>
            </div>
        </main>
        
        <AppFooter />
    </div>
</template>

<script setup>
import { onMounted, computed, watch, ref } from 'vue';
import { useRouter } from 'vue-router';
import AppCard from '@/components/AppCard.vue';
import AppFooter from '@/components/AppFooter.vue';
import { getUserRole } from '@/utils/auth.js';
import { useProjects } from '@/composables/useProjects.js';

const router = useRouter();
const { projects, fetchAllProjects } = useProjects();
const loading = ref(true);

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
const allProjects = projects;


const handleSubmitProject = () => {
    if (localStorage.getItem('authToken')) {
        router.push('/submit-project');
    } else {
        router.push('/login');
    }
};



// Navigation to detail page
const navigateToDetail = (projectId) => {
    router.push({ name: 'AppDetail', params: { id: projectId } });
};



// Update mount hook
onMounted(async () => {
    checkAuthState();
    loading.value = true;
    await fetchAllProjects();
    loading.value = false;
})
</script>