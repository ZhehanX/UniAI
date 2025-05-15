<template>
    <div>
        <!-- Search status -->
        <div v-if="query.trim() || isAdvancedSearch" class="mb-4">
            <p v-if="isSearching" class="text-gray-600">Searching...</p>
            <p v-else-if="results.length === 0" class="text-gray-600">
                No results found {{ query.trim() ? `for "${query}"` : 'for your advanced search' }}
            </p>
            <p v-else class="text-gray-600">
                Found {{ results.length }} results {{ query.trim() ? `for "${query}"` : 'for your advanced search' }}
            </p>
        </div>
        
        <!-- Results list -->
        <div v-if="results.length > 0" class="space-y-6">
            <slot name="results" :results="filteredResults">
                <!-- Default rendering if no slot is provided -->
                <div v-for="result in filteredResults" :key="result.id" 
                     tabindex="0"
                     role="button"
                     @click="$emit('select', result)"
                     @keydown.enter="$emit('select', result)"
                     @keydown.space="$emit('select', result)"
                     class="border rounded-lg p-6 hover:shadow-lg transition-all cursor-pointer">
                    <h3 class="text-xl font-bold mb-2">{{ result.title }}</h3>
                    <p class="text-gray-600">{{ result.short_description }}</p>
                </div>
            </slot>
        </div>
        
        <!-- No results message -->
        <div v-else-if="query.trim() && !isSearching" class="text-center py-8">
            <p class="text-gray-500">No results match your search criteria.</p>
            <button @click="$emit('clear')" class="mt-2 text-blue-600 hover:text-blue-800">
                Clear search
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    results: {
        type: Array,
        default: () => []
    },
    query: {
        type: String,
        default: ''
    },
    isSearching: {
        type: Boolean,
        default: false
    },
    filter: {
        type: Function,
        default: null
    },
    isAdvancedSearch: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['select', 'clear']);

// Apply custom filter if provided, otherwise return all results
const filteredResults = computed(() => {
    if (props.filter) {
        return props.results.filter(props.filter);
    }
    return props.results;
});
</script>