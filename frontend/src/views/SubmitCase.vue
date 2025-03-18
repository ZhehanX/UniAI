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
                                <label class="block text-sm font-medium text-gray-700 mb-2">Title *</label>
                                <input v-model="formData.title" type="text" required
                                    class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                                    placeholder="Enter case title">
                            </div>
                            <div class="relative">
                                <label class="block text-sm font-medium text-gray-700 mb-2">Institution *</label>
                                <input type="text" ref="institutionInput" v-model="institutionSearch"
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
                                                <div class="text-sm text-gray-500">{{ institution.city }}, {{
                    institution.country }}</div>
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
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Institution Name
                                        *</label>
                                    <input v-model="formData.new_institution.name" type="text" required
                                        class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
                                </div>


                                <!-- Country Dropdown -->
                                <div class="relative dropdown-container">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Country *</label>
                                    <div class="relative">
                                        <button type="button" aria-haspopup="listbox"
                                            :aria-expanded="showCountryDropdown"
                                            :aria-activedescendant="focusedCountryIndex >= 0 ? `country-${focusedCountryIndex}` : null"
                                            @click="toggleCountryDropdown" @keydown.down.prevent="handleCountryKeyDown"
                                            @keydown.up.prevent="handleCountryKeyUp"
                                            @keydown.enter.prevent="handleCountryEnter"
                                            @keydown.space.prevent="handleCountryEnter"
                                            @keydown.esc.prevent="closeCountryDropdown"
                                            class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all flex justify-between items-center">
                                            {{ selectedCountryName || 'Select Country' }}
                                            <svg class="w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd"
                                                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </button>
                                        <transition name="fade">
                                            <div v-if="showCountryDropdown"
                                                class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
                                                <div :id="`country-${index}`" v-for="(country, index) in countries"
                                                    :key="country.isoCode" role="option"
                                                    :aria-selected="focusedCountryIndex === index" :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0',
                    { 'bg-gray-100': focusedCountryIndex === index }]" @click="selectCountry(country)"
                                                    @keydown.enter.prevent="selectCountry(country)"
                                                    @keydown.space.prevent="selectCountry(country)"
                                                    @mouseenter="focusedCountryIndex = index" tabindex="-1">
                                                    {{ country.name }}
                                                </div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>


                                <!-- State Dropdown -->
                                <div class="relative dropdown-container" v-if="states.length">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">State/Province *</label>
                                    <div class="relative">
                                        <button type="button" aria-haspopup="listbox" :aria-expanded="showStateDropdown"
                                            :aria-activedescendant="focusedStateIndex >= 0 ? `state-${focusedStateIndex}` : null"
                                            @click="toggleStateDropdown" @keydown.down.prevent="handleStateKeyDown"
                                            @keydown.up.prevent="handleStateKeyUp"
                                            @keydown.enter.prevent="handleStateEnter"
                                            @keydown.space.prevent="handleStateEnter"
                                            @keydown.esc.prevent="closeStateDropdown"
                                            class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all flex justify-between items-center">
                                            {{ selectedStateName || 'Select State' }}
                                            <svg class="w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd"
                                                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </button>
                                        <transition name="fade">
                                            <div v-if="showStateDropdown"
                                                class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
                                                <div :id="`state-${index}`" v-for="(state, index) in states"
                                                    :key="state.isoCode" role="option"
                                                    :aria-selected="focusedStateIndex === index" :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0',
                    { 'bg-gray-100': focusedStateIndex === index }]" @click="selectState(state)"
                                                    @keydown.enter.prevent="selectState(state)"
                                                    @keydown.space.prevent="selectState(state)" tabindex="-1">
                                                    {{ state.name }}
                                                </div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>


                                <!-- City Dropdown -->
                                <div class="relative dropdown-container" v-if="cities.length">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">City *</label>
                                    <div class="relative">
                                        <button type="button" aria-haspopup="listbox" :aria-expanded="showCityDropdown"
                                            :aria-activedescendant="focusedCityIndex >= 0 ? `city-${focusedCityIndex}` : null"
                                            @click="toggleCityDropdown" @keydown.down.prevent="handleCityKeyDown"
                                            @keydown.up.prevent="handleCityKeyUp"
                                            @keydown.enter.prevent="handleCityEnter"
                                            @keydown.space.prevent="handleCityEnter"
                                            @keydown.esc.prevent="closeCityDropdown"
                                            class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all flex justify-between items-center">
                                            {{ formData.new_institution.city || 'Select City' }}
                                            <svg class="w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                                                <path fill-rule="evenodd"
                                                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </button>
                                        <transition name="fade">
                                            <div v-if="showCityDropdown"
                                                class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
                                                <div :id="`city-${index}`" v-for="(city, index) in cities"
                                                    :key="city.name" role="option"
                                                    :aria-selected="focusedCityIndex === index" :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0',
                    { 'bg-gray-100': focusedCityIndex === index }]" @click="selectCity(city)"
                                                    @keydown.enter.prevent="selectCity(city)"
                                                    @keydown.space.prevent="selectCity(city)" tabindex="-1">
                                                    {{ city.name }}
                                                </div>
                                            </div>
                                        </transition>
                                    </div>
                                </div>
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
                                <input v-model="formData.contact" type="email"
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

            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { Country, State, City } from 'country-state-city';

// Add these new reactive states
const countries = ref([]);
const states = ref([]);
const cities = ref([]);
const selectedCountry = ref('');
const selectedState = ref('');
const showCountryDropdown = ref(false);
const showStateDropdown = ref(false);
const showCityDropdown = ref(false);
const focusedCountryIndex = ref(-1);
const focusedStateIndex = ref(-1);
const focusedCityIndex = ref(-1);

const selectedCountryName = computed(() => {
    const country = countries.value.find(c => c.isoCode === selectedCountry.value);
    return country ? country.name : '';
});

const selectedStateName = computed(() => {
    const state = states.value.find(s => s.isoCode === selectedState.value);
    return state ? state.name : '';
});



const selectCountry = (country) => {
    selectedCountry.value = country.isoCode;
    showCountryDropdown.value = false;
    focusedCountryIndex.value = -1; // Reset focus
    loadStates();
};


const selectState = (state) => {
    selectedState.value = state.isoCode;
    showStateDropdown.value = false;
    loadCities();
};


const selectCity = (city) => {
    formData.value.new_institution.city = city;
    showCityDropdown.value = false;
};



const scrollToCountryOption = () => {
    nextTick(() => {
        const option = document.getElementById(`country-${focusedCountryIndex.value}`);
        if (option) option.scrollIntoView({ block: 'nearest' });
    });
};

const scrollToStateOption = () => {
    nextTick(() => {
        const option = document.getElementById(`state-${focusedStateIndex.value}`);
        if (option) option.scrollIntoView({ block: 'nearest' });
    });
};

const scrollToCityOption = () => {
    nextTick(() => {
        const option = document.getElementById(`city-${focusedCityIndex.value}`);
        if (option) option.scrollIntoView({ block: 'nearest' });
    });
};



// Country handlers
const handleCountryEnter = () => {
    if (showCountryDropdown.value) {
        if (focusedCountryIndex.value >= 0) {
            selectCountry(countries.value[focusedCountryIndex.value]);
        }
    } else {
        toggleCountryDropdown();
    }
};

const handleCountryKeyDown = (e) => {
    if (!showCountryDropdown.value) return;
    focusedCountryIndex.value = Math.min(
        focusedCountryIndex.value + 1,
        countries.value.length - 1
    );
    scrollToCountryOption();
};

const handleCountryKeyUp = (e) => {
    if (!showCountryDropdown.value) return;
    focusedCountryIndex.value = Math.max(focusedCountryIndex.value - 1, 0);
    scrollToCountryOption();
};

const toggleCountryDropdown = () => {
    showCountryDropdown.value = !showCountryDropdown.value;
    if (showCountryDropdown.value) {
        const selectedIndex = countries.value.findIndex(c => c.isoCode === selectedCountry.value);
        focusedCountryIndex.value = selectedIndex >= 0 ? selectedIndex : 0;
    } else {
        focusedCountryIndex.value = -1;
    }
};

// State handlers
const handleStateEnter = () => {
    if (showStateDropdown.value) {
        if (focusedStateIndex.value >= 0) {
            selectState(states.value[focusedStateIndex.value]);
        }
    } else {
        toggleStateDropdown();
    }
};

const handleStateKeyDown = (e) => {
    if (!showStateDropdown.value) return;
    focusedStateIndex.value = Math.min(
        focusedStateIndex.value + 1,
        states.value.length - 1
    );
    scrollToStateOption();
};

const handleStateKeyUp = (e) => {
    if (!showStateDropdown.value) return;
    focusedStateIndex.value = Math.max(focusedStateIndex.value - 1, 0);
    scrollToStateOption();
};

const toggleStateDropdown = () => {
    showStateDropdown.value = !showStateDropdown.value;
    if (showStateDropdown.value) {
        const selectedIndex = states.value.findIndex(s => s.isoCode === selectedState.value);
        focusedStateIndex.value = selectedIndex >= 0 ? selectedIndex : 0;
    } else {
        focusedStateIndex.value = -1;
    }
};

// City handlers
const handleCityEnter = () => {
    if (showCityDropdown.value) {
        if (focusedCityIndex.value >= 0) {
            selectCity(cities.value[focusedCityIndex.value]);
        }
    } else {
        toggleCityDropdown();
    }
};

const handleCityKeyDown = (e) => {
    if (!showCityDropdown.value) return;
    focusedCityIndex.value = Math.min(
        focusedCityIndex.value + 1,
        cities.value.length - 1
    );
    scrollToCityOption();
};

const handleCityKeyUp = (e) => {
    if (!showCityDropdown.value) return;
    focusedCityIndex.value = Math.max(focusedCityIndex.value - 1, 0);
    scrollToCityOption();
};

const toggleCityDropdown = () => {
    showCityDropdown.value = !showCityDropdown.value;
    if (showCityDropdown.value) {
        const selectedIndex = cities.value.findIndex(c => c.name === formData.value.new_institution.city);
        focusedCityIndex.value = selectedIndex >= 0 ? selectedIndex : 0;
    } else {
        focusedCityIndex.value = -1;
    }
};


const closeAllDropdowns = () => {
    showCountryDropdown.value = false;
    showStateDropdown.value = false;
    showCityDropdown.value = false;
};

// Add to mounted()
document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
        closeAllDropdowns();
    }
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown-container')) {
        closeAllDropdowns();
    }
});



// Add new reactive states
const focusedItemIndex = ref(-1);
const itemRefs = ref([]);

const handleAddNewInstitution = () => {
    addNewInstitution();
    // Manually focus the first field of new institution
    nextTick(() => {
        document.querySelector('[name="new-institution-name"]')?.focus();
    });
};

// Keyboard navigation handlers
const handleArrowDown = () => {
    if (!showDropdown.value) return;
    focusedItemIndex.value = Math.min(
        focusedItemIndex.value + 1,
        filteredInstitutions.value.length // Include "Add new" option
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


// Load countries on mount
onMounted(() => {
    countries.value = Country.getAllCountries();
});

const loadStates = () => {
    formData.value.new_institution.country = selectedCountry.value;
    states.value = State.getStatesOfCountry(selectedCountry.value);
    cities.value = [];
    selectedState.value = '';
    formData.value.new_institution.city = '';
};

const loadCities = () => {
    formData.value.new_institution.state = selectedState.value;
    cities.value = City.getCitiesOfState(selectedCountry.value, selectedState.value);
    formData.value.new_institution.city = '';
};



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

// Fetch institutions on component mount
onMounted(async () => {
    try {
        loadingInstitutions.value = true;
        const response = await fetch('http://localhost:8000/api/institutions/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        institutions.value = await response.json();
    } catch (error) {
        console.error('Error fetching institutions:', error);
        errorMessage.value = 'Could not load institution list';
    } finally {
        loadingInstitutions.value = false;
    }
});

const institutionSearch = ref('');
const showDropdown = ref(false);
const institutions = ref([]);
const showNewInstitutionFields = ref(false);
const loadingInstitutions = ref(false);
const institutionInput = ref(null)

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

const filteredInstitutions = computed(() => {
    const search = institutionSearch.value.toLowerCase();
    return institutions.value.filter(inst =>
        inst.name.toLowerCase().includes(search) ||
        inst.city?.toLowerCase().includes(search) ||
        inst.country?.toLowerCase().includes(search)
    );
});

// Add these new reactive states
const isInputFocused = ref(false)

// Watch for search changes
watch(institutionSearch, (newVal) => {
    if (isInputFocused.value && newVal === '' && !showNewInstitutionFields.value) {
        showDropdown.value = true;
    }
});




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







// Updated form data structure
const formData = ref({
    title: '',
    institution_id: null,
    new_institution: {
        name: '',
        country: '',
        state: '',
        city: ''
    },
    technology: '',
    contact: '',
    shortDescription: '',
    fullDescription: '',
    url: ''
});


</script>
<style>
.new-institution-section {
    border-left: 2px solid #2563eb;
    padding-left: 1rem;
    transition: all 0.2s ease;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}

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