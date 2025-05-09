<template>
    <div class="relative w-full">
        <!-- Basic/Advanced Search Toggle -->
        <div class="flex justify-end mb-2">
            <button 
                @click="toggleAdvancedSearch" 
                class="text-sm text-blue-600 hover:text-blue-800 flex items-center"
                type="button"
            >
                {{ isAdvancedSearch ? 'Simple Search' : 'Advanced Search' }}
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
            </button>
        </div>

        <!-- Basic Search -->
        <div v-if="!isAdvancedSearch" class="flex items-center border border-gray-300 rounded-lg overflow-hidden shadow-sm">
            <input 
                type="text" 
                v-model="localSearchQuery" 
                @input="handleInput"
                @keydown.enter="handleSearch"
                :placeholder="placeholder" 
                class="w-full px-4 py-3 focus:outline-none"
                :disabled="disabled"
                :aria-label="ariaLabel"
            />
            <button 
                @click="handleSearch" 
                class="bg-blue-600 text-white px-6 py-4 hover:bg-blue-700 transition-colors flex items-center justify-center"
                :disabled="disabled"
                :aria-label="searchButtonAriaLabel"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </button>
        </div>

        <!-- Advanced Search -->
        <div v-else class="border border-gray-300 rounded-lg overflow-hidden shadow-sm">
            <div class="p-4 space-y-4">
                <!-- Title -->
                <div class="grid grid-cols-1 gap-2">
                    <label for="title-search" class="text-sm font-medium text-gray-700">Title</label>
                    <input 
                        id="title-search"
                        type="text" 
                        v-model="advancedFilters.title" 
                        placeholder="Search by title..." 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <!-- Institution -->
                <div class="grid grid-cols-1 gap-2">
                    <label for="institution-search" class="text-sm font-medium text-gray-700">Institution</label>
                    <input 
                        id="institution-search"
                        type="text" 
                        v-model="advancedFilters.institution" 
                        placeholder="Search by institution..." 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <!-- AI Technology -->
                <div class="grid grid-cols-1 gap-2">
                    <label for="technology-search" class="text-sm font-medium text-gray-700">AI Technology</label>
                    <input 
                        id="technology-search"
                        type="text" 
                        v-model="advancedFilters.technology" 
                        placeholder="Search by AI technology..." 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <!-- Location -->
                <div class="grid grid-cols-1 gap-2">
                    <label for="location-search" class="text-sm font-medium text-gray-700">Location</label>
                    <input 
                        id="location-search"
                        type="text" 
                        v-model="advancedFilters.location" 
                        placeholder="Search by location..." 
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <!-- Search and Reset Buttons -->
                <div class="flex justify-end space-x-2">
                    <button 
                        @click="resetAdvancedSearch" 
                        class="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 transition-colors"
                        :disabled="disabled"
                    >
                        Reset
                    </button>
                    <button 
                        @click="handleAdvancedSearch" 
                        class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
                        :disabled="disabled"
                    >
                        Search
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, reactive } from 'vue';

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    placeholder: {
        type: String,
        default: 'Search...'
    },
    disabled: {
        type: Boolean,
        default: false
    },
    ariaLabel: {
        type: String,
        default: 'Search input'
    },
    searchButtonAriaLabel: {
        type: String,
        default: 'Search button'
    }
});

const emit = defineEmits(['update:modelValue', 'search', 'input', 'advanced-search']);

const localSearchQuery = ref(props.modelValue);
const isAdvancedSearch = ref(false);
const advancedFilters = reactive({
    title: '',
    institution: '',
    technology: '',
    location: ''
});

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
    localSearchQuery.value = newValue;
});

// Toggle between basic and advanced search
const toggleAdvancedSearch = () => {
    isAdvancedSearch.value = !isAdvancedSearch.value;
    
    // Reset filters when switching modes
    if (isAdvancedSearch.value) {
        localSearchQuery.value = '';
        emit('update:modelValue', '');
    } else {
        emit('search', ""); // Emit empty search query to reset the search result
        Object.keys(advancedFilters).forEach(key => {
            advancedFilters[key] = '';
        });
    }
};

// Reset advanced search filters
const resetAdvancedSearch = () => {
    emit('search', ""); // Emit empty search query to reset the search result
    Object.keys(advancedFilters).forEach(key => {
        advancedFilters[key] = '';
    });
};

// Handle input for basic search
const handleInput = () => {
    emit('update:modelValue', localSearchQuery.value);
    emit('input', localSearchQuery.value);
};

// Handle basic search button click
const handleSearch = () => {
    emit('search', localSearchQuery.value);
};

// Handle advanced search button click
const handleAdvancedSearch = () => {
    // Filter out empty fields
    const filters = {};
    Object.entries(advancedFilters).forEach(([key, value]) => {
        if (value.trim()) {
            filters[key] = value.trim();
        }
    });
    
    // Only emit if at least one filter is set
    if (Object.keys(filters).length > 0) {
        emit('advanced-search', filters);
    }
};
</script>