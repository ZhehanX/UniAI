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
                                    <li>Information such as contact email and URL can be left blank if you don't
                                        want to make it public.</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!-- Basic Information Section -->
                    <div class="space-y-6">
                        <h2 class="text-xl font-semibold text-gray-900 border-b pb-2">Basic Information</h2>

                        <div class="space-y-6">
                            <div>
                                <label for="case-title" class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                                <input id="case-title" v-model="formData.title" type="text" required
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="Enter case title">
                            </div>

                            <!-- Institution field -->
                            <div class="relative">
                                <label for="institution-search" class="block text-sm font-medium text-gray-700 mb-2">Institution *</label>
                                <input id="institution-search" type="text" ref="institutionInput" v-model="institutionSearch"
                                    @focus="handleInputFocus" @blur="handleInputBlur"
                                    @keydown.down.prevent="handleArrowDown" @keydown.up.prevent="handleArrowUp"
                                    @keydown.enter.prevent="handleEnter" @keydown.esc.prevent="handleEscape"
                                    aria-haspopup="listbox" :aria-expanded="showDropdown"
                                    aria-controls="institution-list" placeholder="Search institutions..."
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">

                                <transition name="fade">
                                    <div v-if="showDropdown" id="institution-list" role="listbox"
                                        class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
                                        <template v-if="filteredInstitutions.length === 0">
                                            <div class="p-3 text-gray-500 text-sm">
                                                No institutions found. Select "Add new institution" below.
                                            </div>
                                        </template>
                                        <template v-else>
                                            <div v-for="(institution, index) in filteredInstitutions"
                                                :key="institution.id" role="option"
                                                :aria-selected="focusedItemIndex === index" :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100',
                                                { 'bg-gray-100': focusedItemIndex === index }]" @mousedown.prevent="selectInstitution(institution)"
                                                @keydown.enter.prevent="selectInstitution(institution)" :tabindex="-1"
                                                :ref="el => setItemRef(el, index)">
                                                <div class="font-medium text-gray-900">{{ institution.name }}</div>
                                                <div class="text-sm text-gray-500">
                                                    {{ [institution.city, institution.state, institution.country].filter(Boolean).join(', ') }}
                                                </div>
                                            </div>
                                        </template>
                                        <div role="option" :class="['p-3 hover:bg-gray-50 cursor-pointer border-t border-gray-100',
                    { 'bg-gray-100': focusedItemIndex === filteredInstitutions.length }]"
                                            @mousedown.prevent="handleAddNewInstitution"
                                            @keydown.enter.prevent="handleAddNewInstitution" :tabindex="-1"
                                            :ref="el => setItemRef(el, filteredInstitutions.length)">
                                            <div class="font-medium text-blue-600">+ Add new institution</div>
                                        </div>
                                    </div>
                                </transition>
                            </div>

                            <!-- New Institution Form Fields -->
                            <div v-if="showNewInstitutionFields" class="mt-4 space-y-4 new-institution-section">
                                <div>
                                    <label for="institution-name" class="block text-sm font-medium text-gray-700 mb-2">Institution Name *</label>
                                    <input id="institution-name" name="new-institution-name" v-model="formData.new_institution.name" type="text" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
                                </div>

                                <!-- Country Dropdown -->
                                <label for="country-dropdown" class="block text-sm font-medium text-gray-700 mb-2">Country *</label>
                                <LocationDropdown id="country-dropdown" v-model="countryDropdown.selectedValue"
                                    v-model:show="countryDropdown.showDropdown.value"
                                    :options="countryDropdown.filteredOptions"
                                    :focused-index="countryDropdown.focusedIndex" @select="countryDropdown.selectOption"
                                    @navigate="countryDropdown.keyboardNav" />

                                <!-- State Dropdown -->
                                <label for="state-dropdown" class="block text-sm font-medium text-gray-700 mb-2">State *</label>
                                <LocationDropdown id="state-dropdown" v-model="stateDropdown.selectedValue"
                                    v-model:show="stateDropdown.showDropdown.value"
                                    :options="stateDropdown.filteredOptions" :focused-index="stateDropdown.focusedIndex"
                                    @select="stateDropdown.selectOption" @navigate="stateDropdown.keyboardNav"
                                    :disabled="!countryDropdown.selectedValue" />

                                <!-- City Dropdown -->
                                <label for="city-dropdown" class="block text-sm font-medium text-gray-700 mb-2">City *</label>
                                <LocationDropdown id="city-dropdown" v-model="cityDropdown.selectedValue"
                                    v-model:show="cityDropdown.showDropdown.value"
                                    :options="cityDropdown.filteredOptions" :focused-index="cityDropdown.focusedIndex"
                                    @select="cityDropdown.selectOption" @navigate="cityDropdown.keyboardNav"
                                    :disabled="!stateDropdown.selectedValue" />
                            </div>

                            <!-- AI Technology Used Section -->
                            <div class="relative">
                                <label for="tech-search" class="block text-sm font-medium text-gray-700 mb-2">AI Technology Used *</label>
                                
                                <!-- Selected Technologies -->
                                <div class="flex flex-wrap gap-2 mb-2">
                                    <div v-for="(tech, index) in formData.technologies" :key="index"
                                        class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center">
                                        {{ tech.name }}
                                        <button @click="removeTechnology(index)"
                                            class="ml-2 text-blue-600 hover:text-blue-800">&times;</button>
                                    </div>
                                </div>
                                
                                <!-- Search Input -->
                                <input id="tech-search" type="text" ref="techInput" v-model="aiTechnologySearch"
                                    @focus="handleTechInputFocus" @blur="handleTechInputBlur"
                                    @keydown.down.prevent="handleTechArrowDown" @keydown.up.prevent="handleTechArrowUp"
                                    @keydown.enter.prevent="handleTechEnter" @keydown.esc.prevent="handleTechEscape"
                                    aria-haspopup="listbox" :aria-expanded="showTechDropdown" aria-controls="tech-list"
                                    placeholder="Search AI technologies..."
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
                                
                                <!-- Dropdown -->
                                <transition name="fade">
                                    <div v-if="showTechDropdown" id="tech-list" role="listbox"
                                        class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
                                        <template v-if="filteredTechnologies.length === 0">
                                            <div class="p-3 text-gray-500 text-sm">
                                                No technologies found. Select "Add new technology" below.
                                            </div>
                                        </template>
                                        <template v-else>
                                            <div v-for="(tech, index) in filteredTechnologies" :key="tech.id"
                                                role="option" :aria-selected="focusedTechIndex === index" :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100',
                    { 'bg-gray-100': focusedTechIndex === index }]" @mousedown.prevent="selectTechnology(tech)"
                                                @keydown.enter.prevent="selectTechnology(tech)" :tabindex="-1"
                                                :ref="el => setTechItemRef(el, index)">
                                                <div class="font-medium text-gray-900">{{ tech.name }}</div>
                                            </div>
                                        </template>
                                        <div role="option" :class="['p-3 hover:bg-gray-50 cursor-pointer border-t border-gray-100',
                    { 'bg-gray-100': focusedTechIndex === filteredTechnologies.length }]"
                                            @mousedown.prevent="handleAddNewTechnology"
                                            @keydown.enter.prevent="handleAddNewTechnology" :tabindex="-1"
                                            :ref="el => setTechItemRef(el, filteredTechnologies.length)">
                                            <div class="font-medium text-blue-600">+ Add new technology</div>
                                        </div>
                                    </div>
                                </transition>
                                
                                <!-- New Technology Input Field -->
                                <div v-if="showNewTechField" class="mt-4 space-y-4 new-institution-section">
                                    <div class="space-y-4">
                                        <div>
                                            <label for="new-tech-name" class="block text-sm font-medium text-gray-700 mb-2">Technology Name *</label>
                                            <input id="new-tech-name" v-model="newTechName" type="text" required ref="newTechInput"
                                                @keydown.enter.prevent="confirmNewTechnology"
                                                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                                placeholder="Enter technology name">
                                        </div>
                                        <div class="flex gap-2 pt-2">
                                            <button @click.prevent="confirmNewTechnology"
                                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                                                Add Technology
                                            </button>
                                            <button @click.prevent="cancelNewTechnology"
                                                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium">
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <label for="contact-email" class="block text-sm font-medium text-gray-700 mb-2">Contact Email</label>
                                <input id="contact-email" v-model="formData.contact" type="email"
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="Enter contact email">
                            </div>
                            <div>
                                <label for="project-date" class="block text-sm font-medium text-gray-700 mb-2">Project Initiation Date *</label>
                                <input id="project-date" v-model="formData.projectInitiationDate" type="date" required
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
                            </div>
                        </div>
                    </div>

                    <!-- Additional Information Section -->
                    <div class="space-y-6">
                        <h2 class="text-xl font-semibold text-gray-900 border-b pb-2">Additional Information</h2>

                        <div>
                            <label for="short-description" class="block text-sm font-medium text-gray-700 mb-2">Short Description *</label>
                            <textarea id="short-description" v-model="formData.shortDescription" v-auto-resize required
                                class="auto-resize-textarea w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Brief summary (max 200 characters)"></textarea>
                        </div>

                        <div>
                            <label for="full-description" class="block text-sm font-medium text-gray-700 mb-2">Full Description </label>
                            <textarea id="full-description" v-model="formData.fullDescription.value" v-auto-resize
                                class="auto-resize-textarea w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                placeholder="Detailed description of the case study"></textarea>
                        </div>

                        <div>
                            <label for="case-url" class="block text-sm font-medium text-gray-700 mb-2">Case Study URL</label>
                            <input id="case-url" v-model="formData.url" type="url"
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
                            :disabled="loading" @click="handleSubmit">
                            <span v-if="!loading">Submit Case</span>
                            <span v-else>Sending...</span>
                        </button>
                    </div>
                </div>

            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { Country, State, City } from 'country-state-city';
import { useLocationDropdown } from '@/composables/useLocationDropdown.js';
import useCaseForm from '@/composables/useCaseForm.js'
import LocationDropdown from '@/components/LocationDropdown.vue';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';

// Form data structure
const formData = ref({
    title: '',
    institution_id: null,
    new_institution: {
        name: '',
        country: '',
        state: '',
        city: ''
    },
    technologies: [],
    contact: '',
    projectInitiationDate: '',
    shortDescription: '',
    fullDescription: {
        value: ''
    },
    url: ''
});

// Form submission handling
const {
    loading,
    successMessage,
    errorMessage,
    submitForm
} = useCaseForm()

// Add submit handler
const handleSubmit = async () => {
    const success = await submitForm(formData.value)
    if (success) {
        // Reset form
        formData.value = {
            title: '',
            institution_id: null,
            new_institution: {
                name: '',
                country: '',
                state: '',
                city: ''
            },
            technologies: [],
            contact: '',
            projectInitiationDate: '',
            shortDescription: '',
            fullDescription: {
                value: ''
            },
            url: ''
        }
    }
}

// ===== INSTITUTION HANDLING =====
const institutionSearch = ref('');
const showDropdown = ref(false);
const showNewInstitutionFields = ref(false);
const institutionInput = ref(null);
const focusedItemIndex = ref(-1);
const itemRefs = ref([]);
const isInputFocused = ref(false);


// Use the institutions composable
const { 
  institutions, 
  loading: loadingInstitutions, 
  error: institutionsError,
  fetchAllInstitutions 
} = useInstitutions();

// Fetch institutions on component mount
onMounted(() => {
  fetchAllInstitutions();
});

const filteredInstitutions = computed(() => {
    const search = institutionSearch.value.toLowerCase();
    return institutions.value.filter(inst =>
        inst.name.toLowerCase().includes(search) ||
        inst.city?.toLowerCase().includes(search) ||
        inst.country?.toLowerCase().includes(search)
    );
});

const selectInstitution = (institution) => {
    formData.value.institution_id = institution.id;
    institutionSearch.value = institution.name;
    showDropdown.value = false;
    // Clear new institution fields when selecting existing
    showNewInstitutionFields.value = false;
    formData.value.new_institution = {
        name: '',
        country: '',
        state: '',
        city: ''
    };
    setTimeout(() => {
        institutionInput.value.blur();
        document.activeElement.blur();
    }, 10);
    focusedItemIndex.value = -1;
};

const addNewInstitution = () => {
    formData.value.institution_id = 'new';
    showDropdown.value = false;
    showNewInstitutionFields.value = true;
    institutionSearch.value = '';

    // Force blur the institution input
    institutionInput.value.blur();

    // Focus new institution name field after blur
    nextTick(() => {
        document.querySelector('[name="new-institution-name"]')?.focus();
    });

    formData.value.new_institution = {
        name: '',
        country: '',
        state: '',
        city: ''
    };
    focusedItemIndex.value = -1;
};

const handleAddNewInstitution = () => {
    addNewInstitution();
    // Manually focus the first field of new institution
    nextTick(() => {
        document.querySelector('[name="new-institution-name"]')?.focus();
    });
};

// Institution dropdown keyboard navigation
const handleArrowDown = () => {
    if (!showDropdown.value) return;
    focusedItemIndex.value = Math.min(
        focusedItemIndex.value + 1,
        filteredInstitutions.value.length
    );
    scrollToFocusedItem();
};

const handleArrowUp = () => {
    if (!showDropdown.value) return;
    focusedItemIndex.value = Math.max(focusedItemIndex.value - 1, 0);
    scrollToFocusedItem();
};

const handleEnter = () => {
    if (!showDropdown.value) return;
    if (focusedItemIndex.value === filteredInstitutions.value.length) {
        addNewInstitution();
    } else if (focusedItemIndex.value >= 0) {
        selectInstitution(filteredInstitutions.value[focusedItemIndex.value]);
    }
};

const handleEscape = () => {
    showDropdown.value = false;
    institutionInput.value.blur();
};

const scrollToFocusedItem = async () => {
    await nextTick();
    itemRefs.value[focusedItemIndex.value]?.scrollIntoView({
        block: 'nearest'
    });
};

const setItemRef = (el, index) => {
    itemRefs.value[index] = el;
};

const handleInputFocus = () => {
    isInputFocused.value = true;
    showDropdown.value = true;
    focusedItemIndex.value = 0;
};

const handleInputBlur = () => {
    setTimeout(() => {
        if (!document.activeElement?.closest('[role="option"]')) {
            showDropdown.value = false;
            focusedItemIndex.value = -1;
        }
    }, 0);
};

// Watch for search changes
watch(institutionSearch, (newVal) => {
    if (isInputFocused.value && newVal === '' && !showNewInstitutionFields.value) {
        showDropdown.value = true;
    }
});

// ===== LOCATION HANDLING =====
const currentCountrycode = ref('');
const currentStatecode = ref('');
const currentCitycode = ref('');

// Country, state, city dropdowns
const countryDropdown = useLocationDropdown({
    getOptions: () => Country.getAllCountries(),
    initialValue: formData.value.new_institution.country
});

const stateDropdown = useLocationDropdown({
    parentValue: countryDropdown.selectedValue,
    getOptions: (countryCode) =>
        countryCode ? State.getStatesOfCountry(countryCode) : [],
    initialValue: formData.value.new_institution.state
});

const cityDropdown = useLocationDropdown({
    parentValue: stateDropdown.selectedValue,
    getOptions: (stateCode) =>
        stateCode ? City.getCitiesOfState(currentCountrycode.value, stateCode) : [],
    initialValue: formData.value.new_institution.city
});

watch(countryDropdown.selectedValue, (newValue) => {
    const country = Country.getCountryByCode(newValue);
    formData.value.new_institution.country = country?.name || '';
    currentCountrycode.value = newValue;
    stateDropdown.selectedValue = '';
    cityDropdown.selectedValue = '';
});

watch(stateDropdown.selectedValue, (newValue) => {
    const state = State.getStateByCodeAndCountry(newValue, currentCountrycode.value);
    formData.value.new_institution.state = state?.name || '';
    currentStatecode.value = newValue;
    cityDropdown.selectedValue = '';
});

watch(cityDropdown.selectedValue, (newValue) => {
    currentCitycode.value = newValue;
    formData.value.new_institution.city = newValue;
});

// ===== TECHNOLOGY HANDLING =====
const aiTechnologySearch = ref('');
const showTechDropdown = ref(false);
const focusedTechIndex = ref(-1);
const techItemRefs = ref([]);
const techInput = ref(null);
const showNewTechField = ref(false);
const newTechName = ref('');
const newTechInput = ref(null);


// Use the AI technologies composable
const { 
    technologies, 
    loading: loadingTechnologies, 
    error: technologiesError,
    fetchAllTechnologies 
} = useAiTechnologies();

// Fetch technologies on component mount
onMounted(async () => {
    fetchAllTechnologies();
});


const filteredTechnologies = computed(() => {
    const search = aiTechnologySearch.value.toLowerCase();
    return technologies.value.filter(tech =>
        tech.name.toLowerCase().includes(search)
    );
});

const selectTechnology = (tech) => {
    if (!formData.value.technologies.some(t => t.id === tech.id)) {
        formData.value.technologies.push(tech);
    }
    aiTechnologySearch.value = '';
    // Keep dropdown open and focus input
    showTechDropdown.value = true;
    nextTick(() => techInput.value?.focus());
};

const handleAddNewTechnology = () => {
    showTechDropdown.value = true;
    showNewTechField.value = true;
    aiTechnologySearch.value = '';
    nextTick(() => {
        newTechInput.value?.focus();
    });
    showTechDropdown.value = false;
};

const confirmNewTechnology = () => {
    if (newTechName.value.trim()) {
        const newTech = {
            name: newTechName.value.trim()
        };

        if (!formData.value.technologies.some(t => t.name.toLowerCase() === newTech.name.toLowerCase())) {
            formData.value.technologies.push(newTech);
        }

        newTechName.value = '';
        showNewTechField.value = false;
        nextTick(() => techInput.value?.focus());
    }
};

const cancelNewTechnology = () => {
    showNewTechField.value = false;
    newTechName.value = '';
    nextTick(() => techInput.value?.focus());
};

const removeTechnology = (index) => {
    formData.value.technologies.splice(index, 1);
};

// Technology dropdown keyboard navigation
const handleTechArrowDown = () => {
    if (!showTechDropdown.value) return;
    focusedTechIndex.value = Math.min(
        focusedTechIndex.value + 1,
        filteredTechnologies.value.length
    );
    scrollToFocusedTechItem();
};

const handleTechArrowUp = () => {
    if (!showTechDropdown.value) return;
    focusedTechIndex.value = Math.max(focusedTechIndex.value - 1, 0);
    scrollToFocusedTechItem();
};

const handleTechEnter = () => {
    if (!showTechDropdown.value) return;
    if (focusedTechIndex.value === filteredTechnologies.value.length) {
        handleAddNewTechnology();
    } else if (focusedTechIndex.value >= 0) {
        selectTechnology(filteredTechnologies.value[focusedTechIndex.value]);
    }
};

const handleTechEscape = () => {
    showTechDropdown.value = false;
    techInput.value.blur();
};

const scrollToFocusedTechItem = async () => {
    await nextTick();
    techItemRefs.value[focusedTechIndex.value]?.scrollIntoView({
        block: 'nearest'
    });
};

const setTechItemRef = (el, index) => {
    techItemRefs.value[index] = el;
};

const handleTechInputFocus = () => {
    showTechDropdown.value = true;
    focusedTechIndex.value = 0;
};

const handleTechInputBlur = () => {
    setTimeout(() => {
        if (!document.activeElement?.closest('[role="option"]')) {
            showTechDropdown.value = false;
            focusedTechIndex.value = -1;
        }
    }, 0);
};

// ===== UTILITIES =====
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
</script>
