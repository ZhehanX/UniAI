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

        <!-- Search Bar -->
        <div class="container mx-auto px-6 py-4">
            <div class="relative max-w-2xl mx-auto">
                <div class="flex items-center border border-gray-300 rounded-lg overflow-hidden shadow-sm">
                    <input 
                        type="text" 
                        v-model="searchQuery" 
                        @input="handleSearch"
                        placeholder="Search AI projects by name, technology, or institution..." 
                        class="w-full px-4 py-3 focus:outline-none"
                    />
                    <button 
                        @click="handleSearch" 
                        class="bg-blue-600 text-white px-6 py-3 hover:bg-blue-700 transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- App Grid -->
        <main class="container mx-auto px-6 py-8">
            <!-- Loading state -->
            <div v-if="loading" class="text-center py-8">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p class="mt-2 text-gray-600">Loading AI tools...</p>
            </div>
            
            <!-- Projects list -->
            <div v-else class="space-y-6">
                <!-- Search status -->
                <div v-if="searchQuery.trim()" class="mb-4">
                    <p v-if="isSearching" class="text-gray-600">Searching...</p>
                    <p v-else-if="searchResults.length === 0" class="text-gray-600">No results found for "{{ searchQuery }}"</p>
                    <p v-else class="text-gray-600">Found {{ searchResults.length }} results for "{{ searchQuery }}"</p>
                </div>
                
                <div v-for="project in displayedProjects" :key="project.id" 
                     tabindex="0"
                     role="button"
                     @click="$router.push(`/app/${project.id}`)"
                     @keydown.enter="$router.push(`/app/${project.id}`)"
                     @keydown.space="$router.push(`/app/${project.id}`)"
                     class="border rounded-lg p-6 hover:shadow-lg transition-all cursor-pointer">
                    <!-- Project content -->
                    <AppCard :app="project" />
                </div>
            </div>
        </main>
        
        <AppFooter />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useProjects } from '@/composables/useProjects.js';
import AppCard from '@/components/AppCard.vue';
import AppFooter from '@/components/AppFooter.vue';
import { getUserRole } from '@/utils/auth.js';

const router = useRouter();
const { projects, fetchAllProjects, searchProjects } = useProjects();
const loading = ref(true);
const searchQuery = ref('');
const searchResults = ref([]);
const isSearching = ref(false);

// Debounce function to limit API calls
const debounce = (fn, delay) => {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
};

// Handle search with debounce
const handleSearch = debounce(async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = [];
    isSearching.value = false;
    return;
  }
  
  isSearching.value = true;
  try {
    const results = await searchProjects(searchQuery.value);
    searchResults.value = results;
  } catch (err) {
    console.error('Search error:', err);
    searchResults.value = [];
  } finally {
    isSearching.value = false;
  }
}, 300);

// Computed property to determine which projects to display
const displayedProjects = computed(() => {
  if (searchQuery.value.trim() && searchResults.value.length > 0) {
    return searchResults.value;
  }
  return projects.value;
});

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