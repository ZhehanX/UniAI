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
                        <!-- Usage Information Notice -->
                        <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                            <div class="flex items-start space-x-2 text-blue-800">
                                <svg class="w-4 h-4 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd"
                                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                        clip-rule="evenodd"></path>
                                </svg>
                                <div class="text-sm">
                                    <p class="font-medium">How we use the information:</p>
                                    <ul class="list-disc pl-4 space-y-1 mt-1">
                                        <li>All the information you submit will be published on our public website.</li> 
                                        <li>Information such as contact email and URL can be left blank if you don't want to make it public.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
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
                                <textarea v-model="formData.fullDescription" v-auto-resize
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

// Auto-resize text-area
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

        // Validate all required fields
        const requiredFields = [
            formData.value.title,
            formData.value.institution,
            formData.value.technology,
            formData.value.contact
        ];

        if (requiredFields.some(field => !field?.trim())) {
            errorMessage.value = 'Please fill all required fields';
            loading.value = false;
            return;
        }

        const response = await fetch("https://formspree.io/f/mkgodnrv", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                email: formData.value.contact,
                _replyto: formData.value.contact,
                _subject: `New Case Submission: ${formData.value.title}`,
                title: formData.value.title,
                institution: formData.value.institution,
                technology: formData.value.technology,
                url: formData.value.url,
                short_description: formData.value.shortDescription,
                full_description: formData.value.fullDescription
            }),
        });

        const data = await response.json();

        if (response.ok) {
            successMessage.value = 'Submission successful! Thank you.';
            // Reset form properly
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
            throw new Error(data.errors?.map(e => e.message).join(', ') || 'Submission failed');
        }
    } catch (error) {
        errorMessage.value = error.message || 'Submission error. Please try again.';
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