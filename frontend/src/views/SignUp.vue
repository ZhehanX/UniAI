<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header section with title and back button -->
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">Sign Up</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Home
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <!-- Sign up form container -->
            <div class="bg-white rounded-lg shadow-md p-8 max-w-md mx-auto">
                <form @submit.prevent="handleSignUp">
                    <div class="space-y-6">
                        <!-- Name input field -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                            <input v-model="formData.name" type="text" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Enter your name">
                        </div>
                        
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
                        
                        <!-- Confirm password input field -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Confirm Password *</label>
                            <input v-model="formData.confirmPassword" type="password" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Confirm your password">
                        </div>

                        <!-- Error message display -->
                        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-700 rounded-lg">
                            {{ errorMessage }}
                        </div>

                        <!-- Submit button with loading state -->
                        <button type="submit"
                            class="w-full bg-blue-600 text-white px-6 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold disabled:bg-gray-400"
                            :disabled="loading">
                            <span v-if="!loading">Create Account</span>
                            <span v-else>Creating account...</span>
                        </button>
                        
                        <!-- Login link for existing users -->
                        <p class="text-center text-gray-600">
                            Already have an account? 
                            <router-link to="/login" class="text-blue-600 hover:text-blue-800">
                                Login here
                            </router-link>
                        </p>
                    </div>
                </form>
            </div>
        </main>
    </div>
    <AppFooter />
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';  
import AppFooter from '@/components/AppFooter.vue';

// Initialize router for navigation after sign up
const router = useRouter();

// Form data reactive object to store user input
const formData = ref({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
});

// State variables for UI feedback
const loading = ref(false);
const errorMessage = ref('');

// Handle form submission
const handleSignUp = async () => {
    try {
        // Set loading state and clear previous errors
        loading.value = true;
        errorMessage.value = '';
        
        // Validate password confirmation
        if (formData.value.password !== formData.value.confirmPassword) {
            throw new Error('Passwords do not match');
        }
        
        // Send registration request to the backend API
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/api/auth/register`,
            {
                username: formData.value.name,
                email: formData.value.email,
                password: formData.value.password
            }
        );

        // Redirect to login page after successful registration
        router.push('/login');
    } catch (error) {
        // Handle and display error messages
        errorMessage.value = error.response?.data?.detail || 
                            error.message || 
                            'Registration failed. Please try again.';
    } finally {
        // Reset loading state regardless of outcome
        loading.value = false;
    }
};
</script>