<script setup lang="ts">
const props = defineProps<{
  script: string;
  timeoutSeconds: number;
  maxConcurrent: number;
}>();

const emit = defineEmits<{
  "update:script": [value: string];
  "update:timeoutSeconds": [value: number];
  "update:maxConcurrent": [value: number];
}>();
</script>

<template>
  <div class="bg-slate-800 rounded-lg shadow-xl p-6">
    <h2 class="text-xl font-semibold text-white mb-4">📝 Script to Execute</h2>

    <div class="mb-4">
      <label class="block text-sm font-medium text-slate-300 mb-2">
        Bash Script
      </label>
      <textarea
        :value="script"
        @input="
          emit('update:script', ($event.target as HTMLTextAreaElement).value)
        "
        rows="10"
        class="w-full px-3 py-2 bg-slate-700 text-white font-mono text-sm rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
        placeholder="#!/bin/bash&#10;echo 'Hello World'"
      ></textarea>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-2">
          Timeout (seconds)
        </label>
        <input
          :value="timeoutSeconds"
          @input="
            emit(
              'update:timeoutSeconds',
              parseInt(($event.target as HTMLInputElement).value)
            )
          "
          type="number"
          min="1"
          max="3600"
          class="w-full px-3 py-2 bg-slate-700 text-white rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
        />
        <p class="text-xs text-slate-500 mt-1">Máximo: 3600s (1 hora)</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-300 mb-2">
          Max Concurrent Connections
        </label>
        <input
          :value="maxConcurrent"
          @input="
            emit(
              'update:maxConcurrent',
              parseInt(($event.target as HTMLInputElement).value)
            )
          "
          type="number"
          min="1"
          max="50"
          class="w-full px-3 py-2 bg-slate-700 text-white rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
        />
        <p class="text-xs text-slate-500 mt-1">
          Recomendado: 5-10 para evitar sobrecarga
        </p>
      </div>
    </div>
  </div>
</template>
