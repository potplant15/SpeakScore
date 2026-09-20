<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import { getSuggestions } from '@/services/practice'
import type { Suggestion } from '@/types/practice'

const props = defineProps<{ modelValue: string; disabled?: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const input = ref<HTMLInputElement | null>(null)
const suggestions = ref<Suggestion[]>([])
const activeIndex = ref(0)
const loading = ref(false)
let requestId = 0
let debounceTimer: number | undefined
const activeSuggestion = computed(() => suggestions.value[activeIndex.value])

function currentWord(value: string) {
  return value.match(/[A-Za-z'-]+$/)?.[0] ?? ''
}

async function loadSuggestions(value: string) {
  const prefix = currentWord(value)
  const currentRequest = ++requestId
  if (!prefix) {
    suggestions.value = []
    return
  }

  loading.value = true
  try {
    const matches = await getSuggestions(prefix)
    if (currentRequest === requestId) {
      suggestions.value = matches
      activeIndex.value = 0
    }
  } catch {
    if (currentRequest === requestId) suggestions.value = []
  } finally {
    if (currentRequest === requestId) loading.value = false
  }
}

function updateValue(event: Event) {
  const value = (event.target as HTMLInputElement).value
  emit('update:modelValue', value)
  if (debounceTimer !== undefined) window.clearTimeout(debounceTimer)
  debounceTimer = window.setTimeout(() => {
    void loadSuggestions(value)
  }, 160)
}

function applySuggestion(suggestion: Suggestion) {
  const nextValue = props.modelValue.replace(/[A-Za-z'-]+$/, suggestion.word)
  emit('update:modelValue', nextValue)
  suggestions.value = []
  void nextTick(() => input.value?.focus())
}

function handleKeydown(event: KeyboardEvent) {
  if (!suggestions.value.length) return
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value + 1) % suggestions.value.length
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value - 1 + suggestions.value.length) % suggestions.value.length
  } else if (event.key === 'Tab' || event.key === 'Enter') {
    event.preventDefault()
    applySuggestion(suggestions.value[activeIndex.value])
  } else if (event.key === 'Escape') {
    suggestions.value = []
  }
}

function clearSuggestions() {
  window.setTimeout(() => { suggestions.value = [] }, 120)
}

onBeforeUnmount(() => {
  if (debounceTimer !== undefined) window.clearTimeout(debounceTimer)
})
</script>

<template>
  <section class="sentence-field">
    <span class="eyebrow">Your sentence</span>
    <div class="sentence-editor">
      <input
        ref="input"
        :value="modelValue"
        :disabled="disabled"
        class="sentence-input"
        aria-label="Your practice sentence"
        autocomplete="off"
        spellcheck="false"
        placeholder="Write something you want to say..."
        @input="updateValue"
        @keydown="handleKeydown"
        @blur="clearSuggestions"
      />
      <span class="completion-hint"><kbd>Tab</kbd> accept · <kbd>↑ ↓</kbd> browse · <kbd>Esc</kbd> close</span>
    </div>

    <section v-if="suggestions.length" class="suggestion-tray" aria-label="Word suggestions">
      <div class="tray-heading">
        <span><i /> Word notes</span>
        <small>{{ loading ? 'finding words…' : `${suggestions.length} matches` }}</small>
      </div>
      <div class="suggestion-list" role="listbox">
        <button
          v-for="(suggestion, index) in suggestions"
          :key="suggestion.word"
          type="button"
          class="suggestion-item"
          :class="{ active: index === activeIndex }"
          role="option"
          :aria-selected="index === activeIndex"
          @mousedown.prevent="applySuggestion(suggestion)"
          @mouseenter="activeIndex = index"
        >
          <span class="suggestion-word">{{ suggestion.word }}</span>
          <span class="suggestion-phonetic">{{ suggestion.phonetic ? `/${suggestion.phonetic}/` : '—' }}</span>
          <span class="suggestion-translation" :title="suggestion.translation">{{ suggestion.translation || 'No translation available' }}</span>
        </button>
      </div>
      <div v-if="activeSuggestion?.translation" class="active-definition">
        <span>Selected · {{ activeSuggestion.word }}</span>
        <p>{{ activeSuggestion.translation }}</p>
      </div>
      <p class="tray-footnote">Press Tab to place the highlighted word into your sentence.</p>
    </section>
  </section>
</template>
