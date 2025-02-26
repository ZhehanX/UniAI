<template>
    <div class="min-h-screen bg-gray-50">
        <header class="bg-white shadow">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">Submit New Case</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Overview
                </button>
            </div>
        </header>

        <main class="container mx-auto px-6 py-8">
            <div class="bg-white rounded-lg shadow-md p-8">
                <form @submit.prevent="submitCase">
                    <div class="space-y-8">
                        <!-- Basic Information Section -->
                        <div class="space-y-6">
                            <h2 class="text-xl font-semibold text-gray-900 border-b pb-2">Basic Information</h2>

                            <div class="space-y-6">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                                    <input v-model="formData.title" type="text" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                        placeholder="Enter case title">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Institution *</label>
                                    <input v-model="formData.institution" type="text" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                        placeholder="Enter institution name">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">AI Technology Used
                                        *</label>
                                    <input v-model="formData.technology" type="text" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                        placeholder="List AI technologies">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Contact Email *</label>
                                    <input v-model="formData.contact" type="email" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                        placeholder="Enter contact email">
                                </div>
                            </div>
                        </div>

                        <!-- Additional Information Section -->
                        <div class="space-y-6">
                            <h2 class="text-xl font-semibold text-gray-900 border-b pb-2">Additional Information</h2>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Short Description *</label>
                                <textarea v-model="formData.shortDescription" v-auto-resize required
                                    class="auto-resize-textarea w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="Brief summary (max 200 characters)"></textarea>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Full Description </label>
                                <textarea v-model="formData.fullDescription" v-auto-resize required
                                    class="auto-resize-textarea w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="Detailed description of the case study"></textarea>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Case Study URL</label>
                                <input v-model="formData.url" type="url"
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="https://example.com/case-study">
                            </div>
                        </div>

                        <!-- Status Messages -->
                        <div v-if="successMessage" class="p-4 bg-green-100 text-green-700 rounded-lg">
                            {{ successMessage }}
                        </div>
                        <div v-if="errorMessage" class="p-4 bg-red-100 text-red-700 rounded-lg">
                            {{ errorMessage }}
                        </div>

                        <!-- Submit Button -->
                        <div class="pt-6">
                            <button type="submit"
                                class="w-full bg-blue-600 text-white px-6 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold disabled:bg-gray-400"
                                :disabled="loading">
                                <span v-if="!loading">Submit Case</span>
                                <span v-else>Sending...</span>
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// Auto-resize directive
const vAutoResize = {
    mounted(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
        el.style.overflowY = 'hidden';
        el.addEventListener('input', () => {
            el.style.height = 'auto';
            el.style.height = el.scrollHeight + 'px';
        });
    },
    updated(el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
    }
};

const formData = ref({
    title: '',
    institution: '',
    technology: '',
    contact: '',
    shortDescription: '',
    fullDescription: '',
    url: ''
});

const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const submitCase = async () => {
    try {
        loading.value = true;
        errorMessage.value = '';
        successMessage.value = '';

        // Send email using Formspree or similar service
        const response = await fetch("https://formspree.io/f/YOUR_FORM_ID", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                subject: `New Case Submission: ${formData.value.title}`,
                _replyto: formData.value.contact,
                message: `
                    New Case Submission Details:
                    
                    Title: ${formData.value.title}
                    Institution: ${formData.value.institution}
                    Technology: ${formData.value.technology}
                    Contact Email: ${formData.value.contact}
                    URL: ${formData.value.url}
                    
                    Short Description:
                    ${formData.value.shortDescription}
                    
                    Full Description:
                    ${formData.value.fullDescription}
                `
            }),
        });

        if (response.ok) {
            successMessage.value = 'Submission successful! Thank you for your contribution.';
            formData.value = {
                title: '',
                institution: '',
                technology: '',
                contact: '',
                shortDescription: '',
                fullDescription: '',
                url: ''
            };
        } else {
            throw new Error('Failed to submit form');
        }
    } catch (error) {
        errorMessage.value = 'There was an error submitting your case. Please try again.';
    } finally {
        loading.value = false;
    }
};
</script>
<style>
.auto-resize-textarea {
    resize: none;
    min-height: 100px;
    max-height: 400px;
    transition: height 0.2s ease-out;
}

@media (min-width: 640px) {
    .auto-resize-textarea {
        min-height: 120px;
        max-height: 600px;
    }
}
</style>