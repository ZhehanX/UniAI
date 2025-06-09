<template>
    <div
        class="group cursor-pointer bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 flex flex-col w-full mx-auto">
        <!-- Content Section -->
        <div class="w-full p-6 md:p-8 flex flex-col justify-between">
            <div>
                <h3 class="text-2xl font-bold text-gray-800 mb-4">{{ app.title }}</h3>
                <p class="text-gray-600 text-lg mb-6 leading-relaxed">
                    {{ app.short_description }}
                </p>
            </div>
            <!-- Metadata Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-600">
                <!-- app.institution is only returned by search, app.institution_id is in both -->
                <div v-if="app.institution || app.institution_id" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">Institution:</span>
                    <span class="ml-2">{{ institutionDisplay }}</span>
                </div>
                <div v-if="app.contact" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">Contact:</span>
                    <span class="ml-2 break-all">{{ app.contact }}</span>
                </div>
                <!-- app.ai_technologies_names is returned by search, app.ai_technologies is the normal return -->
                <div v-if="app.ai_technologies || app.ai_technologies_names" class="flex items-start">
                    <span class="font-semibold min-w-[120px]">AI Technologies:</span>
                    <span class="ml-2">
                        {{ technologiesDisplay }}
                    </span>
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
import { ref, onMounted, computed } from 'vue';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';
import { useInstitutions } from '@/composables/useInstitutions';

const props = defineProps({
    app: {
        type: Object,
        required: true
    }
});


// Import the useAiTechnologies composable
const { fetchTechnologyDetails } = useAiTechnologies();
const { fetchInstitutionDetailsById } = useInstitutions();

// State to store technology names
const techNames = ref([]);
// State to store institution name
let institutionName = ref('');


// Fetch institution on component mount
onMounted(async () => {
    if (props.app.institution_id) {
        try {
            // Fetch institution name
            const institutionDetails = await fetchInstitutionDetailsById(props.app.institution_id);
            institutionName.value = institutionDetails ? institutionDetails.name : `Institution ${props.app.institution_id}`;
        } catch (err) {
            console.error('Error fetching institution details:', err);
        }
    }
});


// Fetch technology names on component mount
onMounted(async () => {
    if (props.app.ai_technologies && Array.isArray(props.app.ai_technologies)) {
        // Fetch each technology name
        const promises = props.app.ai_technologies.map(async (techId) => {
            try {
                const techDetails = await fetchTechnologyDetails(techId);
                return techDetails ? techDetails.name : `Tech ${techId}`;
            } catch (error) {
                console.error(`Error fetching tech ${techId}:`, error);
                return `Tech ${techId}`;
            }
        });

        techNames.value = await Promise.all(promises);
    }
});


// Computed property to display institution name
const institutionDisplay = computed(() => {
    // If institution is present (from search), use it directly. This is what the search returns
    if (props.app.institution) {
        return props.app.institution.name;
    }
    // Otherwise, use fetched names from IDs
    return institutionName.value;
});


// Computed property to display technology names as a comma-separated string
const technologiesDisplay = computed(() => {
    // If ai_technologies_names is present (from search), use it directly. This is what the search returns
    if (props.app.ai_technologies_names) {
        return props.app.ai_technologies_names.join(', ');
    }
    // Otherwise, use fetched names from IDs
    return techNames.value.join(', ');
});
</script>