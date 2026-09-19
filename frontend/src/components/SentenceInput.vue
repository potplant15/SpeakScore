<script setup lang="ts">
defineProps<{ modelValue: string; disabled?: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <label class="sentence-field">
    <span class="eyebrow">Your sentence</span>
    <textarea
      :value="modelValue"
      :disabled="disabled"
      maxlength="1000"
      placeholder="Write something you want to say..."
      rows="3"
      @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />
    <span class="character-count">{{ modelValue.length }} / 1000</span>
  </label>
</template>
