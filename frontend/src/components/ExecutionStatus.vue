<script setup lang="ts">
import type { ExecutionStatus } from "@/types/ssh.types";

defineProps<{
  status: ExecutionStatus | null;
  progressPercentage: number;
}>();
</script>

<template>
  <div v-if="status" class="bg-slate-800 rounded-lg shadow-xl p-6">
    <h2 class="text-xl font-semibold text-white mb-6">📊 Execution Status</h2>

    <div class="mb-6">
      <div class="flex justify-between text-sm text-slate-300 mb-2">
        <span>Progress</span>
        <span
          >{{ status.completed_hosts }} / {{ status.total_hosts }} hosts</span
        >
      </div>
      <div class="w-full bg-slate-700 rounded-full h-4 overflow-hidden">
        <div
          class="bg-linear-to-r from-blue-500 to-blue-600 h-full transition-all duration-500"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
      <div class="text-right text-2xl font-bold text-blue-400 mt-2">
        {{ progressPercentage }}%
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-slate-700 rounded-lg p-4">
        <div class="text-slate-400 text-sm mb-1">✅ Successful</div>
        <div class="text-3xl font-bold text-green-400">
          {{ status.successful_hosts }}
        </div>
      </div>

      <div class="bg-slate-700 rounded-lg p-4">
        <div class="text-slate-400 text-sm mb-1">❌ Failed</div>
        <div class="text-3xl font-bold text-red-400">
          {{ status.failed_hosts }}
        </div>
      </div>

      <div class="bg-slate-700 rounded-lg p-4">
        <div class="text-slate-400 text-sm mb-1">⏱️ Status</div>
        <div class="text-2xl font-bold text-blue-400">
          {{ status.status }}
        </div>
      </div>
    </div>
  </div>
  <div
    v-else
    class="bg-slate-800 rounded-lg shadow-xl p-12 text-center text-slate-400"
  >
    No execution in progress
  </div>
</template>
