<template>
    <div class="group cursor-pointer bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 flex flex-col md:flex-row w-full mx-auto">
        <!-- Image Section (20%) -->
        <div class="w-full md:w-1/5 flex-shrink-0 bg-gray-100 border-r border-gray-200">
            <div v-if="!app.imagePath" class="w-full h-full flex items-center justify-center text-gray-400 p-4 min-h-[200px]">
                <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
            </div>
            <img v-else 
                :src="app.imagePath" 
                :alt="app.name" 
                class="w-full h-full object-cover min-h-[200px] md:min-h-[300px]">
        </div>

        <!-- Content Section (80%) -->
        <div class="w-full md:w-4/5 p-6 md:p-8 flex flex-col justify-between">
            <div>
                <h3 class="text-2xl font-bold text-gray-800 mb-4">{{ app.title }}</h3>
                <p class="text-gray-600 text-lg mb-6 leading-relaxed">
                    {{ app.short_description }}
                </p>
            </div>
            
            <!-- Metadata Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-600">
                <div v-if="app.institution" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">Institution:</span>
                    <span class="ml-2">{{ app.institution }}</span>
                </div>
                <div v-if="app.contact" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">Contact:</span>
                    <span class="ml-2 break-all">{{ app.contact }}</span>
                </div>
                <div v-if="app.ai_technologies" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">AI Technologies:</span>
                    <span class="ml-2">{{ app.ai_technologies.join(', ') }}</span>
                </div>
                <div v-if="app.url" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">Website:</span>
                    <a :href="app.url" target="_blank" class="ml-2 text-blue-600 hover:underline break-all">
                        {{ app.url }}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    app: {
        type: Object,
        required: true
    }
});
</script>