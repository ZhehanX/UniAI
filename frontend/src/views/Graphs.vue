<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="bg-white shadow mb-6 -mx-6 px-6 py-4">
            <div class="container mx-auto flex items-center justify-between">
                <h1 class="text-2xl font-bold text-gray-900">AI Use Cases Analytics</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Overview
                </button>
            </div>
        </header>

        <!-- Toggle Buttons -->
        <div class="flex justify-center mb-6">
            <div class="inline-flex rounded-md shadow-sm" role="group">
                <button @click="activeTab = 'map'" :class="[
                    'px-4 py-2 text-sm font-medium rounded-l-lg border',
                    activeTab === 'map'
                        ? 'bg-blue-200 text-blue-800 border-blue-300'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
                ]">
                    Map
                </button>
                <button @click="activeTab = 'stats'" :class="[
                    'px-4 py-2 text-sm font-medium rounded-r-lg border',
                    activeTab === 'stats'
                        ? 'bg-blue-200 text-blue-800 border-blue-300'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
                ]">
                    Stats
                </button>
            </div>
        </div>

        <!-- Content Area -->
        <div class="bg-white rounded-lg shadow p-6">
            <!-- Map Section -->
            <div v-if="activeTab === 'map'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="h-200 bg-gray-100 rounded-lg">
                    <!-- Map Component will go here -->
                    <MapComponent :cases="filteredCases" />
                    {{ console.log('Passing to map component:', filteredCases) }}
                </div>
                <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <!-- Filters for Map -->
                    <h3 class="text-lg font-medium mb-4">Filters</h3>

                    <div class="mb-4">
                        <h4 class="font-medium mb-2">Institution</h4>
                        <div class="space-y-2">
                            <div v-for="institution in institutions" :key="institution.id" class="flex items-center">
                                <input type="checkbox" :id="`inst-${institution.id}`" v-model="selectedInstitutions"
                                    :value="institution.id" class="mr-2">
                                <label :for="`inst-${institution.id}`">{{ institution.name }}</label>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h4 class="font-medium mb-2">AI Tech</h4>
                        <div class="space-y-2">
                            <div v-for="tech in aiTechnologies" :key="tech.id" class="flex items-center">
                                <input type="checkbox" :id="`tech-${tech.id}`" v-model="selectedTechnologies"
                                    :value="tech.id" class="mr-2">
                                <label :for="`tech-${tech.id}`">{{ tech.name }}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Section -->
            <div v-else-if="activeTab === 'stats'" class="flex flex-col gap-4">
                
                <!-- Chart Navigation -->
                <div class="flex justify-center items-center mb-2">
                    <button @click="prevChart" class="px-3 py-1 text-gray-600 hover:text-gray-800">
                        &lt;
                    </button>
                    <span class="mx-4 text-sm text-gray-700 font-medium">
                        {{ availableCharts[currentChartIndex] === 'technology' ? 'Technology Distribution' : 'Yearly Trends' }}
                    </span>
                    <button @click="nextChart" class="px-3 py-1 text-gray-600 hover:text-gray-800">
                        &gt;
                    </button>
                </div>

                <!-- Charts and Filters Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="h-200 bg-white rounded-lg shadow">
                        <!-- Pie Chart -->
                        <ChartComponent v-if="currentChartType === 'pie'" :data="chartData"
                            title="AI Technologies Distribution" chartType="pie" />
                        <!-- Line Chart -->
                        <ChartComponent v-else-if="currentChartType === 'line'" :data="yearlyTrendData"
                            title="AI Technologies Adoption Over Time" chartType="line" />
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <!-- Filters for Stats -->
                        <h3 class="text-lg font-medium mb-2">Filters</h3>
                        <p class="text-sm text-gray-600 mb-4">
                            {{ currentChartType === 'pie'
                    ? 'Filter technology distribution by location.'
                    : 'Filter yearly trends by AI technology.' }}
                            Select only what you need.
                        </p>

                        <!-- Location filters (for pie chart) -->
                        <div v-if="currentChartType === 'pie'">
                            <div class="mb-4">
                                <h4 class="font-medium mb-2">Country</h4>
                                <LocationDropdown id="country-dropdown" v-model="countryDropdown.selectedValue"
                                    v-model:show="countryDropdown.showDropdown.value"
                                    :options="countryDropdown.filteredOptions"
                                    :focused-index="countryDropdown.focusedIndex" @select="countryDropdown.selectOption"
                                    @navigate="countryDropdown.keyboardNav" />
                            </div>

                            <div class="mb-4">
                                <h4 class="font-medium mb-2">State <span class="text-xs text-gray-500">(optional)</span>
                                </h4>
                                <LocationDropdown id="state-dropdown" v-model="stateDropdown.selectedValue"
                                    v-model:show="stateDropdown.showDropdown.value"
                                    :options="stateDropdown.filteredOptions" :focused-index="stateDropdown.focusedIndex"
                                    @select="stateDropdown.selectOption" @navigate="stateDropdown.keyboardNav"
                                    :disabled="!countryDropdown.selectedValue" />
                            </div>

                            <div class="mb-4">
                                <h4 class="font-medium mb-2">City <span class="text-xs text-gray-500">(optional)</span>
                                </h4>
                                <LocationDropdown id="city-dropdown" v-model="cityDropdown.selectedValue"
                                    v-model:show="cityDropdown.showDropdown.value"
                                    :options="cityDropdown.filteredOptions" :focused-index="cityDropdown.focusedIndex"
                                    @select="cityDropdown.selectOption" @navigate="cityDropdown.keyboardNav"
                                    :disabled="!stateDropdown.selectedValue" />
                            </div>
                        </div>

                        <!-- AI Technology filters (for line chart) -->
                        <div v-else>
                            <h4 class="font-medium mb-2">AI Technology</h4>
                            <div class="space-y-2">
                                <div v-for="tech in aiTechnologies" :key="tech.id" class="flex items-center">
                                    <input type="checkbox" :id="`stat-tech-${tech.id}`" v-model="selectedTechnologies"
                                        :value="tech.id" class="mr-2">
                                    <label :for="`stat-tech-${tech.id}`">{{ tech.name }}</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCases } from '@/composables/useCases.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';
import { useLocationDropdown } from '@/composables/useLocationDropdown.js';
import { Country, State, City } from 'country-state-city';
import MapComponent from '@/components/Map.vue';
import ChartComponent from '@/components/Chart.vue';
import LocationDropdown from '@/components/LocationDropdown.vue';

// Tab state
const activeTab = ref('map');

// Chart type and navigation
const currentChartType = ref('pie');
const currentChartIndex = ref(0);
const availableCharts = computed(() => {
    if (currentChartType.value === 'pie') {
        return ['technology']; // Could add more pie chart types in the future
    } else {
        return ['yearly']; // Could add more line chart types in the future
    }
});

// Chart navigation functions
const nextChart = () => {
    // Check if we have more charts of the current type
    if (currentChartIndex.value < availableCharts.value.length - 1) {
        // Move to next chart of same type
        currentChartIndex.value++;
    } else {
        // Switch to next chart type and reset index
        currentChartType.value = currentChartType.value === 'pie' ? 'line' : 'pie';
        currentChartIndex.value = 0;
    }
};

const prevChart = () => {
    // Check if we have previous charts of the current type
    if (currentChartIndex.value > 0) {
        // Move to previous chart of same type
        currentChartIndex.value--;
    } else {
        // Switch to previous chart type and set index to last chart of that type
        currentChartType.value = currentChartType.value === 'pie' ? 'line' : 'pie';
        // Get the new available charts after changing the type
        const newCharts = currentChartType.value === 'pie'
            ? ['technology']
            : ['yearly'];
        currentChartIndex.value = newCharts.length - 1;
    }
};

// Data sources
const { cases, fetchAllUseCases } = useCases();
const { institutions, fetchAllInstitutions } = useInstitutions();
const { technologies: aiTechnologies, fetchAllTechnologies } = useAiTechnologies();

// Filter states for Map
const selectedInstitutions = ref([]);
const selectedTechnologies = ref([]);

// Location tracking variables
const currentCountrycode = ref('');
const currentStatecode = ref('');

// Keep the existing filter states for Stats but connect them to the dropdowns
const selectedCountry = ref('');
const selectedState = ref('');
const selectedCity = ref('');

// Country dropdown setup
const countryDropdown = useLocationDropdown({
    getOptions: () => Country.getAllCountries(),
    initialValue: ''
});

// State dropdown setup
const stateDropdown = useLocationDropdown({
    parentValue: countryDropdown.selectedValue,
    getOptions: (countryCode) => countryCode ? State.getStatesOfCountry(countryCode) : [],
    initialValue: ''
});

// City dropdown setup
const cityDropdown = useLocationDropdown({
    parentValue: stateDropdown.selectedValue,
    getOptions: (stateCode) => stateCode ? City.getCitiesOfState(currentCountrycode.value, stateCode) : [],
    initialValue: ''
});

// Watch for country changes
watch(countryDropdown.selectedValue, (newValue) => {
    const country = Country.getCountryByCode(newValue);
    selectedCountry.value = country?.name || '';
    currentCountrycode.value = newValue;
    stateDropdown.selectedValue = '';
    cityDropdown.selectedValue = '';
    selectedState.value = '';
    selectedCity.value = '';
});

// Watch for state changes
watch(stateDropdown.selectedValue, (newValue) => {
    const state = State.getStateByCodeAndCountry(newValue, currentCountrycode.value);
    selectedState.value = state?.name || '';
    currentStatecode.value = newValue;
    cityDropdown.selectedValue = '';
    selectedCity.value = '';
});

// Watch for city changes
watch(cityDropdown.selectedValue, (newValue) => {
    selectedCity.value = newValue;
});





// Computed properties for filtered data
const filteredCases = computed(() => {
    let result = cases.value || [];

    if (activeTab.value === 'map') {
        if (selectedInstitutions.value.length > 0) {
            result = result.filter(c => selectedInstitutions.value.includes(c.institution_id));
        }

        if (selectedTechnologies.value.length > 0) {
            result = result.filter(c => {
                return c.ai_technologies && c.ai_technologies.some(tech => selectedTechnologies.value.includes(tech));
            });
        }
    } else if (activeTab.value === 'stats') {
        // For stats tab, filter by location
        if (selectedCountry.value) {
            // Filter by country - need to match institution_id with institutions data
            result = result.filter(c => {
                // Find the institution for this case
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;

                // Match by country name
                return institution.country === selectedCountry.value;
            });
        }

        // Only apply state filter if state is selected
        if (selectedState.value) {
            result = result.filter(c => {
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;
                return institution.state === selectedState.value;
            });
        }

        // Only apply city filter if city is selected
        if (selectedCity.value) {
            result = result.filter(c => {
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;
                return institution.city === selectedCity.value;
            });
        }
        console.log("filtered cases", result);
    }

    console.log('Filtered cases:', result.length);
    return result;
});

// Extract unique location data for filters
const countries = computed(() => {
    const uniqueCountries = new Set();
    cases.value.forEach(c => {
        if (c.institution?.country) uniqueCountries.add(c.institution.country);
    });
    return [...uniqueCountries].sort();
});

const filteredStates = computed(() => {
    const uniqueStates = new Set();
    cases.value
        .filter(c => !selectedCountry.value || c.institution?.country === selectedCountry.value)
        .forEach(c => {
            if (c.institution?.state) uniqueStates.add(c.institution.state);
        });
    return [...uniqueStates].sort();
});

const filteredCities = computed(() => {
    const uniqueCities = new Set();
    cases.value
        .filter(c => {
            return (!selectedCountry.value || c.institution?.country === selectedCountry.value) &&
                (!selectedState.value || c.institution?.state === selectedState.value);
        })
        .forEach(c => {
            if (c.institution?.city) uniqueCities.add(c.institution.city);
        });
    return [...uniqueCities].sort();
});

// Prepare yearly trend data based on project_initiation_date
const yearlyTrendData = computed(() => {
    // Get base cases
    let filteredResult = cases.value || [];
    
    // Create a map to store data by year and technology
    const techsByYear = {};
    const techsToInclude = selectedTechnologies.value.length > 0 
        ? selectedTechnologies.value 
        : aiTechnologies.value.map(tech => tech.id);
    
    // Initialize the years set to track all years
    const yearsSet = new Set();
    
    // Process each case
    filteredResult.forEach(c => {
        if (c.project_initiation_date) {
            try {
                // Extract year from the date string (assuming format like "dd-mm-yyyy")
                const dateParts = c.project_initiation_date.split('-');
                const year = parseInt(dateParts[2], 10);
                
                if (!isNaN(year)) {
                    yearsSet.add(year);
                    
                    // For each technology in this case
                    if (c.ai_technologies && c.ai_technologies.length > 0) {
                        c.ai_technologies.forEach(techId => {
                            // Only include technologies that are in our filter (or all if no filter)
                            if (techsToInclude.includes(techId)) {
                                if (!techsByYear[techId]) {
                                    techsByYear[techId] = {};
                                }
                                techsByYear[techId][year] = (techsByYear[techId][year] || 0) + 1;
                            }
                        });
                    }
                }
            } catch (e) {
                console.error("Error parsing date:", c.project_initiation_date, e);
            }
        }
    });
    
    // Sort years for consistent x-axis
    const years = Array.from(yearsSet).sort();
    
    // Prepare series data for each technology
    const series = [];
    
    Object.entries(techsByYear).forEach(([techId, yearData]) => {
        const tech = aiTechnologies.value.find(t => t.id === parseInt(techId));
        if (tech) {
            // Create a data point for each year (0 if no data)
            const data = years.map(year => yearData[year] || 0);
            
            series.push({
                name: tech.name,
                data: data
            });
        }
    });
    
    return {
        categories: years,
        series: series
    };
});

// Prepare chart data based on filtered cases
const chartData = computed(() => {
    // Group cases by AI technology
    const techCounts = {};

    // Use the filtered cases which already have location filters applied
    filteredCases.value.forEach(c => {
        if (c.ai_technologies && c.ai_technologies.length > 0) {
            c.ai_technologies.forEach(techId => {
                techCounts[techId] = (techCounts[techId] || 0) + 1;
            });
        }
    });

    console.log('Tech counts after filtering:', techCounts);
    console.log('Current filters - Country:', selectedCountry.value, 'State:', selectedState.value, 'City:', selectedCity.value);

    // Format data for chart component
    return Object.entries(techCounts).map(([techId, count]) => {
        const tech = aiTechnologies.value.find(t => t.id === parseInt(techId));
        return {
            name: tech ? tech.name : `Tech ${techId}`,
            value: count
        };
    });
});

// Load data on component mount
onMounted(async () => {
    await fetchAllUseCases();
    await fetchAllInstitutions();
    await fetchAllTechnologies();
});
</script>