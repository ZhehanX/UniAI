<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header section with title and back button -->
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">Login</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Home
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <!-- Login form container -->
            <div class="bg-white rounded-lg shadow-md p-8 max-w-md mx-auto">
                <form @submit.prevent="handleLogin">
                    <div class="space-y-6">
                        <!-- Email input field -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                            <input v-model="formData.email" type="email" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Enter your email">
                        </div>
                        
                        <!-- Password input field -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                            <input v-model="formData.password" type="password" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Enter your password">
                        </div>

                        <!-- Error message display -->
                        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-700 rounded-lg">
                            {{ errorMessage }}
                        </div>

                        <!-- Submit button with loading state -->
                        <button type="submit"
                            class="w-full bg-blue-600 text-white px-6 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold disabled:bg-gray-400"
                            :disabled="loading">
                            <span v-if="!loading">Login</span>
                            <span v-else>Logging in...</span>
                        </button>
                        
                        <!-- Sign up link for new users -->
                        <p class="text-center text-gray-600">
                            Don't have an account? 
                            <router-link to="/signup" class="text-blue-600 hover:text-blue-800">
                                Sign up here
                            </router-link>
                        </p>
                    </div>
                </form>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { setToken, setUserRole } from '@/utils/auth';

// Initialize router for navigation after login
const router = useRouter();

// Form data reactive object to store user input
const formData = ref({
    email: '',
    password: ''
});

// State variables for UI feedback
const loading = ref(false);
const errorMessage = ref('');

// Handle form submission
const handleLogin = async () => {
    try {
        // Set loading state and clear previous errors
        loading.value = true;
        errorMessage.value = '';
        
        // Send login request to the backend API
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/auth/login`,
            {
                email: formData.value.email,
                password: formData.value.password
            }
        );
        
        // Store authentication token and user role in local storage
        setToken(response.data.access_token);
        setUserRole(response.data.role);
        
        // Redirect to home page after successful login
        router.push('/');
    } catch (error) {
        // Handle and display error messages
        errorMessage.value = error.response?.data?.detail || 
                            error.message || 
                            'Login failed. Please check your credentials and try again.';
    } finally {
        // Reset loading state regardless of outcome
        loading.value = false;
    }
};
</script>