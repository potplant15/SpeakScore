<script setup lang="ts">
import type { Accent, Gender } from '@/types/practice'

defineProps<{ accent: Accent; gender: Gender; disabled?: boolean }>()
const emit = defineEmits<{ 'update:accent': [value: Accent]; 'update:gender': [value: Gender] }>()
</script>

<template>
  <div class="selector-grid">
    <fieldset>
      <legend class="eyebrow">Voice</legend>
      <div class="segmented">
        <button :class="{ selected: accent === 'en-US' }" :disabled="disabled" @click="emit('update:accent', 'en-US')">
          <span class="flag">US</span> American
        </button>
        <button :class="{ selected: accent === 'en-GB' }" :disabled="disabled" @click="emit('update:accent', 'en-GB')">
          <span class="flag">GB</span> British
        </button>
      </div>
    </fieldset>
    <fieldset>
      <legend class="eyebrow">Speaker</legend>
      <div class="segmented compact">
        <button :class="{ selected: gender === 'female' }" :disabled="disabled" @click="emit('update:gender', 'female')">Female</button>
        <button :class="{ selected: gender === 'male' }" :disabled="disabled" @click="emit('update:gender', 'male')">Male</button>
      </div>
    </fieldset>
  </div>
</template>
