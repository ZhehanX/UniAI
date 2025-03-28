<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <!-- Toggle Buttons -->
    <div class="flex justify-center mb-6">
      <div class="inline-flex rounded-md shadow-sm" role="group">
        <button 
          @click="activeTab = 'map'" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-l-lg border',
            activeTab === 'map' 
              ? 'bg-blue-200 text-blue-800 border-blue-300' 
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
          ]"
        >
          Map
        </button>
        <button 
          @click="activeTab = 'stats'" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-r-lg border',
            activeTab === 'stats' 
              ? 'bg-blue-200 text-blue-800 border-blue-300' 
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
          ]"
        >
          Stats
        </button>
      </div>
    </div>

    <!-- Content Area -->
    <div class="bg-white rounded-lg shadow p-6">
      <!-- Map Section -->
      <div v-if="activeTab === 'map'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="h-64 bg-gray-100 rounded-lg">
          <!-- Map Component will go here -->
          <MapComponent :cases="cases" />
        </div>
        <div class="bg-white border border-gray-200 rounded-lg p-4">
          <!-- Filters for Map -->
          <h3 class="text-lg font-medium mb-4">Filters</h3>
          
          <div class="mb-4">
            <h4 class="font-medium mb-2">Institution</h4>
            <div class="space-y-2">
              <div v-for="institution in institutions" :key="institution.id" class="flex items-center">
                <input 
                  type="checkbox" 
                  :id="`inst-${institution.id}`" 
                  v-model="selectedInstitutions"
                  :value="institution.id"
                  class="mr-2"
                >
                <label :for="`inst-${institution.id}`">{{ institution.name }}</label>
              </div>
            </div>
          </div>
          
          <div>
            <h4 class="font-medium mb-2">AI Tech</h4>
            <div class="space-y-2">
              <div v-for="tech in aiTechnologies" :key="tech.id" class="flex items-center">
                <input 
                  type="checkbox" 
                  :id="`tech-${tech.id}`" 
                  v-model="selectedTechnologies"
                  :value="tech.id"
                  class="mr-2"
                >
                <label :for="`tech-${tech.id}`">{{ tech.name }}</label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Section -->
      <div v-else-if="activeTab === 'stats'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="h-64 bg-gray-100 rounded-lg">
          <!-- Chart Component will go here -->
          <ChartComponent :data="chartData" />
        </div>
        <div class="bg-white border border-gray-200 rounded-lg p-4">
          <!-- Filters for Stats -->
          <h3 class="text-lg font-medium mb-4">Filters</h3>
          
          <div class="mb-4">
            <h4 class="font-medium mb-2">Country</h4>
            <select v-model="selectedCountry" class="w-full p-2 border rounded">
              <option value="">All Countries</option>
              <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
            </select>
          </div>
          
          <div class="mb-4">
            <h4 class="font-medium mb-2">State</h4>
            <select v-model="selectedState" class="w-full p-2 border rounded">
              <option value="">All States</option>
              <option v-for="state in filteredStates" :key="state" :value="state">{{ state }}</option>
            </select>
          </div>
          
          <div>
            <h4 class="font-medium mb-2">City</h4>
            <select v-model="selectedCity" class="w-full p-2 border rounded">
              <option value="">All Cities</option>
              <option v-for="city in filteredCities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCases } from '@/composables/useCases.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';
import MapComponent from '@/components/MapComponent.vue';
import ChartComponent from '@/components/ChartComponent.vue';

// Tab state
const activeTab = ref('map');

// Data sources
const { cases, fetchAllUseCases } = useCases();
const { institutions, fetchAllInstitutions } = useInstitutions();
const { technologies: aiTechnologies, fetchAllTechnologies } = useAiTechnologies();

// Filter states for Map
const selectedInstitutions = ref([]);
const selectedTechnologies = ref([]);

// Filter states for Stats
const selectedCountry = ref('');
const selectedState = ref('');
const selectedCity = ref('');

// Computed properties for filtered data
const filteredCases = computed(() => {
  let result = cases.value;
  
  if (activeTab.value === 'map') {
    if (selectedInstitutions.value.length > 0) {
      result = result.filter(c => selectedInstitutions.value.includes(c.institution_id));
    }
    
    if (selectedTechnologies.value.length > 0) {
      result = result.filter(c => {
        return c.ai_technologies.some(tech => selectedTechnologies.value.includes(tech));
      });
    }
  } else if (activeTab.value === 'stats') {
    if (selectedCountry.value) {
      result = result.filter(c => c.institution?.country === selectedCountry.value);
    }
    
    if (selectedState.value) {
      result = result.filter(c => c.institution?.state === selectedState.value);
    }
    
    if (selectedCity.value) {
      result = result.filter(c => c.institution?.city === selectedCity.value);
    }
  }
  
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

// Prepare chart data based on filtered cases
const chartData = computed(() => {
  // Group cases by AI technology
  const techCounts = {};
  
  filteredCases.value.forEach(c => {
    if (c.ai_technologies) {
      c.ai_technologies.forEach(techId => {
        techCounts[techId] = (techCounts[techId] || 0) + 1;
      });
    }
  });
  
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