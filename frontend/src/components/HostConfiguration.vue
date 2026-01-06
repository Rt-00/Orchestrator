<script setup lang="ts">
import { ref } from "vue";
import type { Host, UploadMessage } from "../types/ssh.types";
import { parseCSV, csvToHosts, downloadCSVTemplate } from "../utils/csvUtils";

const props = defineProps<{
  modelValue: Host[];
}>();

const emit = defineEmits<{
  "update:modelValue": [value: Host[]];
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const uploadMessage = ref<UploadMessage | null>(null);

const hosts = ref<Host[]>(props.modelValue);

const addHost = () => {
  const updated = [
    ...hosts.value,
    { hostname: "", port: 22, username: "", password: "" },
  ];
  hosts.value = updated;
  emit("update:modelValue", updated);
};

const removeHost = (index: number) => {
  const updated = hosts.value.filter((_, i) => i !== index);
  hosts.value = updated;
  emit("update:modelValue", updated);
};

const clearAllHosts = () => {
  if (confirm("Tem certeza que deseja limpar todos os hosts?")) {
    const updated = [{ hostname: "", port: 22, username: "", password: "" }];
    hosts.value = updated;
    emit("update:modelValue", updated);
    uploadMessage.value = null;
  }
};

const triggerFileUpload = () => {
  fileInput.value?.click();
};

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];

  if (!file) return;

  uploadMessage.value = null;

  if (!file.name.endsWith(".csv")) {
    uploadMessage.value = {
      type: "error",
      text: "❌ Por favor, selecione um arquivo CSV",
    };
    return;
  }

  try {
    const text = await file.text();
    const csvHosts = parseCSV(text);

    if (csvHosts.length === 0) {
      uploadMessage.value = {
        type: "error",
        text: "❌ Nenhum host válido encontrado no CSV",
      };
      return;
    }

    const newHosts = csvToHosts(csvHosts);
    hosts.value = newHosts;
    emit("update:modelValue", newHosts);

    uploadMessage.value = {
      type: "success",
      text: `✅ ${newHosts.length} host(s) carregado(s) com sucesso!`,
    };

    target.value = "";
  } catch (error) {
    console.error("Error parsing CSV:", error);
    uploadMessage.value = {
      type: "error",
      text: "❌ Erro ao processar arquivo CSV",
    };
  }
};

const updateHost = (index: number, field: keyof Host, value: any) => {
  const updated = [...hosts.value];
  updated[index] = { ...updated[index], [field]: value } as Host;
  hosts.value = updated;
  emit("update:modelValue", updated);
};
</script>

<template>
  <div class="bg-slate-800 rounded-lg shadow-xl p-6">
    <div
      class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-3"
    >
      <h2 class="text-xl font-semibold text-white">🖥️ Target Hosts</h2>
      <div class="flex flex-wrap gap-2">
        <input
          ref="fileInput"
          type="file"
          accept=".csv"
          @change="handleFileUpload"
          class="hidden"
        />
        <button
          @click="downloadCSVTemplate"
          class="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition-colors text-sm"
          title="Download CSV template"
        >
          📥 Template CSV
        </button>
        <button
          @click="triggerFileUpload"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
        >
          📂 Importar CSV
        </button>
        <button
          @click="clearAllHosts"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
        >
          🗑️ Limpar Tudo
        </button>
        <button
          @click="addHost"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
        >
          + Add Host
        </button>
      </div>
    </div>

    <div
      v-if="uploadMessage"
      :class="[
        'mb-4 p-3 rounded-lg text-sm font-medium',
        uploadMessage.type === 'success'
          ? 'bg-green-900/30 text-green-400 border border-green-700'
          : 'bg-red-900/30 text-red-400 border border-red-700',
      ]"
    >
      {{ uploadMessage.text }}
    </div>

    <div class="mb-4 p-3 bg-slate-700/50 rounded-lg text-xs text-slate-400">
      <strong class="text-slate-300">Formato CSV:</strong>
      hostname,port,username,password,private_key_path (opcional)
    </div>

    <div class="space-y-4">
      <div
        v-for="(host, index) in hosts"
        :key="index"
        class="bg-slate-700 rounded-lg p-4 relative"
      >
        <button
          v-if="hosts.length > 1"
          @click="removeHost(index)"
          class="absolute top-2 right-2 text-red-400 hover:text-red-300"
        >
          ✕
        </button>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">
              Hostname/IP
            </label>
            <input
              :value="host.hostname"
              @input="
                updateHost(
                  index,
                  'hostname',
                  ($event.target as HTMLInputElement).value
                )
              "
              type="text"
              placeholder="192.168.1.100"
              class="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">
              Port
            </label>
            <input
              :value="host.port"
              @input="
                updateHost(
                  index,
                  'port',
                  parseInt(($event.target as HTMLInputElement).value)
                )
              "
              type="number"
              class="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">
              Username
            </label>
            <input
              :value="host.username"
              @input="
                updateHost(
                  index,
                  'username',
                  ($event.target as HTMLInputElement).value
                )
              "
              type="text"
              placeholder="root"
              class="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-300 mb-1">
              Password
            </label>
            <input
              :value="host.password"
              @input="
                updateHost(
                  index,
                  'password',
                  ($event.target as HTMLInputElement).value
                )
              "
              type="password"
              placeholder="••••••••"
              class="w-full px-3 py-2 bg-slate-600 text-white rounded border border-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
