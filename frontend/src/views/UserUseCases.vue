<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <div class="container mx-auto px-6 py-4 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900">My Submitted Cases</h1>
        <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
          ← Back to Overview
        </button>
      </div>
    </header>

    <main class="container mx-auto px-6 py-8">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-6">Your Submitted Use Cases</h2>

        <!-- Loading state -->
        <div v-if="loading" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-2 text-gray-600">Loading your cases...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-md mb-4">
          {{ error }}
        </div>

        <!-- Success message -->
        <div v-if="successMessage" class="bg-green-50 text-green-700 p-4 rounded-md mb-4">
          {{ successMessage }}
        </div>

        <!-- Cases list -->
        <div v-if="userCases.length && !loading" class="space-y-6">
          <div v-for="caseItem in userCases" :key="caseItem.id"
            class="border rounded-lg p-6 hover:shadow-sm transition-all">
            <!-- Header Section -->
            <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
              <div class="space-y-2 flex-1 min-w-[300px]">
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold text-gray-900">
                    {{ caseItem.title }}
                  </h3>
                  <span :class="statusBadge(caseItem.status)" class="text-sm">
                    {{ caseItem.status }}
                  </span>
                </div>
                <div>
                  <label class="text-gray-500 font-medium block mb-1">Institution</label>
                  <div v-if="caseItem.institution">
                    <p class="font-medium text-gray-800">{{ caseItem.institution.name }}</p>
                    <p class="text-gray-600">
                      {{ [caseItem.institution.city, caseItem.institution.state,
                      caseItem.institution.country].filter(Boolean).join(', ') }}
                    </p>
                  </div>
                  <span v-else class="text-gray-400">No institution associated</span>
                </div>
              </div>
            </div>

            <!-- Main Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 text-sm">
              <!-- Left Column: contact, url, project initiation date and AI Technologies-->
              <div class="space-y-4">
                <div>
                  <label class="text-gray-500 font-medium block mb-1">Contact</label>
                  <a :href="`mailto:${caseItem.contact}`" class="text-blue-600 hover:underline break-all">
                    {{ caseItem.contact || 'Not provided' }}
                  </a>
                </div>

                <div>
                  <label class="text-gray-500 font-medium block mb-1">Project URL</label>
                  <a :href="caseItem.url" target="_blank" class="text-blue-600 hover:underline break-all">
                    {{ caseItem.url || 'Not provided' }}
                  </a>
                </div>
                <div>
                  <label class="text-gray-500 font-medium block mb-1">Project Initiation Date</label>
                  <p class="text-gray-800">
                    {{ caseItem.project_initiation_date || 'Not provided' }}
                  </p>
                </div>
                <div>
                  <label class="text-gray-500 font-medium block mb-1">AI Technologies</label>
                  <div v-if="caseItem.aiTechDetails && caseItem.aiTechDetails.length" class="flex flex-wrap gap-2">
                    <span v-for="(tech, index) in caseItem.aiTechDetails" :key="index"
                      class="px-2.5 py-1 bg-blue-50 text-blue-800 rounded-full text-xs">
                      {{ tech.name }}
                    </span>
                  </div>
                  <div v-else-if="caseItem.ai_technologies && caseItem.ai_technologies.length"
                    class="flex flex-wrap gap-2">
                    <span v-for="(techId, index) in caseItem.ai_technologies" :key="index"
                      class="px-2.5 py-1 bg-gray-50 text-gray-600 rounded-full text-xs flex items-center">
                      <span class="animate-pulse mr-1">⟳</span> Loading...
                    </span>
                  </div>
                  <span v-else class="text-gray-400">None specified</span>
                </div>
              </div>

              <!-- Right Column: short description + full description -->
              <div class="space-y-4">
                <div>
                  <label class="text-gray-500 font-medium block mb-1">Short Description</label>
                  <p class="text-gray-800 whitespace-pre-wrap leading-relaxed">
                    {{ caseItem.short_description }}
                  </p>
                </div>

                <div>
                  <label class="text-gray-500 font-medium block mb-1">Full Description</label>
                  <p class="text-gray-800 whitespace-pre-wrap leading-relaxed max-h-[200px] overflow-y-auto">
                    {{ caseItem.full_description?.value || 'No description provided' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Status information -->
            <div v-if="caseItem.status === 'rejected'" class="mt-6 pt-4 border-t">
              <div class="bg-red-50 p-4 rounded-md">
                <h4 class="text-red-700 font-medium mb-2">Case Rejected</h4>
                <p class="text-red-600">
                  Your case has been reviewed and was not approved. You may submit a new case with updated information.
                </p>
              </div>
            </div>
            <div v-else-if="caseItem.status === 'pending'" class="mt-6 pt-4 border-t">
              <div class="bg-amber-50 p-4 rounded-md">
                <h4 class="text-amber-700 font-medium mb-2">Case Under Review</h4>
                <p class="text-amber-600">
                  Your case is currently being reviewed by our administrators. You'll be notified when a decision is made.
                </p>
              </div>
            </div>
            <div v-else-if="caseItem.status === 'approved'" class="mt-6 pt-4 border-t">
              <div class="bg-green-50 p-4 rounded-md">
                <h4 class="text-green-700 font-medium mb-2">Case Approved</h4>
                <p class="text-green-600">
                  Your case has been approved and is now visible on the public map.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!userCases.length && !loading" class="text-center py-8">
          <div class="text-gray-500 mb-4">You haven't submitted any use cases yet</div>
          <button @click="$router.push('/submit')" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Submit a New Case
          </button>
        </div>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUserId } from '@/utils/auth.js';
import { useCases } from '@/composables/useCases.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';
import AppFooter from '@/components/AppFooter.vue';

const router = useRouter();
const userId = getUserId();
const userCases = ref([]);
const loading = ref(true);
const error = ref('');
const successMessage = ref('');

const { fetchCasesByUserId } = useCases();
const { fetchInstitutionDetailsById } = useInstitutions();
const { fetchTechnologyDetails } = useAiTechnologies();

// Local state
const aiTechnologies = ref({});

// Status badge styling
const statusBadge = (status) => ({
  'px-3 py-1 rounded-full text-sm font-medium': true,
  'bg-amber-100 text-amber-800': status === 'pending',
  'bg-emerald-100 text-emerald-800': status === 'approved',
  'bg-rose-100 text-rose-800': status === 'rejected'
});

// Load institution details for each case
const loadInstitutionDetails = async (caseItem) => {
  if (!caseItem.institution_id) return;

  try {
    const institutionData = await fetchInstitutionDetailsById(caseItem.institution_id);
    if (institutionData) {
      // Update the case item with institution details
      caseItem.institution = institutionData;
    }
  } catch (err) {
    console.error('Error loading institution details:', err);
  }
};

// Load AI technology details
const loadAiTechnologyDetails = async (caseItem) => {
  if (!caseItem.ai_technologies || !caseItem.ai_technologies.length) return;

  try {
    caseItem.aiTechDetails = [];
    for (const techId of caseItem.ai_technologies) {
      // Check if we already have this tech in our cache
      if (!aiTechnologies.value[techId]) {
        const techDetails = await fetchTechnologyDetails(techId);
        if (techDetails) {
          aiTechnologies.value[techId] = techDetails;
        }
      }

      if (aiTechnologies.value[techId]) {
        caseItem.aiTechDetails.push(aiTechnologies.value[techId]);
      }
    }
  } catch (err) {
    console.error('Error loading AI technology details:', err);
  }
};

// Fetch user's cases
const fetchUserCases = async () => {
  if (!userId) {
    router.push('/login');
    return;
  }

  try {
    loading.value = true;
    error.value = '';
    
    const cases = await fetchCasesByUserId(userId);
    userCases.value = cases;

    // Load additional details for each case
    for (const caseItem of userCases.value) {
      await loadInstitutionDetails(caseItem);
      await loadAiTechnologyDetails(caseItem);
    }
  } catch (err) {
    console.error('Error fetching user cases:', err);
    error.value = 'Failed to load your cases. Please try again later.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUserCases();
});
</script>