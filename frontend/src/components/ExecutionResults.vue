<script setup lang="ts">
import type { ExecutionResult } from "@/types/ssh.types";

defineProps<{
  results: ExecutionResult[];
}>();
</script>

<template>
  <div v-if="results.length > 0" class="space-y-4">
    <div
      v-for="(result, index) in results"
      :key="index"
      class="bg-slate-800 rounded-lg shadow-xl p-6"
    >
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white flex items-center">
          <span v-if="result.success" class="text-green-400 mr-2">✅</span>
          <span v-else class="text-red-400 mr-2">❌</span>
          {{ result.hostname }}
        </h3>
        <span class="text-sm text-slate-400">
          {{ result.duration_seconds.toFixed(2) }}s
        </span>
      </div>

      <div v-if="result.output" class="mb-4">
        <div class="text-sm font-medium text-slate-300 mb-2">Output:</div>
        <pre
          class="bg-slate-900 text-green-400 p-4 rounded text-sm overflow-x-auto"
          >{{ result.output }}</pre
        >
      </div>

      <div v-if="result.error" class="mb-4">
        <div class="text-sm font-medium text-slate-300 mb-2">Error:</div>
        <pre
          class="bg-slate-900 text-red-400 p-4 rounded text-sm overflow-x-auto"
          >{{ result.error }}</pre
        >
      </div>
    </div>
  </div>
  <div
    v-else
    class="bg-slate-800 rounded-lg shadow-xl p-12 text-center text-slate-400"
  >
    No results available yet
  </div>
</template>
