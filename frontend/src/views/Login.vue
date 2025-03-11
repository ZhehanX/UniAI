<template>
    <div class="min-h-screen bg-gray-50">
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">Login</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Home
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <div class="bg-white rounded-lg shadow-md p-8 max-w-md mx-auto">
                <form @submit.prevent="handleLogin">
                    <div class="space-y-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                            <input v-model="formData.email" type="email" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Enter your email">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                            <input v-model="formData.password" type="password" required
                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Enter your password">
                        </div>

                        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-700 rounded-lg">
                            {{ errorMessage }}
                        </div>

                        <button type="submit"
                            class="w-full bg-blue-600 text-white px-6 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold disabled:bg-gray-400"
                            :disabled="loading">
                            <span v-if="!loading">Login</span>
                            <span v-else>Logging in...</span>
                        </button>
                        
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

const router = useRouter();
const formData = ref({
    email: '',
    password: ''
});

const loading = ref(false);
const errorMessage = ref('');

const handleLogin = async () => {
    try {
        loading.value = true;
        errorMessage.value = '';
        
        // Add your authentication logic here
        console.log('Login data:', formData.value);
        
        // Simulated successful login
        await new Promise(resolve => setTimeout(resolve, 1000));
        router.push('/');
    } catch (error) {
        errorMessage.value = error.message || 'Login failed. Please try again.';
    } finally {
        loading.value = false;
    }
};
</script>