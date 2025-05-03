<template>
    <div class="relative" ref="dropdownContainer">
        <button type="button" aria-haspopup="listbox" :aria-expanded="show" @click="toggleDropdown" @keydown="handleButtonKeydown"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 bg-white text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all flex justify-between items-center"
            >
            {{ modelValue }}
            <svg class="w-4 h-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                    d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                    clip-rule="evenodd" />
            </svg>
        </button>
        <transition name="fade">
            <div v-if="show"
                class="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto"                
            >                
                <div v-for="(option, index) in options.value"
                    :key="option.isoCode"
                    :class="['p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0',
                    { 'bg-gray-100': props.focusedIndex.value === index }]"
                    @click="handleSelect(option, index)"
                    @keydown="handleOptionKeydown($event, option, index)"
                    :tabindex="props.focusedIndex.value === index ? 0 : -1"
                    role="option"
                    :aria-selected="props.focusedIndex.value === index"
                    :ref="el => { if (props.focusedIndex.value === index) focusedOption = el }"
                >
                    {{ option.name }}
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';


const props = defineProps({
    modelValue: String,
    show: Boolean,
    options: Array,
    disabled: Boolean,
    focusedIndex: {
        type: Number,
        default: -1
    }
});

const dropdownContainer = ref(null);
const focusedOption = ref(null);

const emit = defineEmits(['update:modelValue', 'select', 'update:show', 'navigate']);


// Log selected option
const handleSelect = (option, index) => {
    // Check if isoCode exists
    if (!option.isoCode) {
        console.warn('Selected option is missing isoCode:', option);
    }
    emit('update:modelValue', option.name);
    emit('select', option);
    emit('update:show', false);
};


const toggleDropdown = () => {
    if (!props.disabled) {
        emit('update:show', !props.show);
    }
};

// When press enter, toggle dropdown and focus on the first option
const handleButtonKeydown = (event) => {
  if (['Enter'].includes(event.key)) {
    event.preventDefault();
    toggleDropdown();
    if (props.show) {
      nextTick(() => {
        const firstOption = dropdownContainer.value.querySelector('[role="option"]');
        if (firstOption) firstOption.focus();
      });
    }
  }
};



const handleOptionKeydown = (event, option, index) => {
  // handle key down, up, enter, escape
  if (event.key === 'ArrowDown') {
    event.preventDefault();
    emit('navigate', 'down');
  } else if (event.key === 'ArrowUp') {
    event.preventDefault();
    emit('navigate', 'up');
  } else if (event.key === 'Enter') {
    event.preventDefault();
    handleSelect(option);
  } else if (event.key === 'Escape') {
    emit('update:show', false);
  }
};



// Auto-scroll to focused option
watch(() => props.focusedIndex.value, async (newIndex) => {
    await nextTick();
    if (focusedOption.value) {
        focusedOption.value.scrollIntoView({
            block: 'nearest',
            behavior: 'smooth'
        });
        focusedOption.value.focus();
         
    }
});

watch(() => props.show, (newVal) => {
  if (newVal) {
    nextTick(() => {
      const firstOption = dropdownContainer.value?.querySelector('[role="option"]');
      if (firstOption) {
        firstOption.focus();
        props.focusedIndex.value = 0; // Sync with composable's state
      }
    });
  }
});

// Close dropdown when clicking outside
watch(() => props.show, (newVal) => {
    if (newVal) {
        // handler for click outside
        const handleClickOutside = (event) => {
            // Check if the click is outside the dropdown container
            if (dropdownContainer.value && !dropdownContainer.value.contains(event.target)) {
                emit('update:show', false);
            }
        };
        
        // handler for keyboard navigation
        const handleFocusOut = (event) => {
            const dropdown = dropdownContainer.value;
            if (!dropdown) return;
            
            // Check if focus moved outside the dropdown
            if (!dropdown.contains(event.relatedTarget)) {
                emit('update:show', false);
            }
        };
        // when click outside the dropdown, close it
        document.addEventListener('click', handleClickOutside);
        dropdownContainer.value.addEventListener('focusout', handleFocusOut);
        return () => {
            document.removeEventListener('click', handleClickOutside);
            dropdownContainer.value?.removeEventListener('focusout', handleFocusOut);
        };
    }
});

</script>