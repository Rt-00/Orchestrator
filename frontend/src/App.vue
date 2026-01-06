<script setup lang="ts">
import { ref, computed } from "vue";
import type { Host, TabType } from "@/types/ssh.types";
import { useScriptExecution } from "@/composables/useScriptExecution";
import HostsConfiguration from "@/components/HostConfiguration.vue";
import ScriptConfiguration from "@/components/ScriptConfiguration.vue";
import ExecutionStatus from "@/components/ExecutionStatus.vue";
import ExecutionResults from "@/components/ExecutionResults.vue";

const hosts = ref<Host[]>([
  { hostname: "", port: 22, username: "", password: "" },
]);

const script = ref(`#!/bin/bash
# Example script
uname -a
df -h
free -m
uptime`);

const timeoutSeconds = ref(300);
const maxConcurrent = ref(5);
const activeTab = ref<TabType>("setup");

const {
  executionStatus,
  executionResults,
  isExecuting,
  progressPercentage,
  executeScript,
} = useScriptExecution();

const isFormValid = computed(() => {
  return (
    hosts.value.every(
      (h) => h.hostname && h.username && (h.password || h.private_key_path)
    ) && script.value.trim().length > 0
  );
});

const handleExecute = async () => {
  await executeScript(
    hosts.value,
    script.value,
    timeoutSeconds.value,
    maxConcurrent.value
  );
  activeTab.value = "status";
};
</script>

<template>
  <div
    class="min-h-screen bg-linear-to-br from-slate-900 via-slate-800 to-slate-900"
  >
    <div class="container mx-auto px-4 py-8 max-w-7xl">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-white mb-2">
          🚀 SSH Remote Execution
        </h1>
        <p class="text-slate-400">
          Execute scripts on multiple servers simultaneously
        </p>
      </div>

      <!-- Tabs -->
      <div class="mb-6 flex space-x-2 border-b border-slate-700">
        <button
          v-for="tab in ['setup', 'status', 'results'] as TabType[]"
          :key="tab"
          @click="activeTab = tab"
          :class="[
            'px-6 py-3 font-medium capitalize transition-colors',
            activeTab === tab
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-slate-200',
          ]"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Setup Tab -->
      <div v-show="activeTab === 'setup'" class="space-y-6">
        <HostsConfiguration v-model="hosts" />

        <ScriptConfiguration
          :script="script"
          :timeout-seconds="timeoutSeconds"
          :max-concurrent="maxConcurrent"
          @update:script="script = $event"
          @update:timeout-seconds="timeoutSeconds = $event"
          @update:max-concurrent="maxConcurrent = $event"
        />

        <button
          @click="handleExecute"
          :disabled="!isFormValid || isExecuting"
          class="w-full py-4 bg-linear-to-r from-blue-600 to-blue-700 text-white text-lg font-semibold rounded-lg hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
        >
          {{ isExecuting ? "⏳ Executing..." : "🚀 Execute Script" }}
        </button>
      </div>

      <!-- Status Tab -->
      <div v-show="activeTab === 'status'">
        <ExecutionStatus
          :status="executionStatus"
          :progress-percentage="progressPercentage"
        />
      </div>

      <!-- Results Tab -->
      <div v-show="activeTab === 'results'">
        <ExecutionResults :results="executionResults" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1e293b;
}

::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}
</style>
